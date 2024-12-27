from typing_extensions import TypedDict
from dataclasses import dataclass


@dataclass
class WorkflowState(TypedDict):
    search_terms: list[str]  # Search terms related to the newsletter
    search_result: str  # Search results related to the newsletter content
    summary_content: str  # Translated and summarized content
    newsletter_content: str  # The main content of the newsletter
    is_approved: bool  # Approval status of the newsletter
    urls: list[str]  # URLs related to the newsletter content
    remaining_loops: int
