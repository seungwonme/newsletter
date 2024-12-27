from newsletter.graph.state import WorkflowState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import json


llm = ChatOpenAI(model="gpt-4o-mini")


class EditorNode(BaseModel):
    is_approved: bool
    search_term: str


def confirm_node(state: WorkflowState):
    search_terms = ", ".join(state["search_terms"])
    prompt = f"""You are the editor-in-chief of your 10th year newsletter. Check the content of your newsletter below to make sure it's relevant to '{search_terms}' and is clearly understood by everyone who reads it. If it doesn't seem to make sense, provide a new 'search term' without the '{search_terms}'. 

newsletter:
{state['newsletter_content']}"""

    response = llm.bind_tools([EditorNode]).invoke(prompt)
    arguments = json.loads(
        response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )
    print("====================confirm_node====================")
    print(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])

    new_is_approved = arguments["is_approved"] if state["remaining_loops"] > 0 else True
    new_newsletter_content = state["newsletter_content"]
    new_search_terms = state["search_terms"]
    new_search_terms.append(arguments["search_term"])
    new_remaining_loops = state["remaining_loops"] - 1

    if new_is_approved:
        url_content = "### 참고자료\n\n" + "\n".join(
            [f"- {url}" for url in state["urls"]]
        )
        new_newsletter_content += "\n\n" + url_content

    return {
        "is_approved": new_is_approved,
        "search_terms": new_search_terms,
        "newsletter_content": new_newsletter_content,
        "remaining_loops": new_remaining_loops,
    }
