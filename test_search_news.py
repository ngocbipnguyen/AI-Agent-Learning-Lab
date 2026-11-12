
from tools.search_news import search_news

print("=== NEWS SEARCH TOOL TEST ===")

results = search_news(
    query="Những tin tức AI mới nhất",
    max_results=5
)

for index, item in enumerate(results, start=1):
    print(f"\nTin tức {index}")
    print("Tiêu đề:", item["title"])
    print("Ngày đăng:", item["published_date"])
    print("Link:", item["url"])
    print("Nội dung:", item["content"][:300])
