from pydantic import BaseModel, Field


class EntityRef(BaseModel):
    name: str
    entity_type: str = Field(description="person / place / office / term")
    start: int
    end: int


class QuoteRef(BaseModel):
    text: str
    start: int
    end: int
    source: str | None = None


class Token(BaseModel):
    text: str
    pos: str | None = None


class Annotation(BaseModel):
    book: str
    chapter: str | None = None
    section: str | None = None
    text: str
    tokens: list[Token] = []
    entities: list[EntityRef] = []
    quotes: list[QuoteRef] = []
    notes: list[str] = []
