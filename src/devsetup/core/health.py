"""Health checks for projects and local toolchains."""

from __future__ import annotations

from dataclasses import dataclass

from devsetup.core.models import HealthCheckResult, PackageManager, ProjectSnapshot
from devsetup.core.runner import CommandRunner


@dataclass(slots=True)
class HealthChecker:
    """Run generic health checks before installing dependencies."""

    runner: CommandRunner

    def check_toolchain(self, package_manager: PackageManager) -> tuple[HealthCheckResult, ...]:
        """Check whether the selected package manager is available."""

        executable = self._executable_for(package_manager)
        if executable is None:
            return (
                HealthCheckResult(
                    name=package_manager.value,
                    success=True,
                    message="No dedicated executable required.",
                ),
            )
        if self.runner.exists(executable):
            return (HealthCheckResult(name=executable, success=True, message=f"{executable} is available."),)
        return (HealthCheckResult(name=executable, success=False, message=f"{executable} was not found on PATH."),)

    def check_project(self, snapshot: ProjectSnapshot) -> tuple[HealthCheckResult, ...]:
        """Run project-level checks that apply to every repository."""

        results = [HealthCheckResult(name="repository", success=True, message=f"Scanned {len(snapshot.files)} files.")]
        if snapshot.manifests:
            results.append(HealthCheckResult(name="manifests", success=True, message=f"Found {len(snapshot.manifests)} manifest files."))
        else:
            results.append(HealthCheckResult(name="manifests", success=False, message="No supported manifest files were detected."))
        return tuple(results)

    def _executable_for(self, package_manager: PackageManager) -> str | None:
        """Map a package manager to its expected executable."""

        mapping = {
            PackageManager.NPM: "npm",
            PackageManager.PNPM: "pnpm",
            PackageManager.YARN: "yarn",
            PackageManager.BUN: "bun",
            PackageManager.PIP: "python",
            PackageManager.UV: "uv",
            PackageManager.POETRY: "poetry",
            PackageManager.CARGO: "cargo",
            PackageManager.GO: "go",
            PackageManager.MAVEN: "mvn",
            PackageManager.GRADLE: "gradle",
            PackageManager.COMPOSER: "composer",
            PackageManager.GEM: "gem",
            PackageManager.FLUTTER: "flutter",
            PackageManager.UNKNOWN: None,
        }
        return mapping[package_manager]