# flake8: noqa
# pylint: disable=C0413

from dotenv import load_dotenv

load_dotenv()

import asyncio
import sys

from src.agent.agent import get_graph
from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.state import WorkflowState, initialize_state


async def main():
    graph = get_graph()
    argv = sys.argv
    if len(argv) <= 2:
        print("Usage: python src.app <topics> <sources>")
        sys.exit(1)
    state = WorkflowState(initialize_state(topics=[argv[1]], sources=[argv[2]]))
    res = await graph.ainvoke(state, {"recursion_limit": 100})
    save_text_to_unique_file(res["newsletter_content"], "newsletter")


if __name__ == "__main__":
    asyncio.run(main())
