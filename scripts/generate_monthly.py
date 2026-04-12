#!/usr/bin/env python3
"""
Generate 144 monthly zodiac fortune pages for saju.gon.ai.kr
12 zodiac animals x 12 months = 144 static HTML pages

Based on 오행(五行) element interaction system:
- 상생(相生): Wood->Fire->Earth->Metal->Water->Wood
- 상극(相克): Wood->Earth, Earth->Water, Water->Fire, Fire->Metal, Metal->Wood
"""

import os
import hashlib
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ─── ZODIAC DATA ───────────────────────────────────────────────────────
ZODIACS = [
    {
        "id": "rat", "ko": "쥐띠", "hanja": "子(자)", "element": "수",
        "emoji": "🐀", "yearly_score": 70,
        "years": "1948, 1960, 1972, 1984, 1996, 2008, 2020",
        "trait": "영리하고 재치 있으며 적응력이 뛰어납니다",
        "career": "기획, 분석, 커뮤니케이션 분야",
        "health_organ": "신장과 방광",
        "health_advice_base": "충분한 수분 섭취와 하체 운동이 중요합니다",
        "lucky_colors": "파랑, 검정",
        "lucky_nums": "1, 6",
    },
    {
        "id": "ox", "ko": "소띠", "hanja": "丑(축)", "element": "토",
        "emoji": "🐂", "yearly_score": 68,
        "years": "1949, 1961, 1973, 1985, 1997, 2009, 2021",
        "trait": "성실하고 인내심이 강하며 신뢰할 수 있습니다",
        "career": "관리, 농업, 금융 분야",
        "health_organ": "비장과 위장",
        "health_advice_base": "규칙적인 식사와 소화기 관리가 중요합니다",
        "lucky_colors": "노랑, 갈색",
        "lucky_nums": "5, 10",
    },
    {
        "id": "tiger", "ko": "호랑이띠", "hanja": "寅(인)", "element": "목",
        "emoji": "🐅", "yearly_score": 92,
        "years": "1950, 1962, 1974, 1986, 1998, 2010, 2022",
        "trait": "용감하고 열정적이며 리더십이 뛰어납니다",
        "career": "경영, 군사, 스포츠 분야",
        "health_organ": "간과 담",
        "health_advice_base": "스트레칭과 눈 건강 관리가 중요합니다",
        "lucky_colors": "초록, 청록",
        "lucky_nums": "3, 8",
    },
    {
        "id": "rabbit", "ko": "토끼띠", "hanja": "卯(묘)", "element": "목",
        "emoji": "🐇", "yearly_score": 60,
        "years": "1951, 1963, 1975, 1987, 1999, 2011, 2023",
        "trait": "온화하고 세심하며 예술적 감각이 뛰어납니다",
        "career": "예술, 디자인, 외교 분야",
        "health_organ": "간과 근육",
        "health_advice_base": "유연성 운동과 충분한 휴식이 중요합니다",
        "lucky_colors": "초록, 분홍",
        "lucky_nums": "3, 4",
    },
    {
        "id": "dragon", "ko": "용띠", "hanja": "辰(진)", "element": "토",
        "emoji": "🐉", "yearly_score": 75,
        "years": "1952, 1964, 1976, 1988, 2000, 2012, 2024",
        "trait": "카리스마 있고 야심 차며 자신감이 넘칩니다",
        "career": "사업, 정치, 연예 분야",
        "health_organ": "비장과 위장",
        "health_advice_base": "과로 방지와 규칙적인 식사가 중요합니다",
        "lucky_colors": "노랑, 금색",
        "lucky_nums": "5, 8",
    },
    {
        "id": "snake", "ko": "뱀띠", "hanja": "巳(사)", "element": "화",
        "emoji": "🐍", "yearly_score": 78,
        "years": "1953, 1965, 1977, 1989, 2001, 2013, 2025",
        "trait": "지혜롭고 직관력이 뛰어나며 신비로운 매력이 있습니다",
        "career": "연구, 의료, 철학 분야",
        "health_organ": "심장과 소장",
        "health_advice_base": "심혈관 관리와 명상이 도움됩니다",
        "lucky_colors": "빨강, 주황",
        "lucky_nums": "2, 7",
    },
    {
        "id": "horse", "ko": "말띠", "hanja": "午(오)", "element": "화",
        "emoji": "🐴", "yearly_score": 80,
        "years": "1954, 1966, 1978, 1990, 2002, 2014, 2026",
        "trait": "활발하고 자유로우며 낙천적인 성격입니다",
        "career": "영업, 여행, 운동 분야",
        "health_organ": "심장과 혈관",
        "health_advice_base": "유산소 운동과 스트레스 관리가 중요합니다",
        "lucky_colors": "빨강, 보라",
        "lucky_nums": "2, 7",
    },
    {
        "id": "goat", "ko": "양띠", "hanja": "未(미)", "element": "토",
        "emoji": "🐑", "yearly_score": 88,
        "years": "1955, 1967, 1979, 1991, 2003, 2015",
        "trait": "온순하고 창의적이며 예술적 재능이 풍부합니다",
        "career": "예술, 요리, 패션 분야",
        "health_organ": "비장과 소화계",
        "health_advice_base": "따뜻한 음식과 소화기 건강 관리가 중요합니다",
        "lucky_colors": "노랑, 크림",
        "lucky_nums": "5, 0",
    },
    {
        "id": "monkey", "ko": "원숭이띠", "hanja": "申(신)", "element": "금",
        "emoji": "🐒", "yearly_score": 65,
        "years": "1956, 1968, 1980, 1992, 2004, 2016",
        "trait": "영특하고 재주가 많으며 유머 감각이 뛰어납니다",
        "career": "IT, 발명, 엔터테인먼트 분야",
        "health_organ": "폐와 대장",
        "health_advice_base": "호흡기 관리와 피부 건강에 신경 쓰세요",
        "lucky_colors": "흰색, 은색",
        "lucky_nums": "4, 9",
    },
    {
        "id": "rooster", "ko": "닭띠", "hanja": "酉(유)", "element": "금",
        "emoji": "🐓", "yearly_score": 62,
        "years": "1957, 1969, 1981, 1993, 2005, 2017",
        "trait": "근면하고 정확하며 용기가 있습니다",
        "career": "회계, 법률, 군사 분야",
        "health_organ": "폐와 피부",
        "health_advice_base": "규칙적인 생활과 피부 관리가 중요합니다",
        "lucky_colors": "흰색, 금색",
        "lucky_nums": "4, 9",
    },
    {
        "id": "dog", "ko": "개띠", "hanja": "戌(술)", "element": "토",
        "emoji": "🐕", "yearly_score": 85,
        "years": "1958, 1970, 1982, 1994, 2006, 2018",
        "trait": "충성스럽고 정직하며 의리가 강합니다",
        "career": "공무원, 경찰, 사회복지 분야",
        "health_organ": "비장과 위",
        "health_advice_base": "심리적 안정과 소화기 건강 관리가 중요합니다",
        "lucky_colors": "노랑, 갈색",
        "lucky_nums": "5, 8",
    },
    {
        "id": "pig", "ko": "돼지띠", "hanja": "亥(해)", "element": "수",
        "emoji": "🐷", "yearly_score": 72,
        "years": "1959, 1971, 1983, 1995, 2007, 2019",
        "trait": "관대하고 성실하며 낙관적인 성격입니다",
        "career": "외식, 유통, 엔터테인먼트 분야",
        "health_organ": "신장과 방광",
        "health_advice_base": "체중 관리와 하체 운동이 중요합니다",
        "lucky_colors": "파랑, 검정",
        "lucky_nums": "1, 6",
    },
]

# ─── MONTH DATA ────────────────────────────────────────────────────────
MONTHS = [
    {"num": 1, "ko": "1월", "branch": "寅", "element": "목",
     "season": "초봄", "theme": "새해의 기운이 움트는 시기",
     "nature": "겨울이 물러가고 봄기운이 서서히 올라오는 달"},
    {"num": 2, "ko": "2월", "branch": "卯", "element": "목",
     "season": "봄", "theme": "생명력이 폭발하는 시기",
     "nature": "만물이 소생하고 활기가 넘치는 달"},
    {"num": 3, "ko": "3월", "branch": "辰", "element": "토",
     "season": "늦봄", "theme": "변화와 전환의 시기",
     "nature": "봄에서 여름으로 넘어가는 환절기"},
    {"num": 4, "ko": "4월", "branch": "巳", "element": "화",
     "season": "초여름", "theme": "열정과 활력의 시기",
     "nature": "따뜻한 기운이 강해지고 활동량이 늘어나는 달"},
    {"num": 5, "ko": "5월", "branch": "午", "element": "화",
     "season": "한여름", "theme": "에너지가 절정에 달하는 시기",
     "nature": "양기(陽氣)가 가장 강한 달"},
    {"num": 6, "ko": "6월", "branch": "未", "element": "토",
     "season": "늦여름", "theme": "에너지 전환과 재충전의 시기",
     "nature": "여름이 무르익고 가을을 준비하는 달"},
    {"num": 7, "ko": "7월", "branch": "申", "element": "금",
     "season": "초가을", "theme": "수확과 결실을 준비하는 시기",
     "nature": "서늘한 기운이 시작되고 결실의 기운이 감도는 달"},
    {"num": 8, "ko": "8월", "branch": "酉", "element": "금",
     "season": "가을", "theme": "결실과 풍요의 시기",
     "nature": "가을 기운이 완연하고 수확의 기쁨이 있는 달"},
    {"num": 9, "ko": "9월", "branch": "戌", "element": "토",
     "season": "늦가을", "theme": "정리와 마무리의 시기",
     "nature": "가을이 깊어지고 한 해를 돌아보는 달"},
    {"num": 10, "ko": "10월", "branch": "亥", "element": "수",
     "season": "초겨울", "theme": "내면의 성찰과 준비의 시기",
     "nature": "추위가 시작되고 내면을 돌아보는 달"},
    {"num": 11, "ko": "11월", "branch": "子", "element": "수",
     "season": "한겨울", "theme": "깊은 성찰과 재충전의 시기",
     "nature": "음기(陰氣)가 가장 강하고 내면의 힘을 기르는 달"},
    {"num": 12, "ko": "12월", "branch": "丑", "element": "토",
     "season": "늦겨울", "theme": "한 해를 마무리하고 새해를 준비하는 시기",
     "nature": "겨울이 깊어지지만 봄을 향한 준비가 시작되는 달"},
]

ELEMENT_KO = {"목": "木", "화": "火", "토": "土", "금": "金", "수": "水"}
ELEMENT_NAME = {"목": "목(木)", "화": "화(火)", "토": "토(土)", "금": "금(金)", "수": "수(水)"}

# ─── ELEMENT INTERACTION ───────────────────────────────────────────────
GENERATE_MAP = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
OVERCOME_MAP = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

def get_interaction(zodiac_el, month_el):
    if zodiac_el == month_el:
        return "same"
    if GENERATE_MAP[zodiac_el] == month_el:
        return "generate"
    if GENERATE_MAP[month_el] == zodiac_el:
        return "generated_by"
    if OVERCOME_MAP[zodiac_el] == month_el:
        return "overcome"
    if OVERCOME_MAP[month_el] == zodiac_el:
        return "overcome_by"
    return "neutral"

def _seed(zodiac_id, month_num):
    """Deterministic hash for consistent content selection."""
    h = hashlib.md5(f"{zodiac_id}-{month_num}-2026".encode()).hexdigest()
    return int(h, 16)

# ─── SCORE CALCULATION ─────────────────────────────────────────────────
def calc_scores(zodiac, month):
    interaction = get_interaction(zodiac["element"], month["element"])
    base = zodiac["yearly_score"]
    mod_map = {
        "generated_by": 12, "same": 7, "generate": 3,
        "neutral": 0, "overcome": -3, "overcome_by": -10,
    }
    mod = mod_map[interaction]
    seed = _seed(zodiac["id"], month["num"])

    # Add deterministic micro-variation
    variation = (seed % 11) - 5  # -5 to +5
    total = max(38, min(96, base + mod + variation))

    money = max(35, min(95, total + ((seed >> 4) % 13) - 6))
    love = max(35, min(95, total + ((seed >> 8) % 13) - 6))
    health = max(35, min(95, total + ((seed >> 12) % 11) - 5))

    return {"total": total, "money": money, "love": love, "health": health, "interaction": interaction}

# ─── CONTENT GENERATION ────────────────────────────────────────────────

OVERALL_BY_INTERACTION = {
    "generated_by": [
        "이달은 {month_el_name} 기운이 {zodiac_el_name}인 {ko}에게 생기(生氣)를 불어넣어 주는 상생의 시기입니다. 주변 환경이 자연스럽게 도움을 주므로 새로운 시도에 적극적으로 나서기 좋습니다.",
        "{month_ko}은 {ko}에게 외부로부터 긍정적 에너지가 유입되는 달입니다. {month_el_name}이(가) {zodiac_el_name}을(를) 생(生)하는 구조이므로 기회가 자연스럽게 찾아옵니다.",
        "2026년 {month_ko}, {ko}는 주변의 지원과 행운이 함께하는 시기입니다. 상생(相生)의 기운 덕분에 노력한 만큼 좋은 결과를 기대할 수 있습니다.",
    ],
    "generate": [
        "이달은 {ko}의 {zodiac_el_name} 기운이 {month_el_name}으로 발산되는 시기입니다. 에너지가 바깥으로 흐르므로 주도적으로 행동하되 체력 관리에 신경 쓰세요.",
        "{month_ko}은 {ko}가 자신의 에너지를 적극적으로 발휘하는 달입니다. 창의력과 추진력이 높아지지만 과도한 에너지 소모에 주의가 필요합니다.",
        "2026년 {month_ko}, {ko}는 능동적으로 기회를 만들어가는 시기입니다. {zodiac_el_name}이(가) {month_el_name}을(를) 생하므로 자신의 재능을 발휘할 무대가 열립니다.",
    ],
    "same": [
        "이달은 {ko}의 본래 기운인 {zodiac_el_name}이(가) 한층 강화되는 비화(比和)의 시기입니다. 에너지가 증폭되어 자신감이 높아지지만 과잉에 주의하세요.",
        "{month_ko}은 {ko}에게 같은 {zodiac_el_name} 에너지가 겹치는 달입니다. 자신의 강점이 극대화되는 반면 약점도 함께 부각될 수 있으니 균형이 중요합니다.",
        "2026년 {month_ko}, {ko}는 본연의 기질이 두드러지는 시기입니다. 비화의 기운으로 동료나 같은 분야 사람들과의 협력이 특히 유리합니다.",
    ],
    "overcome": [
        "이달은 {ko}의 {zodiac_el_name} 기운이 {month_el_name}을(를) 제어하는 상극(相克)의 구조입니다. 주도권을 잡기 좋지만 지나친 통제는 갈등을 불러올 수 있습니다.",
        "{month_ko}은 {ko}가 상황을 이끌어갈 힘이 있는 달입니다. 다만 상극의 긴장감이 존재하므로 부드러운 접근 방식이 효과적입니다.",
        "2026년 {month_ko}, {ko}는 도전을 극복할 내적 힘이 충만한 시기입니다. {zodiac_el_name}이(가) {month_el_name}을(를) 극(克)하므로 결단력 있는 행동이 성과를 만듭니다.",
    ],
    "overcome_by": [
        "이달은 {month_el_name}의 기운이 {ko}의 {zodiac_el_name}을(를) 압박하는 시기입니다. 외부 압력이 강해질 수 있으므로 신중하고 보수적인 접근이 유리합니다.",
        "{month_ko}은 {ko}에게 다소 도전적인 달입니다. {month_el_name}이(가) {zodiac_el_name}을(를) 극하는 구조이므로 큰 결정은 미루고 내실을 다지는 데 집중하세요.",
        "2026년 {month_ko}, {ko}는 인내가 필요한 시기입니다. 상극의 에너지를 지혜롭게 활용하면 오히려 성장의 발판으로 삼을 수 있습니다.",
    ],
    "neutral": [
        "이달은 {ko}에게 비교적 평온한 기운이 흐르는 시기입니다. {month_el_name}과(와) {zodiac_el_name}이(가) 직접적 상호작용이 없어 자유롭게 계획을 세울 수 있습니다.",
        "{month_ko}은 {ko}에게 안정적인 에너지가 흐르는 달입니다. 큰 파동 없이 꾸준히 실력을 쌓기 좋은 시기입니다.",
        "2026년 {month_ko}, {ko}는 자기 페이스를 유지하며 나아갈 수 있는 시기입니다. 급격한 변화보다 꾸준한 노력이 빛을 발합니다.",
    ],
}

MONEY_BY_INTERACTION = {
    "generated_by": [
        "재물운이 상승세에 있습니다. 예상치 못한 수입이나 투자 기회가 찾아올 수 있으며, 평소 관심을 두었던 분야에서 경제적 성과가 나타납니다. 적극적인 재테크 활동이 권장됩니다.",
        "금전적으로 여유로운 달입니다. 사업이나 부업에서 좋은 소식이 있을 수 있고, 오래된 채권이 회수되거나 뜻밖의 보너스가 기대됩니다.",
        "재물 기운이 자연스럽게 모이는 시기입니다. 새로운 수입원을 개척하기 좋으며, 저축과 투자 모두 긍정적인 흐름을 보입니다.",
    ],
    "generate": [
        "재물운은 보통 수준이지만 적극적 활동이 수입으로 이어집니다. 지출이 늘어날 수 있으니 예산 관리에 신경 쓰되, 자기 계발 투자는 장기적으로 이득입니다.",
        "돈이 나가는 만큼 들어오는 달입니다. 에너지를 쏟은 곳에서 경제적 보상이 따르지만, 과도한 소비는 자제하세요.",
        "능동적인 재테크가 필요한 시기입니다. 가만히 있으면 기회를 놓칠 수 있으니, 적절한 투자와 부수입 활동을 병행하세요.",
    ],
    "same": [
        "비화의 기운으로 동업이나 협업에서 수익이 기대됩니다. 같은 분야 사람들과의 네트워킹이 재물운과 직결되며, 공동 투자도 고려할 만합니다.",
        "재물운이 안정적입니다. 큰 변동 없이 꾸준한 수입이 유지되며, 동료나 지인을 통한 재테크 정보가 도움이 됩니다.",
        "같은 업종 사람들과의 교류가 경제적 이익으로 이어집니다. 과도한 경쟁보다 상생의 관계가 더 큰 수익을 가져옵니다.",
    ],
    "overcome": [
        "주도적으로 재물을 관리할 수 있는 달입니다. 협상이나 거래에서 유리한 고지를 점할 수 있으며, 적극적인 재테크가 효과를 봅니다.",
        "재물 관련 결정에서 자신감을 가져도 좋습니다. 다만 지나친 욕심은 금물이며, 적정선에서 이익을 확정짓는 지혜가 필요합니다.",
        "경제적 주도권을 쥘 수 있는 시기입니다. 부동산이나 큰 거래에서 유리한 조건을 이끌어낼 수 있으니 기회를 놓치지 마세요.",
    ],
    "overcome_by": [
        "재물운에 주의가 필요합니다. 예상치 못한 지출이 발생할 수 있으니 비상 자금을 확보해 두세요. 큰 투자나 보증은 이달에 피하는 것이 현명합니다.",
        "금전적으로 보수적인 태도가 필요한 달입니다. 충동 구매를 자제하고 필수 지출 위주로 관리하세요. 하반기에 회복될 기운이 있으니 인내하세요.",
        "재물 유출의 기운이 있는 시기입니다. 불필요한 지출을 줄이고 저축에 집중하세요. 다만 건강이나 교육 관련 투자는 아끼지 마세요.",
    ],
    "neutral": [
        "재물운이 평탄합니다. 큰 이득도 큰 손실도 없는 달이니 꾸준히 저축하며 미래를 대비하세요. 소소한 부수입이 생길 수 있습니다.",
        "안정적인 재정 상태가 유지됩니다. 무리한 투자보다 정기적금이나 안전 자산에 투자하는 것이 현명합니다.",
        "큰 변동 없이 무난한 재물운입니다. 장기적 관점에서 재무 계획을 세우기 좋은 시기이며, 불필요한 소비 습관을 정리해 보세요.",
    ],
}

LOVE_BY_INTERACTION = {
    "generated_by": [
        "연애운이 빛나는 달입니다. 솔로라면 매력적인 만남이 기대되며, 커플은 관계가 한층 깊어집니다. 자연스러운 만남의 자리에 적극 참여하세요.",
        "이성에게 특히 매력적으로 보이는 시기입니다. 소개팅이나 모임에서 좋은 인연을 만날 확률이 높으며, 기존 파트너와는 소통이 원활해집니다.",
        "사랑의 기운이 가득한 달입니다. 고백이나 프로포즈에 적합하며, 오랜 짝사랑이 결실을 맺을 수 있는 시기입니다.",
    ],
    "generate": [
        "연애에서 적극적인 모습이 매력으로 작용합니다. 상대에게 먼저 다가가는 용기가 좋은 결과를 가져오며, 데이트는 야외 활동이 좋습니다.",
        "이달은 자신의 감정을 표현하는 것이 중요합니다. 속마음을 솔직히 전달할수록 관계가 발전하며, 새로운 취미 활동에서 인연을 만날 수 있습니다.",
        "능동적인 연애가 유리한 시기입니다. 기다리기보다 직접 행동에 나서되, 상대의 감정도 존중하는 균형이 필요합니다.",
    ],
    "same": [
        "비슷한 성향의 사람과 강한 유대감을 느끼는 달입니다. 같은 관심사를 가진 모임에서 인연이 시작될 수 있으며, 서로를 깊이 이해하는 관계가 형성됩니다.",
        "연애에서 공감과 동질감이 키워드입니다. 커플은 함께하는 활동에서 행복을 느끼며, 솔로는 동호회나 스터디에서 인연을 찾아보세요.",
        "같은 가치관을 가진 사람과의 만남이 유력합니다. 외모보다 내면의 교감이 중요한 시기이며, 깊은 대화가 관계를 발전시킵니다.",
    ],
    "overcome": [
        "연애에서 주도권을 잡게 되는 달입니다. 자신감이 매력으로 작용하지만, 상대를 배려하는 마음을 잊지 마세요. 지나친 주도는 부담을 줄 수 있습니다.",
        "리드하는 연애가 가능한 시기입니다. 데이트 계획을 주도적으로 세우면 좋은 반응을 얻으며, 결단력 있는 모습이 이성에게 어필됩니다.",
        "관계에서 적극적인 역할을 맡게 됩니다. 상대의 고민을 해결해주는 것이 호감도를 높이며, 진지한 대화를 통해 관계가 발전합니다.",
    ],
    "overcome_by": [
        "연애에서 약간의 시련이 있을 수 있습니다. 오해나 갈등이 생기기 쉬우니 감정적 반응보다 차분한 대화를 선택하세요. 인내가 관계를 지킵니다.",
        "이달은 연애보다 자기 관리에 집중하는 것이 좋습니다. 무리한 고백보다 자신의 매력을 가꾸는 시간을 가지세요. 좋은 인연은 자연스럽게 찾아옵니다.",
        "감정의 기복이 클 수 있는 시기입니다. 커플은 사소한 다툼에 주의하고, 솔로는 이상형을 너무 높게 잡지 않는 것이 좋습니다.",
    ],
    "neutral": [
        "연애운이 평온합니다. 특별한 이벤트보다 일상 속 소소한 행복이 관계를 단단하게 합니다. 솔로는 자기 개발에 힘쓰면 자연스럽게 매력이 올라갑니다.",
        "무난한 연애 기운이 흐릅니다. 급한 진전보다 천천히 관계를 쌓아가는 것이 좋으며, 진정성 있는 태도가 상대의 마음을 얻습니다.",
        "안정적인 관계 유지가 가능한 달입니다. 새로운 만남보다 기존 인연을 소중히 하세요. 오랜 친구에게서 새로운 감정을 발견할 수도 있습니다.",
    ],
}

HEALTH_BY_INTERACTION = {
    "generated_by": [
        "건강 기운이 양호한 달입니다. 활력이 넘치고 컨디션이 좋아지는 시기이므로 새로운 운동을 시작하기에 적합합니다. {organ} 건강도 안정적입니다.",
        "체력과 면역력이 상승하는 시기입니다. 규칙적인 운동 습관을 만들면 효과가 배가되며, {organ} 관련 불편함이 자연스럽게 해소됩니다.",
    ],
    "generate": [
        "에너지 소모가 많은 달이므로 충분한 휴식이 필요합니다. 활동량이 늘어 체력이 빠지기 쉬우니 영양 보충에 신경 쓰세요. {organ} 관리도 잊지 마세요.",
        "활발한 활동으로 인한 피로 누적에 주의하세요. 수면의 질을 높이고 비타민 섭취를 늘리는 것이 좋습니다. {organ}에 무리가 가지 않도록 주의하세요.",
    ],
    "same": [
        "건강 기운이 증폭되어 체력이 좋아지는 반면, 과잉 에너지로 인한 불면이나 조급함에 주의하세요. {organ} 건강을 위해 명상이나 요가가 도움됩니다.",
        "본래의 체질적 특성이 강하게 나타나는 달입니다. 장점은 살리고 약점은 보완하는 생활 습관이 중요하며, {organ} 정기 검진을 고려해 보세요.",
    ],
    "overcome": [
        "전반적으로 건강한 편이지만 과로에 주의하세요. 일에 몰두하느라 건강을 소홀히 하기 쉬운 달입니다. {organ} 건강을 위해 가벼운 산책을 추천합니다.",
        "체력은 양호하지만 정신적 피로가 쌓일 수 있습니다. 업무와 휴식의 균형을 맞추고, {organ}에 부담을 줄이는 식이요법을 실천하세요.",
    ],
    "overcome_by": [
        "건강 관리에 각별한 주의가 필요한 달입니다. 면역력이 떨어지기 쉬우니 충분한 수면과 균형 잡힌 식단을 유지하세요. 특히 {organ}에 신경 쓰고, 무리한 운동은 피하세요.",
        "체력이 저하되기 쉬운 시기입니다. 과로를 피하고 충분한 휴식을 취하세요. {organ} 관련 기존 질환이 있다면 정기 검진을 받는 것이 좋습니다.",
    ],
    "neutral": [
        "건강운은 무난합니다. 특별한 건강 이슈 없이 평소 컨디션을 유지할 수 있는 달입니다. 규칙적인 생활 패턴을 유지하면 {organ} 건강도 양호합니다.",
        "건강이 안정적인 시기입니다. 기본적인 생활 습관만 잘 유지하면 큰 문제 없이 지나갈 수 있습니다. {organ} 건강을 위해 가벼운 스트레칭을 병행하세요.",
    ],
}

# ─── SEASONAL ADVICE ───────────────────────────────────────────────────
SEASONAL_HEALTH = {
    1: "겨울철 한파에 대비해 보온에 신경 쓰고, 실내 건조함으로 인한 호흡기 질환에 주의하세요.",
    2: "환절기 온도 변화가 큰 시기이므로 감기 예방에 힘쓰세요. 봄 알레르기가 시작될 수 있습니다.",
    3: "봄철 황사와 미세먼지에 대비해 마스크를 착용하고, 봄나물로 영양을 보충하세요.",
    4: "야외 활동이 늘어나는 시기이므로 자외선 차단에 신경 쓰고, 충분한 수분을 섭취하세요.",
    5: "기온이 급상승하는 달이므로 열사병과 탈수에 주의하세요. 시원한 음식보다 따뜻한 음식이 소화에 좋습니다.",
    6: "장마철 습도 관리가 중요합니다. 곰팡이와 식중독에 주의하고, 실내 환기를 자주 하세요.",
    7: "무더위 속 냉방병에 주의하세요. 찬 음식을 과도하게 섭취하면 소화기에 부담이 됩니다.",
    8: "늦더위와 함께 체력이 저하되기 쉽습니다. 보양식으로 체력을 보충하고 충분한 수면을 취하세요.",
    9: "가을 환절기 건강 관리가 중요합니다. 일교차가 커지므로 겉옷을 챙기고, 제철 과일로 비타민을 보충하세요.",
    10: "건조한 가을 날씨에 피부와 호흡기 관리가 필요합니다. 따뜻한 차와 충분한 수분 섭취를 권합니다.",
    11: "추위가 본격화되므로 관절과 근육 건강에 주의하세요. 실내 운동으로 체력을 유지하는 것이 좋습니다.",
    12: "한파와 연말 피로가 겹치는 시기입니다. 과음과 과식을 자제하고, 충분한 수면으로 면역력을 지키세요.",
}

LUCKY_DAYS = [
    "3일, 12일, 21일", "5일, 14일, 23일", "1일, 10일, 28일",
    "7일, 16일, 25일", "2일, 11일, 20일", "8일, 17일, 26일",
    "4일, 13일, 22일", "6일, 15일, 24일", "9일, 18일, 27일",
    "3일, 15일, 24일", "6일, 12일, 21일", "1일, 14일, 23일",
]

LUCKY_DIRECTIONS = ["동쪽", "남동쪽", "남쪽", "남서쪽", "서쪽", "북서쪽", "북쪽", "북동쪽"]

# ─── HTML TEMPLATE ─────────────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{meta_keywords}">
    <title>{title}</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/zodiac/{animal_id}/{month_num}/">

    <!-- Naver Search Advisor -->
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:url" content="https://saju.gon.ai.kr/zodiac/{animal_id}/{month_num}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{og_title}">
    <meta name="twitter:description" content="{og_description}">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{schema_headline}",
        "description": "{meta_description}",
        "url": "https://saju.gon.ai.kr/zodiac/{animal_id}/{month_num}/",
        "datePublished": "2026-01-01",
        "dateModified": "{today}",
        "publisher": {{
            "@type": "Organization",
            "name": "사주명리",
            "url": "https://saju.gon.ai.kr/"
        }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "https://saju.gon.ai.kr/" }},
                {{ "@type": "ListItem", "position": 2, "name": "띠별 운세", "item": "https://saju.gon.ai.kr/zodiac/" }},
                {{ "@type": "ListItem", "position": 3, "name": "{zodiac_ko} 운세", "item": "https://saju.gon.ai.kr/zodiac/{animal_id}/" }},
                {{ "@type": "ListItem", "position": 4, "name": "{month_num}월 운세", "item": "https://saju.gon.ai.kr/zodiac/{animal_id}/{month_num}/" }}
            ]
        }}
    }}
    </script>

    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "2026년 {month_num}월 {zodiac_ko} 총운은 몇 점인가요?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{faq_overall}"
                }}
            }},
            {{
                "@type": "Question",
                "name": "{zodiac_ko}의 2026년 {month_num}월 재물운은 어떤가요?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{faq_money}"
                }}
            }},
            {{
                "@type": "Question",
                "name": "{zodiac_ko}의 2026년 {month_num}월 연애운은?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{faq_love}"
                }}
            }},
            {{
                "@type": "Question",
                "name": "{zodiac_ko}의 2026년 {month_num}월 건강운과 주의사항은?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{faq_health}"
                }}
            }}
        ]
    }}
    </script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/zodiac.css?v=2">

    <!-- Google AdSense Script -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290"
         crossorigin="anonymous"></script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-BNRL6FRMMM');
    </script>

    <style>
        .zodiac-detail-page {{ max-width: 800px; margin: 0 auto; padding: var(--spacing-lg); }}
        .zodiac-detail-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .zodiac-detail-hero .detail-emoji {{ font-size: 5rem; margin-bottom: var(--spacing-md); filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); }}
        .zodiac-detail-hero .detail-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); margin-bottom: var(--spacing-xs); }}
        .zodiac-detail-hero .detail-name {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-sm); }}
        .zodiac-detail-hero .detail-element-badge {{ display: inline-block; padding: var(--spacing-xs) var(--spacing-lg); border: 1px solid var(--color-gold-muted); border-radius: var(--radius-full); color: var(--color-gold); font-size: var(--text-sm); margin-bottom: var(--spacing-lg); }}
        .zodiac-detail-hero .detail-total-score {{ width: 100px; height: 100px; border: 3px solid; border-radius: var(--radius-full); display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: var(--text-3xl); font-weight: var(--font-bold); margin: 0 auto var(--spacing-md); }}
        .zodiac-detail-hero .detail-total-score small {{ font-size: var(--text-sm); font-weight: var(--font-normal); }}
        .zodiac-detail-hero .years-info {{ font-size: var(--text-sm); color: var(--color-text-tertiary); }}
        .month-badge {{ display: inline-block; padding: 8px 20px; background: linear-gradient(135deg, rgba(212,175,55,0.25), rgba(212,175,55,0.1)); border: 1px solid var(--color-gold-muted); border-radius: var(--radius-full); color: var(--color-gold-light); font-size: var(--text-lg); font-weight: var(--font-semibold); margin-bottom: var(--spacing-lg); }}
        .zodiac-scores-section {{ padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); margin-bottom: var(--spacing-xl); }}
        .zodiac-scores-section .detail-score-item {{ display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-md); }}
        .zodiac-scores-section .detail-score-item:last-child {{ margin-bottom: 0; }}
        .zodiac-scores-section .score-icon {{ font-size: 1.2rem; width: 28px; text-align: center; }}
        .zodiac-scores-section .score-name {{ width: 60px; font-size: var(--text-sm); color: var(--color-text-secondary); }}
        .zodiac-scores-section .score-bar-detail {{ flex: 1; height: 8px; background: rgba(255,255,255,0.06); border-radius: var(--radius-full); overflow: hidden; }}
        .zodiac-scores-section .score-fill-detail {{ height: 100%; border-radius: var(--radius-full); transition: width 1s ease-out; }}
        .zodiac-scores-section .score-value {{ width: 45px; text-align: right; font-size: var(--text-sm); font-weight: var(--font-semibold); }}
        .zodiac-content-section {{ margin-bottom: var(--spacing-xl); }}
        .zodiac-content-section h2 {{ font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-md); color: var(--color-gold-text); }}
        .zodiac-content-section p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); font-size: var(--text-base); margin-bottom: var(--spacing-sm); }}
        .lucky-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); margin-bottom: var(--spacing-xl); }}
        .lucky-grid .lucky-item {{ display: flex; flex-direction: column; gap: var(--spacing-xs); }}
        .lucky-grid .lucky-label {{ font-size: var(--text-xs); color: var(--color-text-tertiary); letter-spacing: var(--letter-spacing-wider); }}
        .lucky-grid .lucky-value {{ font-size: var(--text-base); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .lucky-grid .lucky-value.good {{ color: var(--color-success); }}
        .month-nav {{ display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-lg) 0; margin-bottom: var(--spacing-xl); border-top: 1px solid var(--color-border-light); border-bottom: 1px solid var(--color-border-light); }}
        .month-nav a {{ color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); transition: color var(--duration-fast); }}
        .month-nav a:hover {{ color: var(--color-gold-light); }}
        .month-nav .current {{ color: var(--color-text-primary); font-weight: var(--font-semibold); }}
        .month-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: var(--spacing-sm); margin-bottom: var(--spacing-xl); }}
        .month-grid a {{ display: flex; align-items: center; justify-content: center; padding: var(--spacing-sm); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-lg); text-decoration: none; color: var(--color-text-secondary); font-size: var(--text-sm); transition: all var(--duration-normal); }}
        .month-grid a:hover {{ border-color: var(--color-gold-muted); color: var(--color-gold); transform: translateY(-1px); }}
        .month-grid a.current {{ border-color: var(--color-gold); background: rgba(212,175,55,0.08); color: var(--color-gold); font-weight: var(--font-semibold); }}
        .other-zodiac-section {{ margin-top: var(--spacing-3xl); padding-top: var(--spacing-2xl); border-top: 1px solid var(--color-border-light); }}
        .other-zodiac-section h2 {{ text-align: center; font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-xl); }}
        .other-zodiac-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: var(--spacing-md); }}
        .other-zodiac-link {{ display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-md); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .other-zodiac-link:hover {{ border-color: var(--color-gold-muted); transform: translateY(-2px); }}
        .other-zodiac-link .oz-emoji {{ font-size: 2rem; }}
        .other-zodiac-link .oz-name {{ font-size: var(--text-sm); color: var(--color-text-primary); font-weight: var(--font-medium); }}
        .other-zodiac-link .oz-score {{ font-size: var(--text-xs); color: var(--color-text-tertiary); }}
        .other-zodiac-link.current {{ border-color: var(--color-gold); background: rgba(212,175,55,0.08); }}
        .back-link {{ display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); margin-bottom: var(--spacing-lg); transition: color var(--duration-fast); }}
        .back-link:hover {{ color: var(--color-gold-light); }}
        .element-info {{ font-size: var(--text-sm); color: var(--color-text-tertiary); text-align: center; margin-bottom: var(--spacing-md); padding: var(--spacing-md); background: var(--color-bg-tertiary); border-radius: var(--radius-lg); }}
        @media (max-width: 768px) {{
            .zodiac-detail-hero .detail-name {{ font-size: var(--text-3xl); }}
            .zodiac-detail-hero .detail-emoji {{ font-size: 3.5rem; }}
            .other-zodiac-grid {{ grid-template-columns: repeat(4, 1fr); }}
            .month-grid {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        @media (max-width: 480px) {{
            .other-zodiac-grid {{ grid-template-columns: repeat(3, 1fr); }}
            .month-grid {{ grid-template-columns: repeat(3, 1fr); }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">사주명리</span>
                </h1>
            </a>
            <nav class="nav-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/" class="active">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/palm/">손금 분석</a>
            </nav>
        </nav>
    </header>

    <main class="zodiac-detail-page">
        <a href="/zodiac/{animal_id}/" class="back-link">&larr; {zodiac_ko} 연간 운세 보기</a>

        <!-- Hero -->
        <section class="zodiac-detail-hero">
            <div class="detail-emoji">{emoji}</div>
            <div class="detail-hanja">{hanja}</div>
            <h1 class="detail-name"><span class="gold-text">{month_num}월 {zodiac_ko} 운세</span></h1>
            <div class="month-badge">2026년 {month_num}월</div>
            <div class="detail-element-badge">오행: {element_name} | 월지: {month_branch}</div>
            <div class="detail-total-score" style="border-color: {score_color}; color: {score_color};">
                {total_score}<small>점</small>
            </div>
            <p class="years-info">해당 연도: {years}</p>
        </section>

        <!-- Element Info -->
        <div class="element-info">
            {element_interaction_desc}
        </div>

        <!-- Score Bars -->
        <section class="zodiac-scores-section">
            <div class="detail-score-item">
                <span class="score-icon">💰</span>
                <span class="score-name">재물운</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="width: {money_score}%; background: linear-gradient(90deg, #D4AF37, #F0D78C)"></div></div>
                <span class="score-value">{money_score}점</span>
            </div>
            <div class="detail-score-item">
                <span class="score-icon">💕</span>
                <span class="score-name">연애운</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="width: {love_score}%; background: linear-gradient(90deg, #F87171, #FCA5A5)"></div></div>
                <span class="score-value">{love_score}점</span>
            </div>
            <div class="detail-score-item">
                <span class="score-icon">💪</span>
                <span class="score-name">건강운</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="width: {health_score}%; background: linear-gradient(90deg, #4ADE80, #86EFAC)"></div></div>
                <span class="score-value">{health_score}점</span>
            </div>
        </section>

        <!-- Month Navigation -->
        <div class="month-grid">
            {month_grid_html}
        </div>

        <!-- Overall Fortune -->
        <section class="zodiac-content-section">
            <h2>🔮 {month_num}월 총운</h2>
            <p>{overall_text}</p>
            <p>{season_theme}</p>
        </section>

        <!-- Money -->
        <section class="zodiac-content-section">
            <h2>💰 {month_num}월 재물운</h2>
            <p>{money_text}</p>
        </section>

        <!-- Love -->
        <section class="zodiac-content-section">
            <h2>💕 {month_num}월 연애운</h2>
            <p>{love_text}</p>
        </section>

        <!-- Health -->
        <section class="zodiac-content-section">
            <h2>💪 {month_num}월 건강운</h2>
            <p>{health_text}</p>
            <p>{seasonal_health}</p>
        </section>

        <!-- Lucky Info -->
        <div class="lucky-grid">
            <div class="lucky-item">
                <span class="lucky-label">행운의 날</span>
                <span class="lucky-value good">{lucky_days}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">행운의 방위</span>
                <span class="lucky-value">{lucky_direction}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">행운의 색</span>
                <span class="lucky-value">{lucky_colors}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">행운의 숫자</span>
                <span class="lucky-value">{lucky_nums}</span>
            </div>
        </div>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <a href="/" class="cta-btn">무료 사주풀이 바로가기</a>
        </section>

        <!-- Other Zodiac for same month -->
        <section class="other-zodiac-section">
            <h2><span class="gold-text">{month_num}월 다른 띠 운세</span></h2>
            <div class="other-zodiac-grid">
                {other_zodiac_html}
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>

</body>
</html>"""


# ─── CONTENT GENERATORS ────────────────────────────────────────────────

def select_text(templates, zodiac, month, interaction):
    """Deterministically select a template variant."""
    pool = templates[interaction]
    seed = _seed(zodiac["id"], month["num"])
    idx = seed % len(pool)
    return pool[idx]


def get_element_interaction_desc(zodiac, month, interaction):
    """Generate the element interaction description."""
    z_el = ELEMENT_NAME[zodiac["element"]]
    m_el = ELEMENT_NAME[month["element"]]
    descs = {
        "generated_by": f"이달의 월지 {month['branch']}({m_el})이(가) {zodiac['ko']}의 {z_el}을(를) 생(生)하여 길한 기운이 흐릅니다.",
        "generate": f"{zodiac['ko']}의 {z_el}이(가) 이달의 월지 {month['branch']}({m_el})을(를) 생(生)하여 에너지가 발산됩니다.",
        "same": f"이달의 월지 {month['branch']}({m_el})이(가) {zodiac['ko']}의 {z_el}과(와) 같아 비화(比和)의 기운이 증폭됩니다.",
        "overcome": f"{zodiac['ko']}의 {z_el}이(가) 이달의 월지 {month['branch']}({m_el})을(를) 극(克)하여 주도적 기운이 흐릅니다.",
        "overcome_by": f"이달의 월지 {month['branch']}({m_el})이(가) {zodiac['ko']}의 {z_el}을(를) 극(克)하여 신중함이 요구됩니다.",
        "neutral": f"이달의 월지 {month['branch']}({m_el})과(와) {zodiac['ko']}의 {z_el} 사이에 평온한 기류가 흐릅니다.",
    }
    return descs[interaction]


def get_score_color(score):
    if score >= 85:
        return "#4ADE80"
    elif score >= 70:
        return "#D4AF37"
    elif score >= 55:
        return "#F0D78C"
    else:
        return "#F87171"


def generate_page(zodiac, month):
    """Generate a single monthly fortune page."""
    scores = calc_scores(zodiac, month)
    interaction = scores["interaction"]
    seed = _seed(zodiac["id"], month["num"])

    # Content
    overall_text = select_text(OVERALL_BY_INTERACTION, zodiac, month, interaction).format(
        ko=zodiac["ko"], zodiac_el_name=ELEMENT_NAME[zodiac["element"]],
        month_el_name=ELEMENT_NAME[month["element"]], month_ko=month["ko"],
    )
    money_text = select_text(MONEY_BY_INTERACTION, zodiac, month, interaction)
    love_text = select_text(LOVE_BY_INTERACTION, zodiac, month, interaction)
    health_text = select_text(HEALTH_BY_INTERACTION, zodiac, month, interaction).format(
        organ=zodiac["health_organ"]
    )

    # Season theme
    season_theme = f"{month['season']}인 {month['ko']}은 {month['nature']}입니다. {zodiac['ko']}는 이 시기에 {month['theme']}로서 자신의 {zodiac['trait'].rstrip('다').rstrip('습니')}는 특성을 살려 나아가는 것이 좋습니다."

    # Lucky info
    lucky_day_idx = (seed % len(LUCKY_DAYS))
    lucky_dir_idx = (seed >> 4) % len(LUCKY_DIRECTIONS)

    # Month grid HTML
    month_links = []
    for m in range(1, 13):
        cls = ' class="current"' if m == month["num"] else ""
        month_links.append(f'<a href="/zodiac/{zodiac["id"]}/{m}/"{cls}>{m}월</a>')
    month_grid_html = "\n                ".join(month_links)

    # Other zodiac HTML for same month
    other_links = []
    for z in ZODIACS:
        z_scores = calc_scores(z, month)
        cls = ' current' if z["id"] == zodiac["id"] else ""
        other_links.append(
            f'<a href="/zodiac/{z["id"]}/{month["num"]}/" class="other-zodiac-link{cls}">'
            f'<span class="oz-emoji">{z["emoji"]}</span>'
            f'<span class="oz-name">{z["ko"]}</span>'
            f'<span class="oz-score">{z_scores["total"]}점</span></a>'
        )
    other_zodiac_html = "\n                ".join(other_links)

    # Meta
    title = f"2026년 {month['num']}월 {zodiac['ko']} 운세 | 월별 재물운·연애운·건강운 - 사주명리"
    meta_desc = f"2026년 {month['num']}월 {zodiac['ko']} 운세 총정리. 총운 {scores['total']}점, 재물운 {scores['money']}점, 연애운 {scores['love']}점, 건강운 {scores['health']}점. 오행 {ELEMENT_NAME[zodiac['element']]} 기반 상세 분석."
    meta_kw = f"{zodiac['ko']} {month['num']}월 운세, 2026년 {month['num']}월 {zodiac['ko']}, {zodiac['ko']} 월별운세, {month['num']}월 운세, 띠별 월별 운세, {zodiac['ko']} 재물운, {zodiac['ko']} 연애운"

    html = HTML_TEMPLATE.format(
        title=title,
        meta_description=meta_desc,
        meta_keywords=meta_kw,
        og_title=f"2026년 {month['num']}월 {zodiac['ko']} 운세 | 총운·재물운·연애운·건강운",
        og_description=f"2026년 {month['num']}월 {zodiac['ko']} 운세 상세 분석. 총운 {scores['total']}점.",
        schema_headline=f"2026년 {month['num']}월 {zodiac['ko']} 운세 - 총운·재물운·연애운·건강운 상세 분석",
        today=TODAY,
        animal_id=zodiac["id"],
        month_num=month["num"],
        zodiac_ko=zodiac["ko"],
        emoji=zodiac["emoji"],
        hanja=zodiac["hanja"],
        element_name=ELEMENT_NAME[zodiac["element"]],
        month_branch=month["branch"],
        years=zodiac["years"],
        total_score=scores["total"],
        money_score=scores["money"],
        love_score=scores["love"],
        health_score=scores["health"],
        score_color=get_score_color(scores["total"]),
        element_interaction_desc=get_element_interaction_desc(zodiac, month, interaction),
        overall_text=overall_text,
        season_theme=season_theme,
        money_text=money_text,
        love_text=love_text,
        health_text=health_text,
        seasonal_health=SEASONAL_HEALTH[month["num"]],
        lucky_days=LUCKY_DAYS[lucky_day_idx],
        lucky_direction=LUCKY_DIRECTIONS[lucky_dir_idx],
        lucky_colors=zodiac["lucky_colors"],
        lucky_nums=zodiac["lucky_nums"],
        month_grid_html=month_grid_html,
        other_zodiac_html=other_zodiac_html,
        faq_overall=f"2026년 {month['num']}월 {zodiac['ko']}의 총운은 {scores['total']}점입니다. {overall_text}",
        faq_money=money_text,
        faq_love=love_text,
        faq_health=f"{health_text} {SEASONAL_HEALTH[month['num']]}",
    )

    # Write file
    out_dir = os.path.join(BASE_DIR, "zodiac", zodiac["id"], str(month["num"]))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def generate_sitemap_entries():
    """Generate sitemap XML entries for all monthly pages."""
    entries = []
    for z in ZODIACS:
        for m in MONTHS:
            entries.append(
                f"    <url>\n"
                f"        <loc>https://saju.gon.ai.kr/zodiac/{z['id']}/{m['num']}/</loc>\n"
                f"        <lastmod>{TODAY}</lastmod>\n"
                f"        <changefreq>monthly</changefreq>\n"
                f"        <priority>0.7</priority>\n"
                f"    </url>"
            )
    return "\n".join(entries)


if __name__ == "__main__":
    print("Generating 144 monthly zodiac fortune pages...")
    count = 0
    for zodiac in ZODIACS:
        for month in MONTHS:
            path = generate_page(zodiac, month)
            count += 1
        print(f"  {zodiac['emoji']} {zodiac['ko']}: 12 pages generated")

    print(f"\nTotal: {count} pages generated")
    print(f"\nSitemap entries (copy to sitemap.xml):")
    print(generate_sitemap_entries())
