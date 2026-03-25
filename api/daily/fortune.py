"""SSR daily fortune page - pre-renders zodiac fortune for search engines."""
from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone, timedelta
import json
import re

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
    """Exact replica of JS seededRandom — uses float to match JS double precision."""
    s = seed
    def next_val():
        nonlocal s
        # Must use float arithmetic to replicate JS double precision behavior.
        # Python int is arbitrary precision, so exact math would differ from JS.
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


def render_html(sign, now=None):
    if now is None:
        now = datetime.now(KST)
    f = generate_fortune(sign, now)
    z = f["zodiac"]
    date_str = f"{now.year}년 {now.month}월 {now.day}일"
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    day_name = weekdays[now.weekday()]
    date_full = f"{date_str} {day_name}요일"
    iso_date = now.strftime("%Y-%m-%d")

    # Other zodiac links
    other_signs = ""
    for key, data in ZODIAC_DATA.items():
        active = ' class="active"' if key == sign else ""
        other_signs += f'<a href="/daily/{key}/"{active}>{data["emoji"]} {data["name"]}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{z['name']} 오늘의 운세 ({date_str}) - 총운 {f['overall']}점, 재물운 {f['money']}점, 연애운 {f['love']}점, 건강운 {f['health']}점. {f['overall_msg']}">
    <meta name="keywords" content="{z['name']}운세, {z['name']}오늘의운세, 오늘운세, 띠별운세, {z['name']}, 무료운세">
    <title>{z['name']} 오늘의 운세 ({date_str}) | 사주명리</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/daily/{sign}/">

    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <meta property="og:type" content="article">
    <meta property="og:title" content="{z['name']} 오늘의 운세 - 총운 {f['overall']}점 ({f['grade_text']})">
    <meta property="og:description" content="{f['overall_msg']} 재물운 {f['money']}점, 연애운 {f['love']}점.">
    <meta property="og:url" content="https://saju.gon.ai.kr/daily/{sign}/">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">

    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{z['name']} 오늘의 운세 ({date_str})",
        "description": "{f['overall_msg']}",
        "datePublished": "{iso_date}",
        "dateModified": "{iso_date}",
        "author": {{"@type": "Organization", "name": "사주명리"}},
        "publisher": {{"@type": "Organization", "name": "사주명리", "url": "https://saju.gon.ai.kr"}},
        "mainEntityOfPage": "https://saju.gon.ai.kr/daily/{sign}/"
    }}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=1">

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-BNRL6FRMMM');</script>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;">
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

    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge">{date_full}</div>
            <h1 class="hero-title"><span class="gold-text">{z['emoji']} {z['name']} 오늘의 운세</span></h1>
            <p class="hero-subtitle">{z['hanja']}({z['element']}) | {date_str} 기준</p>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <div class="daily-result" style="display:block;">
                <div class="result-header">
                    <div class="result-emoji">{z['emoji']}</div>
                    <div class="result-info">
                        <h3>{z['name']} <span class="result-hanja">{z['hanja']}({z['element']})</span></h3>
                        <div class="result-stars">{f['stars']}</div>
                    </div>
                    <div class="result-grade {f['grade_class']}">{f['grade_text']}</div>
                </div>

                <div class="result-scores-grid">
                    <div class="result-score-card">
                        <div class="rsc-icon">🔮</div>
                        <div class="rsc-label">총운</div>
                        <div class="rsc-score">{f['overall']}<small>점</small></div>
                        <div class="rsc-bar"><div class="rsc-fill" style="width:{f['overall']}%;background:var(--color-gold);"></div></div>
                    </div>
                    <div class="result-score-card">
                        <div class="rsc-icon">💰</div>
                        <div class="rsc-label">재물운</div>
                        <div class="rsc-score">{f['money']}<small>점</small></div>
                        <div class="rsc-bar"><div class="rsc-fill" style="width:{f['money']}%;background:#D4AF37;"></div></div>
                    </div>
                    <div class="result-score-card">
                        <div class="rsc-icon">💕</div>
                        <div class="rsc-label">연애운</div>
                        <div class="rsc-score">{f['love']}<small>점</small></div>
                        <div class="rsc-bar"><div class="rsc-fill" style="width:{f['love']}%;background:#F87171;"></div></div>
                    </div>
                    <div class="result-score-card">
                        <div class="rsc-icon">💪</div>
                        <div class="rsc-label">건강운</div>
                        <div class="rsc-score">{f['health']}<small>점</small></div>
                        <div class="rsc-bar"><div class="rsc-fill" style="width:{f['health']}%;background:#4ADE80;"></div></div>
                    </div>
                </div>

                <div class="result-messages">
                    <div class="result-msg-card"><h4>🔮 오늘의 총운</h4><p>{f['overall_msg']}</p></div>
                    <div class="result-msg-card"><h4>💰 재물운</h4><p>{f['money_msg']}</p></div>
                    <div class="result-msg-card"><h4>💕 연애운</h4><p>{f['love_msg']}</p></div>
                    <div class="result-msg-card"><h4>💪 건강운</h4><p>{f['health_msg']}</p></div>
                </div>

                <div class="result-lucky">
                    <div class="lucky-chip"><span class="lucky-icon">🔢</span> 행운의 숫자: <strong>{f['lucky_number']}</strong></div>
                    <div class="lucky-chip"><span class="lucky-icon">🎨</span> 행운의 색: <strong>{f['lucky_color']}</strong></div>
                    <div class="lucky-chip"><span class="lucky-icon">🧭</span> 행운의 방향: <strong>{f['lucky_dir']}</strong></div>
                    <div class="lucky-chip"><span class="lucky-icon">⏰</span> 행운의 시간: <strong>{f['lucky_time']}</strong></div>
                </div>
            </div>

            <h2 class="section-title" style="margin-top:2rem;"><span class="gold-text">다른 띠 운세 보기</span></h2>
            <div class="zodiac-nav-grid">
                {other_signs}
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/zodiac/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">2026년 띠별 운세</a>
            </div>
        </div>
    </section>

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

    <style>
    .zodiac-nav-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 0.5rem;
        margin-top: 1rem;
    }}
    .zodiac-nav-grid a {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        text-decoration: none;
        font-size: 0.9rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.15);
        color: var(--text-secondary, #aaa);
        transition: all 0.2s;
    }}
    .zodiac-nav-grid a:hover {{
        border-color: var(--color-gold, #D4AF37);
        color: var(--color-gold, #D4AF37);
    }}
    .zodiac-nav-grid a.active {{
        background: rgba(212,175,55,0.15);
        border-color: var(--color-gold, #D4AF37);
        color: var(--color-gold, #D4AF37);
        font-weight: 600;
    }}
    </style>

</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract sign from path: /daily/rat/ or /api/daily/fortune?sign=rat
        sign = None

        # Check query param
        if "?" in self.path:
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            sign = qs.get("sign", [None])[0]

        if not sign or sign not in ZODIAC_DATA:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Not Found".encode("utf-8"))
            return

        html = render_html(sign)
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
