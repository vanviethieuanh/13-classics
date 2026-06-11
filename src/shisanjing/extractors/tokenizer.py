from pathlib import Path

import jieba


def load_custom_dict(path: Path | None = None) -> None:
    """Load a custom jieba dictionary for classical Chinese.

    If no path is provided, uses the built-in classical dictionary
    shipped with the project (if available).
    """
    if path and path.exists():
        jieba.load_userdict(str(path))


def segment(text: str) -> list[str]:
    """Tokenize classical Chinese text using jieba."""
    return list(jieba.cut(text))
