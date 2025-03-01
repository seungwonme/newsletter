import json
import logging
from urllib.parse import urlparse

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.prompts import CATEGORY_MATCHING_PROMPT
from src.agent.utils.rss_parse import fetch_feed, load_csv, parse_feed
from src.agent.utils.state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def extract_domain(url: str) -> str:
    """URL에서 도메인만 추출합니다."""
    try:
        parsed_url = urlparse(url)
        # 프로토콜이 없는 경우 처리
        if not parsed_url.netloc:
            parsed_url = urlparse(f"https://{url}")
        domain = parsed_url.netloc or parsed_url.path
        domain = domain.lower().replace("www.", "")
        return domain
    except Exception as e:
        logging.error("URL 파싱 오류: %s", str(e))
        return url.lower()


def match_categories(topics: list[str], categories: list[str]) -> list[str]:
    """
    주어진 주제와 가장 관련성이 높은 카테고리들을 찾습니다.

    이 함수는 주어진 토픽 리스트와 카테고리 리스트를 비교하여,
    토픽과 가장 관련성이 높은 카테고리를 최대 3개까지 반환합니다.
    LLM을 활용하여 의미적 연관성을 판단합니다.

    Args:
        topics: 관심 주제 목록(예: ["정치", "경제", "기술"])
        categories: 사용 가능한 카테고리 목록(예: ["world", "politics", "business"])

    Returns:
        매칭된 카테고리의 목록. 일치하는 카테고리가 없으면 빈 목록 반환.
        categories가 ["__all__"]인 경우 그대로 반환.
    """

    class Predict(BaseModel):
        """A list of categories that are most relevant to your topic (up to 3)"""

        categories: list[str]

    if categories == ["__all__"]:
        return ["__all__"]

    try:
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
    except Exception as e:
        logging.error("카테고리 매칭 중 오류 발생: %s", str(e))
        return ["__all__"] if "__all__" in categories else []

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
        source_domain = extract_domain(source)

        # 매칭되는 publisher 찾기 - 도메인 비교
        matching_feeds = feeds_df[
            feeds_df["url"].apply(lambda x, domain=source_domain: extract_domain(x) == domain)
        ]

        if matching_feeds.empty:
            continue

        # 가능한 카테고리들 수집 - DataFrame의 unique 사용
        available_categories = matching_feeds["category"].unique().tolist()

        # 카테고리 매칭
        matched_categories = match_categories(state["topics"], available_categories)
        if not matched_categories:
            continue

        # 매칭된 카테고리에 해당하는 모든 피드 선택
        selected_feeds = matching_feeds[matching_feeds["category"].isin(matched_categories)]

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

    return state


if __name__ == "__main__":
    test_state: WorkflowState = {
        "topics": ["trump", "biden"],
        "sources": [
            # "https://news.google.com/",
            # "https://news.yahoo.com/",
            # "https://www.nytimes.com/",
            # "https://www.bbc.com/",
            # "https://www.bloomberg.com/",
            # "https://www.reuters.com/",
            # "https://www.wsj.com/",
            # "https://www.foxnews.com/",
            # "https://www.washingtonpost.com/",
            # "https://www.vox.com/",
            # "https://www.huffpost.com/",
            # "https://abcnews.go.com/",
            # "https://www.marketwatch.com/",
            # "https://www.dailymail.co.uk/",
            # "https://news.sbs.co.kr/",
            # "https://news.jtbc.co.kr/",
            # "https://www.chosun.com/",
            "https://www.donga.com/",
            "https://sports.donga.com/",
            # "https://www.mk.co.kr/",
            # "https://www.hankyung.com/",
            # "https://www.khan.co.kr/",
            # "https://www.hani.co.kr/",
            # "https://www.newsis.com/",
            # "https://news.mt.co.kr/",
            # "https://www.yonhapnewstv.co.kr/",
            # "https://www.pressian.com/",
            # "https://www.tongilnews.com/",
            # "https://www.ablenews.co.kr/",
            # "https://www.sisajournal.com/",
            # "https://www.segye.com/",
            # "https://www.sportsworldi.com/",
            # "https://www.segyefn.com/",
            # "https://www.mediatoday.co.kr/",
            # "http://www.donga.com/",
            # "https://sports.donga.com/",
            # "https://www.kmib.co.kr/",
        ],
        "language": "Korean",
        "search_contents": [],
        "newsletter_title": "",
        "newsletter_img_url": "",
        "newsletter_content": "",
    }

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
