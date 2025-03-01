import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

from src.agent.utils.file_utils import save_text_to_unique_file
from src.agent.utils.state import ContentData, WorkflowState


async def crawler_node(state: WorkflowState) -> WorkflowState:
    browser_config = BrowserConfig(
        browser_type="chromium",
        # viewport_width=1280,
        # viewport_height=720,
        headless=True,  # 브라우저 창을 띄우지 않고 실행
        verbose=True,  # NOTE: 추가 정보 출력
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
        light_mode=True,
    )

    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        wait_for_images=True,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        excluded_tags=["form", "header", "footer", "nav"],
        exclude_external_links=True,
        exclude_social_media_links=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for item in state["search_contents"]:
            url = item["url"]
            result = await crawler.arun(url=url, config=run_config)
            item["content"] = str(result.markdown)
    return state


if __name__ == "__main__":
    mock_contents: list[ContentData] = [
        {
            "title": "Jeremy Bowen: Three years on, Ukraine's extinction nightmare has returned",
            "url": "https://www.bbc.com/news/articles/cx2xngznyego",
            "description": (
                "Three years on from Russia's invasion of Ukraine, the return of Donald Trump has changed everything"
            ),
            "thumbnail_url": "https://example.com/thumb1.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "How Far Will The UK Go To Protect Ukraine?",
            "url": "https://www.bbc.co.uk/sounds/play/p0kt3vyn",
            "description": "And is the government’s stance on Russia shifting?",
            "thumbnail_url": "https://example.com/thumb2.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Trump right to engage Putin on peace talks, says minister",
            "url": "https://www.bbc.com/news/articles/ckgnrg77ydjo",
            "description": (
                'Bridget Phillipson says the US thawing diplomatic ties with Putin "brought Russians to the table".'
            ),
            "thumbnail_url": "https://example.com/thumb3.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Most USAID staff laid off or placed on leave by Trump administration",
            "url": "https://www.bbc.com/news/articles/cr42r2gw5wzo",
            "description": (
                "In addition to some 4,200 staff who are being placed on leave, at least 1,600 employees are being fired."
            ),
            "thumbnail_url": "https://example.com/thumb4.jpg",
            "content": "Full article content here...",
        },
        {
            "title": "Trump names right-wing commentator Dan Bongino as deputy FBI director",
            "url": "https://www.bbc.com/news/articles/cpwd2qrn1e2o",
            "description": (
                'Trump said Bongino was "a man of incredible love and passion for our Country" and would serve under newly confirmed FBI director Kash Patel.'
            ),
            "thumbnail_url": "https://example.com/thumb5.jpg",
            "content": "Full article content here...",
        },
    ]

    test_state: WorkflowState = {
        "topics": ["trump", "biden", "election"],
        "sources": ["https://www.bbc.com/", "https://www.wsj.com/"],
        "language": "Korean",
        "search_contents": mock_contents,
        "newsletter_title": "",
        "newsletter_img_url": "",
        "newsletter_content": "",
    }

    async def main():
        result_state = await crawler_node(test_state)
        print("\nCrawled Contents:")
        print("-" * 80)

        full_content = ""
        for content in result_state["search_contents"]:
            # 콘솔 출력
            print(f"Title: {content.get('title')}")
            print(f"Date: {content.get('date')}")
            print(f"URL: {content.get('url')}")
            print("-" * 40)

            # 파일 저장용 포맷팅
            full_content += f"# {content.get('title')}\n\n"
            full_content += f"[Article URL]({content.get('url')})\n\n"
            full_content += f"![Thumbnail]({content.get('thumbnail_url')})\n\n"
            full_content += f"Content: {content.get('content')}\n\n"
            full_content += "---\n\n"
        save_text_to_unique_file(full_content, file_name="crawler_test")

    asyncio.run(main())
