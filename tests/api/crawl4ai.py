import asyncio
import sys
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler

from src.agent.utils.file_utils import save_text_to_unique_file


def extract_domain(url: str) -> str:
    """Extract domain name from URL"""
    parsed_url = urlparse(url)
    return parsed_url.netloc


async def main():
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: uv run -m tests.api.crawl4ai <URL>")
        return
    url = argv[1]
    domain = extract_domain(url)
    print(f"Domain: {domain}")  # 도메인 출력

    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url)

        # Save with domain name included
        save_text_to_unique_file(str(result.markdown), domain)


# Run the async main function
asyncio.run(main())

# https://crawl4ai.com/mkdocs/
