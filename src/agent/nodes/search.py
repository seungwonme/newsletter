import os

from tavily import TavilyClient

from src.agent.utils.state import WorkflowState


def _get_raw_contents(response) -> tuple[list[str], list[str]]:
    raw_contents = []
    urls = []
    for result in response["results"]:
        if result.get("raw_content"):
            raw_contents.append(result["raw_content"])
        if result.get("url"):
            urls.append(result["url"])

    return raw_contents, urls


def search_node(state: WorkflowState):
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = tavily.search(
        query=state["search_queries"][-1],
        max_results=5,
        include_answer=False,
        include_raw_content=True,
    )

    raw_contents, urls = _get_raw_contents(response)

    print("====================search_node====================")
    for idx, content in enumerate(raw_contents):
        print(
            f"search_results[{idx}]:" f" {content[:100] + '...' if len(content) > 100 else content}"
        )

    return {"search_results": raw_contents, "search_urls": urls}


# pylint: disable=C0413
from src.agent.utils.state import initialize_state  # noqa: E402

if __name__ == "__main__":
    search_query = "Tell me about the DOGE (Department of Government Efficiency) department in the United States led by Elon Musk."
    state = WorkflowState(initialize_state(search_query=search_query))
    search_node(state)
