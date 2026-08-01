"""Plugin discovery and registry management."""

from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module, util
from importlib.metadata import EntryPoint, entry_points
from pathlib import Path
from types import ModuleType
from typing import cast

from devsetup.core.config import AppConfig
from devsetup.core.models import (
    DetectedProject,
    Framework,
    Language,
    PackageManager,
    PluginAssessment,
    ProjectSnapshot,
)
from devsetup.core.plugin_contract import PluginProtocol
from devsetup.core.runner import CommandRunner


class PluginManager:
    """Discover, cache, and select DevSetup plugins."""

    def __init__(self, config: AppConfig | None = None, runner: CommandRunner | None = None) -> None:
        self._config = config or AppConfig()
        self._runner = runner or CommandRunner()
        self._plugins: dict[str, PluginProtocol] = {}
        self._discovered = False

    def discover(self) -> tuple[PluginProtocol, ...]:
        """Discover plugins from the built-in package and entry points."""

        if self._discovered:
            return tuple(self._plugins.values())

        self._discover_builtin_plugins()
        self._discover_entry_points()
        self._discover_external_paths()
        self._discovered = True
        return tuple(self._plugins.values())

    def register(self, plugin: PluginProtocol) -> None:
        """Register a plugin instance in the in-memory registry."""

        self._plugins[plugin.name] = plugin

    def get(self, plugin_name: str) -> PluginProtocol:
        """Retrieve a plugin by name."""

        self.discover()
        try:
            return self._plugins[plugin_name]
        except KeyError as error:
            raise KeyError(f"Unknown plugin: {plugin_name}") from error

    def assess(self, snapshot: ProjectSnapshot) -> tuple[PluginAssessment, ...]:
        """Assess all discovered plugins against a project snapshot."""

        self.discover()
        assessments = [plugin.detect(snapshot) for plugin in self._plugins.values()]
        return tuple(sorted(assessments, key=lambda item: item.score, reverse=True))

    def detect(self, snapshot: ProjectSnapshot) -> DetectedProject:
        """Select the best matching plugin for the supplied snapshot."""

        assessments = self.assess(snapshot)
        best = next((assessment for assessment in assessments if assessment.matched), None)
        if best is None:
            return DetectedProject(
                plugin_name="unknown",
                language=Language.UNKNOWN,
                framework=Framework.UNKNOWN,
                package_manager=PackageManager.UNKNOWN,
                reasons=("No plugin matched the scanned project.",),
                snapshot=snapshot,
            )
        return DetectedProject(
            plugin_name=best.plugin_name,
            language=best.language,
            framework=best.framework,
            package_manager=best.package_manager,
            reasons=best.reasons,
            snapshot=snapshot,
        )

    def _discover_builtin_plugins(self) -> None:
        """Load plugins shipped inside the devsetup.plugins package."""

        package = import_module("devsetup.plugins")
        package_file = getattr(package, "__file__", None)
        if package_file is None:
            return
        package_path = Path(package_file).resolve().parent
        for child in sorted(package_path.iterdir()):
            if not child.is_dir() or child.name.startswith("_"):
                continue
            module_name = f"devsetup.plugins.{child.name}.plugin"
            try:
                module = import_module(module_name)
            except ModuleNotFoundError:
                continue
            self._register_module_plugin(module)

    def _discover_entry_points(self) -> None:
        """Load third-party plugins exposed through Python entry points."""

        for entry_point in self._iter_entry_points():
            plugin = self._load_entry_point(entry_point)
            if plugin is not None:
                self.register(plugin)

    def _discover_external_paths(self) -> None:
        """Load plugins from configured filesystem search paths."""

        for base_path in self._config.plugin_search_paths:
            if not base_path.exists():
                continue
            for child in sorted(base_path.iterdir()):
                if not child.is_dir() or child.name.startswith("_"):
                    continue
                module_path = child / "plugin.py"
                if not module_path.exists():
                    continue
                spec = util.spec_from_file_location(f"devsetup_external_{child.name}", module_path)
                if spec is None or spec.loader is None:
                    continue
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self._register_module_plugin(module)

    def _register_module_plugin(self, module: ModuleType) -> None:
        """Instantiate and register a plugin exposed by a module."""

        plugin = getattr(module, "Plugin", None)
        if plugin is None:
            return
        instance = plugin(self._runner)
        if isinstance(instance, PluginProtocol):
            self.register(instance)

    def _iter_entry_points(self) -> Iterable[EntryPoint]:
        """Yield registered plugin entry points for the configured group."""

        discovered = entry_points()
        group = self._config.plugin_entrypoint_group
        if hasattr(discovered, "select"):
            return discovered.select(group=group)
        discovered_map = cast(dict[str, list[EntryPoint]], discovered)
        return tuple(discovered_map.get(group, []))

    def _load_entry_point(self, entry_point: EntryPoint) -> PluginProtocol | None:
        """Load a plugin from a setuptools entry point."""

        loaded = entry_point.load()
        plugin = loaded(self._runner) if callable(loaded) else loaded
        return plugin if isinstance(plugin, PluginProtocol) else None