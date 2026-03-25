"""SSR daily fortune index page - pre-renders all 12 zodiac summaries for search engines."""
from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

ZODIAC_DATA = {
    "rat":     {"name": "쥐띠",     "emoji": "🐀", "hanja": "子", "element": "수(水)", "branch": 0},
    "ox":      {"name": "소띠",     "emoji": "🐂", "hanja": "丑", "element": "토(土)", "branch": 1},
    "tiger":   {"name": "호랑이띠", "emoji": "🐅", "hanja": "寅", "element": "목(木)", "branch": 2},
    "rabbit":  {"name": "토끼띠",   "emoji": "🐇", "hanja": "卯", "element": "목(木)", "branch": 3},
    "dragon":  {"name": "용띠",     "emoji": "🐉", "hanja": "辰", "element": "토(土)", "branch": 4},
    "snake":   {"name": "뱀띠",     "emoji": "🐍", "hanja": "巳", "element": "화(火)", "branch": 5},
    "horse":   {"name": "말띠",     "emoji": "🐴", "hanja": "午", "element": "화(火)", "branch": 6},
    "goat":    {"name": "양띠",     "emoji": "🐑", "hanja": "未", "element": "토(土)", "branch": 7},
    "monkey":  {"name": "원숭이띠", "emoji": "🐒", "hanja": "申", "element": "금(金)", "branch": 8},
    "rooster": {"name": "닭띠",     "emoji": "🐓", "hanja": "酉", "element": "금(金)", "branch": 9},
    "dog":     {"name": "개띠",     "emoji": "🐕", "hanja": "戌", "element": "토(土)", "branch": 10},
    "pig":     {"name": "돼지띠",   "emoji": "🐷", "hanja": "亥", "element": "수(水)", "branch": 11},
}

FORTUNE_MESSAGES = {
    "overall": [
        "모든 일이 순조롭게 풀리는 날입니다. 적극적으로 행동하세요.",
        "차분하게 준비하면 좋은 결과를 얻을 수 있는 날입니다.",
        "예상치 못한 기회가 찾아올 수 있습니다. 열린 마음을 가지세요.",
        "인내심이 필요한 날입니다. 서두르지 마세요.",
        "주변 사람들과의 소통이 행운을 가져다줍니다.",
        "자기 자신에게 집중하면 좋은 하루가 됩니다.",
        "새로운 시작에 좋은 날입니다. 미루던 일을 시작해보세요.",
        "감사하는 마음이 더 큰 행복을 가져다줍니다.",
        "작은 변화가 큰 결과를 만들어내는 날입니다.",
        "직감을 믿고 행동하면 좋은 결과를 얻을 수 있습니다.",
        "배움과 성장의 기회가 있는 날입니다. 새로운 것을 배워보세요.",
        "조용히 내면을 돌아보는 시간이 필요한 날입니다.",
    ],
    "money": [
        "재물운이 좋습니다. 투자나 저축에 좋은 시기입니다.",
        "지출을 줄이고 절약하는 것이 좋은 날입니다.",
        "뜻밖의 수입이 있을 수 있습니다.",
        "금전적인 결정은 신중하게 내리세요.",
        "소비보다는 저축에 집중하면 좋겠습니다.",
        "사업적 기회가 올 수 있으니 준비하세요.",
        "과감한 투자보다는 안정적인 운용이 좋습니다.",
        "동업이나 협력에서 재물이 올 수 있습니다.",
        "부수입의 기회가 생길 수 있습니다.",
        "금전 거래는 서류를 꼼꼼히 확인하세요.",
        "절약의 습관이 큰 부를 가져다줍니다.",
        "기다리면 더 좋은 조건이 올 수 있습니다.",
    ],
    "love": [
        "로맨틱한 만남의 기회가 있습니다.",
        "상대방에게 진심을 표현하면 좋은 반응을 얻을 수 있습니다.",
        "가족과의 시간을 가지면 마음이 편안해집니다.",
        "갈등이 있다면 대화로 풀어보세요.",
        "새로운 인연이 다가올 수 있는 날입니다.",
        "기존 관계가 더욱 깊어지는 날입니다.",
        "사소한 배려가 큰 감동을 줍니다.",
        "혼자만의 시간도 중요합니다. 자기 자신을 사랑하세요.",
        "오래된 친구와의 연락이 기쁨을 가져다줍니다.",
        "솔직한 마음이 좋은 관계를 만듭니다.",
        "상대방의 말에 귀 기울이면 관계가 좋아집니다.",
        "만남의 자리에서 좋은 인연을 만날 수 있습니다.",
    ],
    "health": [
        "활력이 넘치는 날입니다. 운동을 시작해보세요.",
        "충분한 수면이 건강의 기본입니다. 일찍 잠자리에 드세요.",
        "스트레스 관리에 신경 쓰세요. 명상이 도움이 됩니다.",
        "가벼운 산책이 기분 전환에 좋은 날입니다.",
        "수분 섭취를 충분히 하세요.",
        "무리한 운동보다는 스트레칭으로 몸을 풀어주세요.",
        "균형 잡힌 식사가 중요한 날입니다.",
        "자연 속에서 시간을 보내면 에너지가 충전됩니다.",
        "정기 건강검진을 미루지 마세요.",
        "눈과 허리에 주의하세요. 자세를 바로 하세요.",
        "따뜻한 차 한 잔이 마음과 몸을 녹여줍니다.",
        "일과 휴식의 균형을 잘 맞추세요.",
    ],
}

LUCKY_COLORS = ["빨강", "주황", "노랑", "초록", "파랑", "남색", "보라", "분홍", "하늘색", "금색", "은색", "갈색"]
LUCKY_DIRECTIONS = ["동쪽", "서쪽", "남쪽", "북쪽", "동남쪽", "동북쪽", "서남쪽", "서북쪽"]


def seeded_random(seed):
    s = seed
    def next_val():
        nonlocal s
        s = int(float(s) * 1103515245.0 + 12345.0) & 0x7FFFFFFF
        return s / 0x7FFFFFFF
    return next_val


def get_day_seed(now=None):
    if now is None:
        now = datetime.now(KST)
    return now.year * 10000 + now.month * 100 + now.day


def generate_fortune(zodiac_key, now=None):
    zodiac = ZODIAC_DATA[zodiac_key]
    day_seed = get_day_seed(now)
    seed = day_seed * 13 + zodiac["branch"] * 7919
    rng = seeded_random(seed)

    overall = int(rng() * 40 + 55)
    money = int(rng() * 40 + 50)
    love = int(rng() * 40 + 50)
    health = int(rng() * 40 + 55)

    overall_msg = FORTUNE_MESSAGES["overall"][int(rng() * len(FORTUNE_MESSAGES["overall"]))]
    money_msg = FORTUNE_MESSAGES["money"][int(rng() * len(FORTUNE_MESSAGES["money"]))]
    love_msg = FORTUNE_MESSAGES["love"][int(rng() * len(FORTUNE_MESSAGES["love"]))]
    health_msg = FORTUNE_MESSAGES["health"][int(rng() * len(FORTUNE_MESSAGES["health"]))]

    ln1 = int(rng() * 45) + 1
    ln2 = int(rng() * 45) + 1
    lucky_color = LUCKY_COLORS[int(rng() * len(LUCKY_COLORS))]
    lucky_dir = LUCKY_DIRECTIONS[int(rng() * len(LUCKY_DIRECTIONS))]
    lucky_time = f"{int(rng() * 12 + 1)}시"
    star = min(5, max(1, round(overall / 20)))

    def grade(s):
        if s >= 90: return "대길", "grade-best"
        if s >= 80: return "길", "grade-good"
        if s >= 70: return "소길", "grade-ok"
        if s >= 60: return "평", "grade-normal"
        return "주의", "grade-caution"

    g_text, g_class = grade(overall)
    stars = "★" * star + "☆" * (5 - star)

    return {
        "zodiac": zodiac, "overall": overall, "money": money, "love": love, "health": health,
        "overall_msg": overall_msg, "money_msg": money_msg, "love_msg": love_msg, "health_msg": health_msg,
        "lucky_number": f"{min(ln1, ln2)}, {max(ln1, ln2)}",
        "lucky_color": lucky_color, "lucky_dir": lucky_dir, "lucky_time": lucky_time,
        "stars": stars, "grade_text": g_text, "grade_class": g_class,
    }

ZODIAC_ORDER = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
                "horse", "goat", "monkey", "rooster", "dog", "pig"]


def render_index_html(now=None):
    if now is None:
        now = datetime.now(KST)

    date_str = f"{now.year}년 {now.month}월 {now.day}일"
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    day_of_week = weekdays[now.weekday()]

    # Generate fortunes for all 12 zodiacs
    fortunes = {}
    for key in ZODIAC_ORDER:
        fortunes[key] = generate_fortune(key, now)

    # Today's energy (same logic as client JS)
    day_seed = get_day_seed(now)
    rng = seeded_random(day_seed * 31)
    day_elements = ["목(木)", "화(火)", "토(土)", "금(金)", "수(水)"]
    day_emojis = ["🌿", "🔥", "⛰️", "⚔️", "💧"]
    day_descs = ["성장과 발전의 에너지", "열정과 활력의 에너지", "안정과 조화의 에너지",
                 "결단과 정리의 에너지", "지혜와 유연함의 에너지"]
    main_element = int(rng() * 5)
    day_energy = int(rng() * 40 + 60)
    energy_desc = "매우 좋은 날!" if day_energy >= 80 else ("괜찮은 하루" if day_energy >= 65 else "평온한 하루")
    advices = [
        "새로운 시도에 열린 마음을 가지세요",
        "주변 사람들에게 감사를 표현하세요",
        "자기 자신에게 투자하는 날로 만드세요",
        "작은 성공을 축하하며 기운을 얻으세요",
        "마음의 여유를 갖고 하루를 보내세요",
    ]
    advice = advices[int(rng() * 5)]

    # Build zodiac summary cards HTML
    zodiac_cards = []
    for key in ZODIAC_ORDER:
        f = fortunes[key]
        z = f["zodiac"]
        zodiac_cards.append(f"""
            <a href="/daily/{key}/" class="zodiac-summary-card">
                <div class="zsc-header">
                    <span class="zsc-emoji">{z['emoji']}</span>
                    <span class="zsc-name">{z['name']}</span>
                    <span class="zsc-grade {f['grade_class']}">{f['grade_text']}</span>
                </div>
                <div class="zsc-scores">
                    <div class="zsc-score-item">
                        <span class="zsc-label">총운</span>
                        <div class="zsc-bar"><div class="zsc-fill" style="width:{f['overall']}%;background:var(--color-gold)"></div></div>
                        <span class="zsc-val">{f['overall']}</span>
                    </div>
                    <div class="zsc-score-item">
                        <span class="zsc-label">재물</span>
                        <div class="zsc-bar"><div class="zsc-fill" style="width:{f['money']}%;background:#D4AF37"></div></div>
                        <span class="zsc-val">{f['money']}</span>
                    </div>
                    <div class="zsc-score-item">
                        <span class="zsc-label">연애</span>
                        <div class="zsc-bar"><div class="zsc-fill" style="width:{f['love']}%;background:#F87171"></div></div>
                        <span class="zsc-val">{f['love']}</span>
                    </div>
                    <div class="zsc-score-item">
                        <span class="zsc-label">건강</span>
                        <div class="zsc-bar"><div class="zsc-fill" style="width:{f['health']}%;background:#4ADE80"></div></div>
                        <span class="zsc-val">{f['health']}</span>
                    </div>
                </div>
                <p class="zsc-msg">{f['overall_msg']}</p>
                <span class="zsc-link">자세히 보기 →</span>
            </a>""")

    zodiac_cards_html = "\n".join(zodiac_cards)

    # Build ranked list for Schema.org
    ranked = sorted(fortunes.items(), key=lambda x: x[1]["overall"], reverse=True)
    faq_items = []
    for key, f in ranked[:3]:
        z = f["zodiac"]
        faq_items.append(f"""{{
            "@type": "Question",
            "name": "오늘 {z['name']} 운세는?",
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": "총운 {f['overall']}점 ({f['grade_text']}). {f['overall_msg']}"
            }}
        }}""")
    faq_schema = ", ".join(faq_items)

    # Best fortune today
    best_key, best_f = ranked[0]
    best_name = best_f["zodiac"]["name"]

    # Description with today's best
    meta_desc = f"오늘의 운세 ({date_str} {day_of_week}요일) - 오늘 가장 운이 좋은 띠: {best_name} (총운 {best_f['overall']}점). 12간지 띠별 총운, 재물운, 연애운, 건강운을 무료로 확인하세요."

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="오늘의운세, 오늘운세, 띠별운세, 일일운세, 무료운세, 데일리운세, 매일운세, 행운의숫자, 행운의색">
    <title>오늘의 운세 ({date_str}) | 매일 업데이트 띠별 운세 - 사주명리</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/daily/">

    <!-- Naver Search Advisor -->
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="오늘의 운세 ({date_str}) | 12띠별 운세">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://saju.gon.ai.kr/daily/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="오늘의 운세 ({date_str}) | 12띠별 운세">
    <meta name="twitter:description" content="{meta_desc}">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "오늘의 운세 ({date_str})",
        "description": "{meta_desc}",
        "url": "https://saju.gon.ai.kr/daily/",
        "dateModified": "{now.strftime('%Y-%m-%d')}",
        "isPartOf": {{
            "@type": "WebSite",
            "name": "사주명리",
            "url": "https://saju.gon.ai.kr/"
        }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "https://saju.gon.ai.kr/" }},
                {{ "@type": "ListItem", "position": 2, "name": "오늘의 운세", "item": "https://saju.gon.ai.kr/daily/" }}
            ]
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{faq_schema}]
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
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=2">

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
    /* SSR zodiac summary cards */
    .zodiac-summary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }}
    .zodiac-summary-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 12px;
        padding: 1.2rem;
        text-decoration: none;
        color: inherit;
        transition: border-color 0.2s, transform 0.2s;
        display: block;
    }}
    .zodiac-summary-card:hover {{
        border-color: rgba(212,175,55,0.4);
        transform: translateY(-2px);
    }}
    .zsc-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
    }}
    .zsc-emoji {{ font-size: 1.5rem; }}
    .zsc-name {{
        font-family: var(--font-heading);
        font-size: 1.1rem;
        font-weight: 700;
        flex: 1;
    }}
    .zsc-grade {{
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    .zsc-grade.grade-best {{ background: rgba(212,175,55,0.2); color: #D4AF37; }}
    .zsc-grade.grade-good {{ background: rgba(74,222,128,0.15); color: #4ADE80; }}
    .zsc-grade.grade-ok {{ background: rgba(96,165,250,0.15); color: #60A5FA; }}
    .zsc-grade.grade-normal {{ background: rgba(163,163,163,0.15); color: #A3A3A3; }}
    .zsc-grade.grade-caution {{ background: rgba(248,113,113,0.15); color: #F87171; }}
    .zsc-scores {{ display: flex; flex-direction: column; gap: 0.3rem; margin-bottom: 0.6rem; }}
    .zsc-score-item {{ display: flex; align-items: center; gap: 0.5rem; }}
    .zsc-label {{ font-size: 0.75rem; color: rgba(255,255,255,0.5); width: 2rem; }}
    .zsc-bar {{
        flex: 1;
        height: 6px;
        background: rgba(255,255,255,0.06);
        border-radius: 3px;
        overflow: hidden;
    }}
    .zsc-fill {{
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease-out;
    }}
    .zsc-val {{ font-size: 0.75rem; color: rgba(255,255,255,0.6); width: 1.5rem; text-align: right; }}
    .zsc-msg {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        line-height: 1.4;
        margin: 0;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}
    .zsc-link {{
        display: inline-block;
        margin-top: 0.5rem;
        font-size: 0.8rem;
        color: var(--color-gold);
    }}
    .ranking-section {{
        margin-top: 1.5rem;
    }}
    .ranking-list {{
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 1rem;
    }}
    .ranking-item {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.8rem 1rem;
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        text-decoration: none;
        color: inherit;
    }}
    .ranking-item:hover {{ background: rgba(255,255,255,0.06); }}
    .ranking-rank {{
        font-size: 1.2rem;
        font-weight: 700;
        width: 2rem;
        text-align: center;
    }}
    .ranking-rank.gold {{ color: #D4AF37; }}
    .ranking-rank.silver {{ color: #C0C0C0; }}
    .ranking-rank.bronze {{ color: #CD7F32; }}
    .ranking-info {{ flex: 1; }}
    .ranking-name {{ font-weight: 600; }}
    .ranking-score {{ color: var(--color-gold); font-weight: 700; }}
    @media (max-width: 640px) {{
        .zodiac-summary-grid {{
            grid-template-columns: 1fr;
        }}
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
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/" class="active">오늘의 운세</a>
                <a href="/palm/">손금 분석</a>
            </nav>
        </nav>
    </header>

    <!-- Hero -->
    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge">{date_str} {day_of_week}요일</div>
            <h1 class="hero-title"><span class="gold-text">오늘의 운세</span></h1>
            <p class="hero-subtitle">매일 새롭게 업데이트되는 띠별 운세입니다.<br>자신의 띠를 선택하여 오늘의 운세를 확인하세요.</p>
        </div>
    </section>

    <!-- Today's Overview (SSR) -->
    <section class="overview-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">오늘의 기운</span></h2>
            <div class="energy-cards">
                <div class="energy-card main">
                    <div class="energy-emoji">{day_emojis[main_element]}</div>
                    <h3>오늘의 주 기운</h3>
                    <p class="energy-element">{day_elements[main_element]}</p>
                    <p class="energy-desc">{day_descs[main_element]}</p>
                </div>
                <div class="energy-card">
                    <div class="energy-emoji">☯</div>
                    <h3>전체 운세 지수</h3>
                    <p class="energy-score">{day_energy}<small>/100</small></p>
                    <p class="energy-desc">{energy_desc}</p>
                </div>
                <div class="energy-card">
                    <div class="energy-emoji">📅</div>
                    <h3>오늘의 조언</h3>
                    <p class="energy-advice">{advice}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Today's Ranking (SSR - SEO value) -->
    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">오늘의 운세 랭킹</span></h2>
            <p style="text-align:center;color:rgba(255,255,255,0.5);margin-bottom:0.5rem;">{date_str} 기준 띠별 총운 순위</p>
            <div class="ranking-list">
                {"".join(f'''
                <a href="/daily/{key}/" class="ranking-item">
                    <span class="ranking-rank {'gold' if i==0 else 'silver' if i==1 else 'bronze' if i==2 else ''}">{i+1}</span>
                    <span style="font-size:1.3rem">{f["zodiac"]["emoji"]}</span>
                    <span class="ranking-info"><span class="ranking-name">{f["zodiac"]["name"]}</span></span>
                    <span class="ranking-score">{f["overall"]}점</span>
                    <span class="zsc-grade {f['grade_class']}" style="margin-left:0.3rem">{f["grade_text"]}</span>
                </a>''' for i, (key, f) in enumerate(ranked))}
            </div>
        </div>
    </section>

    <!-- All 12 Zodiac Summaries (SSR - main SEO content) -->
    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">12간지 띠별 오늘의 운세</span></h2>
            <div class="zodiac-summary-grid">
                {zodiac_cards_html}
            </div>
        </div>
    </section>

    <!-- Birth Year Quick Check (interactive) -->
    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">내 띠 찾기</span></h2>
            <div class="birth-year-check" style="text-align:center;">
                <label>태어난 해로 찾기:</label>
                <input type="number" id="birth-year" placeholder="예: 1990" min="1920" max="2025">
                <button onclick="findZodiacByYear()">확인</button>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/zodiac/" class="cta-btn" style="background: transparent; border: 1px solid var(--color-gold); color: var(--color-gold);">2026년 띠별 운세</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/palm/">손금 분석</a>
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>

    <script>
    function findZodiacByYear() {{
        var yearInput = document.getElementById('birth-year');
        var year = parseInt(yearInput.value);
        if (!year || year < 1920 || year > 2025) {{
            alert('1920~2025 사이의 출생연도를 입력해주세요.');
            return;
        }}
        var zodiacKeys = ['monkey','rooster','dog','pig','rat','ox','tiger','rabbit','dragon','snake','horse','goat'];
        var index = year % 12;
        window.location.href = '/daily/' + zodiacKeys[index] + '/';
    }}
    </script>

</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = render_index_html()
        body = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        # Cache until end of day KST
        now = datetime.now(KST)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_left = int((tomorrow - now).total_seconds())
        self.send_header("Cache-Control", f"public, s-maxage={seconds_left}, max-age=300, stale-while-revalidate=60")
        self.end_headers()
        self.wfile.write(body)
