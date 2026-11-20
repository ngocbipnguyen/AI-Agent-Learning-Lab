from pydantic import BaseModel, Field


class News(BaseModel):
    id: int | None = None
    title: str = Field(min_length=5, max_length=200)
    category: str = Field(min_length=2)
    source: str = Field(min_length=2)