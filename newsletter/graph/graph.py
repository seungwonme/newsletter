from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from newsletter.graph.visualize import save_graph_as_png, display_graph
from newsletter.graph.state import WorkflowState
from newsletter.graph.nodes.search import search_node
from newsletter.graph.nodes.crawling import crawling_node
from newsletter.graph.nodes.summary import translate_and_summarize_node
from newsletter.graph.nodes.editor import editor_node
from newsletter.graph.nodes.confirm import confirm_node


# 워크플로우 구성
def get_graph() -> CompiledStateGraph:
    builder = StateGraph(WorkflowState)

    # 노드 추가
    builder.add_node("search", search_node)
    # NOTE: Tavily가 어차피 요약까지 하는데 굳이 크롤링을 할 필요가 있을까?
    # builder.add_node("crawling", crawling_node)
    builder.add_node("translate_and_summarize", translate_and_summarize_node)
    builder.add_node("create_newsletter", editor_node)
    builder.add_node("confirm_newsletter", confirm_node)

    # def crawl_condition(state: WorkflowState):
    #     return "crawling" if len(state["urls"]) > 0 else "translate_and_summarize"

    def review_condition(state: WorkflowState):
        return END if state["is_approved"] else "search"

    # 엣지 추가
    builder.add_edge(START, "search")
    builder.add_edge("search", "translate_and_summarize")
    # builder.add_conditional_edges(
    #     "crawling", crawl_condition, ["translate_and_summarize", "crawling"]
    # )
    builder.add_edge("translate_and_summarize", "create_newsletter")
    builder.add_edge("create_newsletter", "confirm_newsletter")
    builder.add_conditional_edges(
        "confirm_newsletter", review_condition, [END, "search"]
    )

    graph = builder.compile()

    # 그래프 시각화
    save_graph_as_png(graph, "workflow.png")
    display_graph(graph)

    return graph


import sys

if __name__ == "__main__":
    graph = get_graph()
    argv = sys.argv
    if len(argv) == 1:
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
