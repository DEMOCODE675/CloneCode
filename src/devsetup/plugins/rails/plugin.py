"""Ruby on Rails plugin."""

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
    """Detect Rails projects from Gem metadata."""

    spec = plugin_spec(
        name="rails",
        language=Language.RUBY,
        package_manager=PackageManager.GEM,
        framework=Framework.RAILS,
        manifest_markers=("Gemfile",),
        package_manager_markers=("Gemfile.lock",),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Rails projects with dependency evidence."""

        assessment = super().detect(snapshot)
        manifest = snapshot.manifests.get("Gemfile")
        if manifest is not None:
            content = (snapshot.root / manifest.path).read_text(encoding="utf-8", errors="ignore")
            if "rails" in content:
                return replace(assessment, score=assessment.score + 5.0, reasons=assessment.reasons + ("rails dependency found",))
        return assessment