# oasis/ev_generator/cli_ev.py
import typer
from oasis.ev_generator.core_ev import generate_ev_scenario
from oasis.logger import log

app = typer.Typer()

@app.command()
def generate(n: int = 1):
    log.info({"total": n, "event": "starting_generation"})
    for i in range(1, n + 1):
        log.info({"i": i, "event": "generating"})
        scenario = generate_ev_scenario()
        if scenario:
            typer.echo(f"✅ Generated: {scenario['title']}")
        else:
            typer.echo("❌ Failed to generate scenario.")

if __name__ == "__main__":
    app()
