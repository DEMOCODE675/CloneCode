"""Next.js plugin."""

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
    """Detect Next.js projects from package metadata."""

    spec = plugin_spec(
        name="nextjs",
        language=Language.JAVASCRIPT,
        framework=Framework.NEXTJS,
        package_manager=PackageManager.NPM,
        manifest_markers=("package.json",),
        package_manager_markers=("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Next.js projects with package dependency evidence."""

        assessment = super().detect(snapshot)
        if dependency_present(snapshot, "next"):
            assessment = replace(assessment, score=assessment.score + 6.0, reasons=assessment.reasons + ("next dependency found",))
        return replace(assessment, package_manager=detect_node_package_manager(snapshot))