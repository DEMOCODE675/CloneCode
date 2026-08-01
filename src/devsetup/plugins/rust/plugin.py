"""Rust plugin."""

from __future__ import annotations

from devsetup.core.models import Language, PackageManager
from devsetup.plugins._shared import ManifestDrivenPlugin, plugin_spec


class Plugin(ManifestDrivenPlugin):
    """Detect Rust projects from Cargo metadata."""

    spec = plugin_spec(
        name="rust",
        language=Language.RUST,
        package_manager=PackageManager.CARGO,
        manifest_markers=("Cargo.toml",),
        package_manager_markers=("Cargo.lock",),
        install_command=("cargo", "fetch"),
    )