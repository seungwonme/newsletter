import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.prompts import SUMMARIZER_PROMPT
from src.agent.utils.state import ContentData, WorkflowState

load_dotenv()


def summarizer_node(state: WorkflowState):
    class SummaryResponse(BaseModel):
        summary: str

    new_search_contents = state["search_contents"]
    topic_str = ", ".join(state["topics"])
    llm_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0.5).bind_tools([SummaryResponse])

    for idx, item in enumerate(new_search_contents):
        full_content = f"""
Title: {item.get('title', '')}
Content:
{item.get('content', '')}
"""
        prompt = SUMMARIZER_PROMPT.invoke(
            {
                "language": state["language"],
                "topics": topic_str,
                "article": full_content,
            }
        )
        response = llm_with_tools.invoke(prompt)
        arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
        summary = arguments.get("summary")
        new_search_contents[idx]["content"] = summary

    return {
        "search_contents": new_search_contents,
    }


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
        "language": "Korean",
        "search_contents": mock_contents,
        "newsletter_title": "",
        "newsletter_img_url": "",
        "newsletter_content": "",
    }

    # generator_node 실행
    result_state = summarizer_node(test_state)

    # 결과 출력
    print("\nSummarized Contents:")
    print("-" * 80)
    full_contents = ""
    for item in result_state["search_contents"]:
        full_contents += f"""
Title: {item.get('title', '')}
Content:
{item.get('content', '')}
"""
    print(full_contents)

    # 결과 파일 저장
    save_text_to_unique_file(full_contents, "summarizer_test")
