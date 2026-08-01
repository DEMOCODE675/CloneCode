"""Ruby plugin."""

from __future__ import annotations

from devsetup.core.models import Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Ruby projects from Gem metadata."""

    spec = plugin_spec(
        name="ruby",
        language=Language.RUBY,
        package_manager=PackageManager.GEM,
        manifest_markers=("Gemfile",),
        package_manager_markers=("Gemfile.lock",),
        install_command=("bundle", "install"),
    )