"""Cache command group."""

from __future__ import annotations

import shutil

import typer

from devsetup.cli.ui.console import console
from devsetup.core.orchestrator import build_services


def register(app: typer.Typer) -> None:
    """Register cache subcommands on the supplied Typer app."""

    cache_app = typer.Typer(help="Manage the local DevSetup cache.")

    @cache_app.command("clear")
    def clear() -> None:
        """Clear all cached DevSetup data."""

        services = build_services()
        for path in (services.config.cache.root, services.config.cache.state):
            if path.exists():
                shutil.rmtree(path)
        console.print("[green]Cache cleared[/green]")

    app.add_typer(cache_app, name="cache")