"""Plugins command."""

from __future__ import annotations

from typing import Any

import typer

from devsetup.cli.ui.console import console
from devsetup.core.orchestrator import build_services


def register(app: typer.Typer) -> None:
    """Register the plugins command on the supplied Typer app."""

    @app.command()
    def plugins() -> None:
        """List discovered plugins."""

        services = build_services()
        rows = [
            (
                plugin.name,
                _spec_value(plugin, "language"),
                _spec_value(plugin, "framework"),
                _spec_value(plugin, "package_manager"),
            )
            for plugin in services.plugin_manager.discover()
        ]
        for name, language, framework, package_manager in rows:
            console.print(f"{name:12} {language:12} {framework:12} {package_manager}")


def _spec_value(plugin: Any, attribute: str) -> str:
    """Return a plugin spec attribute value for display purposes."""

    spec = getattr(plugin, "spec", None)
    if spec is None:
        return "unknown"
    value = getattr(spec, attribute, None)
    if value is None:
        return "unknown"
    return getattr(value, "value", str(value))