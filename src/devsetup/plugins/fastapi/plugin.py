"""FastAPI plugin."""

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
    manifest_contains,
    plugin_spec,
)


class Plugin(ManifestDrivenPlugin):
    """Detect FastAPI projects from Python metadata."""

    spec = plugin_spec(
        name="fastapi",
        language=Language.PYTHON,
        framework=Framework.FASTAPI,
        package_manager=PackageManager.UV,
        manifest_markers=("pyproject.toml", "requirements.txt"),
        package_manager_markers=("uv.lock", "poetry.lock"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect FastAPI projects with dependency evidence."""

        assessment = super().detect(snapshot)
        if manifest_contains(snapshot, "pyproject.toml", "fastapi") or manifest_contains(snapshot, "requirements.txt", "fastapi"):
            return replace(assessment, score=assessment.score + 6.0, reasons=assessment.reasons + ("fastapi dependency found",))
        return assessment