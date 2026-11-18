
from pydantic import BaseModel, Field


class News(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    source: str = Field(min_length=2)
    published_date: str | None = None
    views: int = Field(ge=0)


news = News(
    title="OpenAI ra mắt mô hình AI mới",
    source="OpenAI",
    views=15000
)

news_data = news.model_dump()

print(news_data)
print(type(news_data))

news_json = news.model_dump_json(indent=4)

print(news_json)
print(type(news_json))