from datetime import datetime

from typing_extensions import TypedDict


class BaseContentFields(TypedDict):
    title: str
    url: str
    description: str


class ContentData(BaseContentFields, total=False):
    thumbnail_url: str
    content: str
    date: datetime | None


class WorkflowState(TypedDict):
    topics: list[str]
    sources: list[str]
    language: str
    search_contents: list[ContentData]
    newsletter_title: str
    newsletter_content: str
    newsletter_img_url: str


def initialize_state(**kwargs) -> WorkflowState:
    """
    Initialize the workflow state for the newsletter generation process.
    Args:
        search_query (str): The initial search term related to the newsletter.
        **kwargs: Additional keyword arguments to override the default state values.
    Returns:
        WorkflowState: A dictionary representing the initial state of the workflow.
    WorkflowState Structure:
        topics (list[str]): Topics related to the newsletter.
        sources (list[str]): Sources related to the newsletter.
        language (str): Language for the newsletter
        search_contents (list[ContentData]): Content data for the newsletter.
        newsletter_title (str): Title of the newsletter.
        newsletter_content (str): The main content of the newsletter.
    """

    state: WorkflowState = {
        "topics": [],
        "sources": [],
        "language": "",
        "search_contents": [],
        "newsletter_title": "",
        "newsletter_content": "",
        "newsletter_img_url": "",
    }

    for key, value in kwargs.items():
        if key in state:
            state[key] = value

    return state
