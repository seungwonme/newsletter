import sys
from newsletter.utils.parse import parse, get_unique_filename, custom_serializer
from newsletter.utils.graph import get_graph
import json
import os

# query = sys.argv[1]
app = get_graph()


# Use the agent
# res = agent_executor.invoke({"messages": [HumanMessage(content=f"{query}")]}, config)
# from .utils.tmp import res

# (
#     ai_message_contents,
#     tool_message_urls_and_contents,
#     tool_message_artifact_results,
# ) = parse(res)

# output_file_dir = "output"
# os.makedirs(output_file_dir, exist_ok=True)

# output_file_name = "output"
# response_file_name = "response"
# output_file_path = get_unique_filename(
#     output_file_dir,
#     output_file_name,
# )
# response_file_path = get_unique_filename(
#     output_file_dir, response_file_name, "json"
# )

# res_json = custom_serializer(res)
# with open(output_file_path, "w", encoding="utf-8") as f:
#     f.write(
#         json.dumps(
#             res_json,
#             indent=2,
#             ensure_ascii=False,
#         )
#     )

# full_content = ""

# with open(output_file_path, "w", encoding="utf-8") as f:
#     for ai_message in ai_message_contents:
#         f.write("summary: " + ai_message + "\n")
#         full_content += ai_message + "\n"

#     for tool_message in tool_message_urls_and_contents:
#         f.write("\nweb content:\n")
#         f.write("url: " + tool_message.get("url") + "\n")
#         f.write("content: " + tool_message.get("content") + "\n")

#     for tool_message in tool_message_artifact_results:
#         f.write("\nartifact:\n")
#         f.write("---\n")
#         f.write("title: " + tool_message.get("title") + "\n")
#         f.write("url: " + tool_message.get("url") + "\n")
#         f.write("content: " + tool_message.get("content") + "\n")
#         full_content += "title: " + tool_message.get("title") + "\n"
#         full_content += "content: " + tool_message.get("content") + "\n"
#         full_content += "url: " + tool_message.get("url") + "\n"

# from langchain_core.prompts import PromptTemplate
# from langchain_core.messages import HumanMessage

# prompt_template = PromptTemplate.from_template(
#     """You are a skilled newsletter editor. You have a keen ability to instantly recognize what people want to know. Below are materials to create content. To produce a high-quality, complete piece of content, generate 3 search terms that should be researched further.

# Conditions:
# 1. Do not add any unnecessary comments or explanations.
# 2. Provide only 3 search terms, separated by commas.
# 3. Ensure that the search terms yield relevant information for the given content.

# {content}"""
# )

# prompt = prompt_template.invoke({"content": full_content})
# print(prompt)
# res = llm.invoke(prompt)

# print(res)
