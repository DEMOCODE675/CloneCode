"""Remix plugin."""

from __future__ import annotations

from dataclasses import replace

from devsetup.core.models import (
    Framework,
    Language,
    PackageManager,
    PluginAssessment,
    ProjectSnapshot,
)
from devsetup.plugins._shared import (
    ManifestDrivenPlugin,
    dependency_present,
    detect_node_package_manager,
    plugin_spec,
)


class Plugin(ManifestDrivenPlugin):
    """Detect Remix projects from package metadata."""

    spec = plugin_spec(
        name="remix",
        language=Language.JAVASCRIPT,
        framework=Framework.REMIX,
        package_manager=PackageManager.NPM,
        manifest_markers=("package.json",),
        package_manager_markers=("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Remix projects with dependency evidence."""

        assessment = super().detect(snapshot)
        if dependency_present(snapshot, "remix"):
            assessment = replace(assessment, score=assessment.score + 5.0, reasons=assessment.reasons + ("remix dependency found",))
        return replace(assessment, package_manager=detect_node_package_manager(snapshot))