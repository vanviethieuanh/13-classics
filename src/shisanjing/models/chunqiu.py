from pydantic import Field

from shisanjing.models.base import Annotation


class ChunqiuEvent(Annotation):
    year: str = Field(description="e.g., 隐公元年")
    season: str | None = Field(default=None, description="春 / 夏 / 秋 / 冬")
    ganzhi_date: str | None = Field(default=None, description="干支 date")
    states_involved: list[str] = Field(default_factory=list)
    persons: list[str] = Field(default_factory=list)
    event_type: str | None = Field(default=None, description="e.g., 盟、伐、葬、娶")
