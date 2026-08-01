"""Shared Rich console helpers."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from devsetup.core.models import HealthCheckResult

console = Console()


def render_banner() -> Panel:
    """Return the DevSetup banner panel."""

    return Panel.fit("[bold cyan]DevSetup[/bold cyan]\nUniversal development environment bootstrapper", border_style="cyan")


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