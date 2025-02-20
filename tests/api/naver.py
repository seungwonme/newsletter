# https://developers.naver.com/main/
# https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4
import json
import os
from xml.etree import ElementTree as ET

import requests
from dotenv import load_dotenv

from tests.utils import save_text_to_unique_file

# Load environment variables
load_dotenv()


def parse_and_save_news_data(response: str):
    """
    Parses the news data from the API response and saves it to a unique file.

    Args:
        response (str): The API response containing news data in XML format.
    """
    root = ET.fromstring(response)
    items = root.findall(".//item")
    parsed_articles = []

    for item in items:
        parsed_article = {
            "title": item.findtext("title"),
            "link": item.findtext("link"),
            "description": item.findtext("description"),
            "pubDate": item.findtext("pubDate"),
            "source_name": item.findtext("originallink"),
        }
        parsed_articles.append(parsed_article)

    save_text_to_unique_file(
        json.dumps(parsed_articles, indent=4, ensure_ascii=False), file_name="news_data.json"
    )


def main():
    """
    Main function to fetch news data from Naver News API and save it to a unique file.
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError(
            "Client ID or Client Secret not found. Please set the NAVER_CLIENT_ID and NAVER_CLIENT_SECRET environment variables."
        )

    url = "https://openapi.naver.com/v1/search/news.xml"
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    params = {"query": "거시 경제", "display": 10, "start": 1, "sort": "sim"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        parse_and_save_news_data(response.text)
    else:
        print(f"Failed to fetch news data: {response.status_code}")


if __name__ == "__main__":
    main()
