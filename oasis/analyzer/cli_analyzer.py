# oasis/analyzer/cli_analyzer.py

import typer
from oasis.analyzer.linkage import link_signals_to_scenarios

app = typer.Typer(help="OASIS Analyzer — Connect Signals to Scenarios")


@app.command()
def link(
    min_confidence: float = typer.Option(
        0.5, "--min-confidence", help="Minimum confidence to store a link"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="If set, no links are written to the database"
    ),
):
    """
    Link precursor signals to scenarios based on tags, text, and score.
    """
    if dry_run:
        typer.echo(f"[DRY RUN] Linking signals with min_confidence={min_confidence}...")
        import sqlite3
        links = link_signals_to_scenarios(
            min_confidence=min_confidence,
            conn=sqlite3.connect(":memory:")
        )
    else:
        typer.echo(f"Linking signals with min_confidence={min_confidence}...")
        links = link_signals_to_scenarios(min_confidence=min_confidence)

    typer.echo(f"Total links created: {len(links)}")
    if dry_run:
        typer.echo("[DRY RUN] No changes were written to the database.")


@app.command()
def summary():
    from oasis.analyzer.linkage import get_links_for_dashboard
    links = get_links_for_dashboard()
    if not links:
        typer.echo("No signal→scenario links found.")
        return

    typer.echo(f"Total links: {len(links)}")
    for l in links[:10]:
        typer.echo(
            f"{l['signal_title'][:50]:50} → {l['scenario_narrative'][:80]:80} | "
            f"conf: {l['confidence']:.3f}"
        )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("No subcommand specified. Running full link sweep...")
        # ← THIS WAS THE BUG: link() passes OptionInfo objects
        # ← FIXED: manually pass default values
        link(min_confidence=0.5, dry_run=False)

@app.command()
def llm_review(
    limit: int = typer.Option(10, help="Number of links to analyze"),
    model: str = typer.Option("mistral:7b", help="Ollama model name"),
    min_confidence: float = typer.Option(0.5, help="Minimum link confidence")
):
    """Run local LLM (Ollama) review on linked scenarios."""
    from oasis.analyzer.llm_linker import analyze_links
    analyze_links(limit=limit, model=model, min_conf=min_confidence)


if __name__ == "__main__":
    app()