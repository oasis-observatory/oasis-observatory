# oasis/tracker/cli_tracker.py

import typer
from oasis.tracker.core_t import fetch_and_store_github_signals, fetch_and_store_arxiv_signals

app = typer.Typer(help="OASIS Precursor Tracker — Live ASI Signals")


@app.command()
def github(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of repositories to fetch"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview only, do not store"),
):
    """Fetch and store GitHub precursor signals."""
    if dry_run:
        typer.echo(f"[DR yard RUN] Would fetch up to {limit} GitHub repositories")
        return
    count = fetch_and_store_github_signals(limit=limit)
    typer.echo(f"GitHub sweep complete → {count} signals stored")


@app.command()
def arxiv(
    limit: int = typer.Option(15, "--limit", "-l", help="Maximum number of papers to fetch"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview only, do not store"),
):
    """Fetch and store arXiv precursor signals."""
    if dry_run:
        typer.echo(f"[DRY RUN] Would fetch up to {limit} arXiv papers")
        return
    count = fetch_and_store_arxiv_signals(limit=limit)
    typer.echo(f"arXiv sweep complete → {count} signals stored")


@app.command(name="full")  # ← Renamed to avoid shadowing built-in
def full_sweep(
    limit: int = typer.Option(20, "--limit", "-l", help="Max items per source (GitHub capped at 100)"),
):
    """Run a complete sweep of both GitHub and arXiv."""
    typer.echo("Starting full OASIS precursor sweep...\n")
    g_count = fetch_and_store_github_signals(limit=min(limit, 15))
    a_count = fetch_and_store_arxiv_signals(limit=limit)
    total = g_count + a_count

    typer.echo(f"\nFull sweep complete — {total} new/updated signals stored")
    typer.echo(f"   ├─ GitHub : {g_count}")
    typer.echo(f"   └─ arXiv  : {a_count}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # Run full sweep by default
        ctx.invoke(full_sweep, limit=ctx.params.get("limit", 15))


if __name__ == "__main__":
    app()