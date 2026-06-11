from abc import ABC, abstractmethod
from pathlib import Path

from shisanjing.config import INTERIM_DIR, RAW_DIR, STRUCTURED_DIR


class BasePipeline(ABC):
    """Abstract base for per-book extraction pipelines."""

    book_id: str = ""

    def __init__(self) -> None:
        self.raw_path = RAW_DIR / f"{self.book_id}.pdf"
        self.interim_path = INTERIM_DIR / f"{self.book_id}.txt"
        self.output_path = STRUCTURED_DIR / f"{self.book_id}.json"

    @abstractmethod
    def extract_text(self) -> str:
        """Extract raw text from PDF."""

    @abstractmethod
    def parse_structure(self, text: str) -> list[dict]:
        """Parse book-specific structure (chapters, sections, etc.)."""

    @abstractmethod
    def annotate(self, structured: list[dict]) -> list[dict]:
        """Add semantic annotations to each structural unit."""

    def run(self) -> Path:
        """Execute the full pipeline for this book."""
        text = self.extract_text()
        INTERIM_DIR.mkdir(parents=True, exist_ok=True)
        self.interim_path.write_text(text, encoding="utf-8")

        structured = self.parse_structure(text)
        annotated = self.annotate(structured)

        STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)
        import json

        self.output_path.write_text(
            json.dumps(annotated, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return self.output_path
