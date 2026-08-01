"""Project detection orchestration."""

from __future__ import annotations

from pathlib import Path

from devsetup.core.models import DetectedProject, ProjectSnapshot
from devsetup.core.plugin_manager import PluginManager
from devsetup.core.scanner import ProjectScanner


class ProjectDetector:
    """Detect the best matching plugin for a project directory."""

    def __init__(self, scanner: ProjectScanner | None = None, plugin_manager: PluginManager | None = None) -> None:
        self._scanner = scanner or ProjectScanner()
        self._plugin_manager = plugin_manager or PluginManager()

    def detect(self, root: Path) -> DetectedProject:
        """Scan a project root and select the best matching plugin."""

        snapshot = self._scanner.scan(root)
        return self.detect_snapshot(snapshot)

    def detect_snapshot(self, snapshot: ProjectSnapshot) -> DetectedProject:
        """Select the best matching plugin for an already-scanned snapshot."""

        return self._plugin_manager.detect(snapshot)