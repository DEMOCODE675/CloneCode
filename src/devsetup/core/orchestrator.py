"""High-level project orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from devsetup.core.clone import RepositoryCloner
from devsetup.core.config import AppConfig
from devsetup.core.detector import ProjectDetector
from devsetup.core.health import HealthChecker
from devsetup.core.installer import ProjectInstaller
from devsetup.core.plugin_manager import PluginManager
from devsetup.core.runner import CommandRunner
from devsetup.core.scanner import ProjectScanner


@dataclass(slots=True)
class DevSetupServices:
    """Container object for the application's core services."""

    config: AppConfig
    runner: CommandRunner
    cloner: RepositoryCloner
    scanner: ProjectScanner
    plugin_manager: PluginManager
    detector: ProjectDetector
    health_checker: HealthChecker
    installer: ProjectInstaller


def build_services(config: AppConfig | None = None) -> DevSetupServices:
    """Build a fully wired service graph for the CLI."""

    app_config = config or AppConfig()
    runner = CommandRunner()
    plugin_manager = PluginManager(app_config, runner)
    scanner = ProjectScanner(app_config.scan)
    detector = ProjectDetector(scanner=scanner, plugin_manager=plugin_manager)
    health_checker = HealthChecker(runner)
    installer = ProjectInstaller(plugin_manager=plugin_manager, runner=runner, health_checker=health_checker, config=app_config)
    return DevSetupServices(
        config=app_config,
        runner=runner,
        cloner=RepositoryCloner(),
        scanner=scanner,
        plugin_manager=plugin_manager,
        detector=detector,
        health_checker=health_checker,
        installer=installer,
    )


def repository_destination(url: str, config: AppConfig) -> Path:
    """Compute a destination path for cloned repositories."""

    base_name = url.rstrip("/").split("/")[-1].removesuffix(".git")
    destination_root = config.clone.destination or config.cache.state / "repos"
    return destination_root / base_name