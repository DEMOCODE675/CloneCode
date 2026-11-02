"""Tests for cat banners and banner commands."""

from __future__ import annotations

from typer.testing import CliRunner

from devsetup.cli.main import app
from devsetup.cli.ui.cat_art import (
    TOTAL_BANNER_WIDTH,
    build_card_cat_banner,
    build_matrix_cat_banner,
    render_cat_banner,
)
from devsetup.cli.ui.console import render_banner

runner = CliRunner()


def test_matrix_cat_banner_dimensions() -> None:
    """Verify that every line of the matrix banner matches the exact required width."""
    banner = build_matrix_cat_banner(width=TOTAL_BANNER_WIDTH)
    plain_text = banner.plain
    lines = [line for line in plain_text.splitlines() if line]

    assert len(lines) > 5
    for line in lines:
        # Every line starts with '# ' followed by exactly TOTAL_BANNER_WIDTH characters
        assert line.startswith("# ")
        assert len(line) == TOTAL_BANNER_WIDTH + 2  # '# ' + 72 characters


def test_card_cat_banner_contains_cat_and_title() -> None:
    """Verify the card banner builds properly as a Panel."""
    panel = build_card_cat_banner()
    assert panel.title == "[bold cyan]DevSetup[/bold cyan]"


def test_render_cat_banner_options() -> None:
    """Verify render_cat_banner supports both styles."""
    matrix_art = render_cat_banner("matrix")
    card_art = render_cat_banner("card")
    assert "/\\_____/\\" in str(matrix_art)
    assert card_art is not None


def test_render_banner_defaults_to_matrix() -> None:
    """Verify render_banner() returns matrix banner by default."""
    banner = render_banner()
    assert "/\\_____/\\" in str(banner)
    assert "DevSetup" in str(banner)


def test_cli_bare_shows_cat_banner() -> None:
    """Running devsetup with no arguments should output the cat banner and exit 0."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "/\\_____/\\" in result.stdout
    assert "DevSetup" in result.stdout


def test_cli_banner_command() -> None:
    """Running 'devsetup banner' should output the cat banner."""
    result = runner.invoke(app, ["banner"])
    assert result.exit_code == 0
    assert "/\\_____/\\" in result.stdout


def test_cli_cat_command() -> None:
    """Running 'devsetup cat' should output the mascot cat."""
    result = runner.invoke(app, ["cat"])
    assert result.exit_code == 0
    assert "/\\_____/\\" in result.stdout


def test_cli_banner_card_style() -> None:
    """Running 'devsetup banner --style card' should render the card layout."""
    result = runner.invoke(app, ["banner", "--style", "card"])
    assert result.exit_code == 0
    assert "DevSetup" in result.stdout
    assert "Quick Start:" in result.stdout
