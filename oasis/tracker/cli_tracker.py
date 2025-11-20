# oasis/tracker/cli_tracker.py

import typer
from oasis.tracker.core_t import fetch_and_store_github_signals, fetch_and_store_arxiv_signals

app = typer.Typer(help="OASIS Precursor Tracker — Live ASI Signals")

@app.command()
def github(limit: int = 20):
    signals = fetch_and_store_github_signals(limit=limit)
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be fetched")


@app.command()
def arxiv(limit: int = 10):
    signals = fetch_and_store_arxiv_signals(limit=limit)
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be fetched")

@app.command()
def all(limit: int = 10):
    g = fetch_and_store_github_signals(limit=limit)
    a = fetch_and_store_arxiv_signals(limit=limit)
    typer.echo(f"Total signals stored: {len(g) + len(a)} (GitHub: {len(g)}, arXiv: {len(a)})")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("Running full sweep...")
        all()

if __name__ == "__main__":
    app()
