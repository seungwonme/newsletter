import csv
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, NoReturn, Optional

import pytz
import requests

from src.agent.utils.file_utils import save_text_to_unique_file


def load_rss_feeds(csv_path: str) -> Optional[List[Dict[str, str]]]:
    """
    CSV 파일에서 RSS 피드 정보를 로드합니다.

    Args:
        csv_path: RSS 피드 정보가 담긴 CSV 파일 경로

    Returns:
        List[Dict[str, str]]: 성공시 피드 정보 리스트 반환
        None: 실패시 None 반환

    Raises:
        FileNotFoundError: CSV 파일을 찾을 수 없는 경우
        csv.Error: CSV 파싱 중 에러 발생한 경우
    """
    try:
        feeds = []
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not {"publisher", "category", "url"}.issubset(reader.fieldnames or []):
                logging.error("CSV 파일에 필수 컬럼이 누락되었습니다")
                return None

            for row in reader:
                if not all(row.values()):
                    logging.warning("빈 값이 있는 행을 건너뜁니다: %s", row)
                    continue

                feeds.append(
                    {
                        "publisher": row["publisher"].strip(),
                        "category": row["category"].strip(),
                        "url": row["url"].strip(),
                    }
                )

        if not feeds:
            logging.warning("로드된 피드가 없습니다")
            return None

        return feeds

    except FileNotFoundError:
        logging.error("파일을 찾을 수 없습니다: %s", csv_path)
        return None
    except csv.Error as e:
        logging.error("CSV 파싱 중 에러 발생: %s", str(e))
        return None
    except Exception as e:
        logging.error("예상치 못한 에러 발생: %s", str(e))
        return None


def fetch_feed(url: str) -> str | NoReturn:
    """RSS 피드를 가져옵니다.

    Args:
        url: RSS 피드 URL

    Returns:
        str: RSS 피드 내용

    Raises:
        HTTPError: HTTP 요청이 실패한 경우 (상태 코드가 400-599 사이일 때)
        RequestException: 기타 네트워크 관련 오류 발생 시
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_date(date_str: str) -> Optional[datetime]:
    """
    다양한 형식의 날짜 문자열을 KST datetime 객체로 파싱합니다.

    Args:
        date_str: 파싱할 날짜 문자열
        - RFC 822:               "Fri, 21 Feb 2025 04:32:08 GMT"
        - RFC 822 with timezone: "Fri, 21 Feb 2025 04:32:08 +0000"
        - ISO 8601:              "2025-02-21T04:32:08+00:00"
        - Basic datetime:        "2025-02-21 04:32:08"

    Returns:
        Optional[datetime]: 성공시 KST timezone의 datetime 객체, 실패시 None

    Raises:
        None: ValueError는 내부적으로 처리되어 None을 반환
    """
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # RFC 822 with timezone
        "%a, %d %b %Y %H:%M:%S GMT",  # BBC style
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601
        "%Y-%m-%d %H:%M:%S",  # Basic datetime
    ]

    kst_timezone = pytz.timezone("Asia/Seoul")

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            # GMT/UTC 시간을 가정하고 KST로 변환
            if parsed_date.tzinfo is None:
                parsed_date = pytz.utc.localize(parsed_date)
            return parsed_date.astimezone(kst_timezone)
        except ValueError:
            continue

    return None


def parse_feed(xml_content: str) -> List[Dict[str, Optional[str | datetime]]]:
    """
    XML 콘텐츠를 파싱하여 뉴스 항목 리스트를 반환합니다.

    Args:
        xml_content: 파싱할 RSS 피드 XML 문자열

    Returns:
        List[Dict[str, Optional[str | datetime]]]: 파싱된 뉴스 항목 리스트:
        - title: 뉴스 제목
        - link: 뉴스 링크
        - description: 뉴스 설명
        - pub_date: 발행일 (datetime 객체 또는 None)
        - creator: 작성자
        - guid: 고유 식별자
        - thumbnail_url: 썸네일 이미지 URL

    Raises:
        ET.ParseError: XML 파싱 실패시
        KeyError: 필수 XML 요소가 누락된 경우
    """
    ns = {"dc": "http://purl.org/dc/elements/1.1/", "media": "http://search.yahoo.com/mrss/"}
    root = ET.fromstring(xml_content)
    items = root.findall(".//item")
    channel = root.find("channel")

    def get_text(elem: Optional[ET.Element]) -> str:
        """요소의 텍스트를 추출하고 CDATA 섹션을 정리합니다."""
        if elem is None or elem.text is None:
            return ""
        text = elem.text.strip()
        return text.replace("<![CDATA[", "").replace("]]>", "")

    def get_pub_date(item: ET.Element) -> Optional[datetime]:
        """항목의 발행일을 추출합니다."""
        date_elem = item.find("pubDate")
        if date_elem is None:
            date_elem = item.find("lastBuildDate")
        if date_elem is None and channel is not None:
            date_elem = channel.find("lastBuildDate")
        return parse_date(date_elem.text) if date_elem is not None and date_elem.text else None

    def get_thumbnail_url(item: ET.Element) -> str:
        """썸네일 이미지 URL을 추출합니다."""
        thumbnail = item.find("media:thumbnail", ns)
        return thumbnail.get("url", "") if thumbnail is not None else ""

    news_items = []
    for item in items:
        news_item = {
            "title": get_text(item.find("title")),
            "link": get_text(item.find("link")),
            "description": get_text(item.find("description")),
            "pub_date": get_pub_date(item),
            "creator": get_text(item.find("dc:creator", ns)),
            "guid": get_text(item.find("guid")),
            "thumbnail_url": get_thumbnail_url(item),
        }
        news_items.append(news_item)

    return news_items


def format_news_content(news_items: List[Dict], publisher: str, category: str) -> str:
    """뉴스 항목을 포맷팅된 문자열로 변환합니다."""
    content = f"\n=== {publisher.upper()} - {category.upper()} ===\n"
    for item in news_items:
        content += f"\nTitle: {item['title']}\n"
        content += f"Date: {item['pub_date']}\n" if item["pub_date"] else ""
        content += f"Link: {item['link']}\n"
        content += f"Thumbnail: {item['thumbnail_url']}\n"
        content += f"Description: {item['description']}\n"
        content += "-" * 80 + "\n"
    return content


def main():
    try:
        # RSS 피드 정보 로드
        feeds = load_rss_feeds("data/rss_feeds.csv")

        all_news_content = ""
        # for feed in feeds:
        #     try:
        #         xml_content = fetch_feed(feed["url"])
        #         news_items = parse_feed(xml_content)
        #         news_content = format_news_content(news_items, feed["publisher"], feed["category"])
        #         all_news_content += news_content
        #     except (requests.RequestException, ET.ParseError) as e:
        #         print(f"Error processing feed {feed['url']}: {e}")
        #         continue
        feed = feeds[0]
        try:
            xml_content = fetch_feed(feed["url"])
            news_items = parse_feed(xml_content)
            news_content = format_news_content(news_items, feed["publisher"], feed["category"])
            all_news_content += news_content
        except (requests.RequestException, ET.ParseError) as e:
            print(f"Error processing feed {feed['url']}: {e}")

        if all_news_content:
            save_text_to_unique_file(
                all_news_content, file_name=f"news_{datetime.now().strftime('%Y%m%d')}"
            )

    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    main()
