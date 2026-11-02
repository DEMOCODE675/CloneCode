"""ASCII and ANSI styled cat banners for DevSetup CLI."""

from __future__ import annotations

from typing import Literal

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from devsetup.version import __version__

TOTAL_BANNER_WIDTH = 72


def _make_matrix_row(
    row_segments: list[tuple[str, str]], width: int = TOTAL_BANNER_WIDTH
) -> Text:
    """Center a list of styled text segments within a dotted background line."""
    total_len = sum(len(txt) for txt, _ in row_segments)
    rem = max(0, width - total_len)
    left_dots = rem // 2
    right_dots = rem - left_dots

    row_text = Text()
    row_text.append("# " + "." * left_dots, style="dim cyan")
    for txt, style in row_segments:
        row_text.append(txt, style=style)
    row_text.append("." * right_dots + "\n", style="dim cyan")
    return row_text


def build_matrix_cat_banner(
    width: int = TOTAL_BANNER_WIDTH,
    title: str = "DevSetup",
    subtitle: str = "Universal Environment Bootstrapper",
) -> Text:
    """Build the Image 2 styled dotted matrix terminal banner featuring the cartoon cat."""
    banner = Text()
    dash_line = "# " + "-" * width + "\n"
    dots_line = "# " + "." * width + "\n"

    banner.append(dash_line, style="dim cyan")
    banner.append(dots_line, style="dim cyan")

    # Geometry for the cute cartoon cat (matching Image 1)
    cat_rows: list[list[tuple[str, str]]] = [
        [("      /\\_____/\\      ", "bold bright_white")],
        [
            ("     /  ", "bold bright_white"),
            ("/\\", "bold bright_magenta"),
            ("   ", "bold bright_white"),
            ("/\\", "bold bright_magenta"),
            ("  \\     ", "bold bright_white"),
        ],
        [
            ("    (   ", "bold bright_white"),
            ("(o)   (o)", "bold bright_cyan"),
            ("   )    ", "bold bright_white"),
            (" '", "dim white"),
        ],
        [
            (" \\  / ", "bold white"),
            (".. ", "dim cyan"),
            ("(  ", "bold bright_white"),
            ("(*)", "bold bright_magenta"),
            ("  .  ", "bold white"),
            ("(*)", "bold bright_magenta"),
            ("  ) ", "bold bright_white"),
            ("..", "dim cyan"),
            (" \\  /", "bold white"),
        ],
        [
            (" ===  ", "bold white"),
            ("... ", "dim cyan"),
            ("(     ", "bold bright_white"),
            (".w.", "bold yellow"),
            ("     ) ", "bold bright_white"),
            ("...", "dim cyan"),
            ("  === ", "bold white"),
        ],
        [
            (" /  \\ ", "bold white"),
            (".... ", "dim cyan"),
            ("\\           / ", "bold bright_white"),
            ("....", "dim cyan"),
            (" /  \\ ", "bold white"),
        ],
        [("    /     | |     \\    ", "bold bright_white")],
        [("   |      | |      |   ", "bold bright_white")],
        [("   |    ( | | )    |   ", "bold bright_white")],
        [("   (____( | | )____)   ", "bold bright_white")],
    ]

    for row in cat_rows:
        banner.append_text(_make_matrix_row(row, width=width))

    banner.append(dots_line, style="dim cyan")

    # Footer segment
    footer_plain = f"[ {title} {subtitle} ]"
    rem_footer = max(0, width - len(footer_plain))
    left_f = rem_footer // 2
    right_f = rem_footer - left_f

    banner.append("# " + "." * left_f, style="dim cyan")
    banner.append("[", style="dim white")
    banner.append(f" {title} ", style="bold bright_cyan")
    banner.append(f"{subtitle} ", style="white")
    banner.append("]", style="dim white")
    banner.append("." * right_f + "\n", style="dim cyan")

    banner.append(dash_line, style="dim cyan")
    return banner


def build_card_cat_banner(
    title: str = "DevSetup",
    version: str = __version__,
) -> Panel:
    """Build a modern Claude CLI style two-column card banner."""
    cat = Text()
    cat.append("      /\\_____/\\      \n", style="bold bright_white")
    cat.append("     /  ", style="bold bright_white")
    cat.append("/\\", style="bold bright_magenta")
    cat.append("   ", style="bold bright_white")
    cat.append("/\\", style="bold bright_magenta")
    cat.append("  \\     \n", style="bold bright_white")
    cat.append("    (   ", style="bold bright_white")
    cat.append("(o)   (o)", style="bold bright_cyan")
    cat.append("   )   '\n", style="bold bright_white")
    cat.append(" \\  / (  ", style="bold white")
    cat.append("(*)", style="bold bright_magenta")
    cat.append("  .  ", style="bold white")
    cat.append("(*)", style="bold bright_magenta")
    cat.append("  ) \\  /\n", style="bold white")
    cat.append(" === (     ", style="bold white")
    cat.append(".w.", style="bold yellow")
    cat.append("     ) ===\n", style="bold white")
    cat.append(" /  \\ \\           / /  \\\n", style="bold white")
    cat.append("    /     | |     \\    \n", style="bold bright_white")
    cat.append("   |      | |      |   \n", style="bold bright_white")
    cat.append("   (____( | | )____)   \n", style="bold bright_white")

    info = Text()
    info.append(f"{title} ", style="bold bright_cyan")
    info.append(f"v{version}\n", style="dim white")
    info.append("Universal development environment bootstrapper\n\n", style="italic white")
    info.append("Quick Start:\n", style="bold yellow")
    info.append("  devsetup <repo-url>       ", style="bright_white")
    info.append("Clone and bootstrap repository\n", style="dim white")
    info.append("  devsetup doctor           ", style="bright_white")
    info.append("Check system prerequisites\n", style="dim white")
    info.append("  devsetup scan <path>      ", style="bright_white")
    info.append("Detect frameworks and tools\n", style="dim white")
    info.append("  devsetup banner           ", style="bright_white")
    info.append("Display this cat banner\n", style="dim white")
    info.append("  devsetup --help           ", style="bright_white")
    info.append("Show command documentation\n", style="dim white")

    grid = Table.grid(padding=(0, 3))
    grid.add_column(justify="center")
    grid.add_column(justify="left")
    grid.add_row(cat, info)

    return Panel(grid, title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan", expand=False)


def render_cat_banner(
    style: Literal["matrix", "card"] = "matrix",
    width: int = TOTAL_BANNER_WIDTH,
) -> RenderableType:
    """Render the requested cat banner style."""
    if style == "card":
        return build_card_cat_banner()
    return build_matrix_cat_banner(width=width)

