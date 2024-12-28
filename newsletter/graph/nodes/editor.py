from langchain_openai import ChatOpenAI
from newsletter.graph.state import WorkflowState
from newsletter.prompts import NEWS_LETTER


llm = ChatOpenAI(model="gpt-4o-mini")


def editor_node(state: WorkflowState):
    # Construct the prompt for translation and summarization
    prompt = f""" Create a newsletter with the “Content” below. The format of your newsletter should follow the template in “Example” below. Answers must be in Korean.

Content:
{state['summary_content']}

Example:
{NEWS_LETTER}

Answer:
"""

    # Invoke the language model with the constructed prompt
    response = llm.invoke(prompt)
    if isinstance(response.content, list):
        content_str = "".join(map(str, response.content))
    else:
        content_str = response.content
    print("====================editor_node====================")
    print(content_str)
    return {"newsletter_content": content_str}
