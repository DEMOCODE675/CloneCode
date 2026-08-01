"""Spring Boot plugin."""

from __future__ import annotations

from devsetup.core.models import (
    Framework,
    Language,
    PackageManager,
    PluginAssessment,
    ProjectSnapshot,
)
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Spring Boot projects from Maven or Gradle manifests."""

    spec = plugin_spec(
        name="spring",
        language=Language.JAVA,
        package_manager=PackageManager.GRADLE,
        framework=Framework.SPRING,
        manifest_markers=("pom.xml", "build.gradle", "build.gradle.kts"),
        package_manager_markers=("gradlew", "mvnw"),
    )

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Detect Spring Boot projects with build-file evidence."""

        assessment = super().detect(snapshot)
        if self._spring_present(snapshot):
            return PluginAssessment(
                plugin_name=assessment.plugin_name,
                language=assessment.language,
                framework=assessment.framework,
                package_manager=assessment.package_manager,
                score=assessment.score + 5.0,
                matched=True,
                reasons=assessment.reasons + ("spring boot markers found",),
            )
        return assessment

    def _spring_present(self, snapshot: ProjectSnapshot) -> bool:
        """Check whether the project contains Spring Boot indicators."""

        for manifest_name in ("pom.xml", "build.gradle", "build.gradle.kts"):
            manifest = snapshot.manifests.get(manifest_name)
            if manifest is None:
                continue
            content = (snapshot.root / manifest.path).read_text(encoding="utf-8", errors="ignore")
            if "spring-boot" in content or "org.springframework" in content:
                return True
        return False