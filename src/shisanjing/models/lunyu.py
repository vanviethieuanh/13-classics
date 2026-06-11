from pydantic import Field

from shisanjing.models.base import Annotation


class LunyuSaying(Annotation):
    speaker: str | None = Field(default=None, description="Who spoke (e.g., 孔子, 曾子)")
    topic_tags: list[str] = Field(default_factory=list, description="如 仁、礼、孝")
    disciples_present: list[str] = Field(default_factory=list)
