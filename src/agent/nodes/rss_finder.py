import json
import logging
from urllib.parse import urlparse

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.prompts import CATEGORY_MATCHING_PROMPT
from src.agent.utils.rss_parse import fetch_feed, load_csv, parse_feed
from src.agent.utils.state import WorkflowState
from tests.utils import save_text_to_unique_file

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def match_category(topics: list[str], categories: list[str]) -> list[str]:
    """주어진 주제 중 가장 적합한 카테고리를 찾습니다."""

    class Predict(BaseModel):
        categories: list[str]

    topics_str = ",".join(topics)
    categories_str = "\n".join(f"- {category}" for category in categories)
    prompt = CATEGORY_MATCHING_PROMPT.format(topics=topics_str, categories=categories_str)
    response = llm.bind_tools([Predict]).invoke(prompt)
    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
    predicted_categories = arguments.get("categories", [])

    matched_categories = []
    for category in predicted_categories:
        if category in categories:
            matched_categories.append(category)

    return matched_categories


def rss_finder_node(state: WorkflowState) -> WorkflowState:
    """RSS 피드를 찾고 관련 URL들을 수집하는 노드"""

    # RSS 피드 로드
    feeds_df = load_csv("data/rss_feeds.csv")

    # sources가 비어있으면 처리하지 않음
    if not state["sources"]:
        return state

    # 각 소스에 대해 처리
    for source in state["sources"]:
        # 매칭되는 publisher 찾기 - DataFrame 필터링 사용
        # TODO: 소스는 프로토콜 없이 도메인만 입력되도록 수정 + 트레일링 슬래시 여부 판단하기
        matching_feeds = feeds_df[
            feeds_df["url"].str.lower().str.contains(source.lower(), na=False)
        ]

        if matching_feeds.empty:
            continue

        # 가능한 카테고리들 수집 - DataFrame의 unique 사용
        available_categories = matching_feeds["category"].unique().tolist()

        # 카테고리 매칭
        matched_category = match_category(state["topics"], available_categories)
        if not matched_category:
            continue

        # 매칭된 카테고리에 해당하는 모든 피드 선택
        selected_feeds = matching_feeds[matching_feeds["category"].isin(matched_category)]

        if selected_feeds.empty:
            continue

        # DataFrame의 각 행을 순회
        for _, feed in selected_feeds.iterrows():
            try:
                # RSS 피드 가져오기 및 파싱
                xml_content = fetch_feed(feed["rss_url"])
                news_items = parse_feed(xml_content)

                state["search_contents"].extend(news_items)

            except Exception as e:
                logging.error("피드 처리 중 오류 발생: %s", str(e))
                continue

    print(state["search_contents"])

    return state


if __name__ == "__main__":
    test_state: WorkflowState = {
        "topics": ["trump", "biden"],
        "sources": ["https://www.bbc.com/", "https://www.wsj.com/"],
        "language": "Korean",
        "search_contents": [],
        "newsletter_title": "",
        "newsletter_img_url": "",
        "newsletter_content": "",
    }

    print(urlparse("https://www.bbc.com/").hostname)

    result_state = rss_finder_node(test_state)
    full_content = ""
    for content in result_state["search_contents"]:
        full_content += f"# {content.get('title')}\n\n"
        full_content += f"> {content.get('date')}" if content.get("date") else ""
        full_content += "\n\n"
        full_content += f"[Article URL]({content.get('url')})\n\n"
        full_content += f"![Thumbnail]({content.get('thumbnail_url')})\n\n"
        full_content += f"Description: {content.get('description')}\n\n"
        full_content += "-" * 80 + "\n\n"
    save_text_to_unique_file(full_content, file_name="rss_finder_test")
