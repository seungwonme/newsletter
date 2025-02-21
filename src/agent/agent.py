from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agent.nodes.critique import critique_node
from src.agent.nodes.curator import curator_node
from src.agent.nodes.generator import generator_node
from src.agent.nodes.rss_finder import rss_finder_node
from src.agent.nodes.search import search_node
from src.agent.nodes.search_optimizer import search_optimizer_node
from src.agent.utils.state import WorkflowState
from src.agent.utils.visualize import display_graph, save_graph_as_png


# 워크플로우 구성
def get_graph() -> CompiledStateGraph:
    builder = StateGraph(WorkflowState)

    # 노드 추가
    builder.add_node("search_optimizer", search_optimizer_node)
    builder.add_node("rss_finder", rss_finder_node)
    builder.add_node("search", search_node)
    builder.add_node("curator", curator_node)
    builder.add_node("generator", generator_node)
    builder.add_node("critique", critique_node)

    # 엣지 추가
    builder.add_edge(START, "search_optimizer")
    builder.add_edge("search_optimizer", "rss_finder")
    builder.add_edge("rss_finder", "search")
    builder.add_edge("search", "curator")
    builder.add_edge("curator", "generator")
    builder.add_edge("generator", "critique")
    builder.add_conditional_edges(
        "critique", lambda x: END if x["feedback"] is None else "generator", [END, "generator"]
    )

    graph = builder.compile()

    # 그래프 시각화
    save_graph_as_png(graph, "workflow.png")
    display_graph(graph)

    return graph
