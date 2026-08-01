"""Clone command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from devsetup.cli.ui.console import console
from devsetup.core.orchestrator import build_services, repository_destination


def register(app: typer.Typer) -> None:
    """Register the clone command on the supplied Typer app."""

    @app.command()
    def clone(
        repository_url: Annotated[str, typer.Argument(help="GitHub repository URL.")],
        destination: Annotated[Path | None, typer.Option(help="Override the clone destination.")] = None,
    ) -> None:
        """Clone a repository without running setup steps."""

        services = build_services()
        target = destination or repository_destination(repository_url, services.config)
        services.cloner.clone(repository_url, target, branch=services.config.clone.branch, depth=services.config.clone.depth)
        console.print(f"[green]Cloned[/green] {repository_url} -> {target}")