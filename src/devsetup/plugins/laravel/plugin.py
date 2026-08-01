"""Laravel plugin."""

from __future__ import annotations

from dataclasses import replace

from devsetup.core.models import (
    Framework,
    Language,
    PackageManager,
    PluginAssessment,
    ProjectSnapshot,
)
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Laravel projects from Composer metadata."""

    spec = plugin_spec(
        name="laravel",
        language=Language.PHP,
        package_manager=PackageManager.COMPOSER,
        framework=Framework.LARAVEL,
        manifest_markers=("composer.json",),
        package_manager_markers=("composer.lock",),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Laravel projects with dependency evidence."""

        assessment = super().detect(snapshot)
        manifest = snapshot.manifests.get("composer.json")
        if manifest is not None:
            content = (snapshot.root / manifest.path).read_text(encoding="utf-8", errors="ignore")
            if "laravel/framework" in content:
                return replace(assessment, score=assessment.score + 5.0, reasons=assessment.reasons + ("laravel framework dependency found",))
        return assessment