from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

CATEGORY_MATCHING_PROMPT = PromptTemplate(
    input_variables=["topics", "categories"],
    template="""Please select from the following categories that are highly relevant to '{topics}' (maximum of 3 selections allowed):

{categories}
""",
)

CURATOR_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            """You are a newspaper curator.
Your only task is to select the five most relevant articles on a given topics from a list of articles.
Never select duplicate articles.""",
        ),
        (
            "human",
            """# Topics: {topics}

<articles>
{sources}
</articles>
""",
        ),
    ]
)

SUMMARIZER_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            """You are a newspaper summarizer.
Your summary should be detailed enough to make the whole article understandable.
Write in {language}.""",
        ),
        (
            "human",
            """# Topics: {topics}

{article}""",
        ),
    ]
)


WRITER_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            """You are a newspaper writer.
Your only task is to write a well-written article on a topic using a list of articles.
Use a friendly, feminine tone and appropriate emoji in your writing.
Write in {language}.""",
        ),
        (
            "human",
            """# Topics: {topics}

Each article is separated by the following format:
---article_start---.
Title: [Title of article]
Content:
[article body]
---article_end---

{sources}""",
        ),
    ]
)
