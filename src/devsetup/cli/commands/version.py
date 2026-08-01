"""Version command."""

from __future__ import annotations

import typer

from devsetup.cli.ui.console import console
from devsetup.version import __version__


def register(app: typer.Typer) -> None:
    """Register the version command on the supplied Typer app."""

    @app.command()
    def version() -> None:
        """Print the installed DevSetup version."""

        console.print(__version__)