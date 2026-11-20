import json

with open("news.json", "r", encoding="utf-8") as file:
    news_data = json.load(file)

for news in news_data:
    print("Tiêu đề:", news["title"])
    print("Nguồn:", news["source"])
    print("------------------")