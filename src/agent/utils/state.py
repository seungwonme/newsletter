from typing_extensions import Optional, TypedDict


class WorkflowState(TypedDict):
    search_queries: list[str]
    search_urls: list[str]
    search_results: list[str]
    feedback: Optional[str]
    newsletter_title: str
    newsletter_contents: list[str]
    topics: list[str]
    sources: list[str]


def initialize_state(**kwargs) -> WorkflowState:
    """
    Initialize the workflow state for the newsletter generation process.
    Args:
        search_query (str): The initial search term related to the newsletter.
        **kwargs: Additional keyword arguments to override the default state values.
    Returns:
        WorkflowState: A dictionary representing the initial state of the workflow.
    WorkflowState Structure:
        search_queries (list[str]): Search terms related to the newsletter.
        search_urls (list[str]): URLs related to the search results.
        search_results (list[str]): Search results related to the newsletter content.
        feedback (Optional[str]): Feedback of the newsletter content.
        newsletter_title (str): Title of the newsletter.
        newsletter_contents (list[str]): The main content of the newsletter.
        topics (list[str]): Topics related to the newsletter.
        sources (list[str]): Sources related to the newsletter.
    """

    state: WorkflowState = {
        "search_queries": [],
        "search_urls": [],
        "search_results": [],
        "feedback": None,
        "newsletter_title": "",
        "newsletter_contents": [],
        "topics": [],
        "sources": [],
    }

    for key, value in kwargs.items():
        if key in state:
            state[key] = value

    return state
