"""Setup command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from devsetup.cli.ui.console import console, render_banner, render_health_table
from devsetup.cli.ui.progress import progress_session
from devsetup.core.orchestrator import build_services, repository_destination


def register(app: typer.Typer) -> None:
    """Register the setup command on the supplied Typer app."""

    @app.command()
    def setup(
        repository_url: Annotated[str, typer.Argument(help="GitHub repository URL.")],
        destination: Annotated[Path | None, typer.Option(help="Override the clone destination.")] = None,
    ) -> None:
        """Clone, detect, install, and validate a repository."""

        services = build_services()
        console.print(render_banner())
        target = destination or repository_destination(repository_url, services.config)

        with progress_session("Setting up repository") as progress:
            task = progress.tasks[0].id
            progress.update(task, completed=10, description="Cloning repository")
            services.cloner.clone(repository_url, target, branch=services.config.clone.branch, depth=services.config.clone.depth)
            progress.update(task, completed=35, description="Scanning project")
            snapshot = services.scanner.scan(target)
            detected = services.detector.detect_snapshot(snapshot)
            progress.update(task, completed=60, description="Installing dependencies")
            results = services.installer.install(detected)
            progress.update(task, completed=90, description="Running health checks")
            progress.update(task, completed=100)

        console.print(render_health_table(results))
        console.print("[green]Project Ready[/green]")
        console.print(f"Run: [bold]{detected.package_manager.value} dev[/bold]")