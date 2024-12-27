from tavily import TavilyClient
from newsletter.graph.state import WorkflowState
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def get_search_results(response) -> tuple[str, list[str]]:
    urls = []
    full_content = f"{response["answer"]}\n\n"
    for result in response["results"]:
        full_content += f"title: {result['title']}\n"
        full_content += f"content: {result['content']}\n\n"
        urls.append(result["url"])
    return full_content, urls


def search_node(state: WorkflowState):
    response = tavily.search(
        query=state["search_terms"][-1], max_results=5, include_answer=True
    )
    result, urls = get_search_results(response)
    print("====================search_node====================")
    print(result)

    new_search_result = (
        state["search_result"] + "\n\n" + result
        if len(state["search_result"]) > 0
        else result
    )
    new_urls = state["urls"] + urls

    return {"search_result": new_search_result, "urls": new_urls}
