"""Java plugin."""

from __future__ import annotations

from devsetup.core.models import Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect generic Java projects from build files."""

    spec = plugin_spec(
        name="java",
        language=Language.JAVA,
        package_manager=PackageManager.GRADLE,
        manifest_markers=("pom.xml", "build.gradle", "build.gradle.kts"),
        package_manager_markers=("gradlew", "mvnw"),
    )