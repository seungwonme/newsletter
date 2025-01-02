from langchain_openai import ChatOpenAI
from newsletter.graph.state import WorkflowState
from newsletter.prompts import QUERY_OPTIMIZATION_PROMPT
from pydantic import BaseModel
import json


llm = ChatOpenAI(model="gpt-4o-mini")


class _OptimizeSearchQuery(BaseModel):
    intent_of_requested_content: str
    optimized_search_query: str


def search_optimizer_node(state: WorkflowState):
    prompt = QUERY_OPTIMIZATION_PROMPT.format(search_query=state["search_queries"][0])
    response = llm.bind_tools([_OptimizeSearchQuery]).invoke(prompt)
    arguments = json.loads(
        response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )

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


from newsletter.graph.state import WorkflowState, initialize_state

if __name__ == "__main__":
    state = WorkflowState(
        initialize_state(
            "Tell me about the DOGE (Department of Government Efficiency) department in"
            " the United States led by Elon Musk."
        )
    )
    search_optimizer_node(state)
