from newsletter.tools.search import search
from newsletter.tools.crawl import crawl_url
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from newsletter.utils.visualize import save_graph_as_png, display_graph
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search, crawl_url]
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

sys_msg = SystemMessage(
    content=(
        "You are a helpful assistant tasked with performing arithmetic on a set of"
        " inputs."
    )
)


def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


def get_graph():
    builder = StateGraph(MessagesState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("assistant", "tools")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    save_graph_as_png(graph, "output/graph.png")
    display_graph(graph)

    return graph
