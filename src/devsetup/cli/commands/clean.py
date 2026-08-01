"""Clean command."""

from __future__ import annotations

import shutil

import typer

from devsetup.cli.ui.console import console
from devsetup.core.orchestrator import build_services


def register(app: typer.Typer) -> None:
    """Register the clean command on the supplied Typer app."""

    @app.command()
    def clean() -> None:
        """Remove cache and state directories managed by DevSetup."""

        services = build_services()
        for path in (services.config.cache.root, services.config.cache.state):
            if path.exists():
                shutil.rmtree(path)
        console.print("[green]Cleaned[/green] DevSetup cache and state directories")