# flake8: noqa
# pylint: disable=C0413

from dotenv import load_dotenv

load_dotenv()

import asyncio
import sys

from src.agent.utils.file_utils import save_text_to_unique_file
from src.newsletter_generator import create_newsletter


async def main():
    argv = sys.argv
    if len(argv) <= 2:
        print("Usage: python src.app <topics> <sources>")
        sys.exit(1)
    res = await create_newsletter([argv[1]], [argv[2]], language_code="ko")
    full_contents = f"# {res["title"]}\n\n" + res["content"]
    save_text_to_unique_file(full_contents, "newsletter")


if __name__ == "__main__":
    asyncio.run(main())
