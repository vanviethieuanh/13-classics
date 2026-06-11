import json

import typer
from rich import print as rprint

from shisanjing.config import BOOK_IDS, BOOK_NAMES, PHASES, STRUCTURED_DIR

app = typer.Typer(help="13 Classics (十三经) — structured data extraction pipeline")

PIPELINE_REGISTRY: dict[str, type] = {}


def _load_pipeline(book: str):
    import importlib

    mod = importlib.import_module(f"shisanjing.pipelines.{book}")
    for attr in dir(mod):
        val = getattr(mod, attr)
        if isinstance(val, type) and hasattr(val, "book_id") and val.book_id == book:
            return val()
    raise typer.Exit(1)


@app.command()
def info():
    rprint("[bold]13 Classics (十三经) — Pipeline Project[/bold]")
    rprint(f"\nTotal books: {len(BOOK_IDS)}")
    for phase, books in PHASES.items():
        names = ", ".join(f"{b} ({BOOK_NAMES[b]})" for b in books)
        rprint(f"  Phase {phase}: {names}")


@app.command()
def process(
    book: str,
    show: bool = typer.Option(False, "--show", help="Print results to stdout"),
):
    if book not in BOOK_IDS:
        available = ", ".join(BOOK_IDS)
        rprint(f"[red]Unknown book '{book}'. Available: {available}[/red]")
        raise typer.Exit(1)

    pipeline = _load_pipeline(book)

    if not pipeline.raw_path.exists():
        rprint(f"[red]PDF not found: {pipeline.raw_path}[/red]")
        rprint(f"[yellow]Place {book}.pdf in data/raw/[/yellow]")
        raise typer.Exit(1)

    rprint(f"Processing [cyan]{BOOK_NAMES[book]} ({book})[/cyan]...")
    output_path = pipeline.run()

    count = len(json.loads(output_path.read_text(encoding="utf-8")))
    rprint(f"[green]Done — {count} entries → {output_path}[/green]")

    if show:
        rprint(f"\n[bold]Preview ({book}):[/bold]")
        data = json.loads(output_path.read_text(encoding="utf-8"))
        for entry in data[:3]:
            rprint(f"  [{entry.get('section', '?')}] ", end="")
            speaker = entry.get("speaker") or "?"
            rprint(f"{speaker}: ", end="")
            text = entry.get("text", "")
            rprint(f"{text[:80]}..." if len(text) > 80 else text)


@app.command()
def validate(book: str = typer.Argument(None, help="Book ID to validate, or 'all'")):
    if book == "all":
        rprint("[yellow]Validating all structured outputs...[/yellow]")
        for bid in BOOK_IDS:
            p = STRUCTURED_DIR / f"{bid}.json"
            if p.exists():
                rprint(f"  [green]✓ {bid}.json[/green]")
            else:
                rprint(f"  [red]✗ {bid}.json missing[/red]")
    elif book in BOOK_IDS:
        p = STRUCTURED_DIR / f"{book}.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            rprint(f"[green]✓ {book}.json — {len(data)} entries[/green]")
        else:
            rprint(f"[red]✗ {book}.json not found[/red]")
    else:
        rprint(f"[red]Unknown book: {book}[/red]")


if __name__ == "__main__":
    app()
