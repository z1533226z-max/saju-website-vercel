"""Generate English Chinese Zodiac compatibility pages for saju site.

Creates 13 pages total:
- /en/compatibility/                       (hub showing all 12 animals)
- /en/compatibility/{animal}/index.html    (12 pages, each showing all 11 partner matches)

Scoring/relationship logic mirrors the Korean compatibility/ section so the
two language paths stay consistent.
"""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'public', 'en', 'compatibility')

ZODIAC = [
    {"id": "rat",     "name": "Rat",     "emoji": "🐀", "hanja": "子 (Ja)",  "element": "Water (水)", "elem_short": "Water",
     "traits": "Clever, resourceful, and socially adaptable.",
     "years": "1948, 1960, 1972, 1984, 1996, 2008, 2020"},
    {"id": "ox",      "name": "Ox",      "emoji": "🐂", "hanja": "丑 (Chuk)", "element": "Earth (土)", "elem_short": "Earth",
     "traits": "Diligent, patient, and grounded by strong responsibility.",
     "years": "1949, 1961, 1973, 1985, 1997, 2009, 2021"},
    {"id": "tiger",   "name": "Tiger",   "emoji": "🐅", "hanja": "寅 (In)",   "element": "Wood (木)",  "elem_short": "Wood",
     "traits": "Bold, charismatic, and confident leader.",
     "years": "1950, 1962, 1974, 1986, 1998, 2010, 2022"},
    {"id": "rabbit",  "name": "Rabbit",  "emoji": "🐇", "hanja": "卯 (Myo)",  "element": "Wood (木)",  "elem_short": "Wood",
     "traits": "Gentle, artistic, and considerate.",
     "years": "1951, 1963, 1975, 1987, 1999, 2011, 2023"},
    {"id": "dragon",  "name": "Dragon",  "emoji": "🐉", "hanja": "辰 (Jin)",  "element": "Earth (土)", "elem_short": "Earth",
     "traits": "Charismatic, ambitious, and visionary.",
     "years": "1952, 1964, 1976, 1988, 2000, 2012, 2024"},
    {"id": "snake",   "name": "Snake",   "emoji": "🐍", "hanja": "巳 (Sa)",   "element": "Fire (火)",  "elem_short": "Fire",
     "traits": "Wise, intuitive, and analytical.",
     "years": "1953, 1965, 1977, 1989, 2001, 2013, 2025"},
    {"id": "horse",   "name": "Horse",   "emoji": "🐴", "hanja": "午 (O)",    "element": "Fire (火)",  "elem_short": "Fire",
     "traits": "Energetic, free-spirited, and enthusiastic.",
     "years": "1954, 1966, 1978, 1990, 2002, 2014, 2026"},
    {"id": "goat",    "name": "Goat",    "emoji": "🐑", "hanja": "未 (Mi)",   "element": "Earth (土)", "elem_short": "Earth",
     "traits": "Gentle, imaginative, and artistic.",
     "years": "1955, 1967, 1979, 1991, 2003, 2015"},
    {"id": "monkey",  "name": "Monkey",  "emoji": "🐒", "hanja": "申 (Sin)",  "element": "Metal (金)", "elem_short": "Metal",
     "traits": "Clever, versatile, and quick to adapt.",
     "years": "1956, 1968, 1980, 1992, 2004, 2016"},
    {"id": "rooster", "name": "Rooster", "emoji": "🐓", "hanja": "酉 (Yu)",   "element": "Metal (金)", "elem_short": "Metal",
     "traits": "Diligent, observant, and refreshingly honest.",
     "years": "1957, 1969, 1981, 1993, 2005, 2017"},
    {"id": "dog",     "name": "Dog",     "emoji": "🐕", "hanja": "戌 (Sul)",  "element": "Earth (土)", "elem_short": "Earth",
     "traits": "Loyal, principled, and protective.",
     "years": "1958, 1970, 1982, 1994, 2006, 2018"},
    {"id": "pig",     "name": "Pig",     "emoji": "🐷", "hanja": "亥 (Hae)",  "element": "Water (水)", "elem_short": "Water",
     "traits": "Generous, honest, and easygoing.",
     "years": "1959, 1971, 1983, 1995, 2007, 2019"},
]

ZMAP = {z["id"]: z for z in ZODIAC}

# Three Harmonies (Samhap)
SAMHAP = [
    {"signs": {"rat", "dragon", "monkey"}, "name": "Water Triad (水局 삼합)"},
    {"signs": {"ox", "snake", "rooster"},  "name": "Metal Triad (金局 삼합)"},
    {"signs": {"tiger", "horse", "dog"},   "name": "Fire Triad (火局 삼합)"},
    {"signs": {"rabbit", "goat", "pig"},   "name": "Wood Triad (木局 삼합)"},
]

# Six Harmonies (Yukhap) — perfect-match pairings
YUKHAP = {
    frozenset({"rat", "ox"}):        "Ja-Chuk (子丑) Earth Harmony",
    frozenset({"tiger", "pig"}):     "In-Hae (寅亥) Wood Harmony",
    frozenset({"rabbit", "dog"}):    "Myo-Sul (卯戌) Fire Harmony",
    frozenset({"dragon", "rooster"}): "Jin-Yu (辰酉) Metal Harmony",
    frozenset({"snake", "monkey"}):  "Sa-Sin (巳申) Water Harmony",
    frozenset({"horse", "goat"}):    "O-Mi (午未) Fire Harmony",
}

# Six Clashes (Sangchung) — direct opposition
SANGCHUNG = {
    frozenset({"rat", "horse"}):     "Ja-O Chung (子午沖)",
    frozenset({"ox", "goat"}):       "Chuk-Mi Chung (丑未沖)",
    frozenset({"tiger", "monkey"}):  "In-Sin Chung (寅申沖)",
    frozenset({"rabbit", "rooster"}): "Myo-Yu Chung (卯酉沖)",
    frozenset({"dragon", "dog"}):    "Jin-Sul Chung (辰戌沖)",
    frozenset({"snake", "pig"}):     "Sa-Hae Chung (巳亥沖)",
}

# Six Harms (Sanghae) — hidden tension
SANGHAE = {
    frozenset({"rat", "goat"}):      "Ja-Mi Hae (子未害)",
    frozenset({"ox", "horse"}):      "Chuk-O Hae (丑午害)",
    frozenset({"tiger", "snake"}):   "In-Sa Hae (寅巳害)",
    frozenset({"rabbit", "dragon"}): "Myo-Jin Hae (卯辰害)",
    frozenset({"monkey", "pig"}):    "Sin-Hae Hae (申亥害)",
    frozenset({"rooster", "dog"}):   "Yu-Sul Hae (酉戌害)",
}

# Neutral pair scores (mirrored from Korean compatibility generator)
NEUTRAL = {
    frozenset({"rat", "tiger"}): 65,   frozenset({"rat", "rabbit"}): 55,
    frozenset({"rat", "snake"}): 60,   frozenset({"rat", "rooster"}): 58,
    frozenset({"rat", "dog"}): 68,     frozenset({"rat", "pig"}): 72,
    frozenset({"ox", "tiger"}): 55,    frozenset({"ox", "rabbit"}): 62,
    frozenset({"ox", "dragon"}): 65,   frozenset({"ox", "monkey"}): 68,
    frozenset({"ox", "pig"}): 65,      frozenset({"ox", "dog"}): 50,
    frozenset({"tiger", "rabbit"}): 68, frozenset({"tiger", "dragon"}): 72,
    frozenset({"tiger", "snake"}): 48, frozenset({"tiger", "goat"}): 62,
    frozenset({"tiger", "rooster"}): 55,
    frozenset({"rabbit", "snake"}): 60, frozenset({"rabbit", "horse"}): 62,
    frozenset({"rabbit", "monkey"}): 58,
    frozenset({"dragon", "snake"}): 68, frozenset({"dragon", "horse"}): 65,
    frozenset({"dragon", "goat"}): 60,  frozenset({"dragon", "pig"}): 62,
    frozenset({"snake", "horse"}): 65,  frozenset({"snake", "goat"}): 60,
    frozenset({"snake", "dog"}): 58,
    frozenset({"horse", "monkey"}): 60, frozenset({"horse", "rooster"}): 55,
    frozenset({"horse", "pig"}): 62,
    frozenset({"goat", "monkey"}): 58,  frozenset({"goat", "rooster"}): 55,
    frozenset({"goat", "dog"}): 50,
    frozenset({"monkey", "rooster"}): 62, frozenset({"monkey", "dog"}): 65,
    frozenset({"rooster", "pig"}): 58,  frozenset({"dog", "pig"}): 68,
}


def get_match(a_id, b_id):
    """Return dict with score, type, label, detail for the (a, b) pair."""
    if a_id == b_id:
        return {
            "score": 70, "type": "same",
            "label": "Same Sign — Familiar Energy",
            "detail": "You share the same elemental rhythm, so you understand each other instinctively. The flip side is that you also share each other's blind spots."
        }

    pair = frozenset({a_id, b_id})
    if pair in YUKHAP:
        return {
            "score": 95, "type": "yukhap",
            "label": "Perfect Match (Six Harmonies)",
            "detail": f"{YUKHAP[pair]} — yin and yang fit together naturally. One of the strongest possible matches for love, marriage and long-term partnership."
        }
    for sh in SAMHAP:
        if a_id in sh["signs"] and b_id in sh["signs"]:
            return {
                "score": 92, "type": "samhap",
                "label": "Triple Harmony (Three Harmonies)",
                "detail": f"{sh['name']} — three signs that pool into a single element. Powerful synergy when you pursue a shared goal."
            }
    if pair in SANGCHUNG:
        return {
            "score": 35, "type": "clash",
            "label": "Direct Clash (Six Clashes)",
            "detail": f"{SANGCHUNG[pair]} — sitting opposite on the zodiac wheel. Strong initial attraction often gives way to value clashes; needs mature communication."
        }
    if pair in SANGHAE:
        return {
            "score": 45, "type": "harm",
            "label": "Hidden Friction (Six Harms)",
            "detail": f"{SANGHAE[pair]} — surface harmony hides slow-building tension. Workable if both sides keep small frustrations from accumulating."
        }
    score = NEUTRAL.get(pair, 62)
    if score >= 68:
        return {"score": score, "type": "good",
                "label": "Complementary Match",
                "detail": "Different strengths balance each other. Good potential for a steady, well-rounded relationship."}
    if score >= 55:
        return {"score": score, "type": "neutral",
                "label": "Average Match",
                "detail": "Nothing especially supportive or destructive — outcomes depend almost entirely on effort and communication."}
    return {"score": score, "type": "effort",
            "label": "Effort Required",
            "detail": "Significant differences in temperament. Compatibility can be built, but it takes patience and explicit boundaries."}


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


def gradient(score):
    color = score_color(score)
    return f"width:{score}%;background:{color}"


# -----------------------------------------------------------
# Per-animal page
# -----------------------------------------------------------
def gen_animal_page(animal):
    a_id = animal["id"]
    matches = []
    for other in ZODIAC:
        if other["id"] == a_id:
            continue
        m = get_match(a_id, other["id"])
        matches.append((other, m))
    # sort by score desc for readability
    matches.sort(key=lambda x: x[1]["score"], reverse=True)

    # best & worst summary
    best = matches[0]
    worst = matches[-1]

    # Cards markup
    cards = []
    for other, m in matches:
        sc = score_color(m["score"])
        emj = score_emoji(m["score"])
        cards.append(f'''            <a href="/en/compatibility/{other["id"]}/" class="compat-card">
                <div class="compat-card-head">
                    <span class="compat-emoji">{other["emoji"]}</span>
                    <div>
                        <div class="compat-name">{other["name"]}</div>
                        <div class="compat-hanja">{other["hanja"]}</div>
                    </div>
                    <div class="compat-score" style="color:{sc};">{m["score"]}<small>/100</small></div>
                </div>
                <div class="compat-bar"><div class="compat-fill" style="{gradient(m["score"])}"></div></div>
                <div class="compat-label">{emj} {m["label"]}</div>
                <p class="compat-detail">{m["detail"]}</p>
            </a>''')
    cards_html = "\n".join(cards)

    # FAQ schema (compact — 5 entries)
    faq = [
        {
            "q": f"Who is the best match for the {animal['name']} in Chinese zodiac?",
            "a": f"{best[0]['name']} ({best[0]['hanja']}) scores {best[1]['score']}/100 with {animal['name']} — {best[1]['label']}. {best[1]['detail']}"
        },
        {
            "q": f"Who is the worst match for the {animal['name']}?",
            "a": f"{worst[0]['name']} ({worst[0]['hanja']}) scores {worst[1]['score']}/100 — {worst[1]['label']}. {worst[1]['detail']}"
        },
        {
            "q": f"What element is the {animal['name']} in Chinese zodiac?",
            "a": f"The {animal['name']} sign ({animal['hanja']}) belongs to the {animal['element']} element. In Korean Saju astrology this element determines how the {animal['name']} interacts with the other 11 signs through generation and control cycles."
        },
        {
            "q": f"Which birth years are {animal['name']} in Chinese zodiac?",
            "a": f"{animal['name']} years include: {animal['years']}. The zodiac cycle repeats every 12 years."
        },
        {
            "q": "How accurate is Chinese zodiac compatibility?",
            "a": "Zodiac sign matching gives a useful first read on temperament fit, but it only uses one of the four Saju pillars (the year branch). For a full reading you also need the month, day and hour pillars — try the free Saju (Four Pillars) reading on this site for a deeper analysis."
        },
    ]
    faq_json = ",\n        ".join(
        '{"@type":"Question","name":' + escape_json(item["q"]) +
        ',"acceptedAnswer":{"@type":"Answer","text":' + escape_json(item["a"]) + '}}'
        for item in faq
    )

    # Best/worst quick badges
    best_block = f'''<div class="quick-pick best">
                <div class="qp-label">★ Best Match</div>
                <div class="qp-row"><span class="qp-emoji">{best[0]["emoji"]}</span><span class="qp-name">{best[0]["name"]}</span><span class="qp-score" style="color:{score_color(best[1]["score"])};">{best[1]["score"]}/100</span></div>
                <div class="qp-detail">{best[1]["label"]}</div>
            </div>'''
    worst_block = f'''<div class="quick-pick worst">
                <div class="qp-label">⚠ Most Challenging</div>
                <div class="qp-row"><span class="qp-emoji">{worst[0]["emoji"]}</span><span class="qp-name">{worst[0]["name"]}</span><span class="qp-score" style="color:{score_color(worst[1]["score"])};">{worst[1]["score"]}/100</span></div>
                <div class="qp-detail">{worst[1]["label"]}</div>
            </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{animal['name']} Chinese zodiac compatibility — full match scores with all 12 signs. Best match: {best[0]['name']} ({best[1]['score']}/100). Based on Korean Saju (Four Pillars) astrology.">
    <meta name="keywords" content="{animal['name']} compatibility, Chinese zodiac {animal['name']} love match, {animal['name']} best match, {animal['name']} zodiac compatibility chart, Korean Saju, Four Pillars compatibility">
    <title>{animal['name']} Compatibility Chart | All 12 Zodiac Matches - Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/compatibility/{a_id}/">
    <link rel="alternate" hreflang="ko" href="https://saju.gon.ai.kr/compatibility/{a_id}/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/compatibility/{a_id}/">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{animal['name']} Chinese Zodiac Compatibility — All 12 Matches">
    <meta property="og:description" content="Best match: {best[0]['name']} ({best[1]['score']}/100). Korean Saju compatibility chart for the {animal['name']} sign.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/compatibility/{a_id}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{animal['name']} Zodiac Compatibility — All 12 Matches">
    <meta name="twitter:description" content="Best match: {best[0]['name']} ({best[1]['score']}/100). Korean Saju astrology.">

    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{animal['name']} Chinese Zodiac Compatibility Chart",
        "description": "Full {animal['name']} compatibility scores against all 12 Chinese zodiac signs based on Korean Saju astrology.",
        "url": "https://saju.gon.ai.kr/en/compatibility/{a_id}/",
        "datePublished": "2026-05-30",
        "dateModified": "2026-05-30",
        "inLanguage": "en",
        "publisher": {{
            "@type": "Organization",
            "name": "Saju Astrology",
            "url": "https://saju.gon.ai.kr/"
        }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://saju.gon.ai.kr/en/" }},
                {{ "@type": "ListItem", "position": 2, "name": "Compatibility", "item": "https://saju.gon.ai.kr/en/compatibility/" }},
                {{ "@type": "ListItem", "position": 3, "name": "{animal['name']}", "item": "https://saju.gon.ai.kr/en/compatibility/{a_id}/" }}
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

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-BNRL6FRMMM');
    </script>

    <style>
        .compat-page {{ max-width: 880px; margin: 0 auto; padding: var(--spacing-lg); }}
        .compat-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-xl); }}
        .compat-hero .hero-emoji {{ font-size: 5rem; margin-bottom: var(--spacing-md); filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); }}
        .compat-hero .hero-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); margin-bottom: var(--spacing-xs); }}
        .compat-hero h1 {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-sm); }}
        .compat-hero .hero-element {{ display: inline-block; padding: var(--spacing-xs) var(--spacing-lg); border: 1px solid var(--color-gold-muted); border-radius: var(--radius-full); color: var(--color-gold); font-size: var(--text-sm); margin-bottom: var(--spacing-md); }}
        .compat-hero .hero-traits {{ color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 560px; margin: 0 auto var(--spacing-md); line-height: var(--line-height-relaxed); }}
        .compat-hero .hero-years {{ font-size: var(--text-sm); color: var(--color-text-tertiary); }}
        .quick-picks {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin: var(--spacing-xl) 0; }}
        .quick-pick {{ padding: var(--spacing-lg); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid; }}
        .quick-pick.best {{ border-left-color: #4ADE80; }}
        .quick-pick.worst {{ border-left-color: #F87171; }}
        .quick-pick .qp-label {{ font-size: var(--text-xs); color: var(--color-text-tertiary); letter-spacing: var(--letter-spacing-wider); margin-bottom: var(--spacing-sm); }}
        .quick-pick .qp-row {{ display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-xs); }}
        .quick-pick .qp-emoji {{ font-size: 1.8rem; }}
        .quick-pick .qp-name {{ font-size: var(--text-lg); font-weight: var(--font-semibold); flex: 1; }}
        .quick-pick .qp-score {{ font-size: var(--text-xl); font-weight: var(--font-bold); }}
        .quick-pick .qp-detail {{ font-size: var(--text-sm); color: var(--color-text-secondary); }}
        .compat-grid {{ display: flex; flex-direction: column; gap: var(--spacing-md); margin: var(--spacing-xl) 0; }}
        .compat-card {{ display: block; padding: var(--spacing-lg); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; color: inherit; transition: all var(--duration-normal); }}
        .compat-card:hover {{ border-color: var(--color-gold-muted); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.18); }}
        .compat-card-head {{ display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-sm); }}
        .compat-card-head > div:nth-child(2) {{ flex: 1; }}
        .compat-emoji {{ font-size: 2.2rem; }}
        .compat-name {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .compat-hanja {{ font-size: var(--text-xs); color: var(--color-gold-muted); }}
        .compat-score {{ font-size: var(--text-2xl); font-weight: var(--font-bold); }}
        .compat-score small {{ font-size: var(--text-sm); font-weight: var(--font-normal); }}
        .compat-bar {{ height: 6px; background: var(--color-bg-secondary); border-radius: var(--radius-full); overflow: hidden; margin-bottom: var(--spacing-sm); }}
        .compat-fill {{ height: 100%; border-radius: var(--radius-full); transition: width 1s ease; }}
        .compat-label {{ font-size: var(--text-sm); color: var(--color-text-primary); margin-bottom: var(--spacing-xs); font-weight: var(--font-medium); }}
        .compat-detail {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin: 0; }}
        .saju-explainer {{ margin: var(--spacing-2xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid var(--color-gold-muted); }}
        .saju-explainer h2 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-md); }}
        .saju-explainer p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); font-size: var(--text-base); }}
        .all-anims {{ margin-top: var(--spacing-3xl); padding-top: var(--spacing-2xl); border-top: 1px solid var(--color-border-light); }}
        .all-anims h2 {{ text-align: center; font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-xl); }}
        .all-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: var(--spacing-md); }}
        .all-link {{ display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-md); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .all-link:hover {{ border-color: var(--color-gold-muted); transform: translateY(-2px); }}
        .all-link.current {{ border-color: var(--color-gold); background: rgba(212,175,55,0.08); }}
        .all-link .al-emoji {{ font-size: 1.8rem; }}
        .all-link .al-name {{ font-size: var(--text-sm); color: var(--color-text-primary); font-weight: var(--font-medium); }}
        .back-link {{ display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); margin-bottom: var(--spacing-lg); }}
        .back-link:hover {{ color: var(--color-gold-light); }}
        @media (max-width: 640px) {{
            .compat-hero h1 {{ font-size: var(--text-3xl); }}
            .compat-hero .hero-emoji {{ font-size: 3.6rem; }}
            .quick-picks {{ grid-template-columns: 1fr; }}
            .all-grid {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        @media (max-width: 420px) {{
            .all-grid {{ grid-template-columns: repeat(3, 1fr); }}
        }}
    </style>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/en/zodiac/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;"><span class="gold-text">Saju Astrology</span></h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/">Zodiac</a><a href="/en/compatibility/" class="active">Compatibility</a><a href="/en/five-elements/">Five Elements</a><a href="/dream/">Dreams</a><a href="/">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="compat-page">
        <a href="/en/compatibility/" class="back-link">&larr; All Compatibility Charts</a>

        <section class="compat-hero">
            <div class="hero-emoji">{animal['emoji']}</div>
            <div class="hero-hanja">{animal['hanja']}</div>
            <h1><span class="gold-text">{animal['name']} Compatibility Chart</span></h1>
            <div class="hero-element">Element: {animal['element']}</div>
            <p class="hero-traits">{animal['traits']}</p>
            <p class="hero-years">Birth Years: {animal['years']}</p>
        </section>

        <section class="quick-picks">
            {best_block}
            {worst_block}
        </section>

        <section class="zodiac-content-section">
            <h2 style="font-family:var(--font-heading);font-size:var(--text-2xl);margin-bottom:var(--spacing-md);color:var(--color-gold-text);">All 11 Compatibility Matches</h2>
            <p style="color:var(--color-text-secondary);line-height:var(--line-height-relaxed);margin-bottom:var(--spacing-md);">Ranked from strongest to weakest based on Korean Saju (Four Pillars) compatibility theory. Scores reflect Six Harmonies (Yukhap), Three Harmonies (Samhap), Six Clashes (Chung), and Six Harms (Hae).</p>
        </section>

        <div class="compat-grid">
{cards_html}
        </div>

        <section class="saju-explainer">
            <h2>How Chinese Zodiac Compatibility Works</h2>
            <p>Traditional Korean Saju astrology measures compatibility through five core relationships between Earthly Branches: <strong>Six Harmonies (Yukhap, 六合)</strong> are the perfect-match pairs created by yin-yang complementarity; <strong>Three Harmonies (Samhap, 三合)</strong> are triplets that combine into one element; <strong>Six Clashes (Chung, 沖)</strong> sit directly opposite on the wheel and create tension; <strong>Six Harms (Hae, 害)</strong> hide friction under surface harmony. The remaining pairs are neutral, where outcomes depend on individual effort.</p>
        </section>

        <section class="all-anims">
            <h2><span class="gold-text">Check Other Signs</span></h2>
            <div class="all-grid">
                {gen_other_links(a_id)}
            </div>
        </section>

        <section class="cta-section" style="padding:var(--spacing-2xl) 0;text-align:center;">
            <h2 class="gold-text" style="font-size:var(--text-2xl);">Want a Full Four-Pillars Reading?</h2>
            <p>Zodiac matching uses only the year pillar. For an in-depth analysis covering month, day and hour pillars, try our free Saju reading.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/compatibility/">Compatibility</a>
                <a href="/en/five-elements/">Five Elements</a>
                <a href="/dream/">Dream Dictionary</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Compatibility readings are based on traditional East Asian astrology and are for entertainment and reference only. Please consult professionals for important life decisions.</p>
        </div>
    </footer>

</body>
</html>'''


def gen_other_links(current_id):
    parts = []
    for z in ZODIAC:
        cls = "all-link current" if z["id"] == current_id else "all-link"
        parts.append(f'''<a href="/en/compatibility/{z["id"]}/" class="{cls}"><span class="al-emoji">{z["emoji"]}</span><span class="al-name">{z["name"]}</span></a>''')
    return "\n                ".join(parts)


def escape_json(text):
    """Wrap text in double quotes and escape characters that break a JSON string literal."""
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


# -----------------------------------------------------------
# Hub page
# -----------------------------------------------------------
def gen_hub_page():
    cards = []
    for z in ZODIAC:
        # compute best/worst for this animal for the hub card
        best_score = -1
        best_other = None
        for o in ZODIAC:
            if o["id"] == z["id"]:
                continue
            s = get_match(z["id"], o["id"])["score"]
            if s > best_score:
                best_score = s
                best_other = o
        cards.append(f'''            <a href="/en/compatibility/{z["id"]}/" class="hub-card">
                <div class="hub-row">
                    <span class="hub-emoji">{z["emoji"]}</span>
                    <div class="hub-meta">
                        <div class="hub-name">{z["name"]}</div>
                        <div class="hub-hanja">{z["hanja"]}</div>
                    </div>
                </div>
                <div class="hub-best">Best match: <strong>{best_other["name"]}</strong> <span style="color:{score_color(best_score)};">({best_score}/100)</span></div>
                <div class="hub-element">{z["element"]}</div>
            </a>''')
    cards_html = "\n".join(cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="Chinese Zodiac Compatibility Chart — full match scores for all 12 animal signs. Best matches, clashes, and harmonies based on Korean Saju (Four Pillars) astrology.">
    <meta name="keywords" content="Chinese zodiac compatibility, zodiac love match, Chinese zodiac compatibility chart, Korean Saju compatibility, Four Pillars compatibility, Chinese zodiac best match">
    <title>Chinese Zodiac Compatibility Chart | All 12 Sign Matches - Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/compatibility/">
    <link rel="alternate" hreflang="ko" href="https://saju.gon.ai.kr/compatibility/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/compatibility/">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Chinese Zodiac Compatibility Chart | All 12 Signs">
    <meta property="og:description" content="Complete Chinese zodiac compatibility chart for all 12 animal signs. Korean Saju astrology.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/compatibility/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Chinese Zodiac Compatibility Chart">
    <meta name="twitter:description" content="All 12 zodiac compatibility matches — Korean Saju astrology.">

    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Chinese Zodiac Compatibility Chart — All 12 Sign Matches",
        "description": "Complete Chinese zodiac compatibility chart for all 12 animal signs based on Korean Saju astrology.",
        "url": "https://saju.gon.ai.kr/en/compatibility/",
        "inLanguage": "en",
        "publisher": {{
            "@type": "Organization",
            "name": "Saju Astrology",
            "url": "https://saju.gon.ai.kr/"
        }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://saju.gon.ai.kr/en/" }},
                {{ "@type": "ListItem", "position": 2, "name": "Compatibility", "item": "https://saju.gon.ai.kr/en/compatibility/" }}
            ]
        }}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{ "@type": "Question", "name": "How does Chinese zodiac compatibility work?", "acceptedAnswer": {{ "@type": "Answer", "text": "Chinese zodiac compatibility uses the 12 Earthly Branches and their elemental interactions. Korean Saju astrology recognizes five key relationships: Six Harmonies (best match), Three Harmonies (triple combination), Six Clashes (direct opposition), Six Harms (hidden friction), and Neutral pairs. Your year-branch sign predicts a baseline temperament fit." }} }},
            {{ "@type": "Question", "name": "Which zodiac signs are the best matches?", "acceptedAnswer": {{ "@type": "Answer", "text": "The Six Harmony (Yukhap) pairs are considered the strongest matches: Rat-Ox, Tiger-Pig, Rabbit-Dog, Dragon-Rooster, Snake-Monkey, and Horse-Goat. These pairings score around 95/100 in traditional compatibility charts." }} }},
            {{ "@type": "Question", "name": "Which zodiac signs clash?", "acceptedAnswer": {{ "@type": "Answer", "text": "The Six Clash (Chung) pairs sit directly opposite on the zodiac wheel and create the most tension: Rat-Horse, Ox-Goat, Tiger-Monkey, Rabbit-Rooster, Dragon-Dog, Snake-Pig. A clash is not a verdict — it just means the relationship requires more active communication and shared goals." }} }},
            {{ "@type": "Question", "name": "Is Chinese zodiac compatibility the same as Saju compatibility?", "acceptedAnswer": {{ "@type": "Answer", "text": "Zodiac compatibility uses only the year-pillar (one of four pillars in Saju). Full Saju compatibility analyzes all four pillars (year, month, day, hour) plus the Heavenly Stems. The zodiac match is a quick first read; a full Saju reading is much more detailed." }} }}
        ]
    }}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-BNRL6FRMMM');
    </script>

    <style>
        .compat-hub {{ max-width: 900px; margin: 0 auto; padding: var(--spacing-lg); }}
        .compat-hub-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .compat-hub-hero h1 {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-md); }}
        .compat-hub-hero p {{ color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 620px; margin: 0 auto; line-height: var(--line-height-relaxed); }}
        .hub-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .hub-card {{ display: flex; flex-direction: column; gap: var(--spacing-xs); padding: var(--spacing-lg); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; color: inherit; transition: all var(--duration-normal); }}
        .hub-card:hover {{ border-color: var(--color-gold-muted); transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.18); }}
        .hub-row {{ display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xs); }}
        .hub-emoji {{ font-size: 2.2rem; }}
        .hub-meta {{ flex: 1; }}
        .hub-name {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .hub-hanja {{ font-size: var(--text-xs); color: var(--color-gold-muted); }}
        .hub-best {{ font-size: var(--text-sm); color: var(--color-text-secondary); }}
        .hub-element {{ font-size: var(--text-xs); color: var(--color-text-tertiary); }}
        .saju-intro {{ margin: var(--spacing-2xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); }}
        .saju-intro h2 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-md); }}
        .saju-intro p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin-bottom: var(--spacing-md); }}
        .saju-intro p:last-child {{ margin-bottom: 0; }}
        .matches-table {{ width: 100%; margin: var(--spacing-2xl) 0; border-collapse: collapse; font-size: var(--text-sm); }}
        .matches-table caption {{ font-family: var(--font-heading); color: var(--color-gold-text); font-size: var(--text-xl); margin-bottom: var(--spacing-md); text-align: left; }}
        .matches-table th, .matches-table td {{ padding: var(--spacing-sm); border-bottom: 1px solid var(--color-border-light); text-align: left; }}
        .matches-table th {{ color: var(--color-gold-muted); font-weight: var(--font-semibold); }}
        @media (max-width: 640px) {{
            .compat-hub-hero h1 {{ font-size: var(--text-3xl); }}
            .hub-grid {{ grid-template-columns: 1fr; }}
            .matches-table {{ font-size: var(--text-xs); }}
        }}
    </style>
</head>
<body>

    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/en/zodiac/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;"><span class="gold-text">Saju Astrology</span></h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/">Zodiac</a><a href="/en/compatibility/" class="active">Compatibility</a><a href="/en/five-elements/">Five Elements</a><a href="/dream/">Dreams</a><a href="/">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="compat-hub">
        <section class="compat-hub-hero">
            <h1><span class="gold-text">Chinese Zodiac Compatibility Chart</span></h1>
            <p>Find your perfect match across all 12 zodiac signs &mdash; based on traditional Korean Saju (Four Pillars) astrology. Each card shows the strongest match for that sign.</p>
        </section>

        <div class="hub-grid">
{cards_html}
        </div>

        <table class="matches-table">
            <caption>The Six Harmonies (Yukhap) &mdash; Strongest Pairings</caption>
            <thead>
                <tr><th>Pair</th><th>Korean Name</th><th>Element Created</th></tr>
            </thead>
            <tbody>
                <tr><td>Rat &amp; Ox</td><td>Ja-Chuk (子丑)</td><td>Earth</td></tr>
                <tr><td>Tiger &amp; Pig</td><td>In-Hae (寅亥)</td><td>Wood</td></tr>
                <tr><td>Rabbit &amp; Dog</td><td>Myo-Sul (卯戌)</td><td>Fire</td></tr>
                <tr><td>Dragon &amp; Rooster</td><td>Jin-Yu (辰酉)</td><td>Metal</td></tr>
                <tr><td>Snake &amp; Monkey</td><td>Sa-Sin (巳申)</td><td>Water</td></tr>
                <tr><td>Horse &amp; Goat</td><td>O-Mi (午未)</td><td>Fire</td></tr>
            </tbody>
        </table>

        <section class="saju-intro">
            <h2>How Saju Compatibility Works</h2>
            <p><strong>Saju (사주, Four Pillars of Destiny)</strong> is a centuries-old Korean astrology system. While Chinese zodiac compatibility considers only the year-branch sign, a full Saju reading analyzes the year, month, day, and hour pillars together &mdash; eight characters in total.</p>
            <p>Even at the year-branch level, five key relationships emerge: <strong>Six Harmonies (Yukhap)</strong> for perfect pairs, <strong>Three Harmonies (Samhap)</strong> for triple combinations into one element, <strong>Six Clashes (Chung)</strong> for direct opposition, and <strong>Six Harms (Hae)</strong> for hidden friction. The remaining pairings are neutral, where outcomes depend almost entirely on individual effort.</p>
            <p>Use this chart as a quick first read on temperament fit, then drill into a full Saju reading for the deeper picture.</p>
        </section>

        <section class="cta-section" style="padding:var(--spacing-2xl) 0;text-align:center;">
            <h2 class="gold-text" style="font-size:var(--text-2xl);">Get a Full Saju Reading</h2>
            <p>Enter your birth date and time for an in-depth Four Pillars analysis covering compatibility, fortune, and personality.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/compatibility/">Compatibility</a>
                <a href="/en/five-elements/">Five Elements</a>
                <a href="/dream/">Dream Dictionary</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Compatibility readings are based on traditional East Asian astrology and are for entertainment and reference only. Please consult professionals for important life decisions.</p>
        </div>
    </footer>

</body>
</html>'''


def main():
    os.makedirs(BASE, exist_ok=True)

    hub_path = os.path.join(BASE, 'index.html')
    with open(hub_path, 'w', encoding='utf-8') as f:
        f.write(gen_hub_page())
    print(f"Created: {hub_path}")

    for animal in ZODIAC:
        d = os.path.join(BASE, animal['id'])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, 'index.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(gen_animal_page(animal))
        print(f"Created: {p}")

    print(f"\nTotal: {1 + len(ZODIAC)} pages generated")


if __name__ == '__main__':
    main()
