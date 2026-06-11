from pydantic import Field

from shisanjing.models.base import Annotation


class XiaojingSaying(Annotation):
    speaker: str | None = Field(default=None)
    topic_tags: list[str] = Field(default_factory=list)
