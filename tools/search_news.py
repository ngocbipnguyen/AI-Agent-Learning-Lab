
import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Đọc API Key từ file .env
load_dotenv(override=True)

# Khởi tạo Tavily Client
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_news(query: str, max_results: int = 5) -> list:
    """
    Tìm kiếm tin tức mới nhất trên Internet.

    Args:
        query: Chủ đề tin tức cần tìm.
        max_results: Số lượng kết quả tối đa.

    Returns:
        Danh sách tin tức tìm được.
    """

    response = tavily.search(
        query=query,
        topic="news",
        time_range="week",
        max_results=max_results
    )

    news = []

    for item in response.get("results", []):
        news.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content"),
            "published_date": item.get("published_date")
        })

    return news
