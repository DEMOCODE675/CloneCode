"""Package manager detection tests."""

from __future__ import annotations

import json
from pathlib import Path

from devsetup.core.plugin_manager import PluginManager
from devsetup.core.scanner import ProjectScanner


def test_node_package_manager_detection_prefers_lockfile(tmp_path: Path) -> None:
    """Node package manager detection should honor the lockfile present on disk."""

    project = tmp_path / "node-app"
    project.mkdir()
    (project / "package.json").write_text(json.dumps({"name": "node-app"}), encoding="utf-8")
    (project / "bun.lockb").write_text("binary", encoding="utf-8")

    detected = PluginManager().detect(ProjectScanner().scan(project))

    assert detected.package_manager.value == "bun"


def test_python_package_manager_detection_prefers_uv_lock(tmp_path: Path) -> None:
    """Python package manager detection should honor uv.lock when present."""

    project = tmp_path / "python-app"
    project.mkdir()
    (project / "pyproject.toml").write_text(
        """
[project]
name = "python-app"
""".strip(),
        encoding="utf-8",
    )
    (project / "uv.lock").write_text("version = 1", encoding="utf-8")

    detected = PluginManager().detect(ProjectScanner().scan(project))

    assert detected.package_manager.value == "uv"