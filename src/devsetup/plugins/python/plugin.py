"""Python ecosystem plugin."""

from __future__ import annotations

from dataclasses import replace

from devsetup.core.models import (
    Language,
    PackageManager,
    PluginAssessment,
    ProjectSnapshot,
)
from devsetup.plugins._shared import (
    ManifestDrivenPlugin,
    detect_python_package_manager,
    plugin_spec,
)


class Plugin(ManifestDrivenPlugin):
    """Detect and manage Python projects."""

    spec = plugin_spec(
        name="python",
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
        manifest_markers=("pyproject.toml", "requirements.txt"),
        package_manager_markers=("uv.lock", "poetry.lock"),
        install_command=("python", "-m", "pip", "install", "-r", "requirements.txt"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Python projects and infer the package manager."""

        assessment = super().detect(snapshot)
        return replace(assessment, package_manager=detect_python_package_manager(snapshot))