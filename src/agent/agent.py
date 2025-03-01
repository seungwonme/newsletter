from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agent.nodes.crawler import crawler_node
from src.agent.nodes.curator import curator_node
from src.agent.nodes.generator import generator_node
from src.agent.nodes.rss_finder import rss_finder_node
from src.agent.nodes.search import search_node
from src.agent.nodes.summarizer import summarizer_node
from src.agent.utils.state import WorkflowState
from src.agent.utils.visualize import display_graph, save_graph_as_png


# 워크플로우 구성
def get_graph() -> CompiledStateGraph:
    builder = StateGraph(WorkflowState)

    # 노드 추가
    builder.add_node("rss_finder", rss_finder_node)
    builder.add_node("search", search_node)
    builder.add_node("curator", curator_node)
    builder.add_node("crawler", crawler_node)
    builder.add_node("summarizer", summarizer_node)
    builder.add_node("generator", generator_node)

    # 엣지 추가
    builder.add_edge(START, "rss_finder")
    # FIXME: rss checker -> rss_finder or search로 분기해야할듯?
    # 만약 [bbc, 개인 블로그]가 소스라면 지금은 bbc만 처리하고 개인 블로그는 무시함
    builder.add_conditional_edges(
        "rss_finder",
        lambda x: "curator" if len(x["search_contents"]) > 10 else "search",
        ["curator", "search"],
    )
    builder.add_edge("search", "curator")
    builder.add_edge("curator", "crawler")
    builder.add_edge("crawler", "summarizer")
    builder.add_edge("summarizer", "generator")
    builder.add_edge("generator", END)
    graph = builder.compile()

    # TEST: 그래프 시각화
    save_graph_as_png(graph, "workflow.png")
    display_graph(graph)

    return graph
