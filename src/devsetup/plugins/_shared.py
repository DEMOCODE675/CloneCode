"""Shared plugin helpers."""

from __future__ import annotations

from typing import ClassVar

from devsetup.core.models import Framework, Language, PackageManager, ProjectSnapshot
from devsetup.core.plugin_base import BasePlugin, PluginSpec


class ManifestDrivenPlugin(BasePlugin):
    """Plugin base class for manifest-driven ecosystems."""

    spec: ClassVar[PluginSpec]


def package_json(snapshot: ProjectSnapshot) -> dict[str, object] | None:
    """Return the parsed package.json manifest if it exists."""

    manifest = snapshot.manifests.get("package.json")
    if manifest is None:
        return None
    return manifest.data


def dependency_present(snapshot: ProjectSnapshot, *names: str) -> bool:
    """Return whether any dependency name is present in package.json."""

    manifest = package_json(snapshot)
    if manifest is None:
        return False
    sections = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies")
    for section in sections:
        values = manifest.get(section)
        if not isinstance(values, dict):
            continue
        if any(name in values for name in names):
            return True
    scripts = manifest.get("scripts")
    if isinstance(scripts, dict):
        script_text = " ".join(str(value) for value in scripts.values())
        return any(name in script_text for name in names)
    return False


def detect_node_package_manager(snapshot: ProjectSnapshot) -> PackageManager:
    """Infer the node package manager from lockfiles."""

    if snapshot.has_file("pnpm-lock.yaml"):
        return PackageManager.PNPM
    if snapshot.has_file("yarn.lock"):
        return PackageManager.YARN
    if snapshot.has_file("bun.lockb"):
        return PackageManager.BUN
    if snapshot.has_file("package-lock.json"):
        return PackageManager.NPM
    return PackageManager.NPM


def detect_python_package_manager(snapshot: ProjectSnapshot) -> PackageManager:
    """Infer the python package manager from lockfiles and manifests."""

    if snapshot.has_file("uv.lock"):
        return PackageManager.UV
    if snapshot.has_file("poetry.lock"):
        return PackageManager.POETRY
    if snapshot.has_file("requirements.txt"):
        return PackageManager.PIP
    return PackageManager.UV


def manifest_contains(snapshot: ProjectSnapshot, manifest_name: str, *needles: str) -> bool:
    """Return whether a manifest contains any of the supplied substrings."""

    manifest = snapshot.manifests.get(manifest_name)
    if manifest is None:
        return False
    return _contains_value(manifest.data, needles)


def _contains_value(value: object, needles: tuple[str, ...]) -> bool:
    """Recursively search a parsed manifest for any needle."""

    if isinstance(value, dict):
        return any(_contains_value(item, needles) for item in value.values())
    if isinstance(value, list):
        return any(_contains_value(item, needles) for item in value)
    text = str(value).lower()
    return any(needle.lower() in text for needle in needles)


def plugin_spec(
    name: str,
    language: Language,
    *,
    framework: Framework = Framework.UNKNOWN,
    package_manager: PackageManager = PackageManager.UNKNOWN,
    file_markers: tuple[str, ...] = (),
    manifest_markers: tuple[str, ...] = (),
    package_manager_markers: tuple[str, ...] = (),
    install_command: tuple[str, ...] = (),
    run_command: tuple[str, ...] = (),
) -> PluginSpec:
    """Build a declarative plugin specification."""

    return PluginSpec(
        name=name,
        language=language,
        framework=framework,
        package_manager=package_manager,
        file_markers=file_markers,
        manifest_markers=manifest_markers,
        package_manager_markers=package_manager_markers,
        install_command=install_command,
        run_command=run_command,
    )