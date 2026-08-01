"""Node.js ecosystem plugin."""

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
    detect_node_package_manager,
    plugin_spec,
)


class Plugin(ManifestDrivenPlugin):
    """Detect and manage plain Node.js projects."""

    spec = plugin_spec(
        name="node",
        language=Language.JAVASCRIPT,
        package_manager=PackageManager.NPM,
        manifest_markers=("package.json",),
        package_manager_markers=("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"),
        install_command=("npm", "install"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Node.js projects and infer the installed package manager."""

        assessment = super().detect(snapshot)
        return replace(assessment, package_manager=detect_node_package_manager(snapshot))