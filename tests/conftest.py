from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_lunyu_text() -> str:
    return "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？"
