import os
import re


def get_unique_filename(directory, base_filename, extension="md"):
    """
    Returns a unique filename by appending a counter to the base filename if a file with the same name already exists.

    Args:
        directory (str): The directory where the file will be saved.
        base_filename (str): The base name of the file without extension.
        extension (str, optional): The file extension. Defaults to ".md".

    Returns:
        str: A unique file path with the given base filename and extension.
    """
    if not directory.endswith("/"):
        directory += "/"
    file_path = os.path.join(directory, f"{base_filename}.{extension}")
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(directory, f"{base_filename}_{counter}.{extension}")
        counter += 1
    return file_path


def parse(response):
    """
    Parses the response to extract AI messages, tool message URLs and contents, and tool message artifact results.

    Args:
        response (dict): The response dictionary containing messages.

    Returns:
        tuple: A tuple containing three lists:
            - ai_message_contents (list): List of AI message contents.
            - tool_message_urls_and_contents (list): List of dictionaries with URLs and contents from tool messages.
            - tool_message_artifact_results (list): List of dictionaries with artifact results from tool messages.
    """
    ai_message_contents = []
    tool_message_urls_and_contents = []
    tool_message_artifact_results = []
    # Loop through each message in the "messages" list
    for message in response["messages"]:
        # Check if it's an AIMessage and extract its content
        if message.__class__.__name__ == "AIMessage":
            content = getattr(message, "content", "")
            if content:
                ai_message_contents.append(content)

        # Check if it's a ToolMessage and extract its content
        if message.__class__.__name__ == "ToolMessage":
            content = getattr(message, "content", "")

            # Extract URLs and contents from the ToolMessage content using regex
            matches = re.findall(r'{"url": "(.*?)", "content": "(.*?)"}', content)
            for match in matches:
                url, content = match
                tool_message_urls_and_contents.append({"url": url, "content": content})

            # Extract information from the ToolMessage's artifact results
            artifact = getattr(message, "artifact", {})
            results = (
                artifact.get("results", [])
                if isinstance(artifact, dict)
                else getattr(artifact, "results", [])
            )
            for result in results:
                title = (
                    result.get("title", "")
                    if isinstance(result, dict)
                    else getattr(result, "title", "")
                )
                url = (
                    result.get("url", "")
                    if isinstance(result, dict)
                    else getattr(result, "url", "")
                )
                content = (
                    result.get("content", "")
                    if isinstance(result, dict)
                    else getattr(result, "content", "")
                )
                tool_message_artifact_results.append(
                    {"title": title, "url": url, "content": content}
                )
    return (
        ai_message_contents,
        tool_message_urls_and_contents,
        tool_message_artifact_results,
    )


# import tmp

# ai_message_contents, tool_message_urls_and_contents, tool_message_artifact_results = (
#     parse(tmp.res)
# )

# output_file_path = "output.txt"

# with open(output_file_path, "w", encoding="utf-8") as f:
#     for ai_message in ai_message_contents:
#         f.write("summary: " + ai_message + "\n")

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

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage


def custom_serializer(obj):
    """JSON으로 직렬화할 수 없는 객체를 딕셔너리로 변환"""
    if hasattr(obj, "__dict__") or isinstance(
        obj, (HumanMessage, AIMessage, ToolMessage)
    ):
        return obj.__dict__  # 객체의 __dict__ 속성을 반환 (모든 속성을 딕셔너리로 변환)
    return str(obj)  # 그 외의 객체는 문자열로 변환
