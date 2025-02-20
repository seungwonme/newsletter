# https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide
import json
import os

import requests
from dotenv import load_dotenv

from tests.utils import save_text_to_unique_file

# Load environment variables
load_dotenv()


def parse_and_save_news_data(response: dict):
    """
    Kakao Web Search API 응답을 파싱하고 파일로 저장합니다.

    Args:
        response (dict): Kakao API 응답 데이터 (JSON 형식)
    """
    # 메타데이터와 문서 데이터 추출
    meta = response.get("meta", {})
    documents = response.get("documents", [])

    formatted_data = {
        "meta": {
            "total_count": meta.get("total_count", 0),
            "pageable_count": meta.get("pageable_count", 0),
            "is_end": meta.get("is_end", True),
        },
        "documents": [],
    }

    for doc in documents:
        parsed_document = {
            "datetime": doc.get("datetime"),
            "contents": doc.get("contents"),
            "title": doc.get("title"),
            "url": doc.get("url"),
        }
        formatted_data["documents"].append(parsed_document)

    # JSON 형식으로 저장 (한글 지원)
    save_text_to_unique_file(
        json.dumps(formatted_data, indent=4, ensure_ascii=False),
        file_name="kakao_search_results.json",
    )


def main():
    """
    Main function to fetch news data from Kakao Web Search API and save it to a unique file.
    """
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the KAKAO_REST_API_KEY environment variable."
        )

    url = "https://dapi.kakao.com/v2/search/web"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": "거시 경제", "sort": "accuracy", "page": 1, "size": 10}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        parse_and_save_news_data(response.json())
    else:
        print(f"Failed to fetch news data: {response.status_code}")


if __name__ == "__main__":
    main()
