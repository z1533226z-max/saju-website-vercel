#!/usr/bin/env python3
"""
띠별 궁합 쌍별 페이지 생성기
- 144개 페이지: /compatibility/{sign1}/{sign2}/
- 각 페이지는 sign1의 관점에서 sign2와의 궁합 분석
- FAQPage + Article schema 포함
"""
import os
import json
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
COMPAT_DIR = os.path.join(PUBLIC_DIR, "compatibility")
TODAY = date.today().isoformat()

# ──────────────────────────────────────────
# 12간지 기본 데이터
# ──────────────────────────────────────────
ZODIAC = [
    {"id": "rat",     "ko": "쥐띠",     "emoji": "🐀", "hanja": "子", "element": "수(水)", "element_name": "물", "traits": "지혜롭고 재치 있으며, 사교성이 뛰어남"},
    {"id": "ox",      "ko": "소띠",     "emoji": "🐂", "hanja": "丑", "element": "토(土)", "element_name": "흙", "traits": "성실하고 인내심이 강하며, 책임감이 뛰어남"},
    {"id": "tiger",   "ko": "호랑이띠", "emoji": "🐅", "hanja": "寅", "element": "목(木)", "element_name": "나무", "traits": "용감하고 리더십이 강하며, 자신감이 넘침"},
    {"id": "rabbit",  "ko": "토끼띠",   "emoji": "🐇", "hanja": "卯", "element": "목(木)", "element_name": "나무", "traits": "온화하고 예술적 감각이 뛰어나며, 배려심이 깊음"},
    {"id": "dragon",  "ko": "용띠",     "emoji": "🐉", "hanja": "辰", "element": "토(土)", "element_name": "흙", "traits": "카리스마 있고 야심차며, 창의력이 풍부함"},
    {"id": "snake",   "ko": "뱀띠",     "emoji": "🐍", "hanja": "巳", "element": "화(火)", "element_name": "불", "traits": "신중하고 직관력이 뛰어나며, 분석력이 강함"},
    {"id": "horse",   "ko": "말띠",     "emoji": "🐴", "hanja": "午", "element": "화(火)", "element_name": "불", "traits": "활동적이고 자유로우며, 열정적이고 사교적임"},
    {"id": "goat",    "ko": "양띠",     "emoji": "🐑", "hanja": "未", "element": "토(土)", "element_name": "흙", "traits": "온순하고 예술적이며, 상상력이 풍부함"},
    {"id": "monkey",  "ko": "원숭이띠", "emoji": "🐒", "hanja": "申", "element": "금(金)", "element_name": "쇠", "traits": "영리하고 다재다능하며, 적응력이 뛰어남"},
    {"id": "rooster", "ko": "닭띠",     "emoji": "🐓", "hanja": "酉", "element": "금(金)", "element_name": "쇠", "traits": "근면하고 관찰력이 뛰어나며, 솔직함"},
    {"id": "dog",     "ko": "개띠",     "emoji": "🐕", "hanja": "戌", "element": "토(土)", "element_name": "흙", "traits": "충실하고 정의로우며, 의리가 강함"},
    {"id": "pig",     "ko": "돼지띠",   "emoji": "🐷", "hanja": "亥", "element": "수(水)", "element_name": "물", "traits": "너그럽고 솔직하며, 낙천적이고 관대함"},
]

ZODIAC_MAP = {z["id"]: z for z in ZODIAC}

# 삼합
SAMHAP = [
    {"signs": {"rat", "dragon", "monkey"}, "name": "수(水)국 삼합"},
    {"signs": {"ox", "snake", "rooster"}, "name": "금(金)국 삼합"},
    {"signs": {"tiger", "horse", "dog"}, "name": "화(火)국 삼합"},
    {"signs": {"rabbit", "goat", "pig"}, "name": "목(木)국 삼합"},
]

# 육합
YUKHAP = {
    frozenset({"rat", "ox"}): "자축(子丑) 합토",
    frozenset({"tiger", "pig"}): "인해(寅亥) 합목",
    frozenset({"rabbit", "dog"}): "묘술(卯戌) 합화",
    frozenset({"dragon", "rooster"}): "진유(辰酉) 합금",
    frozenset({"snake", "monkey"}): "사신(巳申) 합수",
    frozenset({"horse", "goat"}): "오미(午未) 합화",
}

# 상충
SANGCHUNG = {
    frozenset({"rat", "horse"}): "자오충(子午沖)",
    frozenset({"ox", "goat"}): "축미충(丑未沖)",
    frozenset({"tiger", "monkey"}): "인신충(寅申沖)",
    frozenset({"rabbit", "rooster"}): "묘유충(卯酉沖)",
    frozenset({"dragon", "dog"}): "진술충(辰戌沖)",
    frozenset({"snake", "pig"}): "사해충(巳亥沖)",
}

# 상해
SANGHAE = {
    frozenset({"rat", "goat"}): "자미해(子未害)",
    frozenset({"ox", "horse"}): "축오해(丑午害)",
    frozenset({"tiger", "snake"}): "인사해(寅巳害)",
    frozenset({"rabbit", "dragon"}): "묘진해(卯辰害)",
    frozenset({"monkey", "pig"}): "신해해(申亥害)",
    frozenset({"rooster", "dog"}): "유술해(酉戌害)",
}

# 오행 상생상극
ELEMENT_RELATION = {
    ("수", "목"): ("상생", "물이 나무를 키워줍니다"),
    ("목", "화"): ("상생", "나무가 불을 피웁니다"),
    ("화", "토"): ("상생", "불이 재가 되어 흙을 만듭니다"),
    ("토", "금"): ("상생", "흙에서 금속이 나옵니다"),
    ("금", "수"): ("상생", "금속 표면에 물이 맺힙니다"),
    ("수", "화"): ("상극", "물이 불을 끕니다"),
    ("화", "금"): ("상극", "불이 금속을 녹입니다"),
    ("금", "목"): ("상극", "쇠가 나무를 벱니다"),
    ("목", "토"): ("상극", "나무가 흙의 양분을 빼앗습니다"),
    ("토", "수"): ("상극", "흙이 물을 막습니다"),
}

# 쌍별 구체적 조언
PAIR_ADVICE = {
    "육합": {
        "love": "서로에게 본능적으로 끌리는 최고의 궁합입니다. 자연스럽게 서로의 부족함을 채워주며, 결혼 궁합으로도 매우 좋습니다.",
        "work": "업무에서 환상의 호흡을 보여줍니다. 서로 다른 강점이 시너지를 만들어 큰 성과를 낼 수 있습니다.",
        "friend": "오래 갈 수 있는 우정입니다. 서로를 깊이 이해하며, 어려울 때 든든한 버팀목이 됩니다.",
        "tip": "이미 좋은 관계이지만, 서로를 당연하게 여기지 않도록 감사를 표현하면 더 깊어집니다.",
    },
    "삼합": {
        "love": "강한 끌림이 있는 궁합입니다. 서로의 매력에 빠지기 쉽고, 함께 있으면 에너지가 상승합니다.",
        "work": "같은 목표를 향해 달릴 때 큰 힘을 발휘합니다. 프로젝트 파트너로 최적입니다.",
        "friend": "마음이 통하는 친구가 될 수 있습니다. 취미나 관심사가 비슷해 즐거운 시간을 보냅니다.",
        "tip": "서로의 장점을 인정하고, 때로는 양보하는 자세가 관계를 더욱 단단하게 합니다.",
    },
    "상충": {
        "love": "강한 끌림과 갈등이 공존합니다. 처음에는 매력적이지만, 깊어질수록 가치관 차이가 드러날 수 있습니다.",
        "work": "서로 다른 시각이 오히려 창의적 결과를 만들 수 있습니다. 다만 의견 충돌 시 감정적이 되지 않도록 주의가 필요합니다.",
        "friend": "서로를 자극하는 관계입니다. 적당한 거리를 유지하면서 서로의 다름을 존중하면 좋은 관계를 유지할 수 있습니다.",
        "tip": "상충 관계는 '나쁜 관계'가 아니라 '성장의 관계'입니다. 서로의 차이를 배움의 기회로 삼으세요.",
    },
    "상해": {
        "love": "겉으로는 잘 맞는 것 같지만, 깊어질수록 미묘한 갈등이 생길 수 있습니다. 솔직한 대화가 중요합니다.",
        "work": "표면적으로는 협력적이지만, 속으로 불만이 쌓일 수 있습니다. 정기적으로 피드백을 주고받으세요.",
        "friend": "가까워졌다 멀어지기를 반복할 수 있습니다. 적절한 거리감을 유지하면 오래 갈 수 있는 관계입니다.",
        "tip": "서로의 감정을 숨기지 말고 표현하세요. 작은 불만이 쌓이면 큰 갈등이 됩니다.",
    },
    "동띠": {
        "love": "서로를 잘 이해하지만, 비슷한 단점도 공유합니다. 서로의 약점을 보완해주는 노력이 필요합니다.",
        "work": "같은 방식으로 일하기 때문에 효율적이지만, 새로운 아이디어가 부족할 수 있습니다.",
        "friend": "동질감이 높아 편안한 관계입니다. 하지만 때로는 서로를 과소평가할 수 있으니 주의하세요.",
        "tip": "같은 띠라도 사주팔자에 따라 궁합이 크게 달라집니다. 정확한 분석은 생년월일시로 확인하세요.",
    },
    "보통": {
        "love": "특별히 좋거나 나쁘지 않은 궁합입니다. 서로의 노력에 따라 좋은 관계로 발전할 수 있습니다.",
        "work": "무난하게 협력할 수 있습니다. 서로의 강점을 파악하고 역할을 잘 나누면 효과적입니다.",
        "friend": "편안한 관계를 유지할 수 있습니다. 공통 관심사를 찾으면 더 가까워질 수 있습니다.",
        "tip": "보통 궁합은 노력의 여지가 가장 큰 관계입니다. 서로에 대한 관심과 배려가 관계의 질을 결정합니다.",
    },
}

# 출생 연도 목록
BIRTH_YEARS = {
    "rat":     [1948, 1960, 1972, 1984, 1996, 2008, 2020],
    "ox":      [1949, 1961, 1973, 1985, 1997, 2009, 2021],
    "tiger":   [1950, 1962, 1974, 1986, 1998, 2010, 2022],
    "rabbit":  [1951, 1963, 1975, 1987, 1999, 2011, 2023],
    "dragon":  [1952, 1964, 1976, 1988, 2000, 2012, 2024],
    "snake":   [1953, 1965, 1977, 1989, 2001, 2013, 2025],
    "horse":   [1954, 1966, 1978, 1990, 2002, 2014, 2026],
    "goat":    [1955, 1967, 1979, 1991, 2003, 2015],
    "monkey":  [1956, 1968, 1980, 1992, 2004, 2016],
    "rooster": [1957, 1969, 1981, 1993, 2005, 2017],
    "dog":     [1958, 1970, 1982, 1994, 2006, 2018],
    "pig":     [1959, 1971, 1983, 1995, 2007, 2019],
}


def get_compatibility(sign1_id, sign2_id):
    """두 띠 사이의 궁합 점수와 관계를 반환"""
    if sign1_id == sign2_id:
        return {"score": 70, "type": "동띠", "label": "동질감", "desc": "같은 띠끼리는 서로를 잘 이해하지만, 비슷한 단점도 공유할 수 있습니다."}

    pair = frozenset({sign1_id, sign2_id})

    if pair in YUKHAP:
        return {"score": 95, "type": "육합", "label": "천생연분", "desc": f"{YUKHAP[pair]} — 음양이 자연스럽게 조화를 이루는 최고의 궁합입니다."}

    for sh in SAMHAP:
        if sign1_id in sh["signs"] and sign2_id in sh["signs"]:
            return {"score": 92, "type": "삼합", "label": "최고궁합", "desc": f"{sh['name']} — 세 띠가 하나의 오행으로 모이는 강력한 조합입니다."}

    if pair in SANGCHUNG:
        return {"score": 35, "type": "상충", "label": "상극관계", "desc": f"{SANGCHUNG[pair]} — 정반대 위치의 띠로, 성격과 가치관 차이가 큽니다."}

    if pair in SANGHAE:
        return {"score": 45, "type": "상해", "label": "주의필요", "desc": f"{SANGHAE[pair]} — 겉으로는 괜찮아 보이지만, 깊어질수록 갈등이 생기기 쉽습니다."}

    neutral_scores = {
        frozenset({"rat", "tiger"}): 65, frozenset({"rat", "rabbit"}): 55,
        frozenset({"rat", "snake"}): 60, frozenset({"rat", "rooster"}): 58,
        frozenset({"rat", "dog"}): 68, frozenset({"rat", "pig"}): 72,
        frozenset({"ox", "tiger"}): 55, frozenset({"ox", "rabbit"}): 62,
        frozenset({"ox", "dragon"}): 65, frozenset({"ox", "monkey"}): 68,
        frozenset({"ox", "pig"}): 65, frozenset({"ox", "dog"}): 50,
        frozenset({"tiger", "rabbit"}): 68, frozenset({"tiger", "dragon"}): 72,
        frozenset({"tiger", "snake"}): 48, frozenset({"tiger", "goat"}): 62,
        frozenset({"tiger", "rooster"}): 55,
        frozenset({"rabbit", "snake"}): 60, frozenset({"rabbit", "horse"}): 62,
        frozenset({"rabbit", "monkey"}): 58,
        frozenset({"dragon", "snake"}): 68, frozenset({"dragon", "horse"}): 65,
        frozenset({"dragon", "goat"}): 60, frozenset({"dragon", "pig"}): 62,
        frozenset({"snake", "horse"}): 65, frozenset({"snake", "goat"}): 60,
        frozenset({"snake", "dog"}): 58,
        frozenset({"horse", "monkey"}): 60, frozenset({"horse", "rooster"}): 55,
        frozenset({"horse", "pig"}): 62,
        frozenset({"goat", "monkey"}): 58, frozenset({"goat", "rooster"}): 55,
        frozenset({"goat", "dog"}): 50,
        frozenset({"monkey", "rooster"}): 62, frozenset({"monkey", "dog"}): 65,
        frozenset({"rooster", "pig"}): 58, frozenset({"dog", "pig"}): 68,
    }

    score = neutral_scores.get(pair, 62)
    if score >= 68:
        return {"score": score, "type": "보통", "label": "좋은관계", "desc": "서로 다른 장점을 가지고 있어 보완적인 관계를 형성할 수 있습니다."}
    elif score >= 55:
        return {"score": score, "type": "보통", "label": "무난한관계", "desc": "특별히 좋거나 나쁘지 않은 평범한 궁합입니다."}
    else:
        return {"score": score, "type": "보통", "label": "노력필요", "desc": "성격이나 가치관에 차이가 있을 수 있습니다."}


def score_color(score):
    if score >= 90: return "#4ADE80"
    if score >= 70: return "#D4AF37"
    if score >= 55: return "#F59E0B"
    return "#F87171"


def score_emoji(score):
    if score >= 90: return "💕"
    if score >= 70: return "😊"
    if score >= 55: return "🤝"
    if score >= 45: return "⚠️"
    return "💔"


def get_element_relation(s1, s2):
    """두 띠의 오행 관계 분석"""
    e1 = s1["element"][0]  # 수, 목, 화, 토, 금
    e2 = s2["element"][0]
    if e1 == e2:
        return ("비화", f"같은 {s1['element']} 오행으로, 동질감이 강합니다")
    rel = ELEMENT_RELATION.get((e1, e2))
    if rel:
        return rel
    rel = ELEMENT_RELATION.get((e2, e1))
    if rel:
        return (rel[0], rel[1])
    return ("보통", "특별한 오행 관계 없이 무난합니다")


def get_third_harmony(sign1_id, sign2_id):
    """삼합의 세 번째 띠 찾기"""
    for sh in SAMHAP:
        if sign1_id in sh["signs"] and sign2_id in sh["signs"]:
            third = [s for s in sh["signs"] if s != sign1_id and s != sign2_id][0]
            return ZODIAC_MAP[third], sh["name"]
    return None, None


COMMON_HEAD = """    <!-- Naver Search Advisor -->
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/compatibility.css">

    <!-- Google AdSense Script -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290"
         crossorigin="anonymous"></script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BNRL6FRMMM');
    </script>"""

HEADER_HTML = """    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">사주명리</span>
                </h1>
            </a>
            <nav class="nav-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/compatibility/" class="active">띠별 궁합</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/guide/">사주 가이드</a>
            </nav>
        </nav>
    </header>"""

FOOTER_HTML = """    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/compatibility/">띠별 궁합</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/guide/">사주 가이드</a>
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>"""


def generate_pair_page(sign1_id, sign2_id):
    """sign1의 관점에서 sign2와의 궁합 페이지 생성"""
    s1 = ZODIAC_MAP[sign1_id]
    s2 = ZODIAC_MAP[sign2_id]
    compat = get_compatibility(sign1_id, sign2_id)
    rel_type = compat["type"]
    advice = PAIR_ADVICE.get(rel_type, PAIR_ADVICE["보통"])
    elem_rel = get_element_relation(s1, s2)
    sc = score_color(compat["score"])
    se = score_emoji(compat["score"])

    # 출생 연도
    years1 = ", ".join(str(y) + "년" for y in BIRTH_YEARS[sign1_id][-5:])
    years2 = ", ".join(str(y) + "년" for y in BIRTH_YEARS[sign2_id][-5:])

    # 다른 띠 궁합 비교 (sign1 기준 상위 3개)
    all_compat = []
    for z in ZODIAC:
        if z["id"] == sign1_id:
            continue
        c = get_compatibility(sign1_id, z["id"])
        all_compat.append({"id": z["id"], "ko": z["ko"], "emoji": z["emoji"], "score": c["score"], "label": c["label"]})
    all_compat.sort(key=lambda x: x["score"], reverse=True)

    # 삼합 세 번째 띠
    third, samhap_name = get_third_harmony(sign1_id, sign2_id)

    # 제목과 설명
    title = f"{s1['ko']} {s2['ko']} 궁합 {compat['score']}점 | {compat['label']} - 사주명리"
    desc = f"2026년 {s1['ko']}({s1['hanja']})와 {s2['ko']}({s2['hanja']}) 궁합 {compat['score']}점! {compat['label']}. 연애·결혼·직장 궁합 상세 분석. {s1['element']}과 {s2['element']}의 오행 관계, 삼합·육합·상충 해석."

    # Schema
    article_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{s1['ko']} {s2['ko']} 궁합 - {compat['score']}점 {compat['label']}",
        "description": desc[:160],
        "url": f"https://saju.gon.ai.kr/compatibility/{sign1_id}/{sign2_id}/",
        "datePublished": "2026-01-01",
        "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "사주명리", "url": "https://saju.gon.ai.kr/"},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://saju.gon.ai.kr/"},
                {"@type": "ListItem", "position": 2, "name": "띠별 궁합", "item": "https://saju.gon.ai.kr/compatibility/"},
                {"@type": "ListItem", "position": 3, "name": f"{s1['ko']} 궁합", "item": f"https://saju.gon.ai.kr/compatibility/{sign1_id}/"},
                {"@type": "ListItem", "position": 4, "name": f"{s1['ko']} {s2['ko']} 궁합", "item": f"https://saju.gon.ai.kr/compatibility/{sign1_id}/{sign2_id}/"},
            ]
        }
    }, ensure_ascii=False, indent=4)

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{s1['ko']}와 {s2['ko']}는 궁합이 좋은가요?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{s1['ko']}({s1['hanja']})와 {s2['ko']}({s2['hanja']})의 궁합 점수는 {compat['score']}점으로 '{compat['label']}' 관계입니다. {compat['desc']}"
                }
            },
            {
                "@type": "Question",
                "name": f"{s1['ko']} {s2['ko']} 연애 궁합은?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": advice["love"]
                }
            },
            {
                "@type": "Question",
                "name": f"{s1['ko']}와 {s2['ko']}의 오행 관계는?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{s1['ko']}는 {s1['element']}, {s2['ko']}는 {s2['element']}으로, {elem_rel[0]} 관계입니다. {elem_rel[1]}."
                }
            },
            {
                "@type": "Question",
                "name": f"{s1['ko']}와 {s2['ko']} 궁합을 좋게 하려면?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": advice["tip"]
                }
            },
        ]
    }, ensure_ascii=False, indent=4)

    # 다른 띠 궁합 카드 (sign1 기준, 현재 sign2 강조)
    other_pairs_html = ""
    for ac in all_compat:
        is_current = ' style="border: 2px solid gold; transform: scale(1.02);"' if ac["id"] == sign2_id else ""
        asc = score_color(ac["score"])
        other_pairs_html += f"""                <a href="/compatibility/{sign1_id}/{ac['id']}/" class="pair-mini-card"{is_current}>
                    <span class="pair-mini-emoji">{ac['emoji']}</span>
                    <span class="pair-mini-name">{ac['ko']}</span>
                    <span class="pair-mini-score" style="color: {asc};">{ac['score']}점</span>
                </a>
"""

    # 삼합 추가 정보
    samhap_section = ""
    if third:
        samhap_section = f"""
        <section class="pair-samhap-section">
            <h2>🔺 삼합 보너스</h2>
            <p>{s1['ko']}와 {s2['ko']}는 <strong>{samhap_name}</strong> 관계입니다.</p>
            <p>여기에 {third['emoji']} <strong>{third['ko']}</strong>가 합류하면 삼합이 완성되어 더욱 강력한 시너지를 냅니다.</p>
            <a href="/compatibility/{sign1_id}/{third['id']}/" class="samhap-link">{s1['ko']} + {third['ko']} 궁합 보기 →</a>
        </section>"""

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{desc[:160]}">
    <meta name="keywords" content="{s1['ko']} {s2['ko']} 궁합, {s1['ko']}{s2['ko']}궁합, {s1['ko']}궁합, {s2['ko']}궁합, 띠별궁합, 12간지궁합, 2026년궁합">
    <title>{title}</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/compatibility/{sign1_id}/{sign2_id}/">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{s1['ko']} {s2['ko']} 궁합 {compat['score']}점 | {compat['label']}">
    <meta property="og:description" content="{desc[:100]}">
    <meta property="og:url" content="https://saju.gon.ai.kr/compatibility/{sign1_id}/{sign2_id}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{s1['ko']} + {s2['ko']} 궁합 {compat['score']}점">
    <meta name="twitter:description" content="{desc[:100]}">

{COMMON_HEAD}

    <!-- Schema.org -->
    <script type="application/ld+json">
{article_json}
    </script>
    <script type="application/ld+json">
{faq_json}
    </script>
</head>
<body>

{HEADER_HTML}

    <main class="compat-pair-page">
        <a href="/compatibility/{sign1_id}/" class="back-link">&larr; {s1['ko']} 전체 궁합 보기</a>

        <!-- Hero: 두 띠 궁합 -->
        <section class="pair-hero">
            <div class="pair-hero-signs">
                <div class="pair-sign">
                    <span class="pair-emoji">{s1['emoji']}</span>
                    <span class="pair-hanja">{s1['hanja']}({s1['element']})</span>
                    <span class="pair-name">{s1['ko']}</span>
                </div>
                <div class="pair-score-circle" style="border-color: {sc};">
                    <span class="pair-score-num" style="color: {sc};">{compat['score']}</span>
                    <span class="pair-score-unit">점</span>
                </div>
                <div class="pair-sign">
                    <span class="pair-emoji">{s2['emoji']}</span>
                    <span class="pair-hanja">{s2['hanja']}({s2['element']})</span>
                    <span class="pair-name">{s2['ko']}</span>
                </div>
            </div>
            <div class="pair-label" style="color: {sc};">{se} {compat['label']}</div>
            <h1 class="pair-title"><span class="gold-text">{s1['ko']} + {s2['ko']} 궁합</span></h1>
            <p class="pair-subtitle">{compat['desc']}</p>
        </section>

        <!-- 관계 유형 -->
        <section class="pair-type-section">
            <h2>📋 관계 유형: {rel_type}</h2>
            <div class="pair-type-badge" style="background: {sc}20; border: 1px solid {sc}; color: {sc};">
                {rel_type} · {compat['label']} · {compat['score']}점
            </div>
        </section>

        <!-- 오행 분석 -->
        <section class="pair-element-section">
            <h2>🔥 오행(五行) 분석</h2>
            <div class="element-analysis">
                <div class="element-item">
                    <span class="element-label">{s1['ko']}</span>
                    <span class="element-value">{s1['element']}</span>
                    <span class="element-trait">{s1['traits']}</span>
                </div>
                <div class="element-relation">
                    <span class="element-rel-type">{elem_rel[0]}</span>
                    <span class="element-rel-desc">{elem_rel[1]}</span>
                </div>
                <div class="element-item">
                    <span class="element-label">{s2['ko']}</span>
                    <span class="element-value">{s2['element']}</span>
                    <span class="element-trait">{s2['traits']}</span>
                </div>
            </div>
        </section>

        <!-- 상세 궁합 분석 -->
        <section class="pair-detail-section">
            <h2>💑 연애 · 결혼 궁합</h2>
            <p>{advice['love']}</p>
        </section>

        <section class="pair-detail-section">
            <h2>💼 직장 · 사업 궁합</h2>
            <p>{advice['work']}</p>
        </section>

        <section class="pair-detail-section">
            <h2>🤝 우정 · 친구 궁합</h2>
            <p>{advice['friend']}</p>
        </section>

        <!-- 궁합 팁 -->
        <section class="pair-tip-section">
            <h2>💡 궁합 개선 팁</h2>
            <div class="pair-tip-box">
                <p>{advice['tip']}</p>
            </div>
        </section>
{samhap_section}
        <!-- 출생 연도 -->
        <section class="pair-years-section">
            <h2>📅 해당 띠 출생 연도</h2>
            <div class="years-grid">
                <div class="years-item">
                    <h3>{s1['emoji']} {s1['ko']}</h3>
                    <p>{years1}</p>
                </div>
                <div class="years-item">
                    <h3>{s2['emoji']} {s2['ko']}</h3>
                    <p>{years2}</p>
                </div>
            </div>
        </section>

        <!-- 반대 방향 링크 -->
        <section class="pair-reverse-section">
            <a href="/compatibility/{sign2_id}/{sign1_id}/" class="reverse-link">
                {s2['emoji']} {s2['ko']}의 관점에서 본 {s1['ko']} 궁합 →
            </a>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">더 정확한 궁합이 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 궁합 분석을 받을 수 있습니다.</p>
            <a href="/" class="cta-btn">무료 사주 궁합 바로가기</a>
        </section>

        <!-- 다른 띠와의 궁합 -->
        <section class="pair-others-section">
            <h2>{s1['emoji']} {s1['ko']}의 다른 궁합</h2>
            <div class="pair-others-grid">
{other_pairs_html}            </div>
        </section>

        <!-- 관련 페이지 -->
        <section class="related-links-section">
            <a href="/compatibility/{sign1_id}/" class="related-link">📊 {s1['ko']} 전체 궁합표</a>
            <a href="/compatibility/{sign2_id}/" class="related-link">📊 {s2['ko']} 전체 궁합표</a>
            <a href="/zodiac/{sign1_id}/" class="related-link">🔮 {s1['ko']} 2026년 운세</a>
            <a href="/zodiac/{sign2_id}/" class="related-link">🔮 {s2['ko']} 2026년 운세</a>
        </section>
    </main>

{FOOTER_HTML}

</body>
</html>"""

    return html


def update_sitemap():
    """사이트맵에 144개 쌍별 URL 추가"""
    sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_urls = ""
    count = 0
    for s1 in ZODIAC:
        for s2 in ZODIAC:
            if s1["id"] == s2["id"]:
                continue
            url = f"https://saju.gon.ai.kr/compatibility/{s1['id']}/{s2['id']}/"
            if url in content:
                continue
            new_urls += f"""    <url>
        <loc>{url}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""
            count += 1

    if count > 0:
        content = content.replace("</urlset>", new_urls + "</urlset>")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"  Sitemap updated: +{count} URLs")
    return count


def update_hub_pages():
    """기존 허브 페이지의 궁합 카드 링크를 쌍별 페이지로 변경"""
    count = 0
    for s1 in ZODIAC:
        hub_path = os.path.join(COMPAT_DIR, s1["id"], "index.html")
        if not os.path.exists(hub_path):
            continue
        with open(hub_path, "r", encoding="utf-8") as f:
            content = f.read()

        modified = False
        for s2 in ZODIAC:
            if s1["id"] == s2["id"]:
                continue
            # 카드 링크: /compatibility/ox/ → /compatibility/rat/ox/
            old_link = f'href="/compatibility/{s2["id"]}/" class="compat-card-link"'
            new_link = f'href="/compatibility/{s1["id"]}/{s2["id"]}/" class="compat-card-link"'
            if old_link in content:
                content = content.replace(old_link, new_link)
                modified = True

        if modified:
            with open(hub_path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print(f"  Updated hub: /compatibility/{s1['id']}/index.html")
    return count


def main():
    print("=== 띠별 궁합 쌍별 페이지 생성 시작 ===\n")

    # 1. 144개 쌍별 페이지 생성 (12 x 12 - 12 동띠 = 132 + 12 동띠 = 144)
    # 동띠도 포함 (자기 자신과의 궁합)
    page_count = 0
    for s1 in ZODIAC:
        for s2 in ZODIAC:
            if s1["id"] == s2["id"]:
                continue  # 동띠 페이지는 제외 (허브 페이지가 이미 있음)
            pair_dir = os.path.join(COMPAT_DIR, s1["id"], s2["id"])
            os.makedirs(pair_dir, exist_ok=True)
            pair_path = os.path.join(pair_dir, "index.html")
            with open(pair_path, "w", encoding="utf-8") as f:
                f.write(generate_pair_page(s1["id"], s2["id"]))
            page_count += 1

    print(f"  Created: {page_count} pair pages")

    # 2. 허브 페이지 업데이트 (카드 링크 변경)
    hub_count = update_hub_pages()
    print(f"  Updated: {hub_count} hub pages")

    # 3. 사이트맵 업데이트
    sitemap_count = update_sitemap()

    print(f"\n=== 완료: {page_count}개 쌍별 페이지 생성, {hub_count}개 허브 업데이트, 사이트맵 +{sitemap_count} URLs ===")


if __name__ == "__main__":
    main()
