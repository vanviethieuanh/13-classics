from pydantic import BaseModel, Field

from shisanjing.models.base import Annotation


class Stanza(BaseModel):
    lines: list[str]
    rhyme: str | None = None


class ShijingPoem(Annotation):
    poem_number: int
    genre: str = Field(description="风 / 雅 / 颂")
    stanzas: list[Stanza] = []
    rhyme_scheme: str | None = None
