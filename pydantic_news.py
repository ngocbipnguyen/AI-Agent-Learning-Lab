
import logging
from pydantic import BaseModel, Field


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("TechnologyAgent")


class News(BaseModel):
    title: str = Field(min_length=5)
    source: str = Field(min_length=2)
    views: int = Field(ge=0)


def validate_news(news_data: dict) -> News | None:
    try:
        news = News(**news_data)
        logger.info("Dữ liệu tin tức hợp lệ")
        return news

    except Exception:
        logger.exception("Dữ liệu tin tức không hợp lệ")
        return None



news_list = [
    {
        "title": "OpenAI ra mắt mô hình AI mới",
        "source": "OpenAI",
        "views": 15000
    },
    {
        "title": "AI",
        "source": "Google",
        "views": -100
    },
    {
        "title": "Google phát triển công nghệ AI",
        "source": "Google",
        "views": 20000
    }
]

valid_news = []

for news_data in news_list:
    result = validate_news(news_data)

    if result:
        valid_news.append(result)

print("\n=== TIN TỨC HỢP LỆ ===")

for news in valid_news:
    print(news.model_dump())

print(f"\nTổng số tin hợp lệ: {len(valid_news)}")

