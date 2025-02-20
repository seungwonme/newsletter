import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List

import requests

from tests.utils import save_text_to_unique_file

rss_urls = [
    "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://feeds.bloomberg.com/economics/news.rss",
]


def fetch_feed(url: str) -> str:
    """RSS 피드를 가져옵니다."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_date(date_str: str) -> datetime:
    """날짜 문자열을 datetime 객체로 파싱합니다."""
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")


def parse_feed(xml_content: str) -> List[Dict]:
    """XML 콘텐츠를 파싱하여 뉴스 항목 리스트를 반환합니다."""
    ns = {"dc": "http://purl.org/dc/elements/1.1/"}
    root = ET.fromstring(xml_content)
    items = root.findall(".//item")

    news_items = []
    for item in items:
        news_item = {
            "title": item.find("title").text if item.find("title") is not None else "",
            "link": item.find("link").text if item.find("link") is not None else "",
            "description": (
                item.find("description").text if item.find("description") is not None else ""
            ),
            "pub_date": (
                parse_date(item.find("pubDate").text) if item.find("pubDate") is not None else None
            ),
            "creator": (
                item.find("dc:creator", ns).text if item.find("dc:creator", ns) is not None else ""
            ),
            "guid": item.find("guid").text if item.find("guid") is not None else "",
        }
        news_items.append(news_item)

    return news_items


def main():
    # Thomson Reuters RSS 피드 URL
    rss_url = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"

    try:
        xml_content = fetch_feed(rss_url)
        news_items = parse_feed(xml_content)

        rss_content = ""
        for item in news_items:
            rss_content += f"\nTitle: {item["title"]}\n"
            rss_content += f"Date: {item["pub_date"]}\n"
            rss_content += f"Link: {item["link"]}\n"
            rss_content += "-" * 80 + "\n"

        save_text_to_unique_file(rss_content, file_name="thomson_reuters_news.md")

    except requests.RequestException as e:
        print(f"피드를 가져오는 중 오류 발생: {e}")
    except ET.ParseError as e:
        print(f"XML 파싱 중 오류 발생: {e}")


if __name__ == "__main__":
    main()

# https://www.bbc.co.uk/news/10628494
# https://www.reddit.com/r/rss/comments/u1op2b/does_bloomberg_has_a_rss_feed_for_free/
