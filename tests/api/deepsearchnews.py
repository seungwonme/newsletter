# https://news.deepsearch.com/api/#tag/%ED%95%B4%EC%99%B8-%EA%B8%B0%EC%82%AC/operation/get_global_articles_/v1/global-articles

import json
import os

from a.agent.utils.file_utils import save_text_to_unique_file
from dotenv import load_dotenv
from newsdataapi import NewsDataApiClient

load_dotenv()


def parse_and_save_news_data(response: dict):
    """
    Parses the news data from the API response and saves it to a unique file.

    Args:
        response (dict): The API response containing news data.
    """
    if response.get("status") != "success":
        raise ValueError("Failed to fetch news data")

    articles = response.get("results", [])
    parsed_articles = []

    for article in articles:
        parsed_article = {
            "title": article.get("title"),
            "link": article.get("link"),
            "description": article.get("description"),
            "pubDate": article.get("pubDate"),
            "source_name": article.get("source_name"),
        }
        parsed_articles.append(parsed_article)

    save_text_to_unique_file(
        json.dumps(parsed_articles, indent=4, ensure_ascii=False), file_name="news_data.json"
    )


def main():
    api_key = os.getenv("NEWSDATA_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the NEWSDATA_API_KEY environment variable.")

    api = NewsDataApiClient(apikey=api_key)

    response = api.news_api(
        q="경제",
        language="ko",
        country="KR",
    )
    parse_and_save_news_data(response)


if __name__ == "__main__":
    main()

# https://newsdata.io/documentation/#client_py

a = """
{
    "status": "success",
    "totalResults": 208,
    "results": [
        {
            "article_id": "862a63b8673a81014daba1dbe3376d0f",
            "title": "[3분증시] 미 증시, 재료 부재 속 강보합...코스피 엿새째 상승",
            "link": "https://www.yonhapnewstv.co.kr/news/MYH20250219080351727",
            "keywords": ["경제"],
            "creator": ["손성훈"],
            "video_url": None,
            "description": "[앵커] 세계 증시는 빠르게! 우리 증시는 폭넓게! 3분 증십니다. 연합인포맥스 정윤교 기자와 함께합니다. 먼저 간밤 미국 증시 어떻게 마감했습니까. [기자] 간밤 뉴욕 증시는 한산한 분위기 속에 강보합으로 마감했습니다. 시장을 움직일 뚜렷한 재료는 없었고요. 주요 지수는 약보합을 보이다가 장 막판 힘을 내면서 강보합으로 돌아섰습니다. 3대 지수 종가 보겠습니다. 다우지수는 전장 대비 0.02% 오르면서 장을 마쳤습니다. S&P50...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 23:04:27",
            "pubDateTZ": "UTC",
            "image_url": "https://d2k5miyk6y5zf0.cloudfront.net/article/MYH/20250218/MYH20250219080351727_P1.jpg",
            "source_id": "yonhapnewstv",
            "source_priority": 642061,
            "source_name": "연합뉴스tv",
            "source_url": "https://yonhapnewstv.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/yonhapnewstv.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "129b1c6cb7fdd93da84481ac7352bbbb",
            "title": "구글 등 다국적기업 세무조사 '이행강제금' 첫발 뗐다",
            "link": "https://www.yonhapnewstv.co.kr/news/AKR20250219075724412",
            "keywords": ["경제"],
            "creator": ["윤형섭"],
            "video_url": None,
            "description": "[연합뉴스 제공] 구글, 애플, 넷플릭스 등 다국적기업이 세무조사 자료 제출을 거부하면 이행강제금을 부과할 수 있도록 하는 법안이 국회 상임위원회 문턱을 넘었습니다. 오늘(19일) 기획재정부 등에 따르면 국회 기획재정위원회는 지난 18일 세무조사 과정에서 장부·서류 등을 정당한 사유 없이 제출하지 않는 자에 이행강제금을 부과하도록 하는 국세기본법 개정안을 의결했습니다. 부과액은 이행 기간이 지나면 1일당 일평균 수입금액의 0.3% 이내로 ...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:57:24",
            "pubDateTZ": "UTC",
            "image_url": "https://d2k5miyk6y5zf0.cloudfront.net/article/AKR/20250218/AKR20250219075724412_01_i.jpg",
            "source_id": "yonhapnewstv",
            "source_priority": 642061,
            "source_name": "연합뉴스tv",
            "source_url": "https://yonhapnewstv.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/yonhapnewstv.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "dded3807c614efb67c7b44bb05e513ff",
            "title": "[뉴욕FX] 美 달러화, 리야드 평화회담 주목하며 상승...달러·엔 152.04엔",
            "link": "https://www.etoday.co.kr/news/view/2446213",
            "keywords": ["경제"],
            "creator": ["변효선", "변효선 (hsbyun@etoday.co.kr)"],
            "video_url": None,
            "description": "미국 달러화 가치가 미국과 러시아의 우크라이나전쟁 평화 회담에 주목하면서 상승했다. 18일(현지시간) 미국 경제매체 CNBC...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:56:00",
            "pubDateTZ": "UTC",
            "image_url": "https://img.etoday.co.kr/crop/200/120/2138165.jpg",
            "source_id": "etoday",
            "source_priority": 623226,
            "source_name": "이투데이",
            "source_url": "https://www.etoday.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/etoday.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "923fd0cae9a37dc4ddf7736e368ae0ea",
            "title": "기아·BMW 등 7만6천여 대 리콜...에어백 결함 포함",
            "link": "https://www.yonhapnewstv.co.kr/news/MYH20250219073007356",
            "keywords": ["경제"],
            "creator": ["김수강"],
            "video_url": None,
            "description": "국토교통부는 기아·BMW코리아 등 5개 사에서 제작 또는 수입·판매한 37개 차종 7만 6,382대에서 제작결함이 발견돼 자발적 리콜을 실시한다고 밝혔습니다. 기아 니로 등 2개 차종 3만 5,571대는 동승석 하부 전기배선 설계 오류로 인해 에어백이 작동하지 않을 가능성이 있어 오는 26일부터 시정조치에 들어갑니다. BMW 528i 등 28개 차종 2만 4,371대는 냉각수 펌프 배선 커넥터에 수분이 유입되면서 전기적 단락이 발생해 화재...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:30:17",
            "pubDateTZ": "UTC",
            "image_url": "https://d2k5miyk6y5zf0.cloudfront.net/article/MYH/20250218/MYH20250219073007356_P1.jpg",
            "source_id": "yonhapnewstv",
            "source_priority": 642061,
            "source_name": "연합뉴스tv",
            "source_url": "https://yonhapnewstv.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/yonhapnewstv.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "bdc81f8ec79999814effcf0284c4fcd2",
            "title": "[종합] S&P500 사상 최고치 경신...뉴욕증시 강보합 마감",
            "link": "https://www.etoday.co.kr/news/view/2446210",
            "keywords": ["경제"],
            "creator": ["고대영 (kodae0@etoday.co.kr)", "고대영"],
            "video_url": None,
            "description": "별다른 재료 없이 횡보하다 막판 매수세 국제유가, 러시아 송유관 피격에 상승 뉴욕증시는 S&P500지수가 사상 최고치를 ...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:27:00",
            "pubDateTZ": "UTC",
            "image_url": "https://img.etoday.co.kr/crop/200/120/2138163.jpg",
            "source_id": "etoday",
            "source_priority": 623226,
            "source_name": "이투데이",
            "source_url": "https://www.etoday.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/etoday.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["top"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "218ed29e60da777c2e6c3db0f713c905",
            "title": "[뉴욕금값] 트럼프 관세 불확실성에 상승...1.7%↑",
            "link": "https://www.etoday.co.kr/news/view/2446207",
            "keywords": ["경제"],
            "creator": ["변효선", "변효선 (hsbyun@etoday.co.kr)"],
            "video_url": None,
            "description": "국제금값이 18일(현지시간) 도널드 트럼프 미국 행정부의 관세 정책 불확실성에 상승했다. 미국 경제매체 CNBC방송에 따르면 ...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:03:00",
            "pubDateTZ": "UTC",
            "image_url": "https://img.etoday.co.kr/crop/200/120/2136920.jpg",
            "source_id": "etoday",
            "source_priority": 623226,
            "source_name": "이투데이",
            "source_url": "https://www.etoday.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/etoday.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "1aa201c97e71240b778abed23a580b01",
            "title": "[상보] 국제유가, 러시아 송유관 피습 여파 지속...WTI 1.57%↑",
            "link": "https://www.etoday.co.kr/news/view/2446206",
            "keywords": ["경제"],
            "creator": ["고대영", "고대영 (kodae0@etoday.co.kr)"],
            "video_url": None,
            "description": "국제유가는 러시아 송유관 피습 여파가 지속하면서 상승했다. 18일(현지시간) 뉴욕상업거래소(NYMEX)에서 3월물 미국 서부 텍...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:02:00",
            "pubDateTZ": "UTC",
            "image_url": "https://img.etoday.co.kr/crop/200/120/2098191.jpg",
            "source_id": "etoday",
            "source_priority": 623226,
            "source_name": "이투데이",
            "source_url": "https://www.etoday.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/etoday.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "5be854e2a2346751770fe945ab77c5db",
            "title": "'상습 마약' 유아인, 2심 집행유예 선고...5개월 만에 석방",
            "link": "https://www.mbn.co.kr/pages/news/newsView.php?category=mbn00003&news_seq_no=5095241",
            "keywords": ["경제"],
            "creator": None,
            "video_url": None,
            "description": '【 앵커멘트 】 마약을 상습 투약한 혐의로 1심에서 실형을 선고받고 구속됐던 배우 유아인 씨가 2심에선 집행유예를 선고받아 5개월 만에 석방됐습니다. 법원은 "유 씨가 약물 의존성을 상당 부분 극복한 것으로 보인다"고 판단했습니다. 김태형 기자가 보도합니다.【 기자 】 배우 유아인 씨는 서울 일대 병원에서 의료용 프로포폴 등을 181차례에 걸쳐 상습 투약한 혐의로 재판에 넘겨졌습니다. 지난해 9월, 1심 재판부는 "죄질이 좋지 않다"며 징역 1년을 선고하고 법정구속했습니다.▶ 인터뷰 : 유아인 / 배우 (지난 2023년 12월)- "저로 인해서 크게 실망하시고 많은 피해를 보신 분들께 다시 한 번 진심으로 죄송..',
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:00:00",
            "pubDateTZ": "UTC",
            "image_url": "http://img.vod.mbn.co.kr/vod2/605/2025/02/19/20250219080011_20_605_1381285_1080_7.jpg",
            "source_id": "mbn",
            "source_priority": 355080,
            "source_name": "Mbn",
            "source_url": "https://star.mbn.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/mbn.jpg",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "29e577d8c15e94a3ac508808f59c8e2c",
            "title": '[굿모닝경제] 4월 자동차보험료 인하 / HUG 대신 갚은 보증금 1.6조 / "무차입 공매도 방지 의무화"',
            "link": "https://www.mbn.co.kr/pages/news/newsView.php?category=mbn00003&news_seq_no=5095245",
            "keywords": ["경제"],
            "creator": None,
            "video_url": None,
            "description": "새해 들어 주요 보험사들이 자동차보험 인하에 나서고 있습니다. 메리츠화재를 시작으로 삼성화재, DB손해보험, KB손해보험, 현대해상 등이 개인용 자동차보험료를 0.6~1.0% 수준으로 내린다고 발표했습니다. 금융당국이 상생금융을 압박하자 대형사를 중심으로 연이어 인하 방침을 세운 것으로 보입니다.---------- 임대보증에 가입한 집주인이 세입자에게 보증금을 돌려주지 못해 발생한 사고액이 지난해 1조 6천억 원에 달한 것으로 나타났습니다. 주택도시보증공사(HUG)에 따르면 지난해 임대보증금 보증 사고액은 1조 6천억 원으로, 전년 대비 15%, 3년 새 40배 늘어났습니다. 작년 세입자가 가입하는 전세보증 사고액..",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 22:00:00",
            "pubDateTZ": "UTC",
            "image_url": "http://img.vod.mbn.co.kr/vod2/605/2025/02/19/20250219081827_20_605_1381301_1080_7.jpg",
            "source_id": "mbn",
            "source_priority": 355080,
            "source_name": "Mbn",
            "source_url": "https://star.mbn.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/mbn.jpg",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
        {
            "article_id": "e1da744f4dd1896bec21767d9086e1c7",
            "title": "자율주행 버스·택시 확대...7개 지자체에 26억원 지원",
            "link": "https://www.yonhapnewstv.co.kr/news/MYH20250219065857955",
            "keywords": ["경제"],
            "creator": ["김수강"],
            "video_url": None,
            "description": "국토교통부가 자율주행 서비스 확대를 위해 서울, 세종, 경기, 충남, 경북, 경남, 제주 등 7개 지자체에 총 26억 원을 지원합니다. 서울은 심야·새벽 시간대 자율주행 택시와 첫 차 버스 운행을 확대합니다. 현재 서울 강남 지역 일부에서만 운행하던 자율주행 택시는 하반기부터 강남 전역으로 운행 지역이 확대되고, 운행 대수도 기존 3대에서 7대로 늘어납니다. 경남 하동에서는 대중교통이 부족한 농촌 지역을 위한 자율주행 버스가 도입됩니다. ...",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-02-18 21:59:13",
            "pubDateTZ": "UTC",
            "image_url": "https://d2k5miyk6y5zf0.cloudfront.net/article/MYH/20250218/MYH20250219065857955_P1.jpg",
            "source_id": "yonhapnewstv",
            "source_priority": 642061,
            "source_name": "연합뉴스tv",
            "source_url": "https://yonhapnewstv.co.kr",
            "source_icon": "https://i.bytvi.com/domain_icons/yonhapnewstv.png",
            "language": "korean",
            "country": ["south korea"],
            "category": ["business"],
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": False,
        },
    ],
    "nextPage": "1739915953541593450",
}
"""

print(a)
