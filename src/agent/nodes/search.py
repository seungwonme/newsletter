import os
from datetime import datetime, timedelta
from urllib.parse import urlparse

from langchain_community.tools import DuckDuckGoSearchResults
from tavily import TavilyClient

from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.state import ContentData, WorkflowState


def search_node(state: WorkflowState):
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    news_items = state["search_contents"]
    image_url = ""
    if tavily_api_key:
        tavily = TavilyClient(api_key=tavily_api_key)

        topic_str = ", ".join(state["topics"])
        response = tavily.search(
            query=topic_str,
            max_results=10,
            include_answer=False,
            include_domains=state["sources"],
            include_raw_content=True,
            include_images=True,
        )

        for result in response["results"]:
            news_item: ContentData = ContentData(
                title=result.get("title"),
                url=result.get("url"),
                description=result["content"],
                content=result["raw_content"],
            )
            news_items.append(news_item)
        image_url = response["images"][0] if response["images"] else ""
    else:
        search = DuckDuckGoSearchResults(output_format="list", num_results=10)
        topic_str = ", ".join(state["topics"])
        for source in state["sources"]:
            parsed_url = urlparse(source)
            now = datetime.now().strftime("%Y-%m-%d")
            past_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            query = f"{topic_str} site:{parsed_url.netloc} &df={past_date}..{now}"
            result = search.invoke(query)
            for r in result:
                news_item: ContentData = ContentData(
                    title=r["title"],
                    url=r["link"],
                    description=r["snippet"],
                )
                news_items.append(news_item)

    return {"search_contents": news_items, "newsletter_img_url": image_url}


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

    result_state = search_node(test_state)
    full_content = f"![newsletter_img_url]({result_state['newsletter_img_url']})\n\n"
    for content in result_state["search_contents"]:
        full_content += f"# {content.get('title')}\n\n"
        full_content += f"> {content.get('date')}" if content.get("date") else ""
        full_content += "\n\n"
        full_content += f"[Article URL]({content.get('url')})\n\n"
        if content.get("content"):
            full_content += f"Content: {content.get('content')}\n\n"
        else:
            full_content += f"Description: {content.get('description')}\n\n"
        full_content += "-" * 80 + "\n\n"
    save_text_to_unique_file(full_content, file_name="search_test")
