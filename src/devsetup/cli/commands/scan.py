"""Scan command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from devsetup.cli.ui.console import console
from devsetup.core.orchestrator import build_services


def register(app: typer.Typer) -> None:
    """Register the scan command on the supplied Typer app."""

    @app.command()
    def scan(
        path: Annotated[Path | None, typer.Argument(exists=True, file_okay=False, dir_okay=True)] = None,
    ) -> None:
        """Scan a repository and print the detected plugin metadata."""

        services = build_services()
        target = path or Path.cwd()
        snapshot = services.scanner.scan(target)
        detected = services.detector.detect_snapshot(snapshot)
        console.print(f"Language: [bold]{detected.language.value}[/bold]")
        console.print(f"Framework: [bold]{detected.framework.value}[/bold]")
        console.print(f"Package manager: [bold]{detected.package_manager.value}[/bold]")