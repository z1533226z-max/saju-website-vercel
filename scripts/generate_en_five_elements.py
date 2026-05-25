"""Generate English Five Elements (Wu Xing) pages for saju site - targeting EN market.

Run 2026-05-25 — Jarvis autonomous agent, experiment #34.
Hypothesis: /en/five-elements/ hub + 5 element pages create new EN search surface
for "wu xing", "five elements chinese astrology", "wood element bazi", etc.
"""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'public', 'en', 'five-elements')

ELEMENTS = [
    {
        "slug": "wood",
        "name": "Wood",
        "hanja": "木 (Mu)",
        "korean": "목 (Mok)",
        "emoji": "🌳",
        "color_main": "#4ADE80",
        "color_dark": "#16A34A",
        "season": "Spring",
        "direction": "East",
        "planet": "Jupiter",
        "organ": "Liver & Gallbladder",
        "color_assoc": "Green, Teal",
        "shape": "Rectangular, Columnar",
        "personality": "Wood-element people are visionary, growth-oriented, and naturally compassionate. Like a tree reaching for sunlight, they are driven by purpose and have a strong sense of justice. Wood types are creative leaders who inspire others to grow, often serving as mentors, teachers, or activists. They thrive on new beginnings and long-term planning.",
        "strengths": "Idealistic, determined, generous, organized, forward-thinking. Excellent at strategy and long-term vision. Natural empaths who care deeply about social causes.",
        "weaknesses": "Can become rigid or impatient when blocked. Prone to anger and frustration under stress. May overextend themselves trying to help others. Tendency toward workaholism.",
        "careers": "Education, environmental science, law, social work, architecture, publishing, forestry, entrepreneurship, non-profit leadership, philosophy.",
        "compatible": "Water (nourishes Wood) and Fire (Wood fuels Fire). Earth provides grounding stability.",
        "incompatible": "Metal (cuts Wood) creates friction. Excess Wood with Wood can lead to competition.",
        "year_2026": "2026 (Fire Horse year) is a transformative year for Wood-element individuals. The Fire energy receives nourishment from Wood, meaning your efforts fuel powerful outcomes — but this can be exhausting. Channel your vision into one or two major projects rather than spreading thin. Spring and summer are especially favorable. Watch for liver health and stress-related tension.",
        "lucky_numbers": "3, 4, 8",
        "yin_yang_note": "Yin Wood (乙 Yi) resembles flexible bamboo or vines — adaptive and graceful. Yang Wood (甲 Jia) is like a strong oak — solid and unmoving. Both share growth as their core nature.",
    },
    {
        "slug": "fire",
        "name": "Fire",
        "hanja": "火 (Huo)",
        "korean": "화 (Hwa)",
        "emoji": "🔥",
        "color_main": "#F87171",
        "color_dark": "#DC2626",
        "season": "Summer",
        "direction": "South",
        "planet": "Mars",
        "organ": "Heart & Small Intestine",
        "color_assoc": "Red, Crimson, Pink",
        "shape": "Triangular, Pointed",
        "personality": "Fire-element people radiate charisma, passion, and warmth. Naturally extroverted, they light up rooms and inspire others with their enthusiasm. Fire types are spontaneous communicators, drawn to attention and self-expression. They live in the moment and value joy, beauty, and connection above material concerns.",
        "strengths": "Charismatic, expressive, enthusiastic, optimistic, generous with affection. Natural performers and leaders. Quick decision-makers who energize teams. Strong sense of intuition.",
        "weaknesses": "Impulsive and emotionally volatile. Can burn out quickly from overextension. Tendency toward vanity or attention-seeking. Difficulty with patience and detail work. Anxiety and insomnia under stress.",
        "careers": "Performing arts, sales, marketing, hospitality, public speaking, fashion, beauty industry, broadcasting, religion/spirituality, motivational coaching.",
        "compatible": "Wood (Wood fuels Fire) and Earth (Fire creates Earth/ash). Other Fire types share immediate chemistry.",
        "incompatible": "Water (extinguishes Fire) creates major conflict. Metal melts under Fire — power struggles likely.",
        "year_2026": "2026 is YOUR year — the Fire Horse year amplifies Fire energy dramatically. Fire-element people experience peak vitality, recognition, and opportunity. However, the intensity can lead to burnout, heart strain, or relationship drama. Practice cooling activities: meditation, swimming, time near water. Channel your spotlight wisely. May, June, and July are especially powerful months.",
        "lucky_numbers": "2, 7, 9",
        "yin_yang_note": "Yin Fire (丁 Ding) is like candlelight — gentle, persistent, illuminating. Yang Fire (丙 Bing) is like the sun — bright, far-reaching, all-warming. 2026's Fire Horse contains both energies.",
    },
    {
        "slug": "earth",
        "name": "Earth",
        "hanja": "土 (Tu)",
        "korean": "토 (To)",
        "emoji": "🏔️",
        "color_main": "#D4AF37",
        "color_dark": "#A16207",
        "season": "Late Summer / Transitional",
        "direction": "Center",
        "planet": "Saturn",
        "organ": "Spleen & Stomach",
        "color_assoc": "Yellow, Brown, Gold",
        "shape": "Square, Flat",
        "personality": "Earth-element people are stable, nurturing, and deeply reliable. They are the steady center that holds families, teams, and communities together. Earth types value tradition, security, and meaningful relationships. They prefer routine over adventure and offer practical wisdom over flashy ideas. Patient and loyal, they build slowly but build to last.",
        "strengths": "Trustworthy, patient, supportive, practical, excellent listeners. Strong sense of duty and loyalty. Skilled at mediation and creating harmony. Reliable in crisis. Good with finances and resource management.",
        "weaknesses": "Can become stubborn or resistant to change. Tendency to worry excessively or carry others' burdens. May suppress own needs to please others. Prone to digestive issues and overeating from stress. Slow to adapt.",
        "careers": "Real estate, agriculture, food industry, nursing, banking, accounting, hospitality, social work, ceramics, civil service, family business management.",
        "compatible": "Fire (Fire creates Earth) and Metal (Earth produces Metal). Wood provides healthy challenge through respect.",
        "incompatible": "Wood (Wood depletes Earth's nutrients) creates exhaustion. Water erodes Earth — emotional overwhelm possible.",
        "year_2026": "2026 is a moderately favorable year for Earth-element individuals. The Fire Horse creates Earth energy (Fire → Earth), bringing growth opportunities — but the intensity may feel overwhelming. Stay grounded through routine and nature. Focus on long-term assets like property or stable investments. April, July, and October are strong months. Watch for digestive and stress-related issues.",
        "lucky_numbers": "5, 6, 0",
        "yin_yang_note": "Yin Earth (己 Ji) is like fertile garden soil — receptive and nurturing. Yang Earth (戊 Wu) is like a mountain — immovable and majestic. Both anchor the other elements.",
    },
    {
        "slug": "metal",
        "name": "Metal",
        "hanja": "金 (Jin)",
        "korean": "금 (Geum)",
        "emoji": "⚔️",
        "color_main": "#E5E7EB",
        "color_dark": "#9CA3AF",
        "season": "Autumn",
        "direction": "West",
        "planet": "Venus",
        "organ": "Lungs & Large Intestine",
        "color_assoc": "White, Silver, Gold",
        "shape": "Round, Spherical",
        "personality": "Metal-element people are refined, disciplined, and principled. They have sharp minds, high standards, and a natural sense of justice. Metal types are organized perfectionists who excel at clear thinking and decisive action. They value quality over quantity and tend toward minimalism, precision, and elegant solutions. Independent and self-reliant, they don't need external validation.",
        "strengths": "Disciplined, focused, ethical, organized, articulate. Excellent analytical and strategic thinking. Strong sense of justice and integrity. Natural leaders in technical and professional fields. Resilient under pressure.",
        "weaknesses": "Can become rigid, judgmental, or emotionally distant. Tendency toward perfectionism that delays action. May struggle with vulnerability and intimacy. Prone to respiratory issues, grief, and melancholy. Difficulty letting go.",
        "careers": "Law, engineering, finance, technology, military, surgery, jewelry/metalwork, journalism, academic research, project management.",
        "compatible": "Earth (Earth creates Metal) and Water (Metal contains Water). Metal-Metal can build strong professional partnerships.",
        "incompatible": "Fire (melts Metal) creates conflict and burnout. Wood resists being cut by Metal — passive aggression likely.",
        "year_2026": "2026 (Fire Horse) is a challenging year for Metal-element individuals. Fire melts Metal, meaning external pressure tests your structure. This is a year to refine, not expand. Focus on quality projects, health, and protecting your energy. Avoid major risks. August, September, and November are favorable months. Prioritize lung health, immunity, and emotional release. Setbacks now create strength later.",
        "lucky_numbers": "4, 9",
        "yin_yang_note": "Yin Metal (辛 Xin) is like polished jewelry — refined, ornamental, precise. Yang Metal (庚 Geng) is like a sword or axe — sharp, decisive, weighty. Both prize quality and form.",
    },
    {
        "slug": "water",
        "name": "Water",
        "hanja": "水 (Shui)",
        "korean": "수 (Su)",
        "emoji": "🌊",
        "color_main": "#3B82F6",
        "color_dark": "#1E40AF",
        "season": "Winter",
        "direction": "North",
        "planet": "Mercury",
        "organ": "Kidneys & Bladder",
        "color_assoc": "Blue, Black, Dark Purple",
        "shape": "Wavy, Flowing, Irregular",
        "personality": "Water-element people are intuitive, adaptable, and wise. Like water itself, they flow around obstacles rather than fighting them. Water types are deep thinkers, often introverted, with rich inner lives and strong imagination. They are natural observers — quiet but perceptive. Empathic and creative, they connect easily with the unseen and unspoken. Patient and persistent, they shape stone over time.",
        "strengths": "Intuitive, intelligent, adaptable, creative, diplomatic. Excellent listeners and counselors. Deep emotional intelligence and pattern recognition. Strong willpower hidden beneath gentle exterior. Resourceful in difficulty.",
        "weaknesses": "Can become withdrawn, secretive, or moody. Tendency toward fear, anxiety, and indecision. May avoid confrontation to the point of dishonesty. Prone to kidney issues, fatigue, and reproductive health concerns. Difficulty setting boundaries.",
        "careers": "Writing, psychology, research, philosophy, healing arts, ocean/maritime industries, music composition, intelligence work, diplomacy, spiritual counseling.",
        "compatible": "Metal (Metal generates Water) and Wood (Water nourishes Wood). Water-Water pairs share deep emotional understanding.",
        "incompatible": "Earth (Earth blocks Water) creates emotional suppression. Fire creates evaporation — burnout and exhaustion.",
        "year_2026": "2026 (Fire Horse) requires careful navigation for Water-element individuals. Fire and Water conflict — your natural depth meets external intensity. This year favors inner work, study, writing, and one-on-one connections over crowds. Avoid impulsive decisions. Stay hydrated literally and emotionally. November, December, and January are restorative months. Protect kidney energy through rest, warmth, and quiet time.",
        "lucky_numbers": "1, 6",
        "yin_yang_note": "Yin Water (癸 Gui) is like rain or dew — soft, life-giving, mysterious. Yang Water (壬 Ren) is like an ocean or river — vast, powerful, ever-moving. Both embody wisdom through depth.",
    },
]


def gen_other_elements_links(current_slug):
    links = []
    for e in ELEMENTS:
        cls = ' current' if e['slug'] == current_slug else ''
        links.append(
            f'<a href="/en/five-elements/{e["slug"]}/" class="other-element-link{cls}">'
            f'<span class="oe-emoji">{e["emoji"]}</span>'
            f'<span class="oe-name">{e["name"]}</span>'
            f'<span class="oe-hanja">{e["hanja"]}</span>'
            f'</a>'
        )
    return '\n                '.join(links)


def gen_element_page(e):
    faq_items = [
        {
            "q": f"What is the {e['name']} element in Chinese astrology?",
            "a": f"The {e['name']} element ({e['hanja']}, Korean: {e['korean']}) is one of the Five Elements (Wu Xing) in Chinese metaphysics. It represents the energy of {e['season'].lower()}, the direction {e['direction']}, and governs the {e['organ']}. {e['personality'][:200]}"
        },
        {
            "q": f"What are the personality traits of {e['name']}-element people?",
            "a": f"{e['name']}-element personalities are defined by their {e['strengths'].lower()[:150]}"
        },
        {
            "q": f"What careers suit {e['name']}-element individuals?",
            "a": f"Recommended careers for {e['name']} element: {e['careers']}"
        },
        {
            "q": f"Which elements are compatible with {e['name']}?",
            "a": f"{e['name']} is compatible with: {e['compatible']} Conflicts arise with: {e['incompatible']}"
        },
        {
            "q": f"What is the {e['name']} element fortune in 2026?",
            "a": e['year_2026'][:300]
        },
        {
            "q": f"What body organs does {e['name']} govern?",
            "a": f"In Traditional Chinese Medicine, the {e['name']} element governs the {e['organ']}. Imbalances in this element may manifest as issues with these organs. Lucky numbers for {e['name']}: {e['lucky_numbers']}. Associated season: {e['season']}, direction: {e['direction']}."
        },
    ]
    faq_json = ',\n        '.join([
        f'{{"@type":"Question","name":"{item["q"]}","acceptedAnswer":{{"@type":"Answer","text":"{item["a"]}"}}}}'
        for item in faq_items
    ])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{e['name']} Element ({e['hanja']}) in Chinese Astrology & Five Elements theory (Wu Xing). Personality, career, compatibility, 2026 fortune, and BaZi/Saju meaning. Element of {e['season'].lower()}, direction {e['direction']}.">
    <meta name="keywords" content="{e['name']} element, {e['name']} element personality, Wu Xing {e['name']}, {e['name']} element BaZi, Chinese astrology {e['name']}, five elements {e['name']}, Korean Saju {e['name']}">
    <title>{e['name']} Element (Wu Xing {e['hanja']}) - Personality, Career, 2026 Fortune | Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/five-elements/{e['slug']}/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/five-elements/{e['slug']}/">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{e['name']} Element ({e['hanja']}) - Wu Xing in Chinese Astrology">
    <meta property="og:description" content="Complete guide to the {e['name']} element in Chinese Five Elements theory. Personality, career, compatibility & 2026 Fire Horse year fortune.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/five-elements/{e['slug']}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e['name']} Element ({e['hanja']}) Guide">
    <meta name="twitter:description" content="{e['name']} element personality, career, and 2026 fortune. Wu Xing theory explained.">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{e['name']} Element ({e['hanja']}) in Chinese Astrology - Five Elements (Wu Xing) Guide",
        "description": "Complete guide to the {e['name']} element: personality, career, compatibility, and 2026 fortune in Korean Saju astrology.",
        "url": "https://saju.gon.ai.kr/en/five-elements/{e['slug']}/",
        "datePublished": "2026-05-25",
        "dateModified": "2026-05-25",
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
                {{ "@type": "ListItem", "position": 2, "name": "Five Elements", "item": "https://saju.gon.ai.kr/en/five-elements/" }},
                {{ "@type": "ListItem", "position": 3, "name": "{e['name']}", "item": "https://saju.gon.ai.kr/en/five-elements/{e['slug']}/" }}
            ]
        }}
    }}
    </script>

    <!-- FAQPage -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
        {faq_json}
        ]
    }}
    </script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">

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
        .element-detail-page {{ max-width: 800px; margin: 0 auto; padding: var(--spacing-lg); }}
        .element-detail-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .element-detail-hero .detail-emoji {{ font-size: 5rem; margin-bottom: var(--spacing-md); filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); }}
        .element-detail-hero .detail-hanja {{ font-family: var(--font-heading); font-size: var(--text-2xl); color: var(--color-gold-muted); margin-bottom: var(--spacing-xs); }}
        .element-detail-hero .detail-name {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-sm); }}
        .element-detail-hero .detail-badge {{ display: inline-block; padding: var(--spacing-xs) var(--spacing-lg); border: 1px solid {e['color_main']}; border-radius: var(--radius-full); color: {e['color_main']}; font-size: var(--text-sm); margin-bottom: var(--spacing-lg); }}
        .element-attrs {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: var(--spacing-md); padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); margin-bottom: var(--spacing-xl); }}
        .element-attrs .attr-item {{ display: flex; flex-direction: column; gap: var(--spacing-xs); }}
        .element-attrs .attr-label {{ font-size: var(--text-xs); color: var(--color-text-tertiary); letter-spacing: var(--letter-spacing-wider); text-transform: uppercase; }}
        .element-attrs .attr-value {{ font-size: var(--text-base); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .element-content-section {{ margin-bottom: var(--spacing-xl); }}
        .element-content-section h2 {{ font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-md); color: {e['color_main']}; }}
        .element-content-section p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); font-size: var(--text-base); margin-bottom: var(--spacing-md); }}
        .compat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin-bottom: var(--spacing-xl); }}
        .compat-card {{ padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid; }}
        .compat-card.good {{ border-color: var(--color-success); }}
        .compat-card.bad {{ border-color: var(--color-warning); }}
        .compat-card h3 {{ font-family: var(--font-heading); font-size: var(--text-lg); margin-bottom: var(--spacing-sm); }}
        .compat-card.good h3 {{ color: var(--color-success); }}
        .compat-card.bad h3 {{ color: var(--color-warning); }}
        .yin-yang-box {{ margin: var(--spacing-xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid var(--color-gold-muted); }}
        .yin-yang-box h3 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-sm); }}
        .yin-yang-box p {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); }}
        .other-element-section {{ margin-top: var(--spacing-3xl); padding-top: var(--spacing-2xl); border-top: 1px solid var(--color-border-light); }}
        .other-element-section h2 {{ text-align: center; font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-xl); }}
        .other-element-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--spacing-md); }}
        .other-element-link {{ display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-md); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .other-element-link:hover {{ border-color: var(--color-gold-muted); transform: translateY(-2px); }}
        .other-element-link .oe-emoji {{ font-size: 2rem; }}
        .other-element-link .oe-name {{ font-size: var(--text-sm); color: var(--color-text-primary); font-weight: var(--font-medium); }}
        .other-element-link .oe-hanja {{ font-size: var(--text-xs); color: var(--color-text-tertiary); }}
        .other-element-link.current {{ border-color: {e['color_main']}; background: rgba(212,175,55,0.08); }}
        .back-link {{ display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); margin-bottom: var(--spacing-lg); transition: color var(--duration-fast); }}
        .back-link:hover {{ color: var(--color-gold-light); }}
        @media (max-width: 768px) {{
            .element-detail-hero .detail-name {{ font-size: var(--text-3xl); }}
            .element-detail-hero .detail-emoji {{ font-size: 3.5rem; }}
            .other-element-grid {{ grid-template-columns: repeat(5, 1fr); gap: var(--spacing-xs); }}
            .compat-grid {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 480px) {{
            .other-element-link .oe-name {{ font-size: var(--text-xs); }}
            .other-element-link .oe-emoji {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/en/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">Saju Astrology</span>
                </h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/">Zodiac</a><a href="/en/five-elements/" class="active">Five Elements</a><a href="/compatibility/">Compatibility</a><a href="/palm/">Palm Reading</a><a href="/">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="element-detail-page">
        <a href="/en/five-elements/" class="back-link">&larr; All Five Elements</a>

        <!-- Hero -->
        <section class="element-detail-hero">
            <div class="detail-emoji">{e['emoji']}</div>
            <div class="detail-hanja">{e['hanja']} &middot; {e['korean']}</div>
            <h1 class="detail-name"><span class="gold-text">{e['name']} Element</span></h1>
            <div class="detail-badge">Wu Xing (五行) &middot; {e['season']}</div>
        </section>

        <!-- Core Attributes -->
        <section class="element-attrs">
            <div class="attr-item">
                <span class="attr-label">Season</span>
                <span class="attr-value">{e['season']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Direction</span>
                <span class="attr-value">{e['direction']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Planet</span>
                <span class="attr-value">{e['planet']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Organ</span>
                <span class="attr-value">{e['organ']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Colors</span>
                <span class="attr-value">{e['color_assoc']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Shape</span>
                <span class="attr-value">{e['shape']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Lucky Numbers</span>
                <span class="attr-value">{e['lucky_numbers']}</span>
            </div>
            <div class="attr-item">
                <span class="attr-label">Hanja</span>
                <span class="attr-value">{e['hanja']}</span>
            </div>
        </section>

        <!-- Personality -->
        <section class="element-content-section">
            <h2>{e['name']} Element Personality</h2>
            <p>{e['personality']}</p>
        </section>

        <!-- Strengths -->
        <section class="element-content-section">
            <h2>Strengths</h2>
            <p>{e['strengths']}</p>
        </section>

        <!-- Weaknesses -->
        <section class="element-content-section">
            <h2>Weaknesses &amp; Challenges</h2>
            <p>{e['weaknesses']}</p>
        </section>

        <!-- Careers -->
        <section class="element-content-section">
            <h2>Best Careers for {e['name']} Element</h2>
            <p>{e['careers']}</p>
        </section>

        <!-- Compatibility -->
        <section class="element-content-section">
            <h2>{e['name']} Element Compatibility</h2>
        </section>
        <div class="compat-grid">
            <div class="compat-card good">
                <h3>✓ Compatible Elements</h3>
                <p>{e['compatible']}</p>
            </div>
            <div class="compat-card bad">
                <h3>✗ Conflicting Elements</h3>
                <p>{e['incompatible']}</p>
            </div>
        </div>

        <!-- Yin-Yang -->
        <section class="yin-yang-box">
            <h3>Yin-Yang Aspects of {e['name']}</h3>
            <p>{e['yin_yang_note']}</p>
        </section>

        <!-- 2026 Year -->
        <section class="element-content-section">
            <h2>{e['name']} Element in 2026 (Fire Horse Year)</h2>
            <p>{e['year_2026']}</p>
        </section>

        <!-- Other Elements -->
        <section class="other-element-section">
            <h2><span class="gold-text">Explore All Five Elements</span></h2>
            <div class="other-element-grid">
                {gen_other_elements_links(e['slug'])}
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0; text-align: center;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">Discover Your Day Master Element</h2>
            <p>Get a personalized BaZi (Four Pillars) reading to find your dominant element.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/five-elements/">Five Elements</a>
                <a href="/compatibility/">Compatibility</a>
                <a href="/palm/">Palm Reading</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Five Elements (Wu Xing) interpretations are based on traditional East Asian metaphysics and are for educational and entertainment purposes only.</p>
        </div>
    </footer>

</body>
</html>'''


def gen_index_page():
    cards = []
    for e in ELEMENTS:
        cards.append(f'''            <a href="/en/five-elements/{e['slug']}/" class="element-card" style="border-top: 3px solid {e['color_main']};">
                <span class="element-emoji">{e['emoji']}</span>
                <span class="element-name">{e['name']}</span>
                <span class="element-hanja">{e['hanja']}</span>
                <span class="element-tagline">{e['season']} &middot; {e['direction']}</span>
                <span class="element-cta">Learn more →</span>
            </a>''')
    cards_html = '\n'.join(cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="Five Elements (Wu Xing 五行) in Chinese astrology & Korean Saju - Wood, Fire, Earth, Metal, Water. Personality, compatibility, careers, and 2026 fortune for each element. Complete BaZi guide.">
    <meta name="keywords" content="five elements, Wu Xing, Chinese five elements, BaZi elements, Korean Saju elements, wood fire earth metal water, five elements personality, five elements compatibility, Chinese astrology elements">
    <title>Five Elements (Wu Xing 五行) - Complete Guide to Wood, Fire, Earth, Metal, Water | Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/five-elements/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/five-elements/">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Five Elements (Wu Xing 五行) - Complete Guide">
    <meta property="og:description" content="Master the Five Elements of Chinese astrology: Wood, Fire, Earth, Metal, Water. Personality, compatibility, and 2026 fortune.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/five-elements/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Five Elements (Wu Xing) Guide">
    <meta name="twitter:description" content="Wood, Fire, Earth, Metal, Water — the foundation of Chinese astrology & BaZi.">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Five Elements (Wu Xing) - Complete Guide",
        "description": "Comprehensive guide to the Five Elements of Chinese astrology and Korean Saju: Wood, Fire, Earth, Metal, Water.",
        "url": "https://saju.gon.ai.kr/en/five-elements/",
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
                {{ "@type": "ListItem", "position": 2, "name": "Five Elements", "item": "https://saju.gon.ai.kr/en/five-elements/" }}
            ]
        }}
    }}
    </script>

    <!-- FAQPage -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "What are the Five Elements (Wu Xing) in Chinese astrology?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "The Five Elements (Wu Xing, 五行) are Wood (木), Fire (火), Earth (土), Metal (金), and Water (水). They are the foundation of Chinese astrology, Korean Saju, Traditional Chinese Medicine, and Feng Shui. Each element represents a phase of energy and interacts with others through cycles of generation (Sheng) and control (Ke)."
                }}
            }},
            {{
                "@type": "Question",
                "name": "How do the Five Elements interact?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "The Five Elements interact through two main cycles. The Generating Cycle (Sheng): Wood feeds Fire, Fire creates Earth, Earth bears Metal, Metal carries Water, Water nourishes Wood. The Controlling Cycle (Ke): Wood parts Earth, Earth blocks Water, Water extinguishes Fire, Fire melts Metal, Metal cuts Wood."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What is my Five Element type?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Your dominant element is determined by your Day Master (日主) in BaZi/Saju, which is the Heavenly Stem of the day you were born. Each day pillar corresponds to a Yin or Yang form of one element. A full BaZi chart calculation based on birth year, month, day, and hour is needed for accurate analysis."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Which element is best for 2026?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "2026 is the Year of the Fire Horse (Byeong-o, 丙午). Fire-element individuals experience peak energy. Wood elements (which feed Fire) also benefit but should avoid burnout. Earth elements (which Fire creates) find growth opportunities. Water and Metal elements face more challenges and should focus on protection and refinement."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Are the Five Elements the same as Western astrology elements?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "No. Western astrology uses four elements (Fire, Earth, Air, Water), while Chinese Five Elements (Wu Xing) include Wood and Metal instead of Air. The Chinese system is also more dynamic — focusing on cycles of generation and control between elements rather than fixed personality archetypes."
                }}
            }}
        ]
    }}
    </script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">

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
        .elements-hub {{ max-width: 1000px; margin: 0 auto; padding: var(--spacing-lg); }}
        .elements-hub-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .elements-hub-hero h1 {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-md); }}
        .elements-hub-hero p {{ color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 700px; margin: 0 auto; line-height: var(--line-height-relaxed); }}
        .elements-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .element-card {{ display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-xl) var(--spacing-md); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .element-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }}
        .element-emoji {{ font-size: 3rem; }}
        .element-name {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .element-hanja {{ font-size: var(--text-sm); color: var(--color-gold-muted); }}
        .element-tagline {{ font-size: var(--text-xs); color: var(--color-text-tertiary); margin-top: var(--spacing-xs); }}
        .element-cta {{ font-size: var(--text-xs); color: var(--color-gold); margin-top: var(--spacing-sm); }}
        .wu-xing-intro {{ margin: var(--spacing-2xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); }}
        .wu-xing-intro h2 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-md); }}
        .wu-xing-intro p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin-bottom: var(--spacing-md); }}
        .wu-xing-intro p:last-child {{ margin-bottom: 0; }}
        .cycles-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .cycle-card {{ padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-top: 3px solid; }}
        .cycle-card.sheng {{ border-color: var(--color-success); }}
        .cycle-card.ke {{ border-color: var(--color-warning); }}
        .cycle-card h3 {{ font-family: var(--font-heading); font-size: var(--text-xl); margin-bottom: var(--spacing-sm); }}
        .cycle-card.sheng h3 {{ color: var(--color-success); }}
        .cycle-card.ke h3 {{ color: var(--color-warning); }}
        .cycle-card .cycle-flow {{ font-family: monospace; font-size: var(--text-sm); color: var(--color-text-primary); margin: var(--spacing-md) 0; padding: var(--spacing-md); background: var(--color-bg-secondary); border-radius: var(--radius-md); line-height: 1.8; }}
        .cycle-card p {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); }}
        @media (max-width: 768px) {{
            .elements-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .elements-hub-hero h1 {{ font-size: var(--text-3xl); }}
            .cycles-section {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 480px) {{
            .elements-grid {{ grid-template-columns: repeat(2, 1fr); gap: var(--spacing-md); }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/en/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">Saju Astrology</span>
                </h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/">Zodiac</a><a href="/en/five-elements/" class="active">Five Elements</a><a href="/compatibility/">Compatibility</a><a href="/palm/">Palm Reading</a><a href="/">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="elements-hub">
        <section class="elements-hub-hero">
            <h1><span class="gold-text">Five Elements (Wu Xing 五行)</span></h1>
            <p>Wood, Fire, Earth, Metal, Water — the five fundamental energies that power Chinese astrology, Korean Saju (BaZi), Traditional Chinese Medicine, and Feng Shui. Discover your dominant element and how it shapes your destiny.</p>
        </section>

        <div class="elements-grid">
{cards_html}
        </div>

        <section class="wu-xing-intro">
            <h2>What is Wu Xing (五行)?</h2>
            <p><strong>Wu Xing (五行)</strong>, translated as "Five Elements" or "Five Phases," is one of the most important concepts in East Asian philosophy. It refers to five fundamental energies — <strong>Wood (木), Fire (火), Earth (土), Metal (金), and Water (水)</strong> — that describe how the universe operates through cycles of change.</p>
            <p>Unlike static categories, the Five Elements are dynamic phases that constantly interact, generate, and transform each other. This framework underlies Chinese astrology (BaZi/Saju), Traditional Chinese Medicine, Feng Shui, martial arts theory, and even ancient Chinese statecraft.</p>
            <p>In Korean Saju (사주, Four Pillars of Destiny), each person's birth chart contains a balance of the Five Elements. Your <strong>Day Master (日主)</strong> — the Heavenly Stem of your birth day — represents your core elemental nature and shapes your personality, career path, relationships, and yearly fortune.</p>
        </section>

        <section class="cycles-section">
            <div class="cycle-card sheng">
                <h3>Generating Cycle (相生)</h3>
                <div class="cycle-flow">
                    🌳 Wood → 🔥 Fire<br>
                    🔥 Fire → 🏔️ Earth<br>
                    🏔️ Earth → ⚔️ Metal<br>
                    ⚔️ Metal → 🌊 Water<br>
                    🌊 Water → 🌳 Wood
                </div>
                <p>The Sheng cycle shows how each element nourishes and creates the next. Wood feeds Fire, Fire's ash creates Earth, Earth bears Metal ore, Metal collects Water (condensation), and Water nourishes Wood (plants). This cycle represents growth, support, and natural creation.</p>
            </div>
            <div class="cycle-card ke">
                <h3>Controlling Cycle (相剋)</h3>
                <div class="cycle-flow">
                    🌳 Wood → 🏔️ Earth<br>
                    🏔️ Earth → 🌊 Water<br>
                    🌊 Water → 🔥 Fire<br>
                    🔥 Fire → ⚔️ Metal<br>
                    ⚔️ Metal → 🌳 Wood
                </div>
                <p>The Ke cycle shows how each element controls or restrains another. Wood roots part Earth, Earth dams Water, Water extinguishes Fire, Fire melts Metal, and Metal cuts Wood. This cycle represents balance, regulation, and natural limits — preventing any single element from becoming dominant.</p>
            </div>
        </section>

        <section class="wu-xing-intro">
            <h2>The Five Elements in 2026 (Fire Horse Year)</h2>
            <p>2026 is the Year of the <strong>Fire Horse (병오년, Byeong-o)</strong>. The Horse zodiac sign carries Yang Fire energy, creating one of the most intense Fire years in the 60-year cycle. This influences each element differently:</p>
            <p><strong>🔥 Fire</strong> peaks in vitality but risks burnout. <strong>🌳 Wood</strong> feeds the Fire and benefits from action, but watch exhaustion. <strong>🏔️ Earth</strong> is created by Fire — growth opportunities appear. <strong>⚔️ Metal</strong> is challenged (melted by Fire) — focus on protection and refinement. <strong>🌊 Water</strong> faces evaporation pressure — prioritize rest and inner work.</p>
            <p>Click any element above for a detailed 2026 fortune analysis tailored to your dominant element.</p>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0; text-align: center;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">Find Your Dominant Element</h2>
            <p>A personalized BaZi (Four Pillars / Saju) reading reveals your Day Master and elemental balance.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/five-elements/">Five Elements</a>
                <a href="/compatibility/">Compatibility</a>
                <a href="/palm/">Palm Reading</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Five Elements (Wu Xing) interpretations are based on traditional East Asian metaphysics and are for educational and entertainment purposes only.</p>
        </div>
    </footer>

</body>
</html>'''


def main():
    os.makedirs(BASE, exist_ok=True)

    # Index page
    idx_path = os.path.join(BASE, 'index.html')
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(gen_index_page())
    print(f"Created: {idx_path}")

    # Element pages
    for e in ELEMENTS:
        d = os.path.join(BASE, e['slug'])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, 'index.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(gen_element_page(e))
        print(f"Created: {p}")

    print(f"\nTotal: {1 + len(ELEMENTS)} pages generated")


if __name__ == '__main__':
    main()
