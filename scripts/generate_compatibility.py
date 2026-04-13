#!/usr/bin/env python3
"""
띠별 궁합 페이지 생성기
- 1개 갤러리 페이지: /compatibility/
- 12개 허브 페이지: /compatibility/{sign}/
총 13개 신규 SEO 페이지 생성
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
    {"id": "rat",     "ko": "쥐띠",     "emoji": "🐀", "hanja": "子", "element": "수(水)", "element_color": "#60A5FA"},
    {"id": "ox",      "ko": "소띠",     "emoji": "🐂", "hanja": "丑", "element": "토(土)", "element_color": "#D4AF37"},
    {"id": "tiger",   "ko": "호랑이띠", "emoji": "🐅", "hanja": "寅", "element": "목(木)", "element_color": "#4ADE80"},
    {"id": "rabbit",  "ko": "토끼띠",   "emoji": "🐇", "hanja": "卯", "element": "목(木)", "element_color": "#4ADE80"},
    {"id": "dragon",  "ko": "용띠",     "emoji": "🐉", "hanja": "辰", "element": "토(土)", "element_color": "#D4AF37"},
    {"id": "snake",   "ko": "뱀띠",     "emoji": "🐍", "hanja": "巳", "element": "화(火)", "element_color": "#F87171"},
    {"id": "horse",   "ko": "말띠",     "emoji": "🐴", "hanja": "午", "element": "화(火)", "element_color": "#F87171"},
    {"id": "goat",    "ko": "양띠",     "emoji": "🐑", "hanja": "未", "element": "토(土)", "element_color": "#D4AF37"},
    {"id": "monkey",  "ko": "원숭이띠", "emoji": "🐒", "hanja": "申", "element": "금(金)", "element_color": "#E2E8F0"},
    {"id": "rooster", "ko": "닭띠",     "emoji": "🐓", "hanja": "酉", "element": "금(金)", "element_color": "#E2E8F0"},
    {"id": "dog",     "ko": "개띠",     "emoji": "🐕", "hanja": "戌", "element": "토(土)", "element_color": "#D4AF37"},
    {"id": "pig",     "ko": "돼지띠",   "emoji": "🐷", "hanja": "亥", "element": "수(水)", "element_color": "#60A5FA"},
]

ZODIAC_MAP = {z["id"]: z for z in ZODIAC}

# ──────────────────────────────────────────
# 궁합 관계 데이터 (전통 명리학 기반)
# ──────────────────────────────────────────
# 삼합 (Three Harmonies) - 최고 궁합
SAMHAP = [
    {"signs": {"rat", "dragon", "monkey"}, "name": "수(水)국 삼합"},
    {"signs": {"ox", "snake", "rooster"}, "name": "금(金)국 삼합"},
    {"signs": {"tiger", "horse", "dog"}, "name": "화(火)국 삼합"},
    {"signs": {"rabbit", "goat", "pig"}, "name": "목(木)국 삼합"},
]

# 육합 (Six Harmonies) - 천생연분
YUKHAP = {
    frozenset({"rat", "ox"}): "자축(子丑) 합토",
    frozenset({"tiger", "pig"}): "인해(寅亥) 합목",
    frozenset({"rabbit", "dog"}): "묘술(卯戌) 합화",
    frozenset({"dragon", "rooster"}): "진유(辰酉) 합금",
    frozenset({"snake", "monkey"}): "사신(巳申) 합수",
    frozenset({"horse", "goat"}): "오미(午未) 합화",
}

# 상충 (Clash) - 상극
SANGCHUNG = {
    frozenset({"rat", "horse"}): "자오충(子午沖)",
    frozenset({"ox", "goat"}): "축미충(丑未沖)",
    frozenset({"tiger", "monkey"}): "인신충(寅申沖)",
    frozenset({"rabbit", "rooster"}): "묘유충(卯酉沖)",
    frozenset({"dragon", "dog"}): "진술충(辰戌沖)",
    frozenset({"snake", "pig"}): "사해충(巳亥沖)",
}

# 상해 (Harm)
SANGHAE = {
    frozenset({"rat", "goat"}): "자미해(子未害)",
    frozenset({"ox", "horse"}): "축오해(丑午害)",
    frozenset({"tiger", "snake"}): "인사해(寅巳害)",
    frozenset({"rabbit", "dragon"}): "묘진해(卯辰害)",
    frozenset({"monkey", "pig"}): "신해해(申亥害)",
    frozenset({"rooster", "dog"}): "유술해(酉戌害)",
}


def get_compatibility(sign1_id, sign2_id):
    """두 띠 사이의 궁합 점수와 관계를 반환"""
    if sign1_id == sign2_id:
        return {"score": 70, "type": "동띠", "label": "동질감", "desc": "같은 띠끼리는 서로를 잘 이해하지만, 비슷한 단점도 공유할 수 있습니다. 서로의 장점을 살려주는 관계가 되면 좋은 파트너가 됩니다."}

    pair = frozenset({sign1_id, sign2_id})

    # 육합 체크 (최우선)
    if pair in YUKHAP:
        return {"score": 95, "type": "육합", "label": "천생연분", "desc": f"{YUKHAP[pair]} — 음양이 자연스럽게 조화를 이루는 최고의 궁합입니다. 서로의 부족함을 채워주며, 함께 있으면 안정감과 행복을 느낍니다."}

    # 삼합 체크
    for sh in SAMHAP:
        if sign1_id in sh["signs"] and sign2_id in sh["signs"]:
            return {"score": 92, "type": "삼합", "label": "최고궁합", "desc": f"{sh['name']} — 세 띠가 하나의 오행으로 모이는 강력한 조합입니다. 서로 끌리는 매력이 있고, 협력하면 큰 시너지를 냅니다."}

    # 상충 체크
    if pair in SANGCHUNG:
        return {"score": 35, "type": "상충", "label": "상극관계", "desc": f"{SANGCHUNG[pair]} — 정반대 위치의 띠로, 성격과 가치관 차이가 큽니다. 서로를 이해하려는 노력이 필요하며, 갈등을 성장의 기회로 삼을 수 있습니다."}

    # 상해 체크
    if pair in SANGHAE:
        return {"score": 45, "type": "상해", "label": "주의필요", "desc": f"{SANGHAE[pair]} — 겉으로는 괜찮아 보이지만, 깊어질수록 상처를 주고받기 쉬운 관계입니다. 배려와 거리 조절이 중요합니다."}

    # 보통 관계 (디테일한 점수 차등)
    neutral_scores = {
        frozenset({"rat", "tiger"}): 65,
        frozenset({"rat", "rabbit"}): 55,
        frozenset({"rat", "snake"}): 60,
        frozenset({"rat", "rooster"}): 58,
        frozenset({"rat", "dog"}): 68,
        frozenset({"rat", "pig"}): 72,
        frozenset({"ox", "tiger"}): 55,
        frozenset({"ox", "rabbit"}): 62,
        frozenset({"ox", "dragon"}): 65,
        frozenset({"ox", "monkey"}): 68,
        frozenset({"ox", "pig"}): 65,
        frozenset({"ox", "dog"}): 50,
        frozenset({"tiger", "rabbit"}): 68,
        frozenset({"tiger", "dragon"}): 72,
        frozenset({"tiger", "snake"}): 48,
        frozenset({"tiger", "goat"}): 62,
        frozenset({"tiger", "rooster"}): 55,
        frozenset({"rabbit", "snake"}): 60,
        frozenset({"rabbit", "horse"}): 62,
        frozenset({"rabbit", "monkey"}): 58,
        frozenset({"rabbit", "pig"}): 92,  # 삼합 처리됨
        frozenset({"dragon", "snake"}): 68,
        frozenset({"dragon", "horse"}): 65,
        frozenset({"dragon", "goat"}): 60,
        frozenset({"dragon", "pig"}): 62,
        frozenset({"snake", "horse"}): 65,
        frozenset({"snake", "goat"}): 60,
        frozenset({"snake", "dog"}): 58,
        frozenset({"horse", "monkey"}): 60,
        frozenset({"horse", "rooster"}): 55,
        frozenset({"horse", "pig"}): 62,
        frozenset({"goat", "monkey"}): 58,
        frozenset({"goat", "rooster"}): 55,
        frozenset({"goat", "dog"}): 50,
        frozenset({"monkey", "rooster"}): 62,
        frozenset({"monkey", "dog"}): 65,
        frozenset({"rooster", "pig"}): 58,
        frozenset({"dog", "pig"}): 68,
    }

    score = neutral_scores.get(pair, 62)
    if score >= 68:
        return {"score": score, "type": "보통", "label": "좋은관계", "desc": "서로 다른 장점을 가지고 있어 보완적인 관계를 형성할 수 있습니다. 기본적인 호감이 있으며, 노력하면 더 좋은 관계로 발전합니다."}
    elif score >= 55:
        return {"score": score, "type": "보통", "label": "무난한관계", "desc": "특별히 좋거나 나쁘지 않은 평범한 궁합입니다. 서로에 대한 이해와 존중이 관계의 질을 결정합니다."}
    else:
        return {"score": score, "type": "보통", "label": "노력필요", "desc": "성격이나 가치관에 차이가 있을 수 있습니다. 서로를 이해하려는 적극적인 노력이 관계를 개선하는 열쇠입니다."}


def score_color(score):
    if score >= 90: return "#4ADE80"
    if score >= 70: return "#D4AF37"
    if score >= 55: return "#F59E0B"
    return "#F87171"


def score_bg(score):
    if score >= 90: return "rgba(74,222,128,0.12)"
    if score >= 70: return "rgba(212,175,55,0.12)"
    if score >= 55: return "rgba(245,158,11,0.12)"
    return "rgba(248,113,113,0.12)"


# ──────────────────────────────────────────
# 공통 HTML 부분
# ──────────────────────────────────────────
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
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>"""


# ──────────────────────────────────────────
# 개별 허브 페이지 생성
# ──────────────────────────────────────────
def generate_hub_page(sign):
    s = ZODIAC_MAP[sign]
    pairs = []
    for other in ZODIAC:
        c = get_compatibility(sign, other["id"])
        pairs.append({**other, **c})

    # 정렬: 점수 높은 순
    pairs_sorted = sorted(pairs, key=lambda x: x["score"], reverse=True)
    best3 = [p for p in pairs_sorted if p["id"] != sign][:3]
    worst2 = [p for p in pairs_sorted if p["id"] != sign][-2:]

    all_names = "·".join([ZODIAC_MAP[z["id"]]["ko"] for z in ZODIAC if z["id"] != sign])
    title = f"{s['ko']} 궁합 총정리 2026 | {s['ko']}와 잘 맞는 띠는? - 사주명리"
    desc = f"2026년 {s['ko']}({s['hanja']}) 궁합 완벽 분석. {best3[0]['ko']}({best3[0]['score']}점), {best3[1]['ko']}({best3[1]['score']}점)과 최고 궁합! 12간지 {all_names[:30]}... 궁합 점수 확인."

    # FAQPage schema
    faqs = [
        {"q": f"{s['ko']}와 가장 잘 맞는 띠는 무엇인가요?",
         "a": f"{s['ko']}와 가장 잘 맞는 띠는 {best3[0]['ko']}({best3[0]['score']}점, {best3[0]['label']}), {best3[1]['ko']}({best3[1]['score']}점, {best3[1]['label']}), {best3[2]['ko']}({best3[2]['score']}점)입니다. 특히 {best3[0]['ko']}와는 {best3[0]['type']} 관계로 서로 보완적인 최고의 조합입니다."},
        {"q": f"{s['ko']}와 궁합이 안 좋은 띠는?",
         "a": f"{s['ko']}와 주의가 필요한 관계는 {worst2[0]['ko']}({worst2[0]['score']}점, {worst2[0]['label']})와 {worst2[1]['ko']}({worst2[1]['score']}점, {worst2[1]['label']})입니다. 하지만 궁합이 낮다고 반드시 나쁜 것은 아닙니다. 서로를 이해하려는 노력이 중요합니다."},
        {"q": f"{s['ko']}의 삼합과 육합은?",
         "a": _get_samhap_yukhap_text(sign)},
        {"q": f"2026년 {s['ko']} 궁합 운세는?",
         "a": f"2026년 병오(丙午)년에 {s['ko']}는 전반적으로 인간관계에서 새로운 기회가 생깁니다. 특히 {best3[0]['ko']}와의 관계에서 좋은 에너지를 받을 수 있으며, {worst2[0]['ko']}와는 서로 배려하는 자세가 필요합니다. 자세한 개인 궁합은 생년월일시 기반 사주팔자를 확인해보세요."},
    ]

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ]
    }, ensure_ascii=False, indent=4)

    article_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"2026년 {s['ko']} 궁합 - 12간지 궁합 완벽 분석",
        "description": desc[:160],
        "url": f"https://saju.gon.ai.kr/compatibility/{sign}/",
        "datePublished": "2026-01-01",
        "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "사주명리", "url": "https://saju.gon.ai.kr/"},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://saju.gon.ai.kr/"},
                {"@type": "ListItem", "position": 2, "name": "띠별 궁합", "item": "https://saju.gon.ai.kr/compatibility/"},
                {"@type": "ListItem", "position": 3, "name": f"{s['ko']} 궁합", "item": f"https://saju.gon.ai.kr/compatibility/{sign}/"},
            ]
        }
    }, ensure_ascii=False, indent=4)

    # 궁합 카드 그리드 HTML
    cards_html = ""
    for p in pairs:
        if p["id"] == sign:
            continue
        sc = score_color(p["score"])
        bg = score_bg(p["score"])
        cards_html += f"""                <div class="compat-card" style="border-color: {sc}; background: {bg};">
                    <a href="/compatibility/{p['id']}/" class="compat-card-link">
                        <span class="compat-emoji">{p['emoji']}</span>
                        <span class="compat-name">{p['ko']}</span>
                        <span class="compat-score" style="color: {sc};">{p['score']}점</span>
                        <span class="compat-label" style="color: {sc};">{p['label']}</span>
                    </a>
                </div>
"""

    # 상세 궁합 섹션 (베스트 3 + 주의 2)
    detail_html = ""
    detail_html += '        <section class="compat-detail-section">\n'
    detail_html += '            <h2>💕 최고 궁합 TOP 3</h2>\n'
    for p in best3:
        detail_html += f"""            <div class="compat-detail-item good">
                <div class="detail-header">
                    <span class="detail-emoji">{p['emoji']}</span>
                    <span class="detail-name">{s['ko']} &amp; {p['ko']}</span>
                    <span class="detail-score" style="color: {score_color(p['score'])};">{p['score']}점</span>
                    <span class="detail-badge" style="background: {score_bg(p['score'])}; color: {score_color(p['score'])};">{p['type']} · {p['label']}</span>
                </div>
                <p class="detail-desc">{p['desc']}</p>
            </div>
"""
    detail_html += '        </section>\n'

    detail_html += '        <section class="compat-detail-section">\n'
    detail_html += '            <h2>⚠️ 주의가 필요한 관계</h2>\n'
    for p in worst2:
        detail_html += f"""            <div class="compat-detail-item caution">
                <div class="detail-header">
                    <span class="detail-emoji">{p['emoji']}</span>
                    <span class="detail-name">{s['ko']} &amp; {p['ko']}</span>
                    <span class="detail-score" style="color: {score_color(p['score'])};">{p['score']}점</span>
                    <span class="detail-badge" style="background: {score_bg(p['score'])}; color: {score_color(p['score'])};">{p['type']} · {p['label']}</span>
                </div>
                <p class="detail-desc">{p['desc']}</p>
            </div>
"""
    detail_html += '        </section>\n'

    # 다른 띠 궁합 링크
    other_links = ""
    for z in ZODIAC:
        cls = ' class="other-zodiac-link current"' if z["id"] == sign else ' class="other-zodiac-link"'
        other_links += f'                <a href="/compatibility/{z["id"]}/"{cls}><span class="oz-emoji">{z["emoji"]}</span><span class="oz-name">{z["ko"]}</span></a>\n'

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{desc[:160]}">
    <meta name="keywords" content="{s['ko']}궁합, {s['ko']} 궁합, 띠별궁합, 12간지 궁합, 2026년 궁합, {', '.join([ZODIAC_MAP[b['id']]['ko']+' 궁합' for b in best3])}">
    <title>{title}</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/compatibility/{sign}/">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="2026년 {s['ko']} 궁합 | 잘 맞는 띠 · 안 맞는 띠">
    <meta property="og:description" content="{desc[:100]}">
    <meta property="og:url" content="https://saju.gon.ai.kr/compatibility/{sign}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="2026년 {s['ko']} 궁합 총정리">
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

    <main class="compat-hub-page">
        <a href="/compatibility/" class="back-link">&larr; 전체 띠별 궁합 보기</a>

        <!-- Hero -->
        <section class="compat-hero">
            <div class="hero-emoji">{s['emoji']}</div>
            <div class="hero-hanja">{s['hanja']}({s['element']})</div>
            <h1 class="hero-title"><span class="gold-text">{s['ko']} 궁합</span></h1>
            <p class="hero-subtitle">12간지 궁합 완벽 분석 · 2026 병오년</p>
        </section>

        <!-- 궁합 점수 그리드 -->
        <section class="compat-grid-section">
            <h2>📊 {s['ko']} 궁합 점수표</h2>
            <div class="compat-grid">
{cards_html}            </div>
        </section>

        <!-- 상세 분석 -->
{detail_html}
        <!-- 삼합·육합 설명 -->
        <section class="compat-theory-section">
            <h2>📖 궁합의 원리</h2>
            <div class="theory-grid">
                <div class="theory-item">
                    <h3>삼합(三合)</h3>
                    <p>세 개의 띠가 하나의 오행으로 모이는 가장 강력한 궁합. 서로 끌리는 자연스러운 매력이 있습니다.</p>
                </div>
                <div class="theory-item">
                    <h3>육합(六合)</h3>
                    <p>음양이 조화롭게 만나는 천생연분 관계. 서로의 부족함을 자연스럽게 채워줍니다.</p>
                </div>
                <div class="theory-item">
                    <h3>상충(相沖)</h3>
                    <p>정반대 위치의 띠로, 에너지가 충돌합니다. 하지만 서로를 이해하면 강력한 파트너가 될 수 있습니다.</p>
                </div>
                <div class="theory-item">
                    <h3>상해(相害)</h3>
                    <p>겉으로는 평온해 보이지만 속으로 갈등이 생기기 쉬운 관계. 진솔한 소통이 열쇠입니다.</p>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">더 정확한 궁합이 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 궁합 분석을 받을 수 있습니다.</p>
            <a href="/" class="cta-btn">무료 사주 궁합 바로가기</a>
        </section>

        <!-- 다른 띠 궁합 -->
        <section class="other-zodiac-section">
            <h2><span class="gold-text">다른 띠 궁합 보기</span></h2>
            <div class="other-zodiac-grid">
{other_links}            </div>
        </section>

        <!-- 관련 링크 -->
        <section class="related-links-section">
            <a href="/zodiac/{sign}/" class="related-link">🔮 {s['ko']} 2026년 운세 보기</a>
            <a href="/daily/{sign}/" class="related-link">📅 {s['ko']} 오늘의 운세</a>
        </section>
    </main>

{FOOTER_HTML}

</body>
</html>"""

    return html


def _get_samhap_yukhap_text(sign):
    """삼합/육합 설명 텍스트"""
    samhap_text = ""
    for sh in SAMHAP:
        if sign in sh["signs"]:
            others = [ZODIAC_MAP[s]["ko"] for s in sh["signs"] if s != sign]
            samhap_text = f"삼합: {', '.join(others)}와 {sh['name']}을 이룹니다."
            break

    yukhap_text = ""
    for pair, name in YUKHAP.items():
        if sign in pair:
            other = [ZODIAC_MAP[s]["ko"] for s in pair if s != sign][0]
            yukhap_text = f"육합: {other}와 {name} 관계입니다."
            break

    return f"{samhap_text} {yukhap_text} 삼합은 세 띠가 하나의 오행 에너지로 모이는 관계이고, 육합은 음양이 자연스럽게 조화를 이루는 관계입니다."


# ──────────────────────────────────────────
# 갤러리 페이지 생성
# ──────────────────────────────────────────
def generate_gallery_page():
    title = "2026년 띠별 궁합 | 12간지 궁합 총정리 - 사주명리"
    desc = "12간지 동물띠별 궁합을 확인하세요. 삼합·육합·상충 관계 분석, 나와 잘 맞는 띠 찾기. 쥐띠·소띠·호랑이띠·토끼띠·용띠·뱀띠·말띠·양띠·원숭이띠·닭띠·개띠·돼지띠 궁합."

    collection_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "2026년 띠별 궁합",
        "description": "12간지 동물띠별 궁합 분석",
        "url": "https://saju.gon.ai.kr/compatibility/",
        "isPartOf": {"@type": "WebSite", "name": "사주명리", "url": "https://saju.gon.ai.kr/"},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://saju.gon.ai.kr/"},
                {"@type": "ListItem", "position": 2, "name": "띠별 궁합", "item": "https://saju.gon.ai.kr/compatibility/"},
            ]
        }
    }, ensure_ascii=False, indent=4)

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "띠별 궁합은 어떻게 보나요?",
             "acceptedAnswer": {"@type": "Answer", "text": "띠별 궁합은 12간지(자·축·인·묘·진·사·오·미·신·유·술·해)의 관계를 기반으로 합니다. 삼합(三合)과 육합(六合)은 좋은 궁합, 상충(相沖)은 어려운 관계를 나타냅니다. 정확한 궁합은 생년월일시 기반 사주팔자로 분석합니다."}},
            {"@type": "Question", "name": "삼합(三合)이란 무엇인가요?",
             "acceptedAnswer": {"@type": "Answer", "text": "삼합은 세 개의 띠가 하나의 오행 에너지로 모이는 최고의 궁합 관계입니다. 수국(쥐·용·원숭이), 금국(소·뱀·닭), 화국(호랑이·말·개), 목국(토끼·양·돼지) 4개 그룹이 있습니다."}},
            {"@type": "Question", "name": "육합(六合)이란 무엇인가요?",
             "acceptedAnswer": {"@type": "Answer", "text": "육합은 음양이 자연스럽게 조화를 이루는 천생연분 관계입니다. 쥐-소, 호랑이-돼지, 토끼-개, 용-닭, 뱀-원숭이, 말-양 6쌍이 있습니다."}},
            {"@type": "Question", "name": "상충(相沖)이란 무엇인가요?",
             "acceptedAnswer": {"@type": "Answer", "text": "상충은 12간지에서 정반대 위치에 있는 띠들의 관계로, 에너지가 충돌합니다. 쥐-말, 소-양, 호랑이-원숭이, 토끼-닭, 용-개, 뱀-돼지 6쌍입니다. 하지만 상충도 서로를 이해하면 강한 파트너가 될 수 있습니다."}},
        ]
    }, ensure_ascii=False, indent=4)

    # 띠별 카드 그리드
    cards_html = ""
    for z in ZODIAC:
        # 해당 띠의 최고 궁합 찾기
        best_score = 0
        best_sign = None
        for other in ZODIAC:
            if other["id"] == z["id"]:
                continue
            c = get_compatibility(z["id"], other["id"])
            if c["score"] > best_score:
                best_score = c["score"]
                best_sign = other
        cards_html += f"""                <a href="/compatibility/{z['id']}/" class="gallery-card">
                    <span class="gallery-emoji">{z['emoji']}</span>
                    <span class="gallery-name">{z['ko']}</span>
                    <span class="gallery-best">Best: {best_sign['emoji']} {best_sign['ko']} {best_score}점</span>
                    <span class="gallery-arrow">&rarr;</span>
                </a>
"""

    # 삼합 테이블
    samhap_html = ""
    for sh in SAMHAP:
        signs = [ZODIAC_MAP[s] for s in ["rat","ox","tiger","rabbit","dragon","snake","horse","goat","monkey","rooster","dog","pig"] if s in sh["signs"]]
        emojis = " ".join([s["emoji"] for s in signs])
        names = " · ".join([s["ko"] for s in signs])
        samhap_html += f'                <div class="samhap-item"><span class="samhap-emojis">{emojis}</span><span class="samhap-names">{names}</span><span class="samhap-type">{sh["name"]}</span></div>\n'

    # 육합 테이블
    yukhap_html = ""
    for pair, name in YUKHAP.items():
        signs = [ZODIAC_MAP[s] for s in ZODIAC_MAP if s in pair]
        signs.sort(key=lambda x: [z["id"] for z in ZODIAC].index(x["id"]))
        yukhap_html += f'                <div class="yukhap-item"><span class="yukhap-emojis">{signs[0]["emoji"]} ❤️ {signs[1]["emoji"]}</span><span class="yukhap-names">{signs[0]["ko"]} · {signs[1]["ko"]}</span><span class="yukhap-type">{name}</span></div>\n'

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{desc}">
    <meta name="keywords" content="띠별궁합, 12간지궁합, 삼합, 육합, 상충, 궁합보기, 띠궁합, 2026년궁합, 동물띠궁합">
    <title>{title}</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/compatibility/">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="2026년 띠별 궁합 | 12간지 궁합 총정리">
    <meta property="og:description" content="{desc[:100]}">
    <meta property="og:url" content="https://saju.gon.ai.kr/compatibility/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="2026년 띠별 궁합 총정리">
    <meta name="twitter:description" content="{desc[:100]}">

{COMMON_HEAD}

    <!-- Schema.org -->
    <script type="application/ld+json">
{collection_json}
    </script>
    <script type="application/ld+json">
{faq_json}
    </script>
</head>
<body>

{HEADER_HTML}

    <main class="compat-gallery-page">

        <!-- Hero -->
        <section class="gallery-hero">
            <h1 class="gallery-title"><span class="gold-text">띠별 궁합</span></h1>
            <p class="gallery-subtitle">12간지 동물띠 궁합 · 삼합 · 육합 · 상충 관계 분석</p>
        </section>

        <!-- 12띠 그리드 -->
        <section class="gallery-grid-section">
            <h2>나의 띠를 선택하세요</h2>
            <div class="gallery-grid">
{cards_html}            </div>
        </section>

        <!-- 삼합 -->
        <section class="samhap-section">
            <h2>🔺 삼합(三合) — 최고의 궁합</h2>
            <p class="section-desc">세 개의 띠가 하나의 오행 에너지로 모이는 가장 강력한 조합</p>
            <div class="samhap-grid">
{samhap_html}            </div>
        </section>

        <!-- 육합 -->
        <section class="yukhap-section">
            <h2>💕 육합(六合) — 천생연분</h2>
            <p class="section-desc">음양이 자연스럽게 조화를 이루는 이상적인 짝</p>
            <div class="yukhap-grid">
{yukhap_html}            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">생년월일 기반 정밀 궁합</h2>
            <p>띠별 궁합은 일반적인 참고 자료입니다. 정확한 궁합은 사주팔자로 확인하세요.</p>
            <a href="/" class="cta-btn">무료 사주 궁합 바로가기</a>
        </section>

    </main>

{FOOTER_HTML}

</body>
</html>"""

    return html


# ──────────────────────────────────────────
# 사이트맵 업데이트
# ──────────────────────────────────────────
def update_sitemap():
    sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    # </urlset> 앞에 새 URL 추가
    new_urls = f"""    <url>
        <loc>https://saju.gon.ai.kr/compatibility/</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
"""
    for z in ZODIAC:
        new_urls += f"""    <url>
        <loc>https://saju.gon.ai.kr/compatibility/{z['id']}/</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

    content = content.replace("</urlset>", new_urls + "</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated sitemap.xml (+13 URLs)")


# ──────────────────────────────────────────
# 메인 실행
# ──────────────────────────────────────────
def main():
    print("=== 띠별 궁합 페이지 생성 시작 ===\n")

    # 1. 갤러리 페이지
    gallery_dir = COMPAT_DIR
    os.makedirs(gallery_dir, exist_ok=True)
    gallery_path = os.path.join(gallery_dir, "index.html")
    with open(gallery_path, "w", encoding="utf-8") as f:
        f.write(generate_gallery_page())
    print(f"  Created: /compatibility/index.html")

    # 2. 12개 허브 페이지
    for z in ZODIAC:
        hub_dir = os.path.join(COMPAT_DIR, z["id"])
        os.makedirs(hub_dir, exist_ok=True)
        hub_path = os.path.join(hub_dir, "index.html")
        with open(hub_path, "w", encoding="utf-8") as f:
            f.write(generate_hub_page(z["id"]))
        print(f"  Created: /compatibility/{z['id']}/index.html")

    # 3. 사이트맵 업데이트
    update_sitemap()

    print(f"\n=== 완료: 13개 페이지 생성, sitemap 업데이트 ===")


if __name__ == "__main__":
    main()
