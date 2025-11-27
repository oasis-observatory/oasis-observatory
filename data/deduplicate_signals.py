# oasis/tracker_new/deduplicate.py
"""
Deduplication utility for precursor_signals.db
Keeps only the newest record per (source, url).

Usage:
    python -m oasis.tracker_new.deduplicate                    # interactive mode
    python -m oasis.tracker_new.deduplicate --dry-run          # dry-run only
    python -m oasis.tracker_new.deduplicate --no-dry-run       # delete without prompt
"""

from typing import List, Dict
import typer
from oasis.common.db import get_precursor_conn

app = typer.Typer(
    name="deduplicate",
    help="Remove duplicate precursor signals – keep only the newest entry per (source,url)",
)


def find_duplicates() -> List[List[Dict]]:
    """Group rows by (source,url) and return groups with >1 entry."""
    with get_precursor_conn() as conn:
        rows = conn.execute("""
            SELECT id, source, url, title, collected_at, score, stars, tags
            FROM precursor_signals
            ORDER BY source, url, collected_at DESC
        """).fetchall()

    groups: Dict[str, List[Dict]] = {}
    for row in rows:
        key = f"{row['source']}:{row['url']}"
        groups.setdefault(key, []).append(dict(row))

    return [g for g in groups.values() if len(g) > 1]


def clean_duplicates(dry_run: bool = True) -> int:
    """Delete older duplicates. Returns number of rows deleted."""
    duplicates = find_duplicates()
    if not duplicates:
        typer.echo("✓ No duplicates found – database is clean.")
        return 0

    deleted = 0
    with get_precursor_conn() as conn:
        for group in duplicates:
            keep = group[0]  # newest (because sorted DESC)
            to_delete = group[1:]

            typer.echo(f"\n✓ Keeping → {keep['source']}: {keep['title'][:70]} ({keep['collected_at']})")
            for old in to_delete:
                typer.echo(f"  ✗ Remove  → {old['id']} | {old['collected_at']} | score {old['score']:.1f}")
                if not dry_run:
                    conn.execute("DELETE FROM precursor_signals WHERE id = ?", (old["id"],))
                deleted += 1

        if not dry_run:
            conn.commit()
            typer.echo(f"\n✓ Deleted {deleted} duplicate rows.")
        else:
            typer.echo(f"\n→ Dry-run complete: {deleted} rows would be deleted.")

    return deleted


@app.command()
def run(
        dry_run: bool = typer.Option(
            None,
            "--dry-run/--no-dry-run",
            help="Show what would be deleted or actually delete. If not specified, asks interactively.",
        )
):
    """Run the deduplication process."""

    # Interactive mode if no flag provided
    if dry_run is None:
        typer.echo("=" * 60)
        typer.echo("DEDUPLICATION MODE SELECTION")
        typer.echo("=" * 60)
        choice = typer.prompt(
            "\nChoose mode:\n  1) Dry-run (preview only)\n  2) Deduplication (delete duplicates)\n\nEnter choice",
            type=int,
            default=1
        )

        if choice == 1:
            dry_run = True
        elif choice == 2:
            dry_run = False
        else:
            typer.echo("Invalid choice. Defaulting to dry-run.")
            dry_run = True

    # Display mode and execute
    typer.echo("\n" + "=" * 60)
    if dry_run:
        typer.echo("MODE: DRY-RUN (no changes will be made)")
    else:
        typer.echo("MODE: DEDUPLICATION (duplicates will be deleted)")
    typer.echo("=" * 60 + "\n")

    # Confirm for real deletion
    if not dry_run:
        if not typer.confirm("⚠ Are you sure you want to permanently delete duplicates?", default=False):
            typer.echo("\n✗ Operation cancelled.")
            raise typer.Abort()

    clean_duplicates(dry_run=dry_run)


if __name__ == "__main__":
    app()