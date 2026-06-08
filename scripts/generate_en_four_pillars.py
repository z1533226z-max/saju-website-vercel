"""Generate the English /en/ landing hub and the /en/four-pillars/ BaZi guide section.

Creates 8 pages total:
- /en/index.html                              (English section landing hub — fixes the 404 Home target)
- /en/four-pillars/                           (BaZi / Four Pillars of Destiny hub)
- /en/four-pillars/day-master/                (Day Master)
- /en/four-pillars/heavenly-stems/            (10 Heavenly Stems)
- /en/four-pillars/earthly-branches/          (12 Earthly Branches)
- /en/four-pillars/ten-gods/                  (Ten Gods)
- /en/four-pillars/luck-pillars/              (Luck Pillars / Da Yun)
- /en/four-pillars/reading-chart/             (How to read a BaZi chart)

All pages are English-only educational content (evergreen). hreflang is self
(en) because there is no Korean equivalent page. Existing Korean pages are not
touched.
"""
import os

PUB = os.path.join(os.path.dirname(__file__), '..', 'public')
EN = os.path.join(PUB, 'en')
FP = os.path.join(EN, 'four-pillars')
DATE = "2026-06-08"

GA = "G-BNRL6FRMMM"
ADS = "ca-pub-7479840445702290"
NAVER = '<meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />'

# Shared header nav (consistent across the new section, logo -> /en/)
NAV = (
    '<nav class="nav-links">'
    '<a href="/en/four-pillars/"{fp}>Four Pillars</a>'
    '<a href="/en/zodiac/"{zo}>Zodiac</a>'
    '<a href="/en/five-elements/"{fe}>Five Elements</a>'
    '<a href="/en/compatibility/"{co}>Compatibility</a>'
    '<a href="/">Korean Ver.</a>'
    '</nav>'
)


def nav(active=""):
    return NAV.format(
        fp=' class="active"' if active == "fp" else "",
        zo=' class="active"' if active == "zo" else "",
        fe=' class="active"' if active == "fe" else "",
        co=' class="active"' if active == "co" else "",
    )


def head_common():
    return f'''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS}" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA}');
    </script>'''


def footer():
    return '''    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/four-pillars/">Four Pillars (BaZi)</a>
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/five-elements/">Five Elements</a>
                <a href="/en/compatibility/">Compatibility</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">BaZi (Four Pillars / Saju) interpretations are based on traditional East Asian metaphysics and are provided for educational and entertainment purposes only.</p>
        </div>
    </footer>'''


def faq_schema(faq):
    parts = []
    for q, a in faq:
        parts.append(
            '{"@type":"Question","name":' + esc(q) +
            ',"acceptedAnswer":{"@type":"Answer","text":' + esc(a) + '}}'
        )
    return ",\n        ".join(parts)


def esc(text):
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


# Shared article CSS (used by every four-pillars sub-page)
ARTICLE_CSS = '''        .fp-page { max-width: 860px; margin: 0 auto; padding: var(--spacing-lg); }
        .fp-hero { text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-xl); }
        .fp-hero .fp-hanja { font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); margin-bottom: var(--spacing-xs); }
        .fp-hero h1 { font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-md); }
        .fp-hero p { color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 640px; margin: 0 auto; line-height: var(--line-height-relaxed); }
        .back-link { display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); margin-bottom: var(--spacing-lg); }
        .back-link:hover { color: var(--color-gold-light); }
        .fp-section { margin: var(--spacing-2xl) 0; }
        .fp-section h2 { font-family: var(--font-heading); color: var(--color-gold-text); font-size: var(--text-2xl); margin-bottom: var(--spacing-md); }
        .fp-section h3 { font-family: var(--font-heading); color: var(--color-gold-muted); font-size: var(--text-xl); margin: var(--spacing-lg) 0 var(--spacing-sm); }
        .fp-section p { color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin-bottom: var(--spacing-md); }
        .fp-section ul, .fp-section ol { color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin: 0 0 var(--spacing-md) var(--spacing-lg); }
        .fp-section li { margin-bottom: var(--spacing-xs); }
        .fp-callout { padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid var(--color-gold-muted); margin: var(--spacing-xl) 0; }
        .fp-callout p:last-child { margin-bottom: 0; }
        .fp-table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); margin: var(--spacing-lg) 0; }
        .fp-table th, .fp-table td { padding: var(--spacing-sm); border-bottom: 1px solid var(--color-border-light); text-align: left; vertical-align: top; }
        .fp-table th { color: var(--color-gold-muted); font-weight: var(--font-semibold); }
        .fp-table tr:hover td { background: var(--color-glass-surface); }
        .related-links { margin-top: var(--spacing-3xl); padding-top: var(--spacing-2xl); border-top: 1px solid var(--color-border-light); }
        .related-links h2 { text-align: center; font-family: var(--font-heading); font-size: var(--text-xl); margin-bottom: var(--spacing-lg); }
        .related-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: var(--spacing-md); }
        .related-card { display: block; padding: var(--spacing-md) var(--spacing-lg); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; color: var(--color-text-primary); transition: all var(--duration-normal); }
        .related-card:hover { border-color: var(--color-gold-muted); transform: translateY(-2px); }
        .related-card .rc-title { font-weight: var(--font-semibold); margin-bottom: 2px; }
        .related-card .rc-sub { font-size: var(--text-xs); color: var(--color-text-tertiary); }
        @media (max-width: 640px) {
            .fp-hero h1 { font-size: var(--text-3xl); }
            .fp-table { font-size: var(--text-xs); }
        }'''


# Related links block shown on every sub-page (internal linking for indexing)
def related_block(current_id):
    items = [
        ("four-pillars", "/en/four-pillars/", "Four Pillars Guide", "BaZi overview"),
        ("day-master", "/en/four-pillars/day-master/", "Day Master", "Your core self (日主)"),
        ("heavenly-stems", "/en/four-pillars/heavenly-stems/", "Heavenly Stems", "10 stems (天干)"),
        ("earthly-branches", "/en/four-pillars/earthly-branches/", "Earthly Branches", "12 branches (地支)"),
        ("ten-gods", "/en/four-pillars/ten-gods/", "Ten Gods", "Relationships (十神)"),
        ("luck-pillars", "/en/four-pillars/luck-pillars/", "Luck Pillars", "10-year cycles (大運)"),
        ("reading-chart", "/en/four-pillars/reading-chart/", "Read a Chart", "Step-by-step"),
        ("zodiac", "/en/zodiac/", "Chinese Zodiac", "12 animal signs"),
        ("five-elements", "/en/five-elements/", "Five Elements", "Wu Xing (五行)"),
        ("compatibility", "/en/compatibility/", "Compatibility", "Zodiac love match"),
    ]
    cards = []
    for cid, url, title, sub in items:
        if cid == current_id:
            continue
        cards.append(
            f'<a href="{url}" class="related-card"><div class="rc-title">{title}</div>'
            f'<div class="rc-sub">{sub}</div></a>'
        )
    return "\n                ".join(cards)


# ----------------------------------------------------------------------------
# Sub-page renderer
# ----------------------------------------------------------------------------
def render_subpage(p):
    faq_json = faq_schema(p["faq"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{p['desc']}">
    <meta name="keywords" content="{p['keywords']}">
    <title>{p['title']}</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/four-pillars/{p['id']}/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/four-pillars/{p['id']}/">

    <meta property="og:type" content="article">
    <meta property="og:title" content="{p['og_title']}">
    <meta property="og:description" content="{p['og_desc']}">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/four-pillars/{p['id']}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{p['og_title']}">
    <meta name="twitter:description" content="{p['og_desc']}">

    <meta name="google-adsense-account" content="{ADS}">
    {NAVER}

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{p['h1_plain']}",
        "description": "{p['desc']}",
        "url": "https://saju.gon.ai.kr/en/four-pillars/{p['id']}/",
        "datePublished": "{DATE}",
        "dateModified": "{DATE}",
        "inLanguage": "en",
        "publisher": {{ "@type": "Organization", "name": "Saju Astrology", "url": "https://saju.gon.ai.kr/" }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://saju.gon.ai.kr/en/" }},
                {{ "@type": "ListItem", "position": 2, "name": "Four Pillars", "item": "https://saju.gon.ai.kr/en/four-pillars/" }},
                {{ "@type": "ListItem", "position": 3, "name": "{p['crumb']}", "item": "https://saju.gon.ai.kr/en/four-pillars/{p['id']}/" }}
            ]
        }}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
        {faq_json}
        ]
    }}
    </script>

{head_common()}

    <style>
{ARTICLE_CSS}
    </style>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/en/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;"><span class="gold-text">Saju Astrology</span></h1>
            </a>
            {nav('fp')}
        </nav>
    </header>

    <main class="fp-page">
        <a href="/en/four-pillars/" class="back-link">&larr; Four Pillars Guide</a>

        <section class="fp-hero">
            <div class="fp-hanja">{p['hanja']}</div>
            <h1><span class="gold-text">{p['h1']}</span></h1>
            <p>{p['lead']}</p>
        </section>

{p['body']}

        <section class="related-links">
            <h2><span class="gold-text">Continue Learning</span></h2>
            <div class="related-grid">
                {related_block(p['id'])}
            </div>
        </section>

        <section class="cta-section" style="padding:var(--spacing-2xl) 0;text-align:center;">
            <h2 class="gold-text" style="font-size:var(--text-2xl);">Get Your Own BaZi Reading</h2>
            <p>Enter your birth date and time for a free Four Pillars (Saju) chart and personalized analysis.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

{footer()}

</body>
</html>'''


# ----------------------------------------------------------------------------
# Four Pillars hub
# ----------------------------------------------------------------------------
def render_fp_hub():
    concepts = [
        ("/en/four-pillars/day-master/", "日主", "Day Master", "The Heavenly Stem of your birth day — the single character that represents you."),
        ("/en/four-pillars/heavenly-stems/", "天干", "10 Heavenly Stems", "The ten celestial signs (Jia to Gui) that pair Yin/Yang with the five elements."),
        ("/en/four-pillars/earthly-branches/", "地支", "12 Earthly Branches", "The twelve signs behind the Chinese zodiac animals, each holding hidden stems."),
        ("/en/four-pillars/ten-gods/", "十神", "Ten Gods", "How every other character relates to your Day Master — wealth, power, support."),
        ("/en/four-pillars/luck-pillars/", "大運", "Luck Pillars", "The 10-year luck cycles and annual pillars that move your chart through time."),
        ("/en/four-pillars/reading-chart/", "看命", "Read a BaZi Chart", "A practical, step-by-step method to interpret any Four Pillars chart."),
    ]
    cards = []
    for url, hanja, title, desc in concepts:
        cards.append(f'''            <a href="{url}" class="concept-card">
                <span class="cc-hanja">{hanja}</span>
                <span class="cc-title">{title}</span>
                <span class="cc-desc">{desc}</span>
                <span class="cc-cta">Learn more &rarr;</span>
            </a>''')
    cards_html = "\n".join(cards)

    faq = [
        ("What is BaZi (Four Pillars of Destiny)?",
         "BaZi (八字, literally \"eight characters\") is a Chinese astrology system that maps your birth year, month, day, and hour into four pillars. Each pillar has one Heavenly Stem and one Earthly Branch, giving eight characters in total. Korean Saju (사주) is the same system. The chart describes your innate temperament, strengths, relationships, career direction, and the timing of opportunities and challenges."),
        ("Is BaZi the same as Korean Saju?",
         "Yes. Saju (사주, \"four pillars\") and BaZi (八字, \"eight characters\") refer to the same method. \"Four pillars\" counts the year/month/day/hour columns; \"eight characters\" counts the two characters in each column. Korea, China, and Vietnam share the system with small regional differences in interpretation."),
        ("How is BaZi different from Western astrology?",
         "Western astrology is built on the positions of planets across twelve zodiac constellations. BaZi is built on the Chinese solar calendar and the Five Elements (Wood, Fire, Earth, Metal, Water) expressed through ten Heavenly Stems and twelve Earthly Branches. BaZi focuses on the balance and interaction of elements over time rather than planetary aspects."),
        ("What do I need to calculate my BaZi chart?",
         "Your exact birth date and birth time (hour) plus birth location for time-zone accuracy. The hour pillar is essential — without an accurate birth time you lose one of the four pillars and a major part of the reading."),
        ("Can BaZi predict the future?",
         "BaZi does not claim fixed fate. It describes tendencies and timing — which elements are strong or weak in your chart and when the Luck Pillars activate them. It is best used as a decision-making and self-understanding tool, and is offered here for educational and entertainment purposes."),
    ]
    faq_json = faq_schema(faq)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="What is BaZi (Four Pillars of Destiny)? Complete beginner's guide to Chinese astrology &amp; Korean Saju — Day Master, Heavenly Stems, Earthly Branches, Ten Gods, and Luck Pillars explained.">
    <meta name="keywords" content="BaZi, four pillars of destiny, what is bazi, Chinese astrology, Korean Saju, bazi chart, eight characters, day master, heavenly stems, earthly branches, ten gods, bazi reading">
    <title>BaZi &amp; Four Pillars of Destiny — Complete Beginner's Guide | Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/four-pillars/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/four-pillars/">

    <meta property="og:type" content="website">
    <meta property="og:title" content="BaZi &amp; Four Pillars of Destiny — Complete Guide">
    <meta property="og:description" content="Learn Chinese astrology &amp; Korean Saju from scratch: Day Master, Heavenly Stems, Earthly Branches, Ten Gods, and Luck Pillars.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/four-pillars/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="BaZi &amp; Four Pillars of Destiny — Complete Guide">
    <meta name="twitter:description" content="Chinese astrology &amp; Korean Saju explained from scratch.">

    <meta name="google-adsense-account" content="{ADS}">
    {NAVER}

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "BaZi & Four Pillars of Destiny — Complete Guide",
        "description": "A complete beginner's guide to BaZi (Chinese astrology) and Korean Saju: Day Master, Heavenly Stems, Earthly Branches, Ten Gods, and Luck Pillars.",
        "url": "https://saju.gon.ai.kr/en/four-pillars/",
        "inLanguage": "en",
        "publisher": {{ "@type": "Organization", "name": "Saju Astrology", "url": "https://saju.gon.ai.kr/" }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://saju.gon.ai.kr/en/" }},
                {{ "@type": "ListItem", "position": 2, "name": "Four Pillars", "item": "https://saju.gon.ai.kr/en/four-pillars/" }}
            ]
        }}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
        {faq_json}
        ]
    }}
    </script>

{head_common()}

    <style>
{ARTICLE_CSS}
        .concept-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .concept-card {{ display: flex; flex-direction: column; gap: var(--spacing-xs); padding: var(--spacing-xl); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .concept-card:hover {{ border-color: var(--color-gold-muted); transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.18); }}
        .cc-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); }}
        .cc-title {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .cc-desc {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); }}
        .cc-cta {{ font-size: var(--text-xs); color: var(--color-gold); margin-top: var(--spacing-xs); }}
        .pillars-demo {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--spacing-sm); margin: var(--spacing-xl) 0; }}
        .pillar-col {{ text-align: center; padding: var(--spacing-md) var(--spacing-xs); background: var(--color-bg-tertiary); border-radius: var(--radius-lg); }}
        .pillar-col .pc-label {{ font-size: var(--text-xs); color: var(--color-text-tertiary); margin-bottom: var(--spacing-sm); }}
        .pillar-col .pc-stem {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-text); }}
        .pillar-col .pc-branch {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-text-primary); }}
        @media (max-width: 480px) {{ .pillars-demo {{ gap: 4px; }} .pillar-col {{ padding: var(--spacing-sm) 2px; }} }}
    </style>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/en/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;"><span class="gold-text">Saju Astrology</span></h1>
            </a>
            {nav('fp')}
        </nav>
    </header>

    <main class="fp-page">
        <section class="fp-hero">
            <div class="fp-hanja">四柱八字</div>
            <h1><span class="gold-text">BaZi &amp; the Four Pillars of Destiny</span></h1>
            <p>The complete beginner's guide to Chinese astrology and Korean Saju. Learn how your birth date and time become a chart of eight characters that maps your personality, relationships, career, and life timing.</p>
        </section>

        <section class="fp-section">
            <h2>What Are the Four Pillars?</h2>
            <p>Your <strong>BaZi (八字)</strong> — literally "eight characters" — is built from the moment you were born. Your birth <strong>year, month, day, and hour</strong> each become a <em>pillar</em>, and every pillar holds one <strong>Heavenly Stem (天干)</strong> on top and one <strong>Earthly Branch (地支)</strong> below. Four pillars × two characters = eight characters. In Korea this same chart is called <strong>Saju (사주)</strong>, meaning "four pillars."</p>
            <div class="pillars-demo">
                <div class="pillar-col"><div class="pc-label">Hour</div><div class="pc-stem">甲</div><div class="pc-branch">子</div></div>
                <div class="pillar-col"><div class="pc-label">Day</div><div class="pc-stem">丙</div><div class="pc-branch">午</div></div>
                <div class="pillar-col"><div class="pc-label">Month</div><div class="pc-stem">辛</div><div class="pc-branch">卯</div></div>
                <div class="pillar-col"><div class="pc-label">Year</div><div class="pc-stem">壬</div><div class="pc-branch">寅</div></div>
            </div>
            <p>Each character carries one of the <strong>Five Elements</strong> (Wood, Fire, Earth, Metal, Water) in a Yin or Yang form. A BaZi reading is essentially the study of how these eight elemental forces balance, support, and restrain one another.</p>
        </section>

        <section class="fp-section">
            <h2>The Building Blocks</h2>
            <p>Master these five concepts in order and you can read any BaZi chart. Start with your Day Master — it is the anchor of the entire reading.</p>
            <div class="concept-grid">
{cards_html}
            </div>
        </section>

        <section class="fp-callout">
            <h2 style="font-family:var(--font-heading);color:var(--color-gold-text);margin-bottom:var(--spacing-md);">BaZi vs. Western Astrology</h2>
            <p>Western astrology tracks planets moving through twelve zodiac constellations. BaZi instead uses the Chinese solar calendar and the Five Elements expressed through ten stems and twelve branches. Where Western charts emphasize planetary aspects and houses, BaZi emphasizes <strong>elemental balance and timing</strong> — which forces are strong or weak in you, and when the Luck Pillars bring them forward.</p>
            <p>That difference is why many people read both: the Western chart for psychological archetypes, the BaZi chart for elemental strategy and timing.</p>
        </section>

        <section class="fp-section">
            <h2>How a Reading Comes Together</h2>
            <ol>
                <li><strong>Cast the chart</strong> — convert your birth date and time into four pillars.</li>
                <li><strong>Find the Day Master</strong> — the day-pillar stem that represents you.</li>
                <li><strong>Judge its strength</strong> — is your Day Master well-supported or isolated?</li>
                <li><strong>Find favorable elements</strong> — the elements that bring your chart into balance.</li>
                <li><strong>Map the Ten Gods</strong> — see how wealth, authority, creativity, and support appear.</li>
                <li><strong>Layer the Luck Pillars</strong> — read how the chart unfolds across the decades.</li>
            </ol>
            <p>Our <a href="/en/four-pillars/reading-chart/" style="color:var(--color-gold);">step-by-step chart reading guide</a> walks through each stage with examples.</p>
        </section>

        <section class="related-links">
            <h2><span class="gold-text">Explore the Saju System</span></h2>
            <div class="related-grid">
                {related_block('four-pillars')}
            </div>
        </section>

        <section class="cta-section" style="padding:var(--spacing-2xl) 0;text-align:center;">
            <h2 class="gold-text" style="font-size:var(--text-2xl);">Calculate Your Free BaZi Chart</h2>
            <p>Enter your birth date and time to generate your Four Pillars (Saju) chart and a personalized reading.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

{footer()}

</body>
</html>'''


# ----------------------------------------------------------------------------
# English landing hub (/en/)
# ----------------------------------------------------------------------------
def render_en_home():
    sections = [
        ("/en/four-pillars/", "四柱", "Four Pillars (BaZi)", "Learn the Saju system from scratch — Day Master, stems, branches, Ten Gods, and Luck Pillars.", "Start the guide"),
        ("/en/zodiac/", "十二支", "Chinese Zodiac 2026", "Your animal sign's personality and 2026 (Year of the Fire Horse) fortune.", "Find your sign"),
        ("/en/five-elements/", "五行", "Five Elements", "Wood, Fire, Earth, Metal, Water — the energies behind every BaZi chart.", "Discover your element"),
        ("/en/compatibility/", "宮合", "Zodiac Compatibility", "Full love-match scores for all 12 zodiac signs based on Saju theory.", "Check your match"),
    ]
    cards = []
    for url, hanja, title, desc, cta in sections:
        cards.append(f'''            <a href="{url}" class="home-card">
                <span class="hc-hanja">{hanja}</span>
                <span class="hc-title">{title}</span>
                <span class="hc-desc">{desc}</span>
                <span class="hc-cta">{cta} &rarr;</span>
            </a>''')
    cards_html = "\n".join(cards)

    faq = [
        ("What is Saju (BaZi) astrology?",
         "Saju (사주), known in Chinese as BaZi (八字), is a traditional East Asian astrology system that turns your birth year, month, day, and hour into four pillars of eight characters. It reveals your elemental make-up, personality, relationships, and life timing through the Five Elements and the Chinese zodiac."),
        ("Is this site free?",
         "Yes. You can read every English guide on the Four Pillars, the Chinese zodiac, the Five Elements, and compatibility for free, and generate a free Saju (BaZi) chart from your birth details."),
        ("Do I need to read Korean to use this?",
         "No. This English section covers the full Saju system in English. A Korean version of the site is also available from the navigation if you prefer."),
    ]
    faq_json = faq_schema(faq)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="Saju &amp; BaZi astrology in English — free Four Pillars of Destiny readings, Chinese zodiac 2026, Five Elements, and zodiac compatibility. Learn Korean Saju from scratch.">
    <meta name="keywords" content="Saju, BaZi, four pillars of destiny, Chinese astrology English, Korean astrology, Chinese zodiac 2026, five elements, zodiac compatibility, free bazi reading">
    <title>Saju &amp; BaZi Astrology in English — Four Pillars, Zodiac &amp; Compatibility | Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/">
    <link rel="alternate" hreflang="ko" href="https://saju.gon.ai.kr/">
    <link rel="alternate" hreflang="x-default" href="https://saju.gon.ai.kr/">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Saju &amp; BaZi Astrology in English">
    <meta property="og:description" content="Free Four Pillars of Destiny readings, Chinese zodiac 2026, Five Elements, and compatibility — Korean Saju explained in English.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Saju &amp; BaZi Astrology in English">
    <meta name="twitter:description" content="Four Pillars, Chinese zodiac, Five Elements, and compatibility — in English.">

    <meta name="google-adsense-account" content="{ADS}">
    {NAVER}

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Saju Astrology (English)",
        "url": "https://saju.gon.ai.kr/en/",
        "inLanguage": "en",
        "description": "English guide to Korean Saju and Chinese BaZi astrology: Four Pillars, zodiac, Five Elements, and compatibility.",
        "publisher": {{ "@type": "Organization", "name": "Saju Astrology", "url": "https://saju.gon.ai.kr/" }}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
        {faq_json}
        ]
    }}
    </script>

{head_common()}

    <style>
{ARTICLE_CSS}
        .home-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .home-hero .hh-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); margin-bottom: var(--spacing-sm); }}
        .home-hero h1 {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-md); }}
        .home-hero p {{ color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 680px; margin: 0 auto var(--spacing-lg); line-height: var(--line-height-relaxed); }}
        .home-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .home-card {{ display: flex; flex-direction: column; gap: var(--spacing-xs); padding: var(--spacing-xl); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .home-card:hover {{ border-color: var(--color-gold-muted); transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.18); }}
        .hc-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); }}
        .hc-title {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .hc-desc {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); }}
        .hc-cta {{ font-size: var(--text-xs); color: var(--color-gold); margin-top: var(--spacing-xs); }}
    </style>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/en/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;"><span class="gold-text">Saju Astrology</span></h1>
            </a>
            {nav()}
        </nav>
    </header>

    <main class="fp-page">
        <section class="home-hero">
            <div class="hh-hanja">四柱命理</div>
            <h1><span class="gold-text">Korean Saju &amp; Chinese BaZi — in English</span></h1>
            <p>Discover the ancient East Asian astrology system that maps your destiny from your birth date and time. Free guides, charts, and readings for the Four Pillars, the Chinese zodiac, the Five Elements, and relationship compatibility.</p>
            <a href="/" class="cta-btn">Get a Free Saju Reading</a>
        </section>

        <div class="home-grid">
{cards_html}
        </div>

        <section class="fp-section">
            <h2>What Is Saju (BaZi)?</h2>
            <p><strong>Saju (사주)</strong> — "four pillars" — is the Korean name for the Chinese astrology system known as <strong>BaZi (八字)</strong>, or "eight characters." Your birth year, month, day, and hour each form a pillar of two characters, and the interplay of the Five Elements across those eight characters describes your temperament, talents, relationships, and the timing of your life.</p>
            <p>Unlike Western astrology, which follows the planets, Saju follows the Chinese solar calendar and the cycles of Wood, Fire, Earth, Metal, and Water. New to it? Begin with the <a href="/en/four-pillars/" style="color:var(--color-gold);">Four Pillars guide</a> and find your <a href="/en/zodiac/" style="color:var(--color-gold);">Chinese zodiac sign</a>.</p>
        </section>

        <section class="cta-section" style="padding:var(--spacing-2xl) 0;text-align:center;">
            <h2 class="gold-text" style="font-size:var(--text-2xl);">Ready to See Your Chart?</h2>
            <p>Generate your free Four Pillars (Saju) chart in seconds.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

{footer()}

</body>
</html>'''


# ----------------------------------------------------------------------------
# Content for the six sub-pages
# ----------------------------------------------------------------------------
def build_pages():
    pages = []

    # 1) Day Master --------------------------------------------------------
    pages.append({
        "id": "day-master",
        "crumb": "Day Master",
        "hanja": "日主 / 日元",
        "h1": "The Day Master (日主)",
        "h1_plain": "The Day Master in BaZi",
        "lead": "The Day Master is the single most important character in your BaZi chart — the Heavenly Stem of your birth day, and the symbol of you yourself.",
        "title": "Day Master in BaZi — What It Means &amp; How to Find Yours | Saju Astrology",
        "desc": "The Day Master (日主) is the BaZi character that represents you. Learn the 10 Day Masters, how to judge a strong vs weak Day Master, and find your favorable elements.",
        "keywords": "day master, bazi day master, what is my day master, day master element, strong vs weak day master, ri yuan, saju day master, favorable element bazi",
        "og_title": "The Day Master (日主) in BaZi — Complete Guide",
        "og_desc": "Your Day Master is the character that represents you. Learn the 10 types and how to judge its strength.",
        "body": '''        <section class="fp-section">
            <h2>What Is the Day Master?</h2>
            <p>When a BaZi chart is cast, the four pillars sit side by side: year, month, day, and hour. The <strong>top character of the day pillar</strong> — its Heavenly Stem — is called the <strong>Day Master (日主)</strong>, also known as the Day Element (日元) or <em>Ri Yuan</em>. Every other character in the chart is interpreted <em>in relation to this one stem</em>.</p>
            <p>If the chart is a story, the Day Master is the main character. It represents your core self: your basic nature, your instincts, and the lens through which wealth, relationships, authority, and creativity are measured.</p>
        </section>

        <section class="fp-section">
            <h2>The Ten Possible Day Masters</h2>
            <p>Because there are ten Heavenly Stems, there are ten possible Day Masters — each one a Yin or Yang form of one of the Five Elements.</p>
            <table class="fp-table">
                <thead><tr><th>Day Master</th><th>Element &amp; Polarity</th><th>Classic Image</th><th>Core Nature</th></tr></thead>
                <tbody>
                    <tr><td>甲 Jia</td><td>Yang Wood</td><td>Tall tree</td><td>Upright, pioneering, principled</td></tr>
                    <tr><td>乙 Yi</td><td>Yin Wood</td><td>Grass, vine</td><td>Adaptable, gentle, resilient</td></tr>
                    <tr><td>丙 Bing</td><td>Yang Fire</td><td>The sun</td><td>Warm, expressive, generous</td></tr>
                    <tr><td>丁 Ding</td><td>Yin Fire</td><td>Candle, lamp</td><td>Focused, thoughtful, sensitive</td></tr>
                    <tr><td>戊 Wu</td><td>Yang Earth</td><td>Mountain</td><td>Steady, reliable, protective</td></tr>
                    <tr><td>己 Ji</td><td>Yin Earth</td><td>Garden soil</td><td>Nurturing, practical, flexible</td></tr>
                    <tr><td>庚 Geng</td><td>Yang Metal</td><td>Axe, sword</td><td>Decisive, just, action-oriented</td></tr>
                    <tr><td>辛 Xin</td><td>Yin Metal</td><td>Jewelry, gem</td><td>Refined, precise, image-aware</td></tr>
                    <tr><td>壬 Ren</td><td>Yang Water</td><td>Ocean, river</td><td>Dynamic, resourceful, far-seeing</td></tr>
                    <tr><td>癸 Gui</td><td>Yin Water</td><td>Dew, rain</td><td>Intuitive, quiet, penetrating</td></tr>
                </tbody>
            </table>
            <p>Read the full personalities on the <a href="/en/four-pillars/heavenly-stems/" style="color:var(--color-gold);">Ten Heavenly Stems</a> page.</p>
        </section>

        <section class="fp-section">
            <h2>Strong vs. Weak Day Master</h2>
            <p>The most important judgment in a reading is whether your Day Master is <strong>strong (身強)</strong> or <strong>weak (身弱)</strong>. This is not about being "good" or "bad" — it decides which elements help you and which drain you. A Day Master is considered stronger when:</p>
            <ul>
                <li><strong>It is born in a supportive season</strong> — for example, a Wood Day Master born in spring.</li>
                <li><strong>It has the same element nearby</strong> — companions reinforce it (see Friends &amp; Rob Wealth in the Ten Gods).</li>
                <li><strong>It receives a Resource element</strong> — the element that produces it (Water produces Wood, and so on).</li>
                <li><strong>It is rooted in the branches</strong> — the same or supporting element hides inside the Earthly Branches.</li>
            </ul>
            <p>It is weaker when the chart is dominated by the elements it produces, controls, or is controlled by, with little support of its own.</p>
        </section>

        <section class="fp-callout">
            <h2 style="font-family:var(--font-heading);color:var(--color-gold-text);margin-bottom:var(--spacing-md);">Favorable &amp; Unfavorable Elements (用神)</h2>
            <p>Once strength is known, you can find your <strong>favorable elements (用神, Yong Shen)</strong> — the ones that bring the chart into balance.</p>
            <p>A <strong>strong</strong> Day Master already has plenty of support, so it benefits from elements that <em>release</em> energy: Output (what it produces), Wealth (what it controls), and Authority (what controls it). A <strong>weak</strong> Day Master needs <em>reinforcement</em>: Resource (what produces it) and Companions (its own element). Your favorable elements guide everything from lucky colors to good timing.</p>
        </section>''',
        "faq": [
            ("What is a Day Master in BaZi?",
             "The Day Master (日主) is the Heavenly Stem of your birth day — the character in a BaZi chart that represents you. All other characters are read in relation to it, which is why finding your Day Master is the first step in any reading."),
            ("How do I find my Day Master?",
             "Cast your BaZi chart from your birth date and time, then look at the top character of the day pillar. That Heavenly Stem (one of Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin, Ren, or Gui) is your Day Master."),
            ("What does a strong or weak Day Master mean?",
             "A strong Day Master is well-supported by its season, by companions of the same element, and by Resource elements that produce it. A weak Day Master lacks that support. Strength is neutral — it simply determines which elements are favorable for you."),
            ("Is a strong Day Master better than a weak one?",
             "No. Neither is better. A balanced chart is the goal. A strong Day Master thrives on elements that release energy (output, wealth, authority); a weak Day Master thrives on elements that reinforce it (resource and companions)."),
            ("What are favorable elements (Yong Shen)?",
             "Favorable elements (用神) are the elements that bring your chart into balance based on your Day Master's strength. They inform timing, career direction, and even lucky colors, and they are activated as the Luck Pillars move through the decades."),
        ],
    })

    # 2) Heavenly Stems -----------------------------------------------------
    pages.append({
        "id": "heavenly-stems",
        "crumb": "Heavenly Stems",
        "hanja": "天干",
        "h1": "The 10 Heavenly Stems (天干)",
        "h1_plain": "The Ten Heavenly Stems in BaZi",
        "lead": "The ten Heavenly Stems are the celestial half of every pillar — the Five Elements split into Yang and Yin, each with a vivid personality of its own.",
        "title": "The 10 Heavenly Stems (天干) — Jia to Gui Explained | Saju Astrology",
        "desc": "Complete guide to the 10 Heavenly Stems (天干) of BaZi and Saju: Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin, Ren, Gui — element, Yin/Yang polarity, and personality of each.",
        "keywords": "heavenly stems, ten heavenly stems, tian gan, bazi stems, jia yi bing ding, yang wood yin wood, heavenly stems meaning, saju cheongan",
        "og_title": "The 10 Heavenly Stems (天干) Explained",
        "og_desc": "Jia to Gui — the Five Elements in Yang and Yin form. Element, polarity, and personality of each stem.",
        "body": '''        <section class="fp-section">
            <h2>What Are the Heavenly Stems?</h2>
            <p>The <strong>ten Heavenly Stems (天干, Tian Gan)</strong> are the "sky" layer of a BaZi chart. They take the Five Elements — Wood, Fire, Earth, Metal, Water — and split each into a <strong>Yang</strong> (active, outward) and a <strong>Yin</strong> (receptive, refined) form, giving ten distinct signs. The top character of each of your four pillars is a Heavenly Stem, and the day-pillar stem is your <a href="/en/four-pillars/day-master/" style="color:var(--color-gold);">Day Master</a>.</p>
        </section>

        <section class="fp-section">
            <h2>The Ten Stems at a Glance</h2>
            <table class="fp-table">
                <thead><tr><th>Stem</th><th>Korean</th><th>Element</th><th>Polarity</th><th>Image</th></tr></thead>
                <tbody>
                    <tr><td>甲 Jia</td><td>갑</td><td>Wood</td><td>Yang</td><td>Tall tree, beam</td></tr>
                    <tr><td>乙 Yi</td><td>을</td><td>Wood</td><td>Yin</td><td>Grass, flowers, vine</td></tr>
                    <tr><td>丙 Bing</td><td>병</td><td>Fire</td><td>Yang</td><td>The sun</td></tr>
                    <tr><td>丁 Ding</td><td>정</td><td>Fire</td><td>Yin</td><td>Candle, lamp, starlight</td></tr>
                    <tr><td>戊 Wu</td><td>무</td><td>Earth</td><td>Yang</td><td>Mountain, wall</td></tr>
                    <tr><td>己 Ji</td><td>기</td><td>Earth</td><td>Yin</td><td>Field, garden soil</td></tr>
                    <tr><td>庚 Geng</td><td>경</td><td>Metal</td><td>Yang</td><td>Axe, sword, raw ore</td></tr>
                    <tr><td>辛 Xin</td><td>신</td><td>Metal</td><td>Yin</td><td>Jewelry, fine blade</td></tr>
                    <tr><td>壬 Ren</td><td>임</td><td>Water</td><td>Yang</td><td>Ocean, great river</td></tr>
                    <tr><td>癸 Gui</td><td>계</td><td>Water</td><td>Yin</td><td>Dew, rain, mist</td></tr>
                </tbody>
            </table>
        </section>

        <section class="fp-section">
            <h2>Personality of Each Stem</h2>
            <h3>Wood — 甲 Jia &amp; 乙 Yi</h3>
            <p><strong>甲 Yang Wood</strong> is the tall, straight tree: upright, ambitious, and principled, a natural pioneer who grows toward the light. <strong>乙 Yin Wood</strong> is grass and vine: flexible, sociable, and quietly persistent, bending without breaking.</p>
            <h3>Fire — 丙 Bing &amp; 丁 Ding</h3>
            <p><strong>丙 Yang Fire</strong> is the sun: radiant, warm, generous, and impossible to ignore. <strong>丁 Yin Fire</strong> is candlelight: focused, considerate, and illuminating in a quiet, personal way.</p>
            <h3>Earth — 戊 Wu &amp; 己 Ji</h3>
            <p><strong>戊 Yang Earth</strong> is the mountain: dependable, steady, and protective. <strong>己 Yin Earth</strong> is cultivated soil: nurturing, resourceful, and endlessly accommodating.</p>
            <h3>Metal — 庚 Geng &amp; 辛 Xin</h3>
            <p><strong>庚 Yang Metal</strong> is the axe or sword: decisive, just, and direct. <strong>辛 Yin Metal</strong> is jewelry: refined, precise, and attentive to beauty and reputation.</p>
            <h3>Water — 壬 Ren &amp; 癸 Gui</h3>
            <p><strong>壬 Yang Water</strong> is the ocean: dynamic, broad-minded, and resourceful. <strong>癸 Yin Water</strong> is dew and rain: gentle, intuitive, and quietly penetrating.</p>
        </section>

        <section class="fp-callout">
            <p>Stems combine and clash with one another in set patterns (for example, Jia and Ji form an Earth combination). These interactions, together with the <a href="/en/four-pillars/earthly-branches/" style="color:var(--color-gold);">Earthly Branches</a> below them, are what give each chart its unique texture.</p>
        </section>''',
        "faq": [
            ("What are the 10 Heavenly Stems?",
             "The ten Heavenly Stems (天干) are Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin, Ren, and Gui. They represent the Five Elements (Wood, Fire, Earth, Metal, Water) each split into a Yang and a Yin form, and they sit on top of each pillar in a BaZi chart."),
            ("What is the difference between Yang and Yin stems?",
             "Yang stems (Jia, Bing, Wu, Geng, Ren) are active and outward — the tree, the sun, the mountain, the sword, the ocean. Yin stems (Yi, Ding, Ji, Xin, Gui) are receptive and refined — the vine, the candle, the soil, the jewel, the dew. Both express the same element differently."),
            ("How do Heavenly Stems relate to the Day Master?",
             "The Heavenly Stem of your day pillar is your Day Master, the character that represents you. The other stems in the chart are read in relation to it through the Ten Gods system."),
            ("Are Heavenly Stems the same in Korean Saju?",
             "Yes. In Korean Saju the Heavenly Stems are called Cheongan (천간) and use the same ten characters and meanings. Saju and BaZi share the same underlying system."),
            ("Which element is my Heavenly Stem?",
             "Jia and Yi are Wood; Bing and Ding are Fire; Wu and Ji are Earth; Geng and Xin are Metal; Ren and Gui are Water. The first of each pair is Yang and the second is Yin."),
        ],
    })

    # 3) Earthly Branches ---------------------------------------------------
    pages.append({
        "id": "earthly-branches",
        "crumb": "Earthly Branches",
        "hanja": "地支",
        "h1": "The 12 Earthly Branches (地支)",
        "h1_plain": "The Twelve Earthly Branches in BaZi",
        "lead": "The twelve Earthly Branches are the ground layer of your chart — the signs behind the Chinese zodiac animals, each one a season, a direction, and a set of hidden stems.",
        "title": "The 12 Earthly Branches (地支) — Zodiac, Element &amp; Hidden Stems | Saju Astrology",
        "desc": "Complete guide to the 12 Earthly Branches (地支) of BaZi: their zodiac animals, elements, seasons, months, and hidden stems. The foundation of the Chinese zodiac and Saju.",
        "keywords": "earthly branches, twelve earthly branches, di zhi, bazi branches, hidden stems, earthly branches zodiac, saju jiji, branch element, earthly branch hidden stems",
        "og_title": "The 12 Earthly Branches (地支) Explained",
        "og_desc": "The signs behind the Chinese zodiac — element, season, and hidden stems of each branch.",
        "body": '''        <section class="fp-section">
            <h2>What Are the Earthly Branches?</h2>
            <p>The <strong>twelve Earthly Branches (地支, Di Zhi)</strong> are the "ground" layer of a BaZi chart, sitting beneath the <a href="/en/four-pillars/heavenly-stems/" style="color:var(--color-gold);">Heavenly Stems</a> in each pillar. Most people meet them first as the twelve <a href="/en/zodiac/" style="color:var(--color-gold);">Chinese zodiac animals</a> — Rat, Ox, Tiger, and so on — but in BaZi each branch is much richer: it carries an element, a season, a compass direction, and one or more <strong>hidden stems</strong> tucked inside.</p>
        </section>

        <section class="fp-section">
            <h2>The Twelve Branches in Full</h2>
            <table class="fp-table">
                <thead><tr><th>Branch</th><th>Animal</th><th>Element</th><th>Season / Month</th><th>Hidden Stems</th></tr></thead>
                <tbody>
                    <tr><td>子 Zi</td><td>Rat</td><td>Yang Water</td><td>Winter / Dec</td><td>癸</td></tr>
                    <tr><td>丑 Chou</td><td>Ox</td><td>Yin Earth</td><td>Winter / Jan</td><td>己 癸 辛</td></tr>
                    <tr><td>寅 Yin</td><td>Tiger</td><td>Yang Wood</td><td>Spring / Feb</td><td>甲 丙 戊</td></tr>
                    <tr><td>卯 Mao</td><td>Rabbit</td><td>Yin Wood</td><td>Spring / Mar</td><td>乙</td></tr>
                    <tr><td>辰 Chen</td><td>Dragon</td><td>Yang Earth</td><td>Spring / Apr</td><td>戊 乙 癸</td></tr>
                    <tr><td>巳 Si</td><td>Snake</td><td>Yin Fire</td><td>Summer / May</td><td>丙 庚 戊</td></tr>
                    <tr><td>午 Wu</td><td>Horse</td><td>Yang Fire</td><td>Summer / Jun</td><td>丁 己</td></tr>
                    <tr><td>未 Wei</td><td>Goat</td><td>Yin Earth</td><td>Summer / Jul</td><td>己 丁 乙</td></tr>
                    <tr><td>申 Shen</td><td>Monkey</td><td>Yang Metal</td><td>Autumn / Aug</td><td>庚 壬 戊</td></tr>
                    <tr><td>酉 You</td><td>Rooster</td><td>Yin Metal</td><td>Autumn / Sep</td><td>辛</td></tr>
                    <tr><td>戌 Xu</td><td>Dog</td><td>Yang Earth</td><td>Autumn / Oct</td><td>戊 辛 丁</td></tr>
                    <tr><td>亥 Hai</td><td>Pig</td><td>Yin Water</td><td>Winter / Nov</td><td>壬 甲</td></tr>
                </tbody>
            </table>
        </section>

        <section class="fp-section">
            <h2>Hidden Stems (藏干)</h2>
            <p>Each branch secretly stores one to three Heavenly Stems, called <strong>hidden stems (藏干)</strong>. They are the reason a branch can act like more than one element. The Tiger (寅), for instance, hides Yang Wood, Yang Fire, and Yang Earth — so although the Tiger is "a Wood branch," it can also feed Fire. Hidden stems are essential for judging the real strength of your Day Master, because a stem with roots in the branches is far more powerful than one standing alone.</p>
        </section>

        <section class="fp-callout">
            <h2 style="font-family:var(--font-heading);color:var(--color-gold-text);margin-bottom:var(--spacing-md);">Seasons &amp; Combinations</h2>
            <p>The branches map onto the seasons in groups of three: <strong>寅卯辰</strong> = spring (Wood), <strong>巳午未</strong> = summer (Fire), <strong>申酉戌</strong> = autumn (Metal), <strong>亥子丑</strong> = winter (Water). The same season-mates also form "directional" combinations, while other triplets create the famous <strong>Three Harmonies</strong> used in <a href="/en/compatibility/" style="color:var(--color-gold);">zodiac compatibility</a>. Branches can also clash, harm, or punish one another — the dynamics that make a chart come alive.</p>
        </section>''',
        "faq": [
            ("What are the 12 Earthly Branches?",
             "The twelve Earthly Branches (地支) are Zi, Chou, Yin, Mao, Chen, Si, Wu, Wei, Shen, You, Xu, and Hai. They correspond to the twelve Chinese zodiac animals (Rat through Pig) and sit at the bottom of each pillar in a BaZi chart."),
            ("What are hidden stems?",
             "Hidden stems (藏干) are the Heavenly Stems stored inside each Earthly Branch — one to three per branch. They let a branch express more than one element and are used to judge the true strength of the Day Master, since a rooted stem is much stronger than an isolated one."),
            ("Are Earthly Branches the same as the Chinese zodiac?",
             "The twelve zodiac animals ARE the twelve Earthly Branches in their popular form. Zi is the Rat, Chou is the Ox, and so on. In BaZi the branches add elements, seasons, directions, and hidden stems to those familiar animal signs."),
            ("What element is each Earthly Branch?",
             "Zi is Water, Chou is Earth, Yin and Mao are Wood, Chen is Earth, Si and Wu are Fire, Wei is Earth, Shen and You are Metal, Xu is Earth, and Hai is Water. The four Earth branches (Chou, Chen, Wei, Xu) sit between the seasons."),
            ("What is the Korean name for Earthly Branches?",
             "In Korean Saju the Earthly Branches are called Jiji (지지). They use the same twelve characters and zodiac animals as Chinese BaZi."),
        ],
    })

    # 4) Ten Gods -----------------------------------------------------------
    pages.append({
        "id": "ten-gods",
        "crumb": "Ten Gods",
        "hanja": "十神",
        "h1": "The Ten Gods (十神)",
        "h1_plain": "The Ten Gods in BaZi",
        "lead": "The Ten Gods translate raw elements into real-life meaning — wealth, authority, creativity, support, and rivalry — by measuring how every character relates to your Day Master.",
        "title": "The Ten Gods (十神) in BaZi — Wealth, Officer &amp; Resource Explained | Saju Astrology",
        "desc": "Complete guide to the Ten Gods (十神) of BaZi: Friend, Rob Wealth, Eating God, Hurting Officer, Wealth, Officer, Seven Killings, and Resource. What each god means in a reading.",
        "keywords": "ten gods, ten gods bazi, shi shen, bazi ten gods meaning, direct wealth, seven killings, eating god, hurting officer, direct officer, resource star, ten gods saju",
        "og_title": "The Ten Gods (十神) in BaZi Explained",
        "og_desc": "Wealth, authority, creativity, support, and rivalry — how every character relates to your Day Master.",
        "body": '''        <section class="fp-section">
            <h2>What Are the Ten Gods?</h2>
            <p>Elements on their own are abstract. The <strong>Ten Gods (十神, Shi Shen)</strong> turn them into life themes. Each Heavenly Stem and hidden stem in your chart is compared to your <a href="/en/four-pillars/day-master/" style="color:var(--color-gold);">Day Master</a> in two ways — <em>which of the five relationships</em> it has (same, produced-by-me, controlled-by-me, controls-me, produces-me) and <em>whether the polarity matches or differs</em>. Five relationships × two polarities = ten gods.</p>
        </section>

        <section class="fp-section">
            <h2>The Five Relationships, Ten Gods</h2>
            <table class="fp-table">
                <thead><tr><th>Relationship to Day Master</th><th>Same Polarity</th><th>Opposite Polarity</th><th>Life Theme</th></tr></thead>
                <tbody>
                    <tr><td>Same element (peers)</td><td>比肩 Friend</td><td>劫財 Rob Wealth</td><td>Self, rivals, allies</td></tr>
                    <tr><td>Element I produce (output)</td><td>食神 Eating God</td><td>傷官 Hurting Officer</td><td>Talent, expression, creativity</td></tr>
                    <tr><td>Element I control (wealth)</td><td>偏財 Indirect Wealth</td><td>正財 Direct Wealth</td><td>Money, resources, desire</td></tr>
                    <tr><td>Element that controls me (officer)</td><td>七殺 Seven Killings</td><td>正官 Direct Officer</td><td>Authority, pressure, status</td></tr>
                    <tr><td>Element that produces me (resource)</td><td>偏印 Indirect Resource</td><td>正印 Direct Resource</td><td>Support, learning, protection</td></tr>
                </tbody>
            </table>
        </section>

        <section class="fp-section">
            <h2>What Each God Means</h2>
            <h3>Companions — Friend (比肩) &amp; Rob Wealth (劫財)</h3>
            <p>The same element as you. <strong>Friend</strong> brings allies, independence, and self-confidence. <strong>Rob Wealth</strong> brings competition and boldness, and can scatter money if unchecked. For a weak Day Master, companions are welcome support; for a strong one, they add pressure.</p>
            <h3>Output — Eating God (食神) &amp; Hurting Officer (傷官)</h3>
            <p>What you produce: talent and self-expression. <strong>Eating God</strong> is gentle, enjoyable creativity and a love of life's pleasures. <strong>Hurting Officer</strong> is brilliant, performative, and rule-breaking — dazzling but prone to clashing with authority.</p>
            <h3>Wealth — Direct Wealth (正財) &amp; Indirect Wealth (偏財)</h3>
            <p>What you control. <strong>Direct Wealth</strong> is steady, earned income and a faithful partner (for men, often the wife star). <strong>Indirect Wealth</strong> is windfall, business, and opportunity — bigger upside, more volatility.</p>
            <h3>Officer — Direct Officer (正官) &amp; Seven Killings (七殺)</h3>
            <p>What controls you. <strong>Direct Officer</strong> is legitimate authority, reputation, and discipline (for women, often the husband star). <strong>Seven Killings</strong> is raw power, drive, and challenge — formidable when tamed, harsh when not.</p>
            <h3>Resource — Direct Resource (正印) &amp; Indirect Resource (偏印)</h3>
            <p>What produces you. <strong>Direct Resource</strong> is nurturing support, education, and the mother star — protection and learning. <strong>Indirect Resource</strong> is unconventional knowledge, intuition, and specialized skill.</p>
        </section>

        <section class="fp-callout">
            <p>No god is purely "good" or "bad." A Seven Killings can mean a tyrant or a fearless leader; Direct Wealth can mean stability or stagnation. The verdict depends on whether the god is a <a href="/en/four-pillars/day-master/" style="color:var(--color-gold);">favorable element</a> for your particular Day Master — which is exactly what a full reading determines.</p>
        </section>''',
        "faq": [
            ("What are the Ten Gods in BaZi?",
             "The Ten Gods (十神) are Friend, Rob Wealth, Eating God, Hurting Officer, Direct Wealth, Indirect Wealth, Direct Officer, Seven Killings, Direct Resource, and Indirect Resource. They describe how each character in your chart relates to your Day Master, translating elements into themes like wealth, authority, and creativity."),
            ("How are the Ten Gods calculated?",
             "Compare each stem to your Day Master in two ways: the five-element relationship (same element, what it produces, what it controls, what controls it, what produces it) and whether the Yin/Yang polarity matches. Five relationships times two polarities gives the ten gods."),
            ("Which Ten God represents money?",
             "Wealth is represented by Direct Wealth (正財) — steady, earned income — and Indirect Wealth (偏財) — windfalls and business opportunities. Whether wealth is easy to keep depends on your Day Master's strength and favorable elements."),
            ("What is the Seven Killings (七殺)?",
             "Seven Killings (七殺), or Indirect Officer, is the element that controls your Day Master with the same polarity. It represents raw power, drive, and challenge. Well-managed it makes a fearless leader; unmanaged it brings pressure and conflict."),
            ("Are any Ten Gods bad?",
             "No god is inherently good or bad. Each can be a strength or a weakness depending on whether it is a favorable element for your Day Master. A balanced chart matters more than any single god."),
        ],
    })

    # 5) Luck Pillars -------------------------------------------------------
    pages.append({
        "id": "luck-pillars",
        "crumb": "Luck Pillars",
        "hanja": "大運",
        "h1": "Luck Pillars (大運)",
        "h1_plain": "Luck Pillars and Annual Timing in BaZi",
        "lead": "Your natal chart is the map; the Luck Pillars are the journey. These 10-year cycles, with the annual pillars on top, show when your chart's potential is activated.",
        "title": "Luck Pillars (大運) in BaZi — 10-Year Cycles &amp; Annual Timing | Saju Astrology",
        "desc": "Understand Luck Pillars (大運, Da Yun) in BaZi: how the 10-year luck cycles are derived, which direction they run, and how annual pillars (流年) layer timing onto your chart.",
        "keywords": "luck pillars, da yun, bazi luck pillars, 10 year luck cycle, annual pillar, liu nian, bazi timing, luck cycle bazi, saju daeun",
        "og_title": "Luck Pillars (大運) in BaZi Explained",
        "og_desc": "The 10-year luck cycles and annual pillars that move your chart through time.",
        "body": '''        <section class="fp-section">
            <h2>What Are Luck Pillars?</h2>
            <p>Your four pillars never change — they are fixed at birth. But life clearly has seasons of ease and seasons of struggle. BaZi explains this with the <strong>Luck Pillars (大運, Da Yun)</strong>: a sequence of ten-year periods, each represented by its own Heavenly Stem and Earthly Branch, that wash over your natal chart and switch different elements on and off.</p>
            <p>When a Luck Pillar brings in an element that is <a href="/en/four-pillars/day-master/" style="color:var(--color-gold);">favorable</a> for your Day Master, that decade tends to flow. When it brings an unfavorable element, the same decade asks for more caution and effort.</p>
        </section>

        <section class="fp-section">
            <h2>How Luck Pillars Are Derived</h2>
            <p>Luck Pillars are calculated from the <strong>month pillar</strong>, then counted forward or backward through the cycle of stems and branches:</p>
            <ul>
                <li><strong>Direction</strong> depends on your gender and the Yin/Yang polarity of your birth-year stem. Yang-year men and Yin-year women count <em>forward</em>; Yin-year men and Yang-year women count <em>backward</em>.</li>
                <li><strong>Starting age</strong> is found by measuring the distance from your birth to the nearest solar term, so most people begin their first Luck Pillar somewhere between ages 1 and 10.</li>
                <li><strong>Each pillar then lasts about ten years</strong>, stepping one stem-branch pair along the cycle.</li>
            </ul>
            <p>This is why two people born on the same day can live very differently — their Luck Pillars may run in opposite directions and activate opposite elements.</p>
        </section>

        <section class="fp-callout">
            <h2 style="font-family:var(--font-heading);color:var(--color-gold-text);margin-bottom:var(--spacing-md);">Annual Pillars (流年)</h2>
            <p>On top of the slow ten-year cycle sits the <strong>annual pillar (流年, Liu Nian)</strong> — the stem and branch of each calendar year. For example, <strong>2026 is the year of 丙午 (Yang Fire Horse)</strong>, a strongly Fire year. To read a specific year you stack three layers: your natal chart, your current Luck Pillar, and that year's annual pillar, then see which elements combine, clash, or reinforce one another.</p>
        </section>

        <section class="fp-section">
            <h2>Reading Timing Well</h2>
            <p>Good timing analysis is less about "lucky vs. unlucky" and more about <strong>alignment</strong>. A favorable Luck Pillar is the season to push — launch, invest, commit. An unfavorable one is the season to build foundations, protect what you have, and avoid over-extending. Combine the decade view with the annual view, and you get a practical calendar for major decisions. See it applied in our <a href="/en/four-pillars/reading-chart/" style="color:var(--color-gold);">chart reading walkthrough</a>.</p>
        </section>''',
        "faq": [
            ("What are Luck Pillars in BaZi?",
             "Luck Pillars (大運, Da Yun) are ten-year periods, each with its own Heavenly Stem and Earthly Branch, that move across your fixed natal chart over a lifetime. They activate favorable or unfavorable elements and explain why life has distinct seasons."),
            ("How are Luck Pillars calculated?",
             "They are derived from your month pillar. The direction (forward or backward through the cycle) depends on your gender and birth-year polarity, and the starting age comes from the distance between your birth and the nearest solar term. Each pillar then lasts about ten years."),
            ("What is an annual pillar (Liu Nian)?",
             "The annual pillar (流年) is the Heavenly Stem and Earthly Branch of a given calendar year. For example, 2026 is Bing-Wu, the Yang Fire Horse. Reading a specific year stacks your natal chart, your current Luck Pillar, and that year's annual pillar."),
            ("Why do two people born the same day have different lives?",
             "Because their Luck Pillars can run in opposite directions and start at different ages, based on gender and birth-year polarity. The same natal chart unfolds through different decade-by-decade timing."),
            ("Can Luck Pillars tell me my best years?",
             "They indicate which decades and years bring in elements favorable to your Day Master — seasons that tend to support growth — versus those that call for caution. They describe timing and tendencies, not fixed outcomes, and are for guidance and entertainment."),
        ],
    })

    # 6) Reading a chart ----------------------------------------------------
    pages.append({
        "id": "reading-chart",
        "crumb": "Read a Chart",
        "hanja": "看命",
        "h1": "How to Read a BaZi Chart",
        "h1_plain": "How to Read a BaZi Chart Step by Step",
        "lead": "Six clear steps take you from a wall of unfamiliar characters to a meaningful reading. Here is the method professionals use, in plain English.",
        "title": "How to Read a BaZi Chart — A Step-by-Step Beginner's Guide | Saju Astrology",
        "desc": "Learn how to read a BaZi (Four Pillars / Saju) chart step by step: cast the chart, find the Day Master, judge its strength, find favorable elements, map the Ten Gods, and read Luck Pillars.",
        "keywords": "how to read a bazi chart, read bazi chart, bazi chart reading, interpret bazi, bazi for beginners, how to read saju, four pillars reading, bazi analysis steps",
        "og_title": "How to Read a BaZi Chart — Step by Step",
        "og_desc": "Six clear steps from unfamiliar characters to a meaningful Four Pillars reading.",
        "body": '''        <section class="fp-section">
            <h2>Before You Start</h2>
            <p>You need an accurate <strong>birth date and time</strong> (and ideally birth location for time-zone precision). With those, a calculator casts your four pillars. From there, reading is a repeatable six-step process — the same order whether you call it BaZi or <a href="/en/four-pillars/" style="color:var(--color-gold);">Saju</a>.</p>
        </section>

        <section class="fp-section">
            <h2>Step 1 — Cast the Four Pillars</h2>
            <p>Convert your birth moment into four pillars (year, month, day, hour), each with a <a href="/en/four-pillars/heavenly-stems/" style="color:var(--color-gold);">Heavenly Stem</a> and an <a href="/en/four-pillars/earthly-branches/" style="color:var(--color-gold);">Earthly Branch</a>. Note the element and polarity of all eight characters, and list the hidden stems inside each branch.</p>

            <h2>Step 2 — Find Your Day Master</h2>
            <p>Locate the stem on top of the <strong>day pillar</strong>. This is your <a href="/en/four-pillars/day-master/" style="color:var(--color-gold);">Day Master</a> — the character that represents you. Everything else is read in relation to it.</p>

            <h2>Step 3 — Judge the Day Master's Strength</h2>
            <p>Ask three questions: Is the Day Master <strong>born in a supportive season</strong> (the month branch matters most)? Does it have <strong>companions</strong> of the same element? Is it <strong>rooted</strong> in the hidden stems of the branches and fed by Resource? Many supports means a <em>strong</em> Day Master; few means a <em>weak</em> one.</p>

            <h2>Step 4 — Find the Favorable Elements</h2>
            <p>Use the strength verdict to pick your <strong>favorable elements (用神)</strong>. A strong Day Master wants elements that release energy — Output, Wealth, Officer. A weak Day Master wants elements that reinforce it — Resource and Companions. These favorable elements are the key to the whole chart.</p>

            <h2>Step 5 — Map the Ten Gods</h2>
            <p>Label every other character with its <a href="/en/four-pillars/ten-gods/" style="color:var(--color-gold);">Ten God</a>. Now the chart speaks in life terms: where wealth sits, whether authority is supportive, how strong your self-expression is, and how much support you receive. Pay special attention to whether your favorable elements appear as helpful gods.</p>

            <h2>Step 6 — Layer the Luck Pillars</h2>
            <p>Finally, bring in the <a href="/en/four-pillars/luck-pillars/" style="color:var(--color-gold);">Luck Pillars</a> and the current annual pillar. See which favorable or unfavorable elements each decade and year brings in. This turns a static portrait into a timeline you can actually plan around.</p>
        </section>

        <section class="fp-callout">
            <h2 style="font-family:var(--font-heading);color:var(--color-gold-text);margin-bottom:var(--spacing-md);">A Quick Worked Example</h2>
            <p>Suppose your Day Master is <strong>丙 (Yang Fire)</strong>, born in winter (a Water season). Fire is weak in winter and likely needs support, so <strong>Wood</strong> (which feeds Fire) and more <strong>Fire</strong> become favorable, while too much Water is a challenge. When a Luck Pillar or year brings strong Wood or Fire, expect momentum; when it floods the chart with Water, slow down and protect your base. That single thread — strength, then favorable elements, then timing — is the heart of every reading.</p>
        </section>

        <section class="fp-section">
            <h2>Keep Practicing</h2>
            <p>Reading charts is a skill that grows with repetition. Start with your own chart, then those of people you know well, and check the interpretations against real life. When you want the calculation done for you, generate a free <a href="/" style="color:var(--color-gold);">Saju (BaZi) chart</a> and use these six steps to read it.</p>
        </section>''',
        "faq": [
            ("How do I read a BaZi chart for beginners?",
             "Follow six steps: cast the four pillars, find your Day Master, judge its strength, determine your favorable elements, map the Ten Gods, and layer the Luck Pillars. Working in that order turns unfamiliar characters into a meaningful reading."),
            ("What is the first step in reading a BaZi chart?",
             "Cast the four pillars from your birth date and time, then find your Day Master — the Heavenly Stem on top of the day pillar. The Day Master is the anchor for everything else in the reading."),
            ("How do I know if my Day Master is strong or weak?",
             "Check whether it is born in a supportive season (especially the month branch), whether it has companions of the same element, and whether it is rooted in the branches and fed by Resource. Many supports mean strong; few mean weak."),
            ("Do I need my birth time to read a BaZi chart?",
             "Yes, ideally. The hour pillar is one of the four pillars, and without an accurate birth time you lose a quarter of the chart and the hour-based Ten Gods. Birth location also helps for time-zone accuracy."),
            ("Can I read a BaZi chart without knowing Chinese?",
             "Yes. Once you know the elements and polarities of the ten stems and twelve branches, you can read a chart entirely in English. This guide and the linked pages cover everything you need in English."),
        ],
    })

    return pages


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")


def main():
    # English landing hub
    write(os.path.join(EN, 'index.html'), render_en_home())

    # Four Pillars hub
    write(os.path.join(FP, 'index.html'), render_fp_hub())

    # Sub-pages
    for p in build_pages():
        write(os.path.join(FP, p['id'], 'index.html'), render_subpage(p))

    print("\nTotal: 8 pages generated (1 EN home + 1 FP hub + 6 concept pages)")


if __name__ == '__main__':
    main()
