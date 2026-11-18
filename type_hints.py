
def get_news() -> dict[str, str]:
    return {
        "title": "OpenAI ra mắt mô hình AI mới",
        "source": "OpenAI",
        "category": "AI"
    }


news = get_news()

print(news)
