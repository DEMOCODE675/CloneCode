"""Shared Rich console helpers."""

from __future__ import annotations

from typing import Literal

from rich.console import Console, RenderableType
from rich.table import Table

from devsetup.cli.ui.cat_art import render_cat_banner
from devsetup.core.models import HealthCheckResult

console = Console()


def render_banner(style: Literal["matrix", "card"] = "matrix") -> RenderableType:
    """Return the DevSetup cat banner."""

    return render_cat_banner(style=style)


def render_health_table(results: tuple[HealthCheckResult, ...]) -> Table:
    """Render health check results as a table."""

    table = Table(title="Health Check", show_lines=False)
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Message")
    for result in results:
        status = "[green]PASS[/green]" if result.success else "[red]FAIL[/red]"
        table.add_row(result.name, status, result.message)
    return table
