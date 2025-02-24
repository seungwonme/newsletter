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
            "You are a newspaper writer. Your sole purpose is to write a well-written article about a topic using a list of articles.",
        ),
        (
            "human",
            """# Topics: {topics}
Today's date is {date}.
<articles>
{sources}
</articles>""",
        ),
    ]
)

REVISER_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            "You are a newspaper editor. Your sole purpose is to edit a well-written article about a topic based on given critique",
        ),
        (
            "human",
            """<article>
{articles}
</article>

<critique>
{critique}
</critique>

Your task is to edit the article based on the critique given.
Please return json format of the 'paragraphs' and a new 'message' field to the critique that explain your changes or why you didn't change anything.
please return nothing but a JSON in the following format:
{{
    "title": title of the article,
    "date": today's date,
    "paragraphs": [
        "paragraph 1",
        "paragraph 2",
        "paragraph 3",
        "paragraph 4",
        "paragraph 5"
    ],
    "summary": "2 sentences summary of the article"
}}""",
        ),
    ]
)

CHIEF_EDITOR_PROMPT = ChatPromptTemplate(
    [
        (
            "system",
            "You are a newspaper writer. Your sole purpose is to write a well-written article about a topic using a list of articles.",
        ),
        (
            "human",
            """# Topics: {topics}
Today's date is {date}.
Your task is to write a critically acclaimed article for me about the provided topic based on the sources.
<articles>
{sources}
</articles>

Returns only an integer list of the indices of the articles that are related in this structure.
Please return nothing but a JSON in the following format:
{sample_json}""",
        ),
    ]
)
