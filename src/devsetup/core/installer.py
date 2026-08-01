"""Project installation orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from devsetup.core.config import AppConfig
from devsetup.core.health import HealthChecker
from devsetup.core.models import (
    DetectedProject,
    HealthCheckResult,
    PluginExecutionContext,
)
from devsetup.core.plugin_manager import PluginManager
from devsetup.core.runner import CommandRunner


@dataclass(slots=True)
class ProjectInstaller:
    """Install dependencies and run plugin-driven setup steps."""

    plugin_manager: PluginManager
    runner: CommandRunner
    health_checker: HealthChecker
    config: AppConfig

    def install(self, detected_project: DetectedProject) -> tuple[HealthCheckResult, ...]:
        """Run the full installation pipeline for a detected project."""

        plugin = self.plugin_manager.get(detected_project.plugin_name)
        context = PluginExecutionContext(snapshot=detected_project.snapshot, config=self.config, runner=self.runner, console=None)
        if self.config.install.install_missing_sdks:
            self.health_checker.check_toolchain(detected_project.package_manager)
        plugin.install(context)
        plugin.setup(context)
        return self.health_checker.check_project(detected_project.snapshot) + self.health_checker.check_toolchain(detected_project.package_manager)

    def doctor(self, detected_project: DetectedProject) -> tuple[HealthCheckResult, ...]:
        """Run diagnostics without modifying the project."""

        plugin = self.plugin_manager.get(detected_project.plugin_name)
        context = PluginExecutionContext(snapshot=detected_project.snapshot, config=self.config, runner=self.runner, console=None)
        plugin.doctor(context)
        return self.health_checker.check_project(detected_project.snapshot) + self.health_checker.check_toolchain(detected_project.package_manager)