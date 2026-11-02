"""Banner and cat commands."""

from __future__ import annotations

from typing import Literal

import typer

from devsetup.cli.ui.console import console, render_banner

BannerStyle = Literal["matrix", "card"]


def register(app: typer.Typer) -> None:
    """Register banner and cat commands on the supplied Typer app."""

    @app.command()
    def banner(
        style: str = typer.Option(
            "matrix",
            "--style",
            "-s",
            help="Banner style: 'matrix' (reference dotted art) or 'card' (modern CLI card).",
        ),
    ) -> None:
        """Display the DevSetup cat banner."""
        chosen_style: BannerStyle = "card" if style.lower() == "card" else "matrix"
        console.print(render_banner(style=chosen_style))

    @app.command()
    def cat(
        style: str = typer.Option(
            "matrix",
            "--style",
            "-s",
            help="Banner style: 'matrix' (reference dotted art) or 'card' (modern CLI card).",
        ),
    ) -> None:
        """Show the mascot cat."""
        chosen_style: BannerStyle = "card" if style.lower() == "card" else "matrix"
        console.print(render_banner(style=chosen_style))
