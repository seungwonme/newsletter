from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=False,
    include_images=False,
)
