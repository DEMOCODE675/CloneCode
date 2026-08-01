"""Scanner tests."""

from __future__ import annotations

import json
from pathlib import Path

from devsetup.core.scanner import ProjectScanner


def test_scanner_discovers_manifests_and_lockfiles(tmp_path: Path) -> None:
    """The scanner should detect supported manifests and lock files."""

    project = tmp_path / "sample"
    project.mkdir()
    (project / "package.json").write_text(json.dumps({"name": "sample"}), encoding="utf-8")
    (project / "pnpm-lock.yaml").write_text("lockfileVersion: 9", encoding="utf-8")
    (project / "README.md").write_text("hello", encoding="utf-8")

    snapshot = ProjectScanner().scan(project)

    assert snapshot.root == project
    assert snapshot.has_file("package.json")
    assert snapshot.has_file("pnpm-lock.yaml")
    assert "package.json" in snapshot.manifests
    assert snapshot.manifests["package.json"].data["name"] == "sample"