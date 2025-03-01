# 스크랩 500회만 무료임
# crew4ai가 더 좋은 듯?

import asyncio
import os

from a.agent.utils.file_utils import save_docs_to_unique_file
from dotenv import load_dotenv
from langchain_community.document_loaders.firecrawl import FireCrawlLoader

load_dotenv()


async def main():
    url = "https://www.bbc.com/"
    loader = FireCrawlLoader(api_key=os.getenv("FIRECRAWL_API_KEY"), url=url, mode="crawl")
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)

    save_docs_to_unique_file(docs)

    print(f"Downloaded and saved {len(docs)} documents from {url}.")


if __name__ == "__main__":
    asyncio.run(main())

# https://python.langchain.com/docs/integrations/document_loaders/firecrawl/
# https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.firecrawl.FireCrawlLoader.html
# https://www.firecrawl.dev/extract
