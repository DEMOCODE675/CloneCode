"""Doctor command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from devsetup.cli.ui.console import console, render_health_table
from devsetup.core.orchestrator import build_services


def register(app: typer.Typer) -> None:
    """Register the doctor command on the supplied Typer app."""

    @app.command()
    def doctor(
        path: Annotated[Path | None, typer.Argument(exists=True, file_okay=False, dir_okay=True)] = None,
    ) -> None:
        """Run health checks for the repository at ``path``."""

        services = build_services()
        target = path or Path.cwd()
        snapshot = services.scanner.scan(target)
        detected = services.detector.detect_snapshot(snapshot)
        results = services.installer.doctor(detected)
        console.print(render_health_table(results))