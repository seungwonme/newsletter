from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

CATEGORY_MATCHING_PROMPT = PromptTemplate(
    template="""Please select from the following categories that are highly relevant to '{topics}' (maximum of 3 selections allowed):

{categories}
""",
    input_variables=["topics", "categories"],
)

CURATOR_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            "You are a newspaper curator. Your only task is to select the five most relevant articles on a given topics from a list of articles.",
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

WRITER_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            """You are a newspaper writer.
Your only task is to write a well-written article on a topic using a list of articles.
Write in such detail that someone can understand the whole context just by looking at the article you wrote.
Write in {language}.""",
        ),
        (
            "human",
            """# Topics: {topics}
<articles>
{sources}
</articles>""",
        ),
    ]
)
