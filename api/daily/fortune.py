"""SSR daily fortune page - pre-renders zodiac fortune for search engines."""
from http.server import BaseHTTPRequestHandler
from datetime import datetime, timedelta
import os
import sys

# api/ 를 import 경로에 추가 (api/saju/calculate.py 와 동일한 방식)
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from _core.daily_fortune import KST, ZODIAC_DATA, generate_fortune  # noqa: E402


def render_html(sign, now=None):
    if now is None:
        now = datetime.now(KST)
    f = generate_fortune(sign, now)
    z = f["zodiac"]
    ilji = f["ilji"]
    rel = f["relation"]
    ilji_day = f"{ilji['display']}일"
    also = f" ({'·'.join(rel['also_labels'])} 함께)" if rel["also_labels"] else ""
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
    <meta name="description" content="{z['name']} 오늘의 운세 ({date_str}, {ilji_day}) - 오늘 일진과 {rel['label']} 관계, 총운 {f['overall']}점, 재물운 {f['money']}점, 연애운 {f['love']}점, 건강운 {f['health']}점. {f['overall_msg']}">
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
            <p class="hero-subtitle">{z['hanja']}({z['element']}) | {date_str} {ilji_day} 기준</p>
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

                <div class="result-msg-card" style="margin-bottom:1rem;">
                    <h4>📜 오늘의 일진과 {z['name']}: {rel['label']}{also}</h4>
                    <p>오늘은 {ilji_day}입니다. {z['name']}의 지지 {z['hanja']} ↔ 오늘 일지 {ilji['branch_hanja']}. {rel['explain']}</p>
                    <p style="margin-top:0.4rem;font-size:0.8rem;opacity:0.7;">총운 점수는 이 관계가 정한 범위 안에서 날마다 달라집니다.</p>
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
