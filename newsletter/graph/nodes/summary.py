from newsletter.graph.state import WorkflowState
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")


def translate_and_summarize_node(state: WorkflowState):
    prompt = f"""You're David, a veteran translator with 10 years of experience working on the U.S.-Korea summit. I'd like you to professionally translate the following into Korean and summarize the key points in Korean. Please keep all responses in Korean and follow the "format" below.

format:
**내용**: ...
**요약**: ...

original content:
{state['search_result']}"""
    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        content_str = "".join(map(str, response.content))
    else:
        content_str = response.content

    print("====================translate_and_summarize_node====================")
    print(content_str)

    new_summary_content = (
        state["summary_content"] + "\n\n" + content_str
        if len(state["summary_content"]) > 0
        else content_str
    )

    return {"summary_content": new_summary_content}


def translator_node(state: WorkflowState):
    prompt = f"""You are David, a veteran translator with 10 years of experience participating in Korea-US summits. Please professionally translate the following content into Korean.
    
    Original content:
{state['search_result']}"""


def summarize_node(state: WorkflowState):
    # Construct the prompt for translation and summarization
    prompt = f"""You are an expert in summarizing complex information. Please provide a concise summary of the key points from the following content.

Original content:
{state['search_result']}"""

    # Invoke the language model with the constructed prompt
    summary = llm.invoke(prompt)
    print("====================summary====================")
    print(summary)
    return {"search_result": summary.content}
