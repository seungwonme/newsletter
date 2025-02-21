import json

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.prompts import CHIEF_EDITOR_PROMPT
from src.agent.utils.state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


class _ConfirmResponse(BaseModel):
    is_approved: bool
    new_search_query: str


def _make_prompt_vars(state: WorkflowState) -> dict:
    search_queries = ", ".join(state["search_queries"])
    return {
        "intent_of_requested_content": state["intent_of_requested_content"],
        "search_queries": search_queries,
        "newsletter_content": state["newsletter_contents"][-1],
    }


# pylint: disable=W0622


def critique_node(state: WorkflowState):
    vars = _make_prompt_vars(state)
    prompt = CHIEF_EDITOR_PROMPT.format(**vars)

    response = llm.bind_tools([_ConfirmResponse]).invoke(prompt)
    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])

    print("====================critique_node====================")
    print(arguments)

    new_is_approved = arguments.get("is_approved", True) if state["remaining_loops"] > 0 else True
    new_search_query = arguments.get("new_search_query", "")
    new_search_queries = state["search_queries"]
    if new_search_query:
        new_search_queries.append(arguments.get("new_search_query"))
    new_remaining_loops = state["remaining_loops"] - 1

    return {
        "is_approved": new_is_approved,
        "search_queries": new_search_queries,
        "remaining_loops": new_remaining_loops,
    }
