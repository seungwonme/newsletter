from newsletter.graph.graph import get_graph
from newsletter.graph.state import WorkflowState, initialize_state
from newsletter.graph.parse import get_unique_filename
import sys
import os


if __name__ == "__main__":
    graph = get_graph()
    argv = sys.argv
    if len(argv) == 1:
        print("Usage: python app.py <search_query>")
        sys.exit(0)
    state = WorkflowState(initialize_state(argv[1], remaining_loops=2))
    res = graph.invoke(state, {"recursion_limit": 100})
    print("--------------------------------------")
    print(res["intent_of_requested_content"])
    print(res["search_queries"][0])

    current_directory = os.getcwd()
    filename = get_unique_filename(f"{current_directory}/output", "newsletter")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(res["newsletter_content"][-1])
