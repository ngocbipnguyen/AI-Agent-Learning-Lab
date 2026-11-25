
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient


# Load file .env tại thư mục gốc repository
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

# Khởi tạo MCP Server
mcp = FastMCP("Technology News Server")


@mcp.tool()
def search_news(query: str, max_results: int = 5) -> str:
    """
    Tìm kiếm tin tức công nghệ trên Internet bằng Tavily.
    Trả về tiêu đề, nội dung, ngày đăng và đường dẫn nguồn.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Lỗi: Chưa cấu hình TAVILY_API_KEY trong file .env."

    if not 1 <= max_results <= 20:
        return "Lỗi: max_results phải nằm trong khoảng 1 đến 20."

    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=query,
            topic="news",
            time_range="week",
            max_results=max_results,
        )

        results = response.get("results", [])

        return json.dumps(
            results,
            ensure_ascii=False,
            indent=2
        )

    except Exception as error:
        return f"Lỗi tìm kiếm tin tức: {error}"



if __name__ == "__main__":
    mcp.run(transport="stdio")
