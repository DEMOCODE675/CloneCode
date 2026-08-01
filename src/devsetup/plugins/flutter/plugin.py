"""Flutter plugin."""

from __future__ import annotations

from devsetup.core.models import Framework, Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Flutter projects from Dart metadata."""

    spec = plugin_spec(
        name="flutter",
        language=Language.DART,
        framework=Framework.FLUTTER,
        package_manager=PackageManager.FLUTTER,
        manifest_markers=("pubspec.yaml",),
        package_manager_markers=("pubspec.lock",),
        install_command=("flutter", "pub", "get"),
    )