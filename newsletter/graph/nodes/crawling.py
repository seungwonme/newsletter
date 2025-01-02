import requests
import re
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

UNNECESSARY_CONTENTS = [
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    "form",
    "noscript",
    # 추가
    "iframe",
    "svg",
    "img",
    "button",
    "input",
    "label",
    "select",
    "textarea",
    "video",
    "audio",
    "canvas",
    "map",
    "meter",
]


def _get_content_from_url(url) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while requesting URL: {e}")
        return ""

    soup = BeautifulSoup(response.content, "html.parser")

    for tag in soup(UNNECESSARY_CONTENTS):
        tag.decompose()

    body_content = ""
    if soup.body:
        body_content = str(soup.body)

    # HTML -> Markdown 변환
    cleaned_text = md(body_content, heading_style="ATX", strip=["table", "tr", "td"])

    # 연속된 빈 줄을 하나의 빈 줄로 압축
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return cleaned_text


from newsletter.graph.state import WorkflowState


def crawling_node(state: WorkflowState):
    new_search_result = state["search_result"]
    while len(state["urls"]) > 0:
        url = state["urls"].pop(0)
        content = _get_content_from_url(url)
        new_search_result = (
            state["search_result"] + "\n" + content
            if len(new_search_result) > 0
            else content
        )

    print("====================crawling_node====================")
    print(new_search_result)

    return {"search_result": new_search_result, "urls": []}


import sys
from urllib.parse import urlparse  # 호스트네임 추출을 위한 모듈 추가
from newsletter.graph.parse import get_unique_filename


if __name__ == "__main__":
    url = sys.argv[1]
    content = _get_content_from_url(url)

    # URL의 호스트네임 추출
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    # 결과 파일 저장
    os.makedirs("/Users/anseungwon/dev/easolve/newsletter/output", exist_ok=True)

    # 고유한 파일명 생성
    output_file = get_unique_filename("output", hostname, "md")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"[{hostname}]({url})\n\n")
        file.write(content)

    print(
        "콘텐츠가 파일에 저장되었습니다:"
        f" /Users/anseungwon/dev/easolve/newsletter/{output_file}"
    )
