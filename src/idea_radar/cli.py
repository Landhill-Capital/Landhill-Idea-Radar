"""CLI: `idea-radar run` / `idea-radar latest`."""
from __future__ import annotations
from pathlib import Path
import click

from . import digest


@click.group()
def main():
    """Landhill Idea Radar."""


@main.command()
@click.option("--week", default=None, help="Week label e.g. 2026-W29")
def run(week):
    """Generate this week's digest."""
    path = digest.write(week)
    click.echo(f"Wrote {path}")
    click.echo(path.read_text())


@main.command()
def latest():
    """Show the newest digest."""
    reports = sorted(Path("reports").glob("*-digest.md"))
    if not reports:
        click.echo("No digests yet — run `idea-radar run`.")
        return
    click.echo(reports[-1].read_text())
