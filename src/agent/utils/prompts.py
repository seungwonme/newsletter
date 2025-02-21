from langchain import hub
from langchain_core.prompts import PromptTemplate

# CATEGORY_MATCHING_PROMPT = ChatPromptTemplate(
#     [
#         ("system", "You are a helpful AI bot. Your name is {name}."),
#         ("human", "Hello, how are you doing?"),
#         ("ai", "I'm doing well, thanks!"),
#         ("human", "{user_input}"),
#     ]
# )
CATEGORY_MATCHING_PROMPT = PromptTemplate(
    input_variables=["topics", "categories"],
    template="""다음 중 '{topics}'와 연관성이 높은 카테고리를 선택하세요 (중복 선택 가능):

{categories}
""",
)


QUERY_OPTIMIZATION_PROMPT = hub.pull("aidenme/query_optimizer")
SUMMARIZER_PROMPT = hub.pull("aidenme/summarizer")
GENERATOR_PROMPT = hub.pull("aidenme/newsletter_gerenerator")

CHIEF_EDITOR_PROMPT = PromptTemplate.from_template(
    """You are the general manager of a professional newsletter. Check the content of your newsletter below.
1. the newsletter should be about "{intent_of_requested_content}".
2. the newsletter should be clearly understandable to everyone who reads it.
3. if you don't understand the content, give us a "new search term" without "{search_queries}".

Newsletter:
{newsletter_content}
"""
)

POST_1 = """<새로운 VC 트렌드 시리즈 - 금융기관화 되가는 VC vs 본질을 고수하는 VC> (원문은 댓글 링크)

실리콘밸리 VC 업계는 지난 30년간 큰 변화를 겪고있다.
아래 두 회사가 그 변화를 대변하고 있다.

30년 전 5명이 창업한 Benchmark Capital과, 이들이 뿌린 씨앗에서 잉태된 2명이 그로부터14년 후 창업한 Andreessen Horowitz.

규모를 키우는 Andreessen Horowitz같은 곳에선, 언제 받을 지 모를 성과급 보단 규모에 따라 증가하는 운용보수가 더 매력적 (요즘 대형 Buyout PEF와 비슷한 양상).

규모를 작게 가져가며 성과급이 더 중요한 Benchmark Capital같은 곳은 투자업체 성공이 관건이라, 한 배 탄 심정으로 포트폴리오 업체 밸류업에 더 관심.

반면 한국 VC 업계는 어떤가? 비슷한 듯하나 다소 다른 양상.
규모가 커진 VC는 국내 시장규모 한계로 인해 VC fund 규모를 늘리지 못하고 PEF로 확장. 단일 VC fund 중 가장 큰 것도 아직 1조원 이하.

규모는 그렇다 치고, 국내 VC 중에 Benchmark Capital처럼 규모를 늘리기 보단 본질적 투자에 집중하는 하우스가 어디 있을까?


1. 실리콘밸리의 대조적인 두 VC 🏢
- 30년 전 설립된 Benchmark Capital은 "작은 것이 아름답다"는 철학 고수
- 전통적인 벤처캐피털 방식을 따르며 소규모 투자와 기업 지원에 집중
- 14년 후 설립된 Andreessen Horowitz는 "anti-Benchmark"를 표방하며 대규모 확장 노선 채택

2. Andreessen Horowitz의 폭발적 성장 📈
- 현재 440억 달러 규모의 자금 운용
- 80명의 투자 파트너와 5개 사무소 보유
- 8개의 뉴스레터, 7개의 팟캐스트 운영
- 800개 이상의 포트폴리오 기업 보유
- 최근 프라이빗 웰스 매니지먼트 서비스까지 확장

3. Benchmark의 전통 고수 ⚓
- 여전히 5명의 파트너만으로 투자 결정
- 2004년부터 동일한 규모인 4억 2500만 달러의 펀드 유지
- 웹사이트는 단 한 페이지로 운영
- 작은 규모를 통한 집중도 유지

4. 벤처캐피털 산업의 변화 상 💫
- 2009년 2,320억 달러에서 2023년 1.2조 달러로 산업 규모 성장
- 많은 VC들이 Andreessen Horowitz 모델을 따라 대형화
- 기술이 모든 산업에 침투하며 스타트업 기회 확대
- 사회 문제 해결을 위해 더 큰 자금력 필요성 제기

5. 업계 내 우려와 논란 ⚠️
- 너무 큰 펀드 규모로 인한 수익성 악화 우려
- 작은 VC들의 경쟁력 약화 문제
- 투자할 만한 좋은 스타트업 부족 현상
- 전통적인 VC 모델의 생존 가능성에 대한 의문 제기

6. 상징적 투자 사례 💎
- Benchmark의 eBay 투자: 670만 달러 투자가 2년 만에 40억 달러로 성장
- Andreessen Horowitz의 Airbnb, Stripe 등 성공적인 투자 포트폴리오 구축
- 두 회사의 투자 철학과 방식의 차이가 실제 투자에서도 명확히 드러남
"""

POST_2 = """"Venture Capital Partners Are Leaving Big Firms in Droves" - 대형 VC 파트너들의 이직 러시와 업계 변화

1. 주요 인물들의 잇단 이탈 🚪
- Sequoia Capital의 Matt Miller, Lux Capital의 Bilal Zuberi, Andreessen Horowitz의 Sriram Krishnan 등 핵심 인물들 퇴사
- 백악관 AI 정책 자문직 등 새로운 진로 모색
- Index Ventures의 Mike Volpi, Bessemer Venture Partners의 Ethan Kurzweil 등 새 회사 설립

2. 이직 급증의 주요 원인 📉
- 장기화된 스타트업 침체로 인한 투자 환경 악화
- 수십억 달러 규모 메가펀드 운영의 제약에 대한 좌절감 증가
- 펀드 모금 어려움으로 인한 운영 간소화 필요성
- 투자 실적 부진한 파트너들과의 결별

3. 이탈 유형의 두 가지 패턴 🔄
- 자산관리 중심으로 변화하는 VC 환경에 지친 고성과 투자자들의 이탈
- 팬데믹 시기 저금리 환경에서 경험 부족한 채 영입된 투자자들의 퇴출

4. 새로운 트렌드의 등장 🌱
- 소규모 민첩한 펀드 설립 증가
- Chemistry, Hanabi Capital 등 새로운 초기 단계 펀드 출현
- AI 특화 펀드 등 전문화된 투자 영역 개척

5. 신생 펀드의 도전과제 ⚔️
- 2024년 VC 펀드 총자본의 50%를 상위 9개 기업이 독점
- 신흥 펀드들의 전체 모금액은 14%에 불과
- 검증된 대형 VC 선호하는 투자자들로 인한 자금조달 어려움
- 2025년 더 치열해질 것으로 예상되는 펀드 간 경쟁
"""

POST_3 = """💡돈 되는 AI service 만들기 시리즈 - 오프라인 Agency 싸게 인수 후, AI 활용해 밸류 올려 팔아먹기.

AI 기술력에 투자하는 게 아니라, AI로 기업 밸류를 올려 매각하는 (순수 VC 투자가 아닌) 소규모 PEF 차원의 접근.

AI로 효과가 바로 나타날 수 있는 업종을 고르는 게 핵심. 바꿔 말하면, 그런 업종에서 AI를 적용할 경우 효과가 직빵이라는 얘기. 그러나 그런 업종일 수록 이런 AI 같은 신기술 도입에 밍기적. 그러니 직접 인수해서 손 보는 게 빠름.

<Agents + Agencies: Building Tomorrow's Moats>

1. AI 스타트업의 새로운 경쟁 전략 🎯
- 기존 에이전시 인수를 통한 시장 진입 전략 부상
- 수십 년간 축적된 고객 데이터 활용이 핵심
- 워크플로우 인텔리전스와 도메인 전문성 확보

2. 에이전시 인수의 장점 💼
- 즉각적인 수익 창출 가능
- 기존 고객 기반 및 유통 채널 활용
- 실제 사용자 행동 데이터 확보로 AI 학습 가능

3. 주요 타겟 에이전시 분야 🎯
- 보안 서비스(MSSP)
- 가상 인력 관리
- ERP 구현 및 지원
- 마케팅 및 영업 지원
- 의료 청구 및 회계

4. 인수 실행 전략 🔄
- 300만 달러 이하 매출 기업 타겟팅
- EBITDA 마진 17% 미만 기업 선호
- 15인 이하 소규모 팀 우선 고려
- 500-700만 달러 벤처 자금 활용

5. AI 통합 및 확장 전략 🚀
- 반복 작업 자동화 구현
- AI 기반 의사결정 시스템 도입
- 고객 가치 향상을 위한 AI 도구 개발
- 플랫폼 확장성 확보

6. 투자 경제성 분석 💰
- 초기 에이전시 매출 300만 달러 미만
- EBITDA 40-60만 달러 규모
- 인수 승수 4-5배 적용
- 70-75% 총 마진 목표

7. 벤처캐피털 투자 적합성 📈
- AI 도구 통합을 위한 초기 투자 필요
- 낮은 EBITDA 마진으로 PE 부적합
- 부채 금융 활용으로 지분 희석 최소화
- 높은 성장 잠재력

8. 시장 기회 요인 🌟
- AI 에이전트 통한 인력 자동화 가능성
- M&A 시장 위축으로 인한 기회 증가
- 베이비부머 세대 은퇴로 인한 매물 증가
- 기술 현대화 통한 가치 창출 잠재력
"""

# coffeepot
NEWS_LETTER = """# 혼다와 닛산 합병 너머로 보이는 것들

최근 혼다와 닛산의 합병 소식은 자동차 업계뿐만 아니라 전 산업에 걸쳐 메시지를 건네기도 했습니다. 새로운 기술과 산업의 흐름에 뒤처진 레거시 기업들이 이제는 벼랑 끝에 다다르고 있으며, 앞으로의 생존을 위해서는 힘을 합치는 선택을 할 수밖에 없는 상황이라는 것이죠.

여기에 더해 이번 합병은 현재 일본의 자본 시장에서 일어나고 있는 또 다른 일면을 보여주기도 합니다. 소위 '잃어버린 30년' 동안 거의 일어나지 않았던 일본 기업들에 대한 인수합병이 앞으로 더 자주 일어날 수 있는 일임을 말이죠.

- 닛산은 대만의 폭스콘이 인수에 관심이 컸다는 보도가 나왔습니다.
- IT 기업인 후지소프트는 최근 사모펀드인 KKR과 베인캐피털이 쟁탈전을 벌이고 있습니다.
- 세븐앤아이 홀딩스는 캐나다의 유통 기업인 알리멘타시옹 쿠시타르가 인수를 위해 뛰어들어 몸값이 치솟았습니다.

과거에 보기 어려웠던 일이 최근 들어서 연속적으로 일어나고 있습니다.

## 일본 기업 합병의 의미

이렇게 일본의 기업들이 합병을 하거나, 외국 기업들의 인수 타겟이 되는 것은 무엇을 의미할까요?

- 이들에 대한 **기업 지배 구조 개선**과 **주주 환원 확대 요구**는 더 커지고 있고,
- 앞으로 **저출생으로 인한 내수 부진과 노동력 부족**이 현실화하는 모습을 고려하면
  **인수합병을 통해 덩치를 키우고 장기적인 생존을 모색하는 일**은 필수가 되어가고 있습니다.

오늘은 혼다와 닛산의 합병의 이유를 들여다보면서 일본 시장의 사정 전반을 살펴봅니다.
그리고 그 사정은 우리가 앞으로 겪게 될 사정과 비슷하기도 하다는 것을 일러줍니다.

## 혼다와 닛산 합병 너머로 보이는 것들: 일본 그리고 국내 자본 시장의 미래

혼다와 닛산이 합병을 발표했습니다.
우치다 마코토 닛산자동차 사장, 미베 토시히로 혼다 CEO, 카토 타카오 미쓰비시자동차공업 CEO는 12월 23일 도쿄에서 공동 기자회견을 열어 합병을 위한 양해각서를 체결했음을 밝히고 향후 일정과 기업 구조를 공개했습니다.

### 합병 주요 내용

- **합병 일정**:
  - 내년 6월까지 합병 계약 체결
  - 2026년에 도쿄 증권거래소에 상장되는 신규 지주회사 편입
- **합병 참여**:
  - 닛산의 최대 주주인 미쓰비시 자동차도 합류 가능성 있음 (별도 양해각서 체결 예정)
- **합병 후 규모**:
  - 시가총액: 8.4조 엔 (약 78조 원)
  - 매출: 32조 엔 (약 297조 원)
  - 영업이익: 2조 엔 (약 18조 원)
  - 매출액 기준 세계 3위 자동차 제조업체
- **브랜드 전략**:
  - 각 브랜드는 유지
  - 차량 플랫폼 단일화로 비용 절감
  - 하이브리드 및 전기차 시장의 니즈 충족

## 혼다 주도의 합병

이번 합병은 적어도 초기에는 **시가총액 기준 혼다가 닛산의 4배 규모**인 만큼 혼다가 주도할 것으로 보입니다.

- **이사회 구성**: 혼다가 과반수를 지명.
- **경영 구조**: 사장 역시 혼다가 지명하는 이사 중에서 선임.
- **닛산의 재정 부담**: 닛산의 구조 조정 및 실적 개선이 합병의 전제 조건.

## 주요 도전 과제

### 닛산의 재무 상태

- 닛산은 최근 9000명 해고, 생산량 20% 감축 등 구조 조정 발표.
- 투자자들은 닛산의 자력 생존 가능성에 여전히 의문을 제기.

### 시장 반응

- 합병 발표 후 주가 변동:
  - 닛산: 30% 상승
  - 혼다: 5% 하락
- 투자자들은 **혼다가 닛산을 떠안는 형태**로 보고 우려.

## 전기차 시대에서의 전략적 협력

### 닛산의 강점

- 일본 전기차 시장 선도 모델: **리프(Leaf)**
- 자율주행 기술 개발 선도.

### 혼다의 약점

- 전기차 및 자율주행 기술에서 경쟁력 부족.
- 소니와 합작한 **소니 혼다 모빌리티(Sony Honda Mobility Inc.)**로 격차를 메우는 중.

## 글로벌 이해관계: 르노와 폭스콘

- **르노**: 닛산의 주요 주주로 합병 논의에 영향력을 행사할 가능성.
- **폭스콘**: 닛산 인수에 관심을 보였고, 이는 이번 합병 논의를 촉발한 계기 중 하나.

## 결론

혼다와 닛산의 합병은 **전기차와 자율주행 시대에서 생존을 모색**하기 위한 전략적 움직임으로 보입니다.
하지만 성공적인 통합과 이해관계 조율이 이루어지지 않는다면 합병의 효과는 제한적일 수 있습니다.

> 일본 자본 시장의 변화는 국내 기업들에게도 중요한 시사점을 제공합니다.
> 합병과 협력은 생존의 필수 조건이 되어가고 있습니다.
"""

# newneek
NEWS_LETTER_1 = """# ‘냉장고를 부탁해’부터 ‘흑백요리사’까지, 우리는 왜 요리 예능에 푹 빠진 걸까?

JTBC 요리 예능 ‘냉장고를 부탁해’가 5년 만에 시즌2로 돌아왔습니다. 게스트의 냉장고에 든 재료들로 두 셰프가 제한시간 15분 내에 먹을 만한 음식을 내어놓는 프로그램인데요. 기존에 냉부해에 출연했던 셰프들과 올해 가을 모든 화제성을 휩쓸었던 넷플릭스 요리 예능 ‘흑백 요리사: 요리 계급 전쟁’의 상위 순위권에 올랐던 셰프들이 참여했죠. 시즌2는 첫 화부터 시청률 5.2%를 기록하며 익숙한 웃음을 이끌어냈습니다.

그런데 우리는 왜 그렇게 요리 예능을 즐겨보는 걸까요? 오늘은 요리 예능의 역사와 앞으로 나아가야 할 길을 살펴봅니다.

## 요리 경연 프로그램, 심사위원을 심사하다

2012년 올리브TV에서 방영된 ‘마스터 셰프 코리아’는 BBC ‘마스터 셰프(MasterChef)’의 판권을 수입해 제작한 프로그램입니다. 2012년은 Mnet ‘슈퍼스타K’가 시즌 4를, MBC ‘나는 가수다’ 시즌 2가 방영되며 대중들이 서바이벌 프로그램의 문법을 온전히 받아들인 시기였어요. ‘마스터 셰프 코리아’는 요리 서바이벌 프로그램의 시초가 되었고 첫 시즌부터 큰 사랑을 받았습니다.

이듬해인 2013년, 올리브TV는 이 기세를 이어 또 다른 음식 경연 프로그램인 ‘한식대첩’을 방영합니다. 마셰코에 국경을 넘나드는 음식들이 등장한 것과 달리, ‘한식대첩’에는 대한민국의 팔도를 대표하는 팀들이 출연해 오직 한식만을 다루며 차별점을 더했죠. 총 네 개의 시즌이 진행되는 동안 전라남도 팀이 3시즌 연속 결승에 진출하며 저력을 보여주었는데요. 이 과정에서 전라남도만의 고유한 지역 특산물과 그간 묵묵히 자리를 지켜온 명인들의 존재를 알렸습니다. 또한, 두 번째 시즌부터는 북한팀도 참여하면서 북한에는 평양냉면만 있는 게 아니라는 걸 톡톡히 알려주었고요.

경연 프로그램 제1의 원칙은 언제나 공정성입니다. 주어진 시간 동안 자신의 기량을 충분히 발휘하는 참가자만큼이나 심사위원이 중요한 이유인데요. ‘마스터 셰프 코리아’의 김소희, 강레오, 노희영, ‘한식대첩’의 심영순, 백종원, 최현석 등은 모두 심사하는 역할로서 이름을 알린 인물들입니다. 이들이 요리를 익힌 배경과 맥락은 모두 다를지 몰라도 경연 프로그램의 심사위원은 전문성과 예능감을 동시에 갖추어야 합니다.

경연 프로그램의 역사가 쌓여갈수록 시청자는 심사위원을 심사하게 됩니다. ‘마스터 셰프 코리아’의 레전드 시즌으로 회자되는 시즌 2에서는 심사위원들이 전 시즌 대비 더욱 냉철한 심사를 하면서 참가자들을 향해 독설을 건네는 장면이 그대로 노출되었는데요. 프로그램의 긴장감이 더해졌지만 심사위원들이 가지고 있는 예능감이 그것을 상쇄시켜 준 덕에 보는 재미가 있었다는 감상이 다수였습니다.

이러한 점에서, 2024년 넷플릭스 ‘흑백 요리사: 요리 계급 전쟁’의 두 심사위원 안성재와 백종원은 전문성과 예능감을 두루 갖춘 캐릭터이기에 큰 주목을 받았다고 볼 수 있습니다. 초반부터 같은 음식을 두고 상반된 평가를 내리는 두 사람의 차이가 부각되었는데요. 2라운드에서는 여기에 기상천외한 심사 방식이 더해졌습니다. 조리 과정과 완성된 요리의 플레이팅을 보지 않은 채 오직 맛에만 집중해서 평가하기 위해 두 사람이 안대를 두른 것이죠. 안대 심사는 색상과 모양이 똑같은 음식들을 일렬로 늘어놓고 순위를 매기던 기존 블라인드 테스트 포맷의 새로운 장을 열었을 뿐만 아니라, 시종일관 웃음을 자아냈습니다.

어떻습니까? 짭니다!

JTBC ‘냉장고를 부탁해’는 승패보다는 예능적 요소에 더욱 집중합니다. 이 프로그램의 진짜 재미는 정신없이 요리를 하고 있는 셰프에게 MC가 카메라를 들고 다가가 인터뷰를 청할 때 발생하는데요. 자신에게 주어진 제한시간 15분 동안 분초를 다투던 셰프들은 요리에만 집중하기에도 모자란 상황에서 마지못해 성실하게 혹은 당황하는 듯한 모습을 숨기지 못하며 지금 어떤 요리를 어떤 의도로 조리하고 있는지 이야기합니다.

## 요리 경연 프로그램의 한계와 가능성

이미지 출처: 넷플릭스
요리 경연 프로그램은 언제나 ‘블록버스터물’을 지향했습니다. 2024년 넷플릭스 ‘흑백 요리사: 요리 계급 지옥’에 참여한 촬영, 오디오, 편집, 보조 등의 스태프는 300명 내외로 추정됩니다. 특히 촬영 인원만 100명 이상에 달하고요. 또한 1000평 규모의 세트를 갖춘 경기도 파주의 모 스튜디오에서 촬영된 것으로 알려집니다. 2012년 마셰코가 총제작비 40억 원, 300평 규모의 스튜디오에서 촬영된 것과 견주어보자면 몸집이 엄청나게 커졌죠.

그러나 스케일을 키우는 과정에서 생겨나는 낭비를 줄여야 한다는 목소리도 높아지고 있습니다. 세트를 철거하는 비용이 과도하게 발생하는 것은 물론이고, 음식물 쓰레기가 대거 발생하기 때문이죠. ‘흑백요리사: 요리 계급 전쟁’ 제작진은 "쓰이지 않은 식재료는 버리지 않도록 노력했다"며 논란에 대한 입장을 직접 밝히기도 했습니다.

요리 예능이 육식 위주라는 점도 고민해 볼 필요가 있습니다. 한국채식연합에 따르면 국내 채식 인구수는 2019년 150만 명에서 2024년 250만 명으로 크게 증가했습니다. 채식을 선택한 사람이 이렇게 많은데도 대다수의 요리 예능 프로그램들은 여전히 육식중심적으로 미션을 기획하고 프로그램을 연출합니다. ‘나의 비거니즘 만화’의 저자 보선이 "한 명의 완벽한 비건보다 불완전한 100명의 비건 지향인이 더 가치 있다"라고 말한 것처럼, 설령 100% 비건은 아니더라도 비건을 지향하는 과정에서 나름의 즐거움을 찾아나가는 방법을 미디어가 더 많이 보여줄 필요가 있습니다. 다양한 채소를 창의적으로 쓰는 메뉴나 현재 시중에서 구매할 수 있는 식물성 대체육 브랜드 식품들을 활용한 신규 미션을 기획해 보는 것도 좋을 테고요.

선례가 없지는 않습니다. ‘흑백 요리사: 요리 계급 전쟁’의 ‘셸럽의 셰프’ 임희원 셰프는 자신의 시그니쳐 메뉴인 베지테리언 사시미와 후토마키를 선보이며 첫 번째 라운드를 통과했습니다. 당시 안성재 셰프의 심사평은 "땅에서 자라는 채소들을 예의를 갖춰 다룬 게 느껴진다"였는데, 채식에 전혀 관심이 없던 사람들의 호기심을 불러일으켰죠. 유튜브 ‘요정재형’의 정재형 또한 게스트를 초대해 요리를 내어주고 이야기를 나누는 ‘요정식탁’ 시리즈에서 배우 임수정, 뮤지션 이효리를 초대했을 때 게스트 맞춤형으로 비건 메뉴를 선보인 적이 있습니다. 정재형은 2021년, EBS의 요리 경연 파일럿 프로그램 ‘채소가지구’에도 진행자로 함께하며 ‘채식 = 샐러드’라는 편견을 깨고 채소 요리의 다양한 면모를 보여준 적이 있고요.

## 셀럽의 유튜브, 그런데 이제 음식을 곁들인

유튜브에서는 ‘먹방’을 넘어 요리라는 소재에서 예능적 요소를 이끌어내는 콘텐츠가 늘어나고 있습니다. 그러면서 요리 예능은 더 다채로워지고 있어요. 지난 6월, 방송인 최화정은 27년간 자리를 지킨 SBS 라디오 ‘최화정의 파워타임’에서 하차한 후 유튜브 ‘안녕하세요 최화정이에요’를 개설했습니다. 첫 에피소드부터 자신의 주방을 공개했고, 거기에서 순식간에 오이 김밥을 말고, 여름 국수를 해 먹었죠. 모두 쉽고 간단하게 시도해 볼 수 있는 음식들이었고 SNS에서는 최화정표 레시피로 완성된 요리 인증이 이어졌어요. 그동안 최화정의 연관 검색어에는 ‘동안’, ‘관리’ 같은 키워드가 올라 있었지만, 유튜브를 통해 드러난 그는 자기가 만든 음식을 세상에서 가장 맛있게 먹는 것처럼 보이는 사람입니다. 그렇게 자신을 돌보고 건강한 삶을 꾸리는 60대 여성 최화정의 모습을 보여준 이 채널은 유튜브가 발표한 2024 올해의 최고 인기 크리에이터 리스트에서도 7위에 올랐죠.

언니가 말했어, "맛있으면 0칼로리"라고

‘먹는 사람’ 최화정의 명언이 시작된 곳도 바로 9년 전 ‘냉장고를 부탁해’ 였는데요. 커스터드 크림과 머랭을 섞은 시부스트 크림와 프렌치토스트를 곁들인 김풍 셰프의 ‘풍살기’를 시식하고 난 후 그는 바로 이런 말을 남겼죠. "이렇게 맛있는 음식을 먹을 때는 칼로리 계산하면 안 돼요. 맛있으면 0칼로리에요."

요리가 주를 이루는 채널은 아니지만, 가수 다비치 멤버 강민경이 운영하는 유튜브 ‘걍밍경’의 차밥 열끼 시리즈도 빼놓을 수 없습니다. 강민경은 대학 축제 등 지역 공연이 많은 시즌에 다비치가 카니발을 타고 전국으로 이동하면서 음식을 먹는 모습을 담고 있는데요. 흔들리는 차 안에서도 멀미 없이 가뿐하게, 마치 식당에 앉아 있는 것처럼 전국 각지의 다양한 음식들을 먹어봅니다. 특히 먹는 취향이 겹치지 않는 다비치 두 멤버의 서로 다른 리액션을 교차해서 보여준다는 것도 이 콘텐츠의 차별점이고요. 2022년 가을부터 시작된 이 시리즈는 꾸준히 조회수 150만 회 이상을 기록하고 있습니다.

MBC ‘나 혼자 산다’에서 보여준 것처럼 수년간 이사를 거듭했던 코미디언 박나래는 지인을 집에 초대해 음식을 내어주는 공간인 ‘나래바’가 진화하는 과정을 보여주었습니다. 박나래는 음식을 만들어 지인들과 나누는 즐거움을 느끼는 인물인데요. 이제 그는 자신의 강점인 ‘큰 손’을 십분 살리는 방식으로 유튜브 ‘나래식’을 통해 게스트를 만나 음식을 나누어 먹고 인터뷰를 진행합니다. 박나래는 첫 에피소드부터 목포에서 7kg짜리 민어를 공수해 직접 회를 뜨는 묘기부터 보여주는 정공법을 택합니다. 이처럼 박나래의 음식 토크쇼는 호스트가 그동안 음식과 어떤 관계를 맺어온 사람인지를 있는 그대로 드러냅니다. 음식과 술을 곁들인 토크쇼 포맷의 유튜브 콘텐츠가 많아지고 있다는 사실을 알아도, 그가 유행에 편승했다는 생각이 들지 않는 거죠.

여러분은 왜 요리 예능을 즐겨보시나요? 그건 단지 군침이 돌고 도파민이 폭발하기 때문만은 아닐 겁니다. 우리는 요리 예능을 통해 다양한 음식 문화를 배우고, 누군가를 위해 요리하는 즐거움을 깨닫고, 나와 음식이 맺는 관계를 생각하게 됩니다. 경연이든, 토크쇼든, 브이로그든, 음식을 소재로 하는 예능은 결국 ‘더 잘 사는 방법’에 대한 이야기라는 생각도 들고요. 여러분은 어떤 요리 예능을 좋아하시나요?

> [비욘드 트렌드] 에디터의 관점을 담아 지금 우리의 심장을 뛰게하는 트렌드를 소개해요. 나와 가까운 트렌드부터 낯선 분야의 흥미로운 이야기까지. 비욘드 트렌드에서 트렌드 너머의 세상 이야기를 만나보세요.
"""

# themilk
NEWS_LETTER_2 = """# 인간처럼 '보고 듣고 말하고'를 한번에... 오픈AI, 옴니모델 GPT-4o 출시

> [오픈AI 스프링 업데이트 이벤트] 최초의 옴니모델 등장
> 사람처럼 보고 듣고 말할 수 있는 인공지능
> 텍스트, 이미지, 음성 데이터를 동시에 입력해서 추론
> 실시간 통역도 자연스러워... 영상 보며 수학문제도 풀어

오픈AI가 13일 진행한 스프링 제품 업데이트 라이브 스트리밍 이벤트에서 GPT-4o라는 새로운 AI 모델을 발표했다. GPT-4o는 음성 인식과 스피치-투-텍스트 기능을 통합한 대화형 인터페이스 형태의 멀티모달 모델로, 실시간으로 자연스러운 상호작용이 가능하다. 또한, GPT-4 터보에 비해 2배 빠른 API를 제공한다. [AI요약 by 구버]

오픈AI는 13일(현지시각) 진행한 스프링 제품 업데이트 라이브 스트리밍 이벤트에서 새로운 AI 모델 GPT-4o를 공개했다.

GPT-4o는 음성 인식, 스피치-투-텍스트(Speech to text), 이미지 인식 기능 등이 통합돼 대화형 인터페이스 형태로 자연스러운 실시간 상호작용이 가능한 멀티모달(Multimodal, 다중 모드) 모델이다.

기존 GPT 모델이 프롬프트를 데스크톱이나 모바일을 통해 글자(텍스트)를 입력하는 것에 그쳤다면 GPT-4o는 음성, 텍스트, 시각 등 다양한 인간의 활동을 입력, AI가 추론하고 그 결과를 거의 실시간으로 내놓을 수 있도록 한 것이다. GPT-4o의 o는 모든 것을 아우른다는 의미인 ‘옴니(omni)’에 따왔다.

이날 발표는 샘 알트만 CEO가 아닌 미라 무라티 CTO(최고기술책임자)가 무대에 올라 주요 기능을 설명했다.발표를 맡은 무라티 오픈AI CTO는 "GPT-4o는 GPT-4 터보 대비 2배 빠른 API(애플리케이션 프로그래밍 인터페이스)를 제공한다"고 밝혔다. 전 세계 인구 97%가 사용하는 50개 언어를 지원하며 텍스트 및 이미지 기능은 무료로 사용할 수 있다.

GPT4o는 새로운 데스크톱 UI(사용자 인터페이스)를 통해 마치 '코파일럿' 처럼 작동할 수 있게 했다. 기존 GPT4 터보에 비해 2배 빠르고 50% 저렴하며 글자 제한도 5배나 높였다. 또 사람의 감정과 얼굴 표정도 인식하면서 현장에 참석한 오픈AI 직원들의 큰 박수를 받았다.

무라티 CTO는 "GPT-4o는 GPT-4 레벨의 지능을 더 빨리 제공한다"고 강조했다. 사람이 물흐르듯 대화하듯 빠른 반응을 내세운 것이다. 실제 GPT-4o의 평균 응답 시간은 232밀리초인데 이는 평균 320밀리초로 대답하는 인간과 비슷하다. GPT-3.5는 평균 2.8초의 응답 시간을, GPT-4가 5.4초였다.

GPT-4o의 특징

- 무료 챗GPT 사용자에게도 텍스트 및 이미지 기능 제공
- 다중 모드로 설계. 이미지, 텍스트 및 음성을 동시에 분석
- 인간과 유사한 실시간 음성 상호작용을 지원. 말 끊기 가능
- 음성 및 비전 기능을 갖춘 챗GPT 데스크톱 앱 출시
- 향후 몇 주에 걸쳐 점진적으로 배포

## AI, 인간처럼 보고 듣고 말하다

AI와 실시간 대화와 통역

GPT-4o의 가장 큰 업그레이드는 실시간 대화 기능이었다. 기존 챗GPT는 몇 초간 기다려야 하는 지연이 있었으나 GPT-4o는 음성으로 궁금한 것을 입력하면 실시간으로 음성 답변을 들을 수 있다.

GPT-4o는 대답이 자연스러울 뿐 아니라 심지어 감정까지 표현할 수 있었다. 잠잘 때 동화를 만들어달라는 요청부터 로봇 소리로 바꿔달라, 강렬한 드라마처럼 표현해달라는 요청에 즉각 반응했다.

실제 오픈AI 팀이 "로봇과 관련된 잠자리 동화를 들려줘"라고 말하자 즉시 동화를 만들어냈다. 연구원이 중간에 끊고 "아니, 좀 더 극적인 말투로 해줘"라고 요청하자 바로 성우처럼 감정을 추가한 말투로 동화를 읊었다.

또 실시간 '통역'도 시연했다. 오픈AI 팀은 실시간 통역 도구 역할을 하는 챗GPT 보이스의 기능을 시연했는데 미라 무라티가 이탈리아어로 얘기하면 영어로 변환한 다음 바로 영어로 응답을 받아 이탈리아어로 대화하는 높은 수준의 통번역 기능을 소개했다.

## AI에 눈이 생겼다

AI가 스마트폰 카메라를 통해 대상을 해석하고 대답을 할 수 있게 됐다. 시연에서 오픈AI 팀은 종이에 실시간으로 작성한 수학 방정식을 GPT에 보여주고 AI에게 문제 해결을 도와달라고 요청했다.

오픈AI 팀은 챗GPT의 음성 대화 모드를 실행하고 "수학 문제를 풀건데 정답을 말하지 말고 풀이 과정을 도와줘"라고 요청했다. 이후 카메라를 실행시켜 화면에 ‘3x+1=4′라는 수식을 비춰주자, AI는 "x의 값을 구하기 위해선 x를 제외한 모든 숫자를 한쪽으로 모이게 해야한다. 저 1을 어떻게 해야할까?"라고 문제 풀이를 안내하는 모습을 보였다. 답을 주는 것이 아니라, 조언을 해주고 단계별로 문제를 풀어 나간 것이다.

또 연구원이 스마트폰 카메라로 웃고 있는 자신의 얼굴을 비추며 "내가 지금 어때보여"라고 묻자 챗GPT는 "기쁘고 신난 것 같다"고 대답하기도 했다. 오픈AI는 이날 시연을 마치고 공개한 웹사이트에 AI간에 대화를 주고 받는 데모 영상을 공개하기도 했다. AI가 "무엇이 보이냐?"고 묻자 다른 AI가 주변을 인식해 "검은 가죽 자켓을 입은 남성이 앉아있다"고 답했다.

## 코드와 그래프를 실시간으로 분석

GPT-4o는 작성 중인 코드를 보고 코드를 분석했다. 잠재적인 문제를 발견할 수 있었으며 현재 데스크톱에서 작업 중인 내용도 설명할 수 있었다. 데모 중에 그래프를 보고 실제 피드백과 정보를 제공하는 놀라운 장면을 연출했다.

미라 무라티 오픈AI CTO(사진 왼쪽)과 연구원들이 옴니모델인 GPT-4o를 시연하고 있다 (출처 : 유튜브 캡쳐)
언어 장벽을 더 낮춘다

GPT-4o는 통역, 번역 기능이 우수하고 비영어권 언어의 성능과 토큰 효율을 크게 개선한 것이 특징이다.

오픈AI는 벤치마크 테스트를 공개하며 GPT-4o가 지난해 11월 출시된 'GPT-4 터보'와 동급 이상의 성능을 보여줬다. 제로샷 COT MMLU에선 88.7점으로 최고 성능을 기록했다. 한국어 등 비영어권 언어 성능과 토큰 효율도 개선했다.

예를 들어 '안녕하세요, 제 이름은 GPT-4o입니다. 저는 새로운 유형의 언어 모델입니다, 만나서 반갑습니다!' 라는 문장을 쓰면 문장에 기존에는 토큰 45개가 쓰였는데 27개로 줄었다. 1.7배 (70%) 개선됐다는게 오픈AI의 설명이다.

이번 글로벌 언어 업데이트엔 인도의 다양한 언어들에 대한 성는을 대폭 개선시켰다. 오픈AI가 인도 시장을 다음 타깃으로 삼고 있음을 시사하고 있다.
"""
