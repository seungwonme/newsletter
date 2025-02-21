import sys

from src.agent.agent import get_graph
from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.state import WorkflowState, initialize_state

if __name__ == "__main__":
    graph = get_graph()
    argv = sys.argv
    if len(argv) == 1:
        print("Usage: python src.app <search_query>")
        sys.exit(1)
    state = WorkflowState(initialize_state(query=argv[1]))
    res = graph.invoke(state, {"recursion_limit": 100})
    print("--------------------------------------")
    print(res["intent_of_requested_content"])

    save_text_to_unique_file(res["newsletter_contents"][-1], "newsletter")
