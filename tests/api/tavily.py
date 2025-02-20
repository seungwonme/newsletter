# https://docs.tavily.com/sdk/reference/python
# https://python.langchain.com/docs/integrations/tools/tavily_search/

import asyncio

from dotenv import load_dotenv
from tavily import AsyncTavilyClient

from tests.utils import save_text_to_unique_file

load_dotenv()


async def parse_to_markdown(response):
    markdown = f"""# {response["query"]}

검색 시간: {response["response_time"]}초

## 검색 결과

"""
    for idx, result in enumerate(response["results"], 1):
        markdown += f"""### {idx}. {result["title"]}
- 🔗 링크: {result["url"]}
- 📊 관련도: {result["score"]:.2%}
- 📝 내용:
  {result["content"]}

"""
    return markdown


async def main():
    tavily_client = AsyncTavilyClient()
    response = await tavily_client.search("거시경제 뉴스")

    markdown_content = await parse_to_markdown(response)
    save_text_to_unique_file(markdown_content)


if __name__ == "__main__":
    asyncio.run(main())

a = {
    "query": "거시경제 뉴스",
    "follow_up_questions": None,
    "answer": None,
    "images": [],
    "results": [
        {
            "title": "거시경제 뉴스 | 한국경제 - 한경닷컴",
            "url": "https://www.hankyung.com/economy/macro/economic-policy/macro",
            "content": (
                "거시경제 뉴스, 성공을 부르는 습관 한국경제신문 한경닷컴 ... 거시경제 韓 신용도, 계엄 이전 수준 회복…환율·국채 금리도 안정세 . 원·달러"
            ),
            "score": 0.76152116,
            "raw_content": None,
        },
        {
            "title": "거시경제 뉴스 | 한국경제 - 한경닷컴",
            "url": "https://www.hankyung.com/economy/macro/macro",
            "content": (
                "거시경제 뉴스, 성공을 부르는 습관 한국경제신문 한경닷컴 ... 거시경제 주택 거래 뚝…은행 가계대출 22개월만에 2달 연속 감소 . 지난달 은행 가계"
            ),
            "score": 0.7445268,
            "raw_content": None,
        },
        {
            "title": (
                "거시경제 풍파 덜 흔들리려면... 돌고 돌아도 '밸류업' [국장 탈출 해법] | 한국일보"
            ),
            "url": "https://www.hankookilbo.com/News/Read/A2024111517460002740",
            "content": (
                "거시경제 풍파 덜 흔들리려면... 돌고 돌아도 '밸류업' [국장 탈출 해법] ... 선택 항목 미동의 시 뉴스 추천서비스 혹은 이벤트/행사 당첨 혜택에서"
            ),
            "score": 0.42048118,
            "raw_content": None,
        },
        {
            "title": "거시경제금융회의 - 연합뉴스",
            "url": "https://www.yna.co.kr/view/PYH20241108011200013",
            "content": (
                "(서울=연합뉴스) 서대연 기자 = 최상목 경제부총리 겸 기획재정부 장관을 비롯한 금융수장들이 8일 서울 영등포구 한국수출입은행에서 열린 거시경제금융회의에 앞서 기념촬영을 하고 있다."
            ),
            "score": 0.3985943,
            "raw_content": None,
        },
        {
            "title": "[Weekly Coin] 비트코인, 거시경제 불안으로 횡보 < 증권 < 기사본문 - 시사저널e",
            "url": "https://www.sisajournal-e.com/news/articleView.html?idxno=409537",
            "content": (
                "/사진=연합뉴스 ... 거시경제 불안정성이 이어지자 비트코인 현물 상장지수펀드(etf)에서도 자금이 대거 빠져나갔다. 지난 12일(현지시각) 비트코인 현물 etf에서 총 2억5100만달러(약 3620억1214만원)의 자금이 순유출됐다. 전날 순유출액(5670달러) 대비 약 다섯 배"
            ),
            "score": 0.38435796,
            "raw_content": None,
        },
    ],
    "response_time": 1.53,
}

print(a)
