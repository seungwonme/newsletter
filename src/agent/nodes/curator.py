# flake8: noqa
# pylint: disable=C0413
from dotenv import load_dotenv

load_dotenv()

import json

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.prompts import CURATOR_PROMPT
from src.agent.utils.state import ContentData, WorkflowState
from tests.utils import save_text_to_unique_file


def curator_node(state: WorkflowState):
    class CuratorResponse(BaseModel):
        indices: list[int]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 평가할 데이터 문자열 생성
    content_overviews = "\n".join(
        [
            f"[{idx}]: {content['title']}\n{content['description']}"
            for idx, content in enumerate(state["search_contents"])
        ]
    )
    topic_str = ", ".join(state["topics"])
    prompt = CURATOR_PROMPT.invoke({"topics": topic_str, "sources": content_overviews})
    response = llm.bind_tools([CuratorResponse]).invoke(prompt)

    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
    predicted_indices = arguments.get("indices", [])
    new_content_data = [state["search_contents"][index] for index in predicted_indices]

    return {"search_contents": new_content_data}


if __name__ == "__main__":
    mock_contents: list[ContentData] = [
        {
            "title": "Trump and Biden Set for Rematch as Super Tuesday Looms",
            "url": "https://example.com/article1",
            "description": (
                "Former President Donald Trump and President Joe Biden are preparing for a potential rematch in the 2024 presidential election as Super Tuesday approaches."
            ),
            "thumbnail_url": "https://example.com/thumb1.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Economic Plans Clash as Candidates Focus on Inflation",
            "url": "https://example.com/article2",
            "description": (
                "Presidential candidates outline different approaches to handling inflation and economic growth."
            ),
            "thumbnail_url": "https://example.com/thumb2.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Climate Change Policy Takes Center Stage in Debate",
            "url": "https://example.com/article3",
            "description": (
                "Environmental policies become key discussion point in recent political debates."
            ),
            "thumbnail_url": "https://example.com/thumb3.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Biden Administration's Foreign Policy Challenges",
            "url": "https://example.com/article4",
            "description": (
                "Analysis of current international relations and diplomatic challenges facing the Biden administration."
            ),
            "thumbnail_url": "https://example.com/thumb4.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Trump's Campaign Strategy Ahead of Primaries",
            "url": "https://example.com/article5",
            "description": (
                "Detailed look at former President Trump's campaign approach and strategy for upcoming primaries."
            ),
            "thumbnail_url": "https://example.com/thumb5.jpg",
            "content": "Full article content here...",
        },
    ]

    test_state: WorkflowState = {
        "topics": ["trump", "biden", "election"],
        "sources": ["https://www.bbc.com/", "https://www.wsj.com/"],
        "search_contents": mock_contents,
        "feedback": None,
        "newsletter_title": "",
        "newsletter_img_url": "",
        "newsletter_content": "",
    }

    # curator_node 실행
    result_state = curator_node(test_state)

    # 결과 출력
    print("\nCurated Contents:")
    print("-" * 80)

    full_content = ""
    for content in result_state["search_contents"]:
        # 콘솔 출력
        print(f"Title: {content.get('title')}")
        print(f"Date: {content.get('date')}")
        print(f"URL: {content.get('url')}")
        print("-" * 40)

        # 파일 저장용 포맷팅
        full_content += f"# {content.get('title')}\n\n"
        full_content += f"[Article URL]({content.get('url')})\n\n"
        full_content += f"![Thumbnail]({content.get('thumbnail_url')})\n\n"
        full_content += f"Description: {content.get('description')}\n\n"
        full_content += "---\n\n"

    # 결과 파일 저장
    save_text_to_unique_file(full_content, file_name="curator_test")
