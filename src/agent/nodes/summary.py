# import json

# from langchain_openai import ChatOpenAI
# from pydantic import BaseModel

# from src.agent.utils.prompts import SUMMARIZER_PROMPT
# from src.agent.utils.state import WorkflowState

# llm = ChatOpenAI(model="gpt-4o-mini")


# class _SummarizerResponse(BaseModel):
#     is_related: bool
#     summary: str


# def _summarize_content(summary_dict: dict):
#     prompt = SUMMARIZER_PROMPT.format(**summary_dict)

#     response = llm.bind_tools([_SummarizerResponse]).invoke(prompt)
#     arguments = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
#     is_related = arguments.get("is_related", False)
#     summary = arguments.get("summary", "")
#     if is_related:
#         return summary
#     else:
#         return ""


# def summarizer_node(state: WorkflowState):
#     new_summary_contents = state["summary_contents"]
#     summary_dict = {
#         "original_content": "",
#         "intent_of_requested_content": state["intent_of_requested_content"],
#     }

#     while len(state["search_results"]) > 0:
#         summary_dict["original_content"] = state["search_results"].pop(0)
#         if len(summary_dict["original_content"]) > 5000:
#             summary_content = _summarize_content(summary_dict)
#         else:
#             summary_content = summary_dict["original_content"]
#         if summary_content:
#             new_summary_contents.append(summary_content)

#     print("====================summarizer_node====================")
#     for idx, content in enumerate(new_summary_contents):
#         print(
#             f"search_results[{idx}]:" f" {content[:100] + '...' if len(content) > 100 else content}"
#         )

#     return {"summary_contents": new_summary_contents}


# from src.agent.utils.state import initialize_state  # noqa: E402

# if __name__ == "__main__":
#     state = WorkflowState(initialize_state("news"))
#     state["intent_of_requested_content"] = "news"
#     state["search_results"] = [
#         "The quick brown fox jumps over the lazy dog.",
#         "Trump has won the 2025 US presidential election.",
#     ]
#     summarizer_node(state)
