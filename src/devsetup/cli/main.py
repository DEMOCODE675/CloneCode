"""Typer application entry point."""

from __future__ import annotations

import typer

from devsetup.cli.commands.cache import register as register_cache
from devsetup.cli.commands.clean import register as register_clean
from devsetup.cli.commands.clone import register as register_clone
from devsetup.cli.commands.doctor import register as register_doctor
from devsetup.cli.commands.plugins import register as register_plugins
from devsetup.cli.commands.scan import register as register_scan
from devsetup.cli.commands.setup import register as register_setup
from devsetup.cli.commands.version import register as register_version
from devsetup.cli.ui.console import console, render_banner
from devsetup.core.orchestrator import build_services, repository_destination

app = typer.Typer(add_completion=False, help="Universal development environment bootstrapper.", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Handle the bare URL invocation and print the banner when appropriate."""

    if ctx.invoked_subcommand is not None:
        return
    if not ctx.args:
        console.print(render_banner())
        raise typer.Exit(code=0)
    repository_url = ctx.args[0]
    services = build_services()
    target = repository_destination(repository_url, services.config)
    services.cloner.clone(repository_url, target, branch=services.config.clone.branch, depth=services.config.clone.depth)
    snapshot = services.scanner.scan(target)
    detected = services.detector.detect_snapshot(snapshot)
    results = services.installer.install(detected)
    console.print(render_banner())
    for result in results:
        status = "PASS" if result.success else "FAIL"
        console.print(f"{status} {result.name}: {result.message}")
    console.print("Project Ready")
    console.print(f"Run: {detected.package_manager.value} dev")
    raise typer.Exit(code=0)


register_clone(app)
register_setup(app)
register_doctor(app)
register_scan(app)
register_plugins(app)
register_clean(app)
register_cache(app)
register_version(app)


if __name__ == "__main__":
    app()