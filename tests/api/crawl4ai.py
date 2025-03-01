import asyncio
import sys
from urllib.parse import urlparse

from a.agent.utils.file_utils import save_text_to_unique_file
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig


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
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=True,
        viewport_width=1280,
        viewport_height=720,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
    )
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=["form", "header", "footer", "nav"],
        exclude_external_links=True,
        exclude_social_media_links=True,
        wait_for_images=True,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url, config=run_config)
        print(result.media)

        # Save with domain name included
        save_text_to_unique_file(str(result.markdown), domain)


# Run the async main function
asyncio.run(main())

# https://crawl4ai.com/mkdocs/
