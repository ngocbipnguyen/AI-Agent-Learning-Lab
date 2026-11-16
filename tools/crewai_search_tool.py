from crewai.tools import tool
from tools.search_news import search_news


@tool("Technology News Search")
def technology_news_search(query: str) -> str:
    """
    Tìm kiếm tin tức công nghệ mới nhất trên Internet
    bằng Tavily. Trả về tiêu đề, nội dung, ngày đăng
    và đường dẫn nguồn của từng tin.
    """

    news = search_news(query=query, max_results=5)

    if not news:
        return "Không tìm thấy tin tức phù hợp."

    return str(news)