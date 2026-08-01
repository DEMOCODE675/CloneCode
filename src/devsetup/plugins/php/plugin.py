"""PHP plugin."""

from __future__ import annotations

from devsetup.core.models import Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect PHP projects from Composer metadata."""

    spec = plugin_spec(
        name="php",
        language=Language.PHP,
        package_manager=PackageManager.COMPOSER,
        manifest_markers=("composer.json",),
        package_manager_markers=("composer.lock",),
        install_command=("composer", "install"),
    )