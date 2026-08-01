"""Language and framework detection tests."""

from __future__ import annotations

import json
from pathlib import Path

from devsetup.core.detector import ProjectDetector


def test_detector_detects_fastapi_project(tmp_path: Path) -> None:
    """FastAPI projects should be detected from Python manifest files."""

    project = tmp_path / "fastapi-app"
    project.mkdir()
    (project / "pyproject.toml").write_text(
        """
[project]
name = "fastapi-app"
dependencies = ["fastapi"]
""".strip(),
        encoding="utf-8",
    )
    (project / "uv.lock").write_text("version = 1", encoding="utf-8")

    detected = ProjectDetector().detect(project)

    assert detected.language.value == "python"
    assert detected.framework.value == "fastapi"
    assert detected.package_manager.value == "uv"


def test_detector_detects_react_project(tmp_path: Path) -> None:
    """React projects should be detected from package dependencies."""

    project = tmp_path / "react-app"
    project.mkdir()
    (project / "package.json").write_text(
        json.dumps({"name": "react-app", "dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"}}),
        encoding="utf-8",
    )
    (project / "yarn.lock").write_text("# yarn lockfile", encoding="utf-8")

    detected = ProjectDetector().detect(project)

    assert detected.language.value == "javascript"
    assert detected.framework.value == "react"
    assert detected.package_manager.value == "yarn"