import asyncio
import sys

from pycountry import languages

from src.agent.agent import get_graph
from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.state import WorkflowState, initialize_state


async def create_newsletter(
    topics: list[str], sources: list[str], language_code: str = "en"
) -> dict:
    """
    Asynchronously generates a newsletter based on given topics and sources in the specified language.
    Args:
        topics (list[str]): List of topics to cover in the newsletter
        sources (list[str]): List of sources to gather information from
        language_code (str): Two-letter ISO 639-1 language code (e.g. 'ko', 'en', 'es'). default is 'en'
    Returns:
        dict: A dictionary containing the newsletter with the following keys:
            - title (str): The generated newsletter title
            - content (str): The generated newsletter content
    Raises:
        ValueError: If the provided language code is invalid
    Example:
        >>> topics = ["technology", "AI"]
        >>> sources = ["techcrunch.com", "wired.com"]
        >>> result = await create_newsletter(topics, sources, "en")
        >>> print(result["title"])
        "Latest Tech and AI Updates"
    """

    language = languages.get(alpha_2=language_code.lower())
    if not language:
        raise ValueError(f"Invalid language code: {language_code}")
    graph = get_graph()
    state = WorkflowState(initialize_state(topics=topics, sources=sources, language=language.name))
    res = await graph.ainvoke(state, {"recursion_limit": 100})

    res_dict = {
        "title": res["newsletter_title"],
        "content": res["newsletter_content"],
    }
    return res_dict


async def main():
    argv = sys.argv
    if len(argv) <= 2:
        print(
            "No arguments provided. Using default values (Topics: economy, Exchange Rates, Sources: BBC, WSJ)"
        )
        res = await create_newsletter(
            ["economy", "Exchange Rates"],
            ["https://www.bbc.com/", "https://www.wsj.com/"],
            language_code="ko",
        )
    else:
        res = await create_newsletter([argv[1]], [argv[2]], language_code="ko")

    full_contents = f"# {res['title']}\n\n" + res["content"]
    save_text_to_unique_file(full_contents, "newsletter")


if __name__ == "__main__":
    asyncio.run(main())
