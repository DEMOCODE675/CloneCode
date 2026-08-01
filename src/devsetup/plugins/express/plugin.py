"""Express plugin."""

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
    """Detect Express projects from Node.js metadata."""

    spec = plugin_spec(
        name="express",
        language=Language.JAVASCRIPT,
        framework=Framework.EXPRESS,
        package_manager=PackageManager.NPM,
        manifest_markers=("package.json",),
        package_manager_markers=("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Express projects with package dependency evidence."""

        assessment = super().detect(snapshot)
        if dependency_present(snapshot, "express"):
            assessment = replace(assessment, score=assessment.score + 5.5, reasons=assessment.reasons + ("express dependency found",))
        return replace(assessment, package_manager=detect_node_package_manager(snapshot))