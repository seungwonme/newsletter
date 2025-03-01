import json
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing_extensions import List

from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.prompts import WRITER_PROMPT
from src.agent.utils.state import ContentData, WorkflowState

load_dotenv()


# TODO: llm 6번 돌리기 (5번 기사 + 1번 전체 요약 및 틀 다듬기)
def generator_node(state: WorkflowState):
    class NewsSection(BaseModel):
        """
        A model representing a section of a newsletter, with a 1:1 mapping to an input article.
        Consider all articles collectively when creating subheadings or content.

        Attributes:
            subheading (str): The subheading of the content section
            content (str): The summarized or reformatted content from the source article.
        """

        subheading: str
        content: str

    class WriterResponse(BaseModel):
        """A model representing the response from a writer agent.

        This class encapsulates the structured output of a writing task. The number of content
        sections must exactly match the number of input articles, maintaining a 1:1 relationship
        between source articles and output sections.

        Attributes:
            title (str): The main title of the written content.
            contents (List[NewsSection]): A list of content sections, where each NewsSection corresponds to exactly one input article.
            summary (str): A brief 3-line summary of all processed documents
        """

        title: str
        contents: List[NewsSection]
        summary: str

    topic_str = ", ".join(state["topics"])
    full_contents = ""
    for idx, item in enumerate(state["search_contents"]):
        full_contents += f"---article_{idx + 1}_start---\n"
        full_contents += f"Title: {item.get('title', '')}\n"
        full_contents += "Content:\n"
        full_contents += f"{item.get('content', '')}\n"
        full_contents += f"---article_{idx + 1}_end---\n\n"
    now = datetime.now().strftime("%Y-%m-%d")
    prompt = WRITER_PROMPT.invoke(
        {
            "language": state["language"],
            "topics": topic_str,
            "sources": full_contents,
        }
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    response = llm.bind_tools([WriterResponse]).invoke(prompt)
    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
    title = arguments.get("title", [])
    contents = arguments.get("contents", [])
    summary = arguments.get("summary", [])

    full_contents = now + "\n\n"
    if state["newsletter_img_url"]:
        full_contents += f"![]({state['newsletter_img_url']})\n\n"
    # FIXME: 지금은 기사와 그 기사의 요약이 1:1 매칭이라고 가정하고 있음
    for idx, news_section in enumerate(contents):
        full_contents += (
            f"## [{news_section['subheading']}]({state['search_contents'][idx]['url']})\n\n"
        )
        if state["search_contents"][idx].get("thumbnail_url"):
            full_contents += f"![]({state['search_contents'][idx].get('thumbnail_url', '')})\n\n"
        full_contents += f"{news_section['content']}\n\n"
    full_contents += f"## Summary\n\n{summary}\n"

    return {
        "newsletter_title": title,
        "newsletter_content": full_contents,
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
    result_state = generator_node(test_state)

    # 결과 출력
    print("\nGenerated Contents:")
    print("-" * 80)
    print(result_state["newsletter_content"])

    # 결과 파일 저장
    save_text_to_unique_file(result_state["newsletter_content"], "generator_test")
