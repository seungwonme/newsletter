from src.agent.agent import get_graph
from src.agent.utils.state import WorkflowState, initialize_state


def create_newsletter(topics: list[str], sources: list[str]) -> dict:
    graph = get_graph()
    state = WorkflowState(initialize_state(topics=topics, sources=sources))
    res = graph.invoke(state, {"recursion_limit": 100})

    res_dict = {
        "title": res["newsletter_title"],
        "content": res["newsletter_contents"][-1],
    }
    return res_dict
