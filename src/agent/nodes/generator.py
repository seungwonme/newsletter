import json
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing_extensions import List

from src.agent.utils.prompts import REVISER_PROMPT, WRITER_PROMPT
from src.agent.utils.state import ContentData, WorkflowState
from tests.utils import save_text_to_unique_file

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def write(state: WorkflowState):
    class NewsSection(BaseModel):
        """
        A model representing a section of a newsletter.

        Attributes:
            subtitle (str): The subtitle or heading of the news section.
            content (str): The main text content of the news section.
        """

        subtitle: str
        content: str

    class WriterResponse(BaseModel):
        """A model representing the response from a writer agent.

        This class encapsulates the structured output of a writing task, containing
        a title, content sections, and a summary.

        Attributes:
            title (str): The main title of the written content.
            contents (List[NewsSection]): A list of content sections, each being a NewsSection object.
            summary (str): A brief summary or abstract of the entire content.
        """

        title: str
        contents: List[NewsSection]
        summary: str

    topic_str = ", ".join(state["topics"])
    full_contents = ""
    for idx, item in enumerate(state["search_contents"]):
        full_contents += f"##{idx + 1}. {item.get('title', '')}\n"
        if item.get("thumbnail_url"):
            full_contents += f"![]({item.get('thumbnail_url', '')})\n"
        full_contents += item.get("content", "") + "\n\n"
    now = datetime.now().strftime("%Y-%m-%d")
    prompt = WRITER_PROMPT.invoke(
        {
            "topics": topic_str,
            "date": now,
            "sources": full_contents,
        }
    )
    response = llm.bind_tools([WriterResponse]).invoke(prompt)
    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
    title = arguments.get("title", [])
    contents = arguments.get("contents", [])
    summary = arguments.get("summary", [])

    full_contents = ""
    if state["newsletter_img_url"]:
        full_contents += f"![]({state['newsletter_img_url']})\n\n"
    for idx, news_section in enumerate(contents):
        full_contents += (
            f"## [{news_section['subtitle']}]({state['search_contents'][idx]['url']})\n\n"
        )
        if state["search_contents"][idx].get("thumbnail_url"):
            full_contents += f"![]({state['search_contents'][idx].get('thumbnail_url', '')})\n\n"
        full_contents += f"{news_section['content']}\n\n"
    full_contents += f"## Summary\n\n{summary}\n"

    return {
        "newsletter_title": title,
        "newsletter_content": full_contents,
    }


def revise(state: WorkflowState):
    article = state["newsletter_content"]
    prompt = REVISER_PROMPT.invoke({"articles": article, "critique": state["feedback"]})
    response = llm.invoke(prompt)
    if isinstance(response.content, list):
        content_str = "".join(map(str, response.content))
    else:
        content_str = response.content
    print("====================generator_node(revise)====================")
    print(content_str)

    return {"newsletter_content": content_str}


def generator_node(state: WorkflowState):
    return write(state)
    # return write(state) if state["feedback"] is None else revise(state)


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

    # generator_node 실행
    result_state = generator_node(test_state)

    # 결과 출력
    print("\nGenerated Contents:")
    print("-" * 80)
    print(result_state["newsletter_content"])

    # 결과 파일 저장
    save_text_to_unique_file(result_state["newsletter_content"], "generator_test", "json")
