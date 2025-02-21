import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.prompts import CATEGORY_MATCHING_PROMPT
from src.agent.utils.rss_parse import fetch_feed, load_rss_feeds, parse_feed
from src.agent.utils.state import WorkflowState

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def match_category(topics: list[str], categories: list[str]) -> list[str]:
    """주어진 주제 중 가장 적합한 카테고리를 찾습니다."""

    class Predict(BaseModel):
        categories: list[str]

    llm_with_tool = llm.with_structured_output(Predict)
    chain = CATEGORY_MATCHING_PROMPT | llm_with_tool

    topics_str = ",".join(topics)
    categories_str = "\n".join(f"- {category}" for category in categories)
    print(f"{topics_str} | {categories_str}")

    response = chain.invoke({"topics": topics_str, "categories": categories_str})
    print(response)
    predicted_categories = response.categories

    matched_categories = []
    for category in predicted_categories:
        if category in categories:
            matched_categories.append(category)

    return matched_categories


def rss_finder_node(state: WorkflowState) -> WorkflowState:
    """RSS 피드를 찾고 관련 URL들을 수집하는 노드"""

    # RSS 피드 로드
    feeds = load_rss_feeds("data/rss_feeds.csv")
    if not feeds:
        logging.error("RSS 피드를 로드할 수 없습니다")
        return state

    # sources가 비어있으면 처리하지 않음
    if not state["sources"]:
        return state

    # 각 소스에 대해 처리
    for source in state["sources"]:
        # 매칭되는 publisher 찾기
        matching_feeds = [feed for feed in feeds if source.lower() in feed["url"].lower()]

        if not matching_feeds:
            continue

        # 가능한 카테고리들 수집
        available_categories = list(set(feed["category"] for feed in matching_feeds))

        # 카테고리 매칭
        matched_category = match_category(state["topics"], available_categories)
        if not matched_category:
            continue

        # DEBUG
        print("*" * 80)
        print(matched_category)
        print("*" * 80)

        # 매칭된 카테고리에 해당하는 모든 피드 선택
        selected_feeds = [feed for feed in matching_feeds if feed["category"] in matched_category]
        # 첫 번째 피드 선택 (없으면 None)
        if not selected_feeds:
            continue

        for feed in selected_feeds:
            try:
                # RSS 피드 가져오기 및 파싱
                xml_content = fetch_feed(feed["rss_url"])
                news_items = parse_feed(xml_content)
                print("*" * 50)
                print(news_items)
                print("*" * 50)

                # 뉴스 아이템의 URL들을 state에 추가
                new_urls = [item["link"] for item in news_items if item["link"]]
                state["search_urls"].extend(new_urls)

            except Exception as e:
                logging.error("피드 처리 중 오류 발생: %s", str(e))
                continue

    # 중복 URL 제거
    state["search_urls"] = list(set(state["search_urls"]))

    return state


if __name__ == "__main__":
    # 테스트용 상태
    test_state: WorkflowState = {
        "search_queries": [],
        "search_contents": [],
        "feedback": None,
        "newsletter_title": "",
        "newsletter_contents": [],
        "topics": ["trump", "biden"],
        "sources": ["https://www.bbc.com/", "https://www.wsj.com/"],
    }

    result_state = rss_finder_node(test_state)
    print(f"Found URLs: {len(result_state['search_urls'])}")
    for url in result_state["search_urls"][:5]:  # 처음 5개만 출력
        print(f"- {url}")
