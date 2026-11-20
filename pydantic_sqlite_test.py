from database import get_all_news
from news_schema import News

news_list = get_all_news()

for news in news_list:
    news_model = News.model_validate(dict(news))

    print(news_model.model_dump())