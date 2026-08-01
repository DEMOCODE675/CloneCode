"""Go plugin."""

from __future__ import annotations

from devsetup.core.models import Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Go projects from module metadata."""

    spec = plugin_spec(
        name="go",
        language=Language.GO,
        package_manager=PackageManager.GO,
        manifest_markers=("go.mod",),
        install_command=("go", "mod", "download"),
    )