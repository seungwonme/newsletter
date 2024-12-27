import sys
from newsletter.graph.graph import get_graph
from newsletter.graph.state import WorkflowState
from newsletter.graph.parse import get_unique_filename

if __name__ == "__main__":
    graph = get_graph()
    argv = sys.argv
    if len(argv) == 1:
        print("Usage: python app.py <search_term>")
        sys.exit(0)
    state = WorkflowState(
        search_terms=[argv[1]],
        search_result="",
        summary_content="",
        newsletter_content="",
        is_approved=False,
        urls=[],
        remaining_loops=3,
    )

    res = graph.invoke(state)
    print(res["search_terms"])
    print(res["search_result"])
    print(res["newsletter_content"])
    print(res["is_approved"])

    # 결과를 파일에 저장합니다.
    filename = get_unique_filename("../output", "newsletter")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(res["newsletter_content"])
