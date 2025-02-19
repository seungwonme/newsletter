import asyncio

from crawl4ai import AsyncWebCrawler

from tests.api.utils import save_text_to_unique_file


async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://crawl4ai.com")

        # Print the extracted content
        print(result.markdown)

        save_text_to_unique_file(str(result.markdown))


# Run the async main function
asyncio.run(main())  # Run the async main function

# https://crawl4ai.com/mkdocs/
