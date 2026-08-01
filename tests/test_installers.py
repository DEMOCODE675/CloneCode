"""Installer orchestration tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from devsetup.core.config import AppConfig
from devsetup.core.health import HealthChecker
from devsetup.core.installer import ProjectInstaller
from devsetup.core.models import (
    DetectedProject,
    Framework,
    HealthCheckResult,
    Language,
    PackageManager,
    ProjectSnapshot,
)
from devsetup.core.runner import CommandRunner


@dataclass
class DummyPlugin:
    """Minimal plugin implementation used for installer tests."""

    name: str = "dummy"
    install_calls: int = 0
    setup_calls: int = 0
    doctor_calls: int = 0

    def install(self, context):
        self.install_calls += 1
        return True

    def setup(self, context):
        self.setup_calls += 1
        return True

    def doctor(self, context):
        self.doctor_calls += 1
        return True


class DummyPluginManager:
    """Return a single plugin for tests."""

    def __init__(self, plugin: DummyPlugin) -> None:
        self.plugin = plugin

    def get(self, plugin_name: str) -> DummyPlugin:
        return self.plugin


class DummyHealthChecker(HealthChecker):
    """Health checker that avoids touching the host system."""

    def __init__(self) -> None:
        super().__init__(runner=CommandRunner())

    def check_project(self, snapshot: ProjectSnapshot):
        return (HealthCheckResult(name="repository", success=True, message="ok"),)

    def check_toolchain(self, package_manager: PackageManager):
        return (HealthCheckResult(name=package_manager.value, success=True, message="ok"),)


def test_installer_invokes_plugin_steps(tmp_path: Path) -> None:
    """Installer should call plugin install and setup hooks."""

    plugin = DummyPlugin()
    installer = ProjectInstaller(
        plugin_manager=DummyPluginManager(plugin),
        runner=CommandRunner(),
        health_checker=DummyHealthChecker(),
        config=AppConfig(),
    )
    snapshot = ProjectSnapshot(root=tmp_path, files=(), signals=())
    detected = DetectedProject(
        plugin_name="dummy",
        language=Language.UNKNOWN,
        framework=Framework.UNKNOWN,
        package_manager=PackageManager.UNKNOWN,
        reasons=(),
        snapshot=snapshot,
    )

    results = installer.install(detected)

    assert plugin.install_calls == 1
    assert plugin.setup_calls == 1
    assert len(results) == 2