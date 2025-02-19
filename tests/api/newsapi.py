# 한국어 안됨
# https://newsapi.org/docs/endpoints/everything

import os

from dotenv import load_dotenv
from newsapi import NewsApiClient

# from tests.api.utils import save_text_to_unique_file

load_dotenv()


def main():
    newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(
        q="bitcoin",
        category="business",
        language="en",
    )

    print(top_headlines)

    # # /v2/everything
    # all_articles = newsapi.get_everything(
    #     q="bitcoin",
    #     sources="bbc-news,the-verge",
    #     domains="bbc.co.uk,techcrunch.com",
    #     from_param="2017-12-01",
    #     to="2017-12-12",
    #     language="en",
    #     sort_by="relevancy",
    #     page=2,
    # )

    # # /v2/top-headlines/sources
    # sources = newsapi.get_sources()


if __name__ == "__main__":
    main()

# https://ahrefs.com/blog/google-advanced-search-operators/
# https://news.google.com/search?q=economy%20site%3Abbc.com%20after%3A2025-02-10&hl=ko&gl=KR&ceid=KR%3Ako
# https://brunch.co.kr/@moaikim/38
# https://brunch.co.kr/@moaikim/38
