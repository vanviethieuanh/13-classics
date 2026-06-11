from pathlib import Path


def extract_text(pdf_path: Path) -> str:
    """Extract text content from a PDF.

    Uses PyMuPDF to extract selectable text while preserving
    reading order as much as possible.
    """
    import fitz

    doc = fitz.open(pdf_path)
    pages: list[str] = []
    for page in doc:
        text = page.get_text("text")
        pages.append(text)
    doc.close()
    return "\n\n".join(pages)
