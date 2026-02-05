from datetime import datetime
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    position: int = Field(...)
    title: str = Field(...)
    url: str = Field(...)
    snippet: str | None = Field(None)


class SearchResponse(BaseModel):
    query: str = Field(...)
    fetched_at: datetime = Field(...)
    provider: str = Field(default="serpapi")
    total_returned: int = Field(...)
    results: list[SearchResult] = Field(default_factory=list)
