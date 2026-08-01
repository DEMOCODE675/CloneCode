"""Plugin manager tests."""

from __future__ import annotations

import json
from pathlib import Path

from devsetup.core.plugin_manager import PluginManager
from devsetup.core.scanner import ProjectScanner


def test_plugin_manager_discovers_builtin_plugins() -> None:
    """The plugin manager should discover built-in plugins automatically."""

    manager = PluginManager()
    plugins = manager.discover()
    names = {plugin.name for plugin in plugins}

    assert {"node", "python", "react", "nextjs", "fastapi", "django"}.issubset(names)


def test_plugin_manager_detects_nextjs_from_package_json(tmp_path: Path) -> None:
    """Detection should prefer framework-specific package metadata over generic node projects."""

    project = tmp_path / "nextjs"
    project.mkdir()
    (project / "package.json").write_text(
        json.dumps(
            {
                "name": "next-app",
                "dependencies": {"next": "^14.0.0", "react": "^18.0.0"},
            }
        ),
        encoding="utf-8",
    )
    (project / "pnpm-lock.yaml").write_text("lockfileVersion: 9", encoding="utf-8")

    manager = PluginManager()
    snapshot = ProjectScanner().scan(project)
    detected = manager.detect(snapshot)

    assert detected.plugin_name == "nextjs"
    assert detected.framework.value == "nextjs"
    assert detected.package_manager.value == "pnpm"