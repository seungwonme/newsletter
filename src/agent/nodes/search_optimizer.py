import datetime
import json

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.agent.utils.prompts import QUERY_OPTIMIZATION_PROMPT
from src.agent.utils.state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


class _OptimizeSearchQuery(BaseModel):
    intent_of_requested_content: str
    optimized_search_query: str


def search_optimizer_node(state: WorkflowState):
    prompt = QUERY_OPTIMIZATION_PROMPT.format(
        search_query=state["search_queries"][0],
        current_date=datetime.datetime.now(),
    )
    response = llm.bind_tools([_OptimizeSearchQuery]).invoke(prompt)
    arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])

    intent_of_requested_content = arguments.get("intent_of_requested_content", "")
    optimized_search_query = arguments.get("optimized_search_query", "")
    print("====================search_optimizer====================")
    print(f"Intent of requested content: {intent_of_requested_content}")
    print(f"Optimized search query: {optimized_search_query}")
    state["search_queries"].pop()
    if optimized_search_query:
        state["search_queries"].append(optimized_search_query)

    return {
        "intent_of_requested_content": intent_of_requested_content,
        "search_queries": state["search_queries"],
    }


# pylint: disable=C0413, W0404
from src.agent.utils.state import initialize_state  # noqa: E402

if __name__ == "__main__":
    state = WorkflowState(
        initialize_state(
            search_queries=[
                "Tell me about the DOGE (Department of Government Efficiency) department in"
                " the United States led by Elon Musk."
            ]
        )
    )
    search_optimizer_node(state)
