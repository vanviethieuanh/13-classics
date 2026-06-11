import typer
from rich import print as rprint

from shisanjing.config import BOOK_IDS, BOOK_NAMES, PHASES

app = typer.Typer(help="13 Classics (十三经) — structured data extraction pipeline")


@app.command()
def info():
    rprint("[bold]13 Classics (十三经) — Pipeline Project[/bold]")
    rprint(f"\nTotal books: {len(BOOK_IDS)}")
    for phase, books in PHASES.items():
        names = ", ".join(f"{b} ({BOOK_NAMES[b]})" for b in books)
        rprint(f"  Phase {phase}: {names}")


@app.command()
def extract(book: str = typer.Argument(None, help="Book ID to extract, or --all")):
    if book == "all":
        rprint("[yellow]Extracting all PDFs...[/yellow]")
    elif book in BOOK_IDS:
        rprint(f"Extracting [cyan]{BOOK_NAMES.get(book, book)}[/cyan]...")
    else:
        rprint(f"[red]Unknown book: {book}[/red]")


@app.command()
def process(book: str):
    if book not in BOOK_IDS:
        available = ", ".join(BOOK_IDS)
        rprint(f"[red]Unknown book '{book}'. Available: {available}[/red]")
        raise typer.Exit(1)
    rprint(f"Processing [cyan]{BOOK_NAMES[book]} ({book})[/cyan]...")


@app.command()
def validate(book: str = typer.Argument(None, help="Book ID to validate, or --all")):
    if book == "all":
        rprint("[yellow]Validating all structured outputs...[/yellow]")
    elif book in BOOK_IDS:
        rprint(f"Validating [cyan]{BOOK_NAMES.get(book, book)}[/cyan]...")
    else:
        rprint(f"[red]Unknown book: {book}[/red]")


if __name__ == "__main__":
    app()
