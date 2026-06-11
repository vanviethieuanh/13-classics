from pydantic import Field

from shisanjing.models.base import Annotation


class YijingHexagram(Annotation):
    hexagram_number: int = Field(ge=1, le=64)
    hexagram_name: str
    trigram_upper: str
    trigram_lower: str
    judgment: str | None = None
    image: str | None = None
    line_texts: list[str] = Field(default_factory=list)
