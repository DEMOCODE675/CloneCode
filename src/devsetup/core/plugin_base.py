"""Shared base class for all plugins."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from devsetup.core.models import (
    Framework,
    Language,
    PackageManager,
    PluginAssessment,
    PluginExecutionContext,
    ProjectSnapshot,
)
from devsetup.core.runner import CommandRunner


@dataclass(slots=True, frozen=True)
class PluginSpec:
    """Declarative plugin metadata used by the generic base implementation."""

    name: str
    language: Language
    framework: Framework = Framework.UNKNOWN
    package_manager: PackageManager = PackageManager.UNKNOWN
    file_markers: tuple[str, ...] = ()
    manifest_markers: tuple[str, ...] = ()
    package_manager_markers: tuple[str, ...] = ()
    install_command: tuple[str, ...] = ()
    run_command: tuple[str, ...] = ()


class BasePlugin:
    """Generic plugin implementation driven by a declarative spec."""

    spec: ClassVar[PluginSpec]

    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner or CommandRunner()

    @property
    def name(self) -> str:
        """Return the plugin name."""

        return self.spec.name

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Score the plugin against the supplied snapshot."""

        score = 0.0
        reasons: list[str] = []

        for marker in self.spec.file_markers:
            if snapshot.has_file(marker):
                score += 2.0
                reasons.append(f"found file marker: {marker}")

        for marker in self.spec.manifest_markers:
            if marker in snapshot.manifests:
                score += 3.0
                reasons.append(f"found manifest: {marker}")

        if self.spec.package_manager_markers and snapshot.has_any_file(list(self.spec.package_manager_markers)):
            score += 2.0
            reasons.append("found package manager marker")

        matched = score > 0.0
        return PluginAssessment(
            plugin_name=self.spec.name,
            language=self.spec.language,
            framework=self.spec.framework,
            package_manager=self.spec.package_manager,
            score=score,
            matched=matched,
            reasons=tuple(reasons),
        )

    def validate(self, context: PluginExecutionContext) -> bool:
        """Validate that the plugin has enough evidence to run safely."""

        return self.detect(context.snapshot).matched

    def install(self, context: PluginExecutionContext) -> bool:
        """Install project dependencies using the configured package manager."""

        command = self._install_command(context)
        if not command:
            return True
        self._runner.run(command, cwd=context.snapshot.root)
        return True

    def setup(self, context: PluginExecutionContext) -> bool:
        """Apply plugin-specific setup. Defaults to a validation pass."""

        return self.validate(context)

    def doctor(self, context: PluginExecutionContext) -> bool:
        """Run a lightweight health check. Defaults to validation."""

        return self.validate(context)

    def run(self, context: PluginExecutionContext) -> bool:
        """Run the project with the configured command if one is defined."""

        command = self._run_command(context)
        if not command:
            return False
        self._runner.run(command, cwd=context.snapshot.root)
        return True

    def _install_command(self, context: PluginExecutionContext) -> tuple[str, ...]:
        """Return the command used to install dependencies."""

        return self.spec.install_command

    def _run_command(self, context: PluginExecutionContext) -> tuple[str, ...]:
        """Return the command used to run the project."""

        return self.spec.run_command
