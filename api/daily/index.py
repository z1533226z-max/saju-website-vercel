"""SSR daily fortune index page - pre-renders all 12 zodiac summaries for search engines."""
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import os
import sys

# api/ 를 import 경로에 추가 (api/saju/calculate.py 와 동일한 방식)
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from _core.daily_fortune import (  # noqa: E402
    KST, ZODIAC_ORDER, cache_control_until_midnight, day_energy, generate_fortune, get_day_ilji,
)
from _core.site_layout import RELATED_LINKS_CSS, footer_links_html, nav_links_html  # noqa: E402

# 일간(日干) 오행별 오늘의 기운 (표기, 이모지, 설명, 조언)
ELEMENT_INFO = {
    "목": ("목(木)", "🌿", "성장과 발전의 에너지", "새로운 시도에 열린 마음을 가지세요"),
    "화": ("화(火)", "🔥", "열정과 활력의 에너지", "작은 성공을 축하하며 기운을 얻으세요"),
    "토": ("토(土)", "⛰️", "안정과 조화의 에너지", "마음의 여유를 갖고 하루를 보내세요"),
    "금": ("금(金)", "⚔️", "결단과 정리의 에너지", "미뤄 둔 일을 정리하고 매듭을 지어 보세요"),
    "수": ("수(水)", "💧", "지혜와 유연함의 에너지", "자기 자신에게 투자하는 날로 만드세요"),
}


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

    # Today's energy: 오늘 일진(日辰)의 일간 오행 + 일진·월주 관계로 정한 전체 운세 지수
    ilji = get_day_ilji(now)
    ilji_day = f"{ilji['display']}일"
    el_label, el_emoji, el_desc, advice = ELEMENT_INFO[ilji["element"]]
    energy = day_energy(now)

    # Build zodiac summary cards HTML
    zodiac_cards = []
    for key in ZODIAC_ORDER:
        f = fortunes[key]
        z = f["zodiac"]
        rel = f["relation"]
        also = f" · {'·'.join(rel['also_labels'])} 함께" if rel["also_labels"] else ""
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
                <div class="zsc-rel">
                    <span class="zsc-rel-chip tone-{rel['tone']}">{rel['label']}</span>
                    <span class="zsc-rel-basis">{z['hanja']} ↔ {ilji['branch_hanja']}(오늘 일지){also}</span>
                </div>
                <p class="zsc-msg">{rel['explain']}</p>
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
                "text": "총운 {f['overall']}점 ({f['grade_text']}). 오늘 일진 {ilji_day}과 {z['name']}의 관계는 {f['relation']['label']}입니다. {f['relation']['explain']}"
            }}
        }}""")
    faq_schema = ", ".join(faq_items)

    # Best fortune today
    best_key, best_f = ranked[0]
    best_name = best_f["zodiac"]["name"]

    # Description with today's best
    meta_desc = f"오늘의 운세 ({date_str} {day_of_week}요일, {ilji_day}) - 오늘 가장 운이 좋은 띠: {best_name} (총운 {best_f['overall']}점, {best_f['relation']['label']}). 12간지 띠별 총운·재물운·연애운·건강운과 오늘 일진 풀이를 무료로 확인하세요."

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
    .zsc-rel {{ display: flex; align-items: center; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.4rem; }}
    .zsc-rel-chip {{
        display: inline-block;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
    }}
    .zsc-rel-chip.tone-good {{ background: rgba(74,222,128,0.15); color: #4ADE80; }}
    .zsc-rel-chip.tone-neutral {{ background: rgba(163,163,163,0.15); color: #C8C8C8; }}
    .zsc-rel-chip.tone-caution {{ background: rgba(248,113,113,0.15); color: #F87171; }}
    .zsc-rel-basis {{ font-size: 0.75rem; color: rgba(255,255,255,0.5); }}
    .score-basis {{
        text-align: center;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.45);
        line-height: 1.5;
        margin: 0 auto 0.5rem;
        max-width: 640px;
    }}
    {RELATED_LINKS_CSS}
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
            {nav_links_html("/daily/")}
        </nav>
    </header>

    <!-- Hero -->
    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge">{date_str} {day_of_week}요일 · {ilji_day}</div>
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
                    <div class="energy-emoji">{el_emoji}</div>
                    <h3>오늘의 주 기운</h3>
                    <p class="energy-element">{el_label}</p>
                    <p class="energy-desc">{el_desc}<br>오늘 일진 {ilji_day} · 일간 {ilji['stem_ko']}({ilji['stem_hanja']}) 기준</p>
                </div>
                <div class="energy-card">
                    <div class="energy-emoji">☯</div>
                    <h3>전체 운세 지수</h3>
                    <p class="energy-score">{energy['score']}<small>/100</small></p>
                    <p class="energy-desc">{energy['desc']}<br><small>{energy['reason']}</small></p>
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
            <p class="score-basis">산정 기준: 오늘 일지 {ilji['branch_ko']}({ilji['branch_hanja']}) ↔ 각 띠의 지지 관계(육합·삼합·충·형·해·파·원진). 관계가 총운 점수 범위를 정하고, 그 안에서 날마다 달라집니다.</p>
            <div class="ranking-list">
                {"".join(f'''
                <a href="/daily/{key}/" class="ranking-item">
                    <span class="ranking-rank {'gold' if i==0 else 'silver' if i==1 else 'bronze' if i==2 else ''}">{i+1}</span>
                    <span style="font-size:1.3rem">{f["zodiac"]["emoji"]}</span>
                    <span class="ranking-info"><span class="ranking-name">{f["zodiac"]["name"]}</span> <span class="zsc-rel-chip tone-{f['relation']['tone']}">{f['relation']['label']}</span></span>
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

    <!-- Related content (internal links) -->
    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">함께 보면 좋은 운세</span></h2>
            <nav class="daily-more-links" aria-label="관련 운세">
                <a href="/yearly/">🎍 2027 신년운세</a>
                <a href="/dream/">🌙 인기 꿈해몽</a>
                <a href="/compatibility/">💞 띠별 궁합</a>
                <a href="/palm/">✋ 손금 보기</a>
            </nav>
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
            {footer_links_html()}
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
        self.send_header("Cache-Control", cache_control_until_midnight())
        self.end_headers()
        self.wfile.write(body)
