# flake8: noqa
# pylint: disable=W0613,W0611

from langchain_openai import ChatOpenAI

from src.agent.utils.rss_parse import (
    fetch_feed,
    format_news_content,
    load_rss_feeds,
    parse_date,
    parse_feed,
)
from src.agent.utils.state import WorkflowState


def rss_finder_node(state: WorkflowState):
    pass


if __name__ == "__main__":
    pass
