"""Generate English zodiac pages for saju site - targeting EN market."""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'public', 'en', 'zodiac')

ANIMALS = [
    {
        "slug": "rat", "emoji": "🐀", "name": "Rat", "hanja": "子 (Ja)",
        "element": "Water (水)", "score": 70, "wealth": 65, "love": 75, "health": 72,
        "years": "1948, 1960, 1972, 1984, 1996, 2008, 2020",
        "personality": "Clever, resourceful, and adaptable. Rats are sociable and have a keen eye for opportunity. They excel at turning challenges into advantages.",
        "overview": "2026, the Year of the Fire Horse (Byeong-o), brings a year of change and adaptation for Rats. The Ja-O Chung (子午沖) clash between Rat and Horse energies may bring unexpected shifts, but with wisdom, these can be transformed into opportunities. Build a solid foundation in the first half; opportunities will open up from the second half onward.",
        "wealth_text": "Financial luck is moderate. Prioritize stable income sources over large investments. June and November may bring unexpected windfalls.",
        "love_text": "Romance looks promising. New encounters are likely, and existing relationships will benefit from improved communication. July is your month of destiny.",
        "health_text": "Overall health is good, but pay attention to your heart and blood circulation. Regular exercise is especially important this year.",
        "lucky_months": "July, November", "caution_months": "January, June",
        "lucky_colors": "Blue, Black", "lucky_numbers": "1, 6",
        "clash": "Ja-O Chung (子午沖)"
    },
    {
        "slug": "ox", "emoji": "🐂", "name": "Ox", "hanja": "丑 (Chuk)",
        "element": "Earth (土)", "score": 68, "wealth": 70, "love": 60, "health": 75,
        "years": "1949, 1961, 1973, 1985, 1997, 2009, 2021",
        "personality": "Diligent, dependable, and strong-willed. Oxen are methodical workers who value tradition and stability. Their patience and perseverance lead to lasting success.",
        "overview": "2026 is a year of steady progress for Ox signs. The Fire Horse energy supports your natural diligence, bringing rewards for hard work. Focus on long-term goals rather than quick gains. The second half of the year favors career advancement and financial stability.",
        "wealth_text": "Financial prospects are solid. Your careful approach to money pays off this year. Avoid speculative investments and focus on saving. October brings a good opportunity for property or long-term investments.",
        "love_text": "Romance requires patience. Existing relationships deepen through shared goals. Singles may find love through work or community activities. April and September are favorable months.",
        "health_text": "Maintain your digestive health and watch your diet. Stress management through meditation or nature walks is highly recommended.",
        "lucky_months": "April, October", "caution_months": "March, August",
        "lucky_colors": "Yellow, Brown", "lucky_numbers": "2, 8",
        "clash": ""
    },
    {
        "slug": "tiger", "emoji": "🐅", "name": "Tiger", "hanja": "寅 (In)",
        "element": "Wood (木)", "score": 92, "wealth": 85, "love": 90, "health": 88,
        "years": "1950, 1962, 1974, 1986, 1998, 2010, 2022",
        "personality": "Bold, competitive, and charismatic. Tigers are natural leaders with magnetic personalities. They inspire others with their courage and passion.",
        "overview": "2026 is an outstanding year for Tigers! The In-O Hapwa (寅午 half-combination of Fire) creates powerful synergy with the Fire Horse year. Your natural leadership shines, and bold moves are rewarded. This is the year to pursue your biggest dreams with confidence.",
        "wealth_text": "Excellent financial year. Business ventures and investments yield strong returns. May and September are peak months for financial opportunities. Trust your instincts on major decisions.",
        "love_text": "Romance flourishes! Singles attract partners effortlessly, while couples experience renewed passion. March and August bring significant romantic developments.",
        "health_text": "Energy levels are high, but avoid overexertion. Balance intense activity with proper rest. Your liver and muscles need extra care.",
        "lucky_months": "March, September", "caution_months": "July, December",
        "lucky_colors": "Green, Orange", "lucky_numbers": "3, 7",
        "clash": ""
    },
    {
        "slug": "rabbit", "emoji": "🐇", "name": "Rabbit", "hanja": "卯 (Myo)",
        "element": "Wood (木)", "score": 60, "wealth": 55, "love": 65, "health": 62,
        "years": "1951, 1963, 1975, 1987, 1999, 2011, 2023",
        "personality": "Gentle, elegant, and diplomatic. Rabbits are empathetic and artistic, with a refined sense of beauty. They excel in creating harmony in their surroundings.",
        "overview": "2026 requires caution and patience for Rabbits. The Myo-O Paha (卯午 Destruction) relationship creates tension. Avoid impulsive decisions and focus on protecting what you have. The year improves significantly after August.",
        "wealth_text": "Be conservative with finances. Avoid lending money or making risky investments. Focus on steady income and building emergency savings. November brings modest financial relief.",
        "love_text": "Relationships need extra care and communication. Misunderstandings are likely in the first half. Singles should take time to know potential partners well before committing.",
        "health_text": "Watch your nervous system and sleep quality. Stress-related issues may arise. Prioritize self-care, relaxation, and maintaining a regular sleep schedule.",
        "lucky_months": "August, November", "caution_months": "February, May",
        "lucky_colors": "Pink, White", "lucky_numbers": "4, 9",
        "clash": ""
    },
    {
        "slug": "dragon", "emoji": "🐉", "name": "Dragon", "hanja": "辰 (Jin)",
        "element": "Earth (土)", "score": 75, "wealth": 78, "love": 70, "health": 74,
        "years": "1952, 1964, 1976, 1988, 2000, 2012, 2024",
        "personality": "Ambitious, confident, and visionary. Dragons are natural-born achievers who dream big and pursue their goals with unwavering determination.",
        "overview": "2026 brings a mix of opportunities and challenges for Dragons. The Fire Horse energy fuels your ambition, but requires strategic thinking. Focus on quality over quantity in your endeavors. Mid-year brings breakthrough moments.",
        "wealth_text": "Financial luck is above average. Real estate and stable investments are favored. Avoid get-rich-quick schemes. June and October are strong months for financial growth.",
        "love_text": "Romance is steady. Existing relationships benefit from grand gestures and quality time. Singles may find love through social events or travel. May is a romantically charged month.",
        "health_text": "Generally good health, but watch your stomach and digestive system. Moderate your diet and avoid excessive dining out.",
        "lucky_months": "May, October", "caution_months": "April, September",
        "lucky_colors": "Gold, Red", "lucky_numbers": "5, 8",
        "clash": ""
    },
    {
        "slug": "snake", "emoji": "🐍", "name": "Snake", "hanja": "巳 (Sa)",
        "element": "Fire (火)", "score": 78, "wealth": 72, "love": 80, "health": 76,
        "years": "1953, 1965, 1977, 1989, 2001, 2013, 2025",
        "personality": "Wise, intuitive, and sophisticated. Snakes possess deep insight and a natural elegance. They are strategic thinkers who value quality over quantity.",
        "overview": "2026 is a favorable year for Snakes. The Sa-O (巳午) neighboring relationship creates smooth energy flow. Your intuition is especially sharp this year, guiding you toward the right decisions. Trust your inner wisdom.",
        "wealth_text": "Financial intuition serves you well. Investment opportunities appear in the first quarter. Side projects or creative ventures may become profitable. March and August are peak financial months.",
        "love_text": "Romance is vibrant. Deep emotional connections form naturally. Singles attract intellectually stimulating partners. Couples rediscover their spark. June is the month of love.",
        "health_text": "Good overall health, but manage your energy wisely. Avoid burning out from overwork. Eye health and skin care deserve attention.",
        "lucky_months": "March, August", "caution_months": "June, November",
        "lucky_colors": "Red, Purple", "lucky_numbers": "6, 9",
        "clash": ""
    },
    {
        "slug": "horse", "emoji": "🐴", "name": "Horse", "hanja": "午 (O)",
        "element": "Fire (火)", "score": 80, "wealth": 75, "love": 82, "health": 78,
        "years": "1954, 1966, 1978, 1990, 2002, 2014, 2026",
        "personality": "Energetic, free-spirited, and adventurous. Horses are passionate individuals who thrive on excitement and new experiences. They inspire others with their enthusiasm.",
        "overview": "2026 is YOUR year — the Year of the Horse! The Tae-se (太歲) year brings both power and responsibility. Major life changes are likely: career shifts, relocations, or relationship milestones. Embrace transformation with confidence while staying grounded.",
        "wealth_text": "Dynamic financial year with significant ups and downs. Bold career moves may lead to substantial rewards. Avoid gambling or speculative trading. April and November are financially favorable.",
        "love_text": "Romance is intense and transformative. Existing relationships face tests that ultimately strengthen bonds. Singles may experience love at first sight. February and July are key romantic months.",
        "health_text": "High energy but watch for injuries from overactivity. Heart health and blood pressure need monitoring. Balance excitement with proper rest.",
        "lucky_months": "February, November", "caution_months": "May, August",
        "lucky_colors": "Orange, Crimson", "lucky_numbers": "2, 7",
        "clash": ""
    },
    {
        "slug": "goat", "emoji": "🐑", "name": "Goat", "hanja": "未 (Mi)",
        "element": "Earth (土)", "score": 88, "wealth": 82, "love": 90, "health": 85,
        "years": "1955, 1967, 1979, 1991, 2003, 2015, 2027",
        "personality": "Creative, gentle, and harmonious. Goats are artistic souls with a deep appreciation for beauty. They bring peace and warmth to their surroundings.",
        "overview": "2026 is an excellent year for Goats! The Mi-O Hapwa (未午 Fire combination) creates beautiful harmony. Your creativity peaks, relationships blossom, and opportunities appear in unexpected places. This is a year to trust the process and enjoy the journey.",
        "wealth_text": "Strong financial year, especially in creative and service industries. Partnerships bring prosperity. July and December are excellent for financial decisions and new ventures.",
        "love_text": "Romance is magical. Deep soul connections form effortlessly. Couples experience a golden period of harmony. Singles: your ideal partner may appear through artistic or social gatherings.",
        "health_text": "Excellent health year. Your emotional well-being supports physical vitality. Focus on maintaining balance through gentle exercise like yoga or tai chi.",
        "lucky_months": "July, December", "caution_months": "March, October",
        "lucky_colors": "Lavender, Cream", "lucky_numbers": "3, 8",
        "clash": ""
    },
    {
        "slug": "monkey", "emoji": "🐒", "name": "Monkey", "hanja": "申 (Sin)",
        "element": "Metal (金)", "score": 65, "wealth": 60, "love": 68, "health": 63,
        "years": "1956, 1968, 1980, 1992, 2004, 2016, 2028",
        "personality": "Witty, clever, and versatile. Monkeys are master problem-solvers with quick minds and infectious humor. They adapt to any situation with ease.",
        "overview": "2026 presents mixed energies for Monkeys. The Fire Horse year challenges your Metal element, requiring flexibility. Your cleverness helps you navigate obstacles, but patience is essential. Focus on skill-building and networking for future gains.",
        "wealth_text": "Financial caution is advised. Avoid impulsive purchases and risky schemes. Focus on developing new skills that increase your earning potential. September brings a turnaround in finances.",
        "love_text": "Communication is key in relationships. Express your feelings honestly rather than using humor as a shield. Singles find connections through intellectual pursuits. May is a promising month.",
        "health_text": "Respiratory health needs attention. Avoid pollution and maintain good air quality in your living space. Regular breathing exercises help significantly.",
        "lucky_months": "May, September", "caution_months": "January, July",
        "lucky_colors": "White, Silver", "lucky_numbers": "4, 9",
        "clash": ""
    },
    {
        "slug": "rooster", "emoji": "🐓", "name": "Rooster", "hanja": "酉 (Yu)",
        "element": "Metal (金)", "score": 62, "wealth": 58, "love": 64, "health": 66,
        "years": "1957, 1969, 1981, 1993, 2005, 2017, 2029",
        "personality": "Honest, hardworking, and observant. Roosters are detail-oriented perfectionists who take pride in their work. They are courageous and outspoken.",
        "overview": "2026 requires steady effort for Roosters. The Fire element of the Horse year creates pressure on your Metal nature, but this friction can produce refinement. Focus on perfecting your craft and building reliable systems. Consistency beats brilliance this year.",
        "wealth_text": "Moderate financial year. Steady income is reliable, but windfalls are unlikely. Focus on reducing unnecessary expenses. August and November offer modest investment opportunities.",
        "love_text": "Relationships improve through patience and understanding. Let go of perfectionism in love. Singles should be open to partners who are different from their usual type. October is favorable.",
        "health_text": "Pay attention to your lungs and skin. Seasonal changes may trigger sensitivities. Stay hydrated and maintain a consistent skincare routine.",
        "lucky_months": "August, November", "caution_months": "February, June",
        "lucky_colors": "White, Gold", "lucky_numbers": "5, 7",
        "clash": ""
    },
    {
        "slug": "dog", "emoji": "🐕", "name": "Dog", "hanja": "戌 (Sul)",
        "element": "Earth (土)", "score": 85, "wealth": 80, "love": 85, "health": 82,
        "years": "1958, 1970, 1982, 1994, 2006, 2018, 2030",
        "personality": "Loyal, honest, and protective. Dogs are the most faithful of all zodiac signs, valuing justice and standing up for those they love.",
        "overview": "2026 is a very positive year for Dogs! The Sul-O (戌午) Fire combination creates warm, supportive energy. Your loyalty is rewarded, and trustworthy people enter your life. This is a year of meaningful connections and steady advancement.",
        "wealth_text": "Good financial prospects, especially through teamwork and partnerships. Your reputation opens doors to new opportunities. June and October are strong months for career and financial growth.",
        "love_text": "Romance blossoms beautifully. Trust and loyalty deepen in existing relationships. Singles attract partners who value authenticity. April and September are romantically significant.",
        "health_text": "Generally strong health. Focus on joint health and flexibility. Regular stretching and moderate exercise keep you in top form.",
        "lucky_months": "April, October", "caution_months": "January, August",
        "lucky_colors": "Earth tones, Orange", "lucky_numbers": "3, 6",
        "clash": ""
    },
    {
        "slug": "pig", "emoji": "🐷", "name": "Pig", "hanja": "亥 (Hae)",
        "element": "Water (水)", "score": 72, "wealth": 70, "love": 74, "health": 70,
        "years": "1959, 1971, 1983, 1995, 2007, 2019, 2031",
        "personality": "Generous, compassionate, and sincere. Pigs are warm-hearted individuals who enjoy the finer things in life while caring deeply for others.",
        "overview": "2026 brings a balanced year for Pigs. The Water-Fire interaction creates a need for harmony and moderation. Your generous nature attracts good fortune, but set healthy boundaries. The year favors personal growth and self-discovery.",
        "wealth_text": "Moderate financial luck. Generosity should be balanced with financial planning. Avoid co-signing loans. March and August bring positive financial developments.",
        "love_text": "Warm and nurturing romantic energy. Existing relationships reach new depths of intimacy. Singles attract caring partners. June and November are key months for love.",
        "health_text": "Watch your kidneys and urinary system. Stay well-hydrated and limit alcohol consumption. Spa treatments and warm baths are therapeutic.",
        "lucky_months": "March, August", "caution_months": "May, October",
        "lucky_colors": "Dark Blue, Black", "lucky_numbers": "1, 4",
        "clash": ""
    },
]

def score_color(score):
    if score >= 85: return "#4ADE80"
    if score >= 70: return "#D4AF37"
    return "#F87171"

def wealth_gradient(score):
    return f"width: {score}%; background: linear-gradient(90deg, #D4AF37, #F0D78C)"

def love_gradient(score):
    return f"width: {score}%; background: linear-gradient(90deg, #F87171, #FCA5A5)"

def health_gradient(score):
    return f"width: {score}%; background: linear-gradient(90deg, #4ADE80, #86EFAC)"

def gen_other_links(current_slug):
    links = []
    for a in ANIMALS:
        cls = ' current' if a['slug'] == current_slug else ''
        links.append(f'<a href="/en/zodiac/{a["slug"]}/" class="other-zodiac-link{cls}"><span class="oz-emoji">{a["emoji"]}</span><span class="oz-name">{a["name"]}</span><span class="oz-score">{a["score"]}pts</span></a>')
    return '\n                '.join(links)

def gen_animal_page(a):
    sc = score_color(a['score'])
    faq_items = [
        {"q": f"What is the {a['name']} zodiac overall fortune score for 2026?", "a": f"The {a['name']} ({a['hanja']}, element {a['element']}) has an overall fortune score of {a['score']} points for 2026. {a['overview'][:200]}"},
        {"q": f"What is the {a['name']} zodiac financial luck in 2026?", "a": a['wealth_text']},
        {"q": f"What is the {a['name']} zodiac love fortune in 2026?", "a": a['love_text']},
        {"q": f"What is the {a['name']} zodiac health outlook for 2026?", "a": a['health_text']},
        {"q": f"What are the lucky months for {a['name']} zodiac in 2026?", "a": f"Lucky months: {a['lucky_months']}. Caution months: {a['caution_months']}. Lucky colors: {a['lucky_colors']}. Lucky numbers: {a['lucky_numbers']}."},
        {"q": f"Which birth years are {a['name']} zodiac?", "a": f"The {a['name']} zodiac years are: {a['years']}. This 2026 horoscope applies to all {a['name']} zodiac individuals. For a more personalized reading, a full Four Pillars (Saju) analysis based on birth date and time is recommended."},
    ]
    faq_json = ',\n        '.join([
        f'{{"@type":"Question","name":"{item["q"]}","acceptedAnswer":{{"@type":"Answer","text":"{item["a"]}"}}}}'
        for item in faq_items
    ])
    clash_note = f' The influence of the {a["clash"]} should also be considered for managing your fortune.' if a['clash'] else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="2026 {a['name']} Chinese Zodiac Horoscope - Overall score {a['score']}/100. Detailed analysis of wealth, love, career and health fortune. Based on traditional Korean Saju (Four Pillars) astrology.">
    <meta name="keywords" content="{a['name']} zodiac 2026, Chinese zodiac {a['name']}, {a['name']} horoscope, Korean astrology, Saju, Four Pillars, {a['name']} fortune 2026">
    <title>2026 {a['name']} Zodiac Horoscope | Fortune, Love &amp; Health - Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/zodiac/{a['slug']}/">
    <link rel="alternate" hreflang="ko" href="https://saju.gon.ai.kr/zodiac/{a['slug']}/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/zodiac/{a['slug']}/">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="2026 {a['name']} Zodiac Horoscope | Fortune &amp; Love">
    <meta property="og:description" content="2026 {a['name']} Chinese zodiac forecast. Overall score: {a['score']}/100. Detailed analysis based on traditional Korean Saju astrology.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/zodiac/{a['slug']}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="2026 {a['name']} Zodiac Horoscope | Fortune &amp; Love">
    <meta name="twitter:description" content="2026 {a['name']} Chinese zodiac forecast. Score: {a['score']}/100.">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "2026 {a['name']} Zodiac Horoscope - Fortune, Love & Health Analysis",
        "description": "2026 {a['name']} Chinese zodiac horoscope. Overall score {a['score']}/100.",
        "url": "https://saju.gon.ai.kr/en/zodiac/{a['slug']}/",
        "datePublished": "2026-01-01",
        "dateModified": "2026-05-12",
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
                {{ "@type": "ListItem", "position": 2, "name": "Zodiac", "item": "https://saju.gon.ai.kr/en/zodiac/" }},
                {{ "@type": "ListItem", "position": 3, "name": "{a['name']}", "item": "https://saju.gon.ai.kr/en/zodiac/{a['slug']}/" }}
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
    <link rel="stylesheet" href="/css/zodiac.css?v=1">

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
        .zodiac-scores-section {{ padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); margin-bottom: var(--spacing-xl); }}
        .zodiac-scores-section .detail-score-item {{ display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-md); }}
        .zodiac-scores-section .detail-score-item:last-child {{ margin-bottom: 0; }}
        .zodiac-scores-section .score-icon {{ font-size: 1.2rem; width: 28px; text-align: center; }}
        .zodiac-scores-section .score-name {{ width: 60px; font-size: var(--text-sm); color: var(--color-text-secondary); }}
        .zodiac-scores-section .score-bar-detail {{ flex: 1; height: 8px; background: var(--color-bg-secondary); border-radius: var(--radius-full); overflow: hidden; }}
        .zodiac-scores-section .score-fill-detail {{ height: 100%; border-radius: var(--radius-full); transition: width 1s ease; }}
        .zodiac-scores-section .score-value {{ width: 40px; text-align: right; font-size: var(--text-sm); font-weight: var(--font-semibold); }}
        .zodiac-content-section {{ margin-bottom: var(--spacing-xl); }}
        .zodiac-content-section h2 {{ font-family: var(--font-heading); font-size: var(--text-2xl); margin-bottom: var(--spacing-md); color: var(--color-gold-text); }}
        .zodiac-content-section p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); font-size: var(--text-base); }}
        .lucky-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); margin-bottom: var(--spacing-xl); }}
        .lucky-grid .lucky-item {{ display: flex; flex-direction: column; gap: var(--spacing-xs); }}
        .lucky-grid .lucky-label {{ font-size: var(--text-xs); color: var(--color-text-tertiary); letter-spacing: var(--letter-spacing-wider); }}
        .lucky-grid .lucky-value {{ font-size: var(--text-base); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .lucky-grid .lucky-value.good {{ color: var(--color-success); }}
        .lucky-grid .lucky-value.caution {{ color: var(--color-warning); }}
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
        .saju-explainer {{ margin: var(--spacing-xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); border-left: 3px solid var(--color-gold-muted); }}
        .saju-explainer h3 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-sm); }}
        .saju-explainer p {{ font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--line-height-relaxed); }}
        @media (max-width: 768px) {{
            .zodiac-detail-hero .detail-name {{ font-size: var(--text-3xl); }}
            .zodiac-detail-hero .detail-emoji {{ font-size: 3.5rem; }}
            .other-zodiac-grid {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        @media (max-width: 480px) {{
            .other-zodiac-grid {{ grid-template-columns: repeat(3, 1fr); }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/en/zodiac/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">Saju Astrology</span>
                </h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/" class="active">Zodiac</a><a href="/en/compatibility/">Compatibility</a><a href="/dream/">Dreams</a><a href="/palm/">Palm Reading</a><a href="/">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="zodiac-detail-page">
        <a href="/en/zodiac/" class="back-link">&larr; All Zodiac Signs</a>

        <!-- Hero -->
        <section class="zodiac-detail-hero">
            <div class="detail-emoji">{a['emoji']}</div>
            <div class="detail-hanja">{a['hanja']}</div>
            <h1 class="detail-name"><span class="gold-text">{a['name']} Zodiac 2026</span></h1>
            <div class="detail-element-badge">Element: {a['element']}</div>
            <div class="detail-total-score" style="border-color: {sc}; color: {sc};">
                {a['score']}<small>pts</small>
            </div>
            <p class="years-info">Birth Years: {a['years']}</p>
        </section>

        <!-- Score Bars -->
        <section class="zodiac-scores-section">
            <div class="detail-score-item">
                <span class="score-icon">💰</span>
                <span class="score-name">Wealth</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="{wealth_gradient(a['wealth'])}"></div></div>
                <span class="score-value">{a['wealth']}pts</span>
            </div>
            <div class="detail-score-item">
                <span class="score-icon">💕</span>
                <span class="score-name">Love</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="{love_gradient(a['love'])}"></div></div>
                <span class="score-value">{a['love']}pts</span>
            </div>
            <div class="detail-score-item">
                <span class="score-icon">💪</span>
                <span class="score-name">Health</span>
                <div class="score-bar-detail"><div class="score-fill-detail" style="{health_gradient(a['health'])}"></div></div>
                <span class="score-value">{a['health']}pts</span>
            </div>
        </section>

        <!-- Personality -->
        <section class="zodiac-content-section">
            <h2>Personality Traits</h2>
            <p>{a['personality']}</p>
        </section>

        <!-- Overview -->
        <section class="zodiac-content-section">
            <h2>2026 Overall Fortune</h2>
            <p>{a['overview']}</p>
        </section>

        <!-- Money -->
        <section class="zodiac-content-section">
            <h2>Wealth &amp; Career</h2>
            <p>{a['wealth_text']}</p>
        </section>

        <!-- Love -->
        <section class="zodiac-content-section">
            <h2>Love &amp; Relationships</h2>
            <p>{a['love_text']}</p>
        </section>

        <!-- Health -->
        <section class="zodiac-content-section">
            <h2>Health &amp; Wellness</h2>
            <p>{a['health_text']}</p>
        </section>

        <!-- Lucky Info -->
        <div class="lucky-grid">
            <div class="lucky-item">
                <span class="lucky-label">LUCKY MONTHS</span>
                <span class="lucky-value good">{a['lucky_months']}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">CAUTION MONTHS</span>
                <span class="lucky-value caution">{a['caution_months']}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">LUCKY COLORS</span>
                <span class="lucky-value">{a['lucky_colors']}</span>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">LUCKY NUMBERS</span>
                <span class="lucky-value">{a['lucky_numbers']}</span>
            </div>
        </div>

        <!-- What is Saju -->
        <section class="saju-explainer">
            <h3>What is Saju (Four Pillars) Astrology?</h3>
            <p>Saju (사주, Four Pillars of Destiny) is a traditional Korean and East Asian astrology system that analyzes a person's fate based on the year, month, day, and hour of birth. Each pillar consists of a Heavenly Stem and Earthly Branch, creating eight characters (팔자) that reveal your life path, personality, and fortune. Unlike Western astrology that focuses on star positions, Saju uses the Five Elements (Wood, Fire, Earth, Metal, Water) and Yin-Yang theory to provide deep insights into your destiny.</p>
        </section>

        <!-- Compatibility Link -->
        <section class="related-links-section" style="display:flex;gap:var(--spacing-md);margin-bottom:var(--spacing-xl);flex-wrap:wrap;">
            <a href="/en/compatibility/{a['slug']}/" style="flex:1;min-width:200px;display:flex;align-items:center;justify-content:center;gap:var(--spacing-xs);padding:var(--spacing-md) var(--spacing-lg);background:var(--color-glass-surface);border:1px solid var(--color-glass-border);border-radius:var(--radius-xl);text-decoration:none;color:var(--color-gold);font-size:var(--text-sm);font-weight:var(--font-medium);transition:all var(--duration-normal);">Check {a['name']} Compatibility</a>
        </section>

        <!-- Other Zodiac Links -->
        <section class="other-zodiac-section">
            <h2><span class="gold-text">All Zodiac Signs</span></h2>
            <div class="other-zodiac-grid">
                {gen_other_links(a['slug'])}
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">Want a More Accurate Reading?</h2>
            <p>Enter your birth date and time for a personalized Four Pillars (Saju) analysis.</p>
            <a href="/" class="cta-btn">Free Saju Reading</a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/compatibility/">Compatibility</a>
                <a href="/dream/">Dream Dictionary</a>
                <a href="/palm/">Palm Reading</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Horoscope readings are based on traditional East Asian astrology and are for entertainment and reference only. Please consult professionals for important life decisions.</p>
        </div>
    </footer>

</body>
</html>'''


def gen_index_page():
    cards = []
    for a in ANIMALS:
        sc = score_color(a['score'])
        cards.append(f'''            <a href="/en/zodiac/{a['slug']}/" class="zodiac-card">
                <span class="zodiac-emoji">{a['emoji']}</span>
                <span class="zodiac-name">{a['name']}</span>
                <span class="zodiac-hanja">{a['hanja']}</span>
                <span class="zodiac-score" style="color:{sc}">{a['score']} pts</span>
                <span class="zodiac-years">{a['years'].split(', ')[-1]} ...</span>
            </a>''')
    cards_html = '\n'.join(cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="2026 Chinese Zodiac Horoscope - All 12 animal signs fortune ranking. Detailed analysis based on Korean Saju (Four Pillars) astrology. Find your zodiac sign and discover your 2026 fortune.">
    <meta name="keywords" content="Chinese zodiac 2026, zodiac horoscope, Korean astrology, Saju, Four Pillars, zodiac fortune, Chinese new year zodiac, 12 animal signs">
    <title>2026 Chinese Zodiac Horoscope | All 12 Signs Fortune - Saju Astrology</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/en/zodiac/">
    <link rel="alternate" hreflang="ko" href="https://saju.gon.ai.kr/zodiac/">
    <link rel="alternate" hreflang="en" href="https://saju.gon.ai.kr/en/zodiac/">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="2026 Chinese Zodiac Horoscope | All 12 Signs">
    <meta property="og:description" content="Complete 2026 Chinese zodiac forecast for all 12 animal signs. Based on Korean Saju (Four Pillars) astrology.">
    <meta property="og:url" content="https://saju.gon.ai.kr/en/zodiac/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Saju Astrology">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="2026 Chinese Zodiac Horoscope | All 12 Signs">
    <meta name="twitter:description" content="Complete 2026 Chinese zodiac forecast. Korean Saju astrology.">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "2026 Chinese Zodiac Horoscope - All 12 Animal Signs",
        "description": "Complete 2026 Chinese zodiac horoscope for all 12 animal signs based on Korean Saju astrology.",
        "url": "https://saju.gon.ai.kr/en/zodiac/",
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
                {{ "@type": "ListItem", "position": 2, "name": "Zodiac", "item": "https://saju.gon.ai.kr/en/zodiac/" }}
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
                "name": "What is the Chinese Zodiac?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "The Chinese Zodiac (Shengxiao) is a 12-year cycle where each year is represented by an animal sign: Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, and Pig. Your zodiac is determined by your birth year. 2026 is the Year of the Fire Horse."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What is Saju (Four Pillars) astrology?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Saju (Four Pillars of Destiny) is a traditional Korean astrology system that analyzes fate using four pillars derived from birth year, month, day, and hour. It uses the Five Elements (Wood, Fire, Earth, Metal, Water) and Yin-Yang theory to provide insights into personality, fortune, and compatibility."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Which zodiac sign has the best fortune in 2026?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "In 2026 (Year of the Fire Horse), Tiger has the highest overall fortune score at 92 points, followed by Goat at 88 points and Dog at 85 points. The Fire element combinations create especially favorable energy for these signs."
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
    <link rel="stylesheet" href="/css/zodiac.css?v=1">

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
        .zodiac-hub {{ max-width: 900px; margin: 0 auto; padding: var(--spacing-lg); }}
        .zodiac-hub-hero {{ text-align: center; padding: var(--spacing-3xl) 0 var(--spacing-2xl); }}
        .zodiac-hub-hero h1 {{ font-family: var(--font-heading); font-size: var(--text-4xl); margin-bottom: var(--spacing-md); }}
        .zodiac-hub-hero p {{ color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 600px; margin: 0 auto; line-height: var(--line-height-relaxed); }}
        .zodiac-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: var(--spacing-lg); margin: var(--spacing-2xl) 0; }}
        .zodiac-card {{ display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-xl) var(--spacing-md); background: var(--color-glass-surface); border: 1px solid var(--color-glass-border); border-radius: var(--radius-xl); text-decoration: none; transition: all var(--duration-normal); }}
        .zodiac-card:hover {{ border-color: var(--color-gold-muted); transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }}
        .zodiac-emoji {{ font-size: 3rem; }}
        .zodiac-name {{ font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--color-text-primary); }}
        .zodiac-hanja {{ font-size: var(--text-sm); color: var(--color-gold-muted); }}
        .zodiac-score {{ font-size: var(--text-xl); font-weight: var(--font-bold); }}
        .zodiac-years {{ font-size: var(--text-xs); color: var(--color-text-tertiary); }}
        .saju-intro {{ margin: var(--spacing-2xl) 0; padding: var(--spacing-xl); background: var(--color-bg-tertiary); border-radius: var(--radius-xl); }}
        .saju-intro h2 {{ font-family: var(--font-heading); color: var(--color-gold-text); margin-bottom: var(--spacing-md); }}
        .saju-intro p {{ color: var(--color-text-secondary); line-height: var(--line-height-relaxed); margin-bottom: var(--spacing-md); }}
        .saju-intro p:last-child {{ margin-bottom: 0; }}
        .lang-switch {{ display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-gold); text-decoration: none; font-size: var(--text-sm); padding: var(--spacing-xs) var(--spacing-md); border: 1px solid var(--color-gold-muted); border-radius: var(--radius-full); transition: all var(--duration-fast); }}
        .lang-switch:hover {{ background: rgba(212,175,55,0.1); }}
        @media (max-width: 768px) {{
            .zodiac-grid {{ grid-template-columns: repeat(3, 1fr); }}
            .zodiac-hub-hero h1 {{ font-size: var(--text-3xl); }}
        }}
        @media (max-width: 480px) {{
            .zodiac-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header id="site-header">
        <nav class="container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem;">
            <a href="/en/zodiac/" class="logo-link" style="text-decoration: none;">
                <h1 style="font-family: var(--font-heading); font-size: var(--text-xl); margin: 0;">
                    <span class="gold-text">Saju Astrology</span>
                </h1>
            </a>
            <nav class="nav-links"><a href="/en/zodiac/" class="active">Zodiac</a><a href="/en/compatibility/">Compatibility</a><a href="/dream/">Dreams</a><a href="/palm/">Palm Reading</a><a href="/" class="lang-switch">Korean Ver.</a></nav>
        </nav>
    </header>

    <main class="zodiac-hub">
        <section class="zodiac-hub-hero">
            <h1><span class="gold-text">2026 Chinese Zodiac Horoscope</span></h1>
            <p>Discover your fortune for the Year of the Fire Horse. Based on traditional Korean Saju (Four Pillars) astrology &mdash; a unique East Asian system analyzing destiny through the Five Elements.</p>
        </section>

        <div class="zodiac-grid">
{cards_html}
        </div>

        <section class="saju-intro">
            <h2>What is Saju Astrology?</h2>
            <p><strong>Saju (사주, Four Pillars of Destiny)</strong> is a centuries-old Korean astrology system rooted in Chinese metaphysics. Unlike Western astrology based on star positions, Saju uses the interaction of Five Elements (Wood, Fire, Earth, Metal, Water) and the 12 Earthly Branches (the zodiac animals) to map out a person's life path.</p>
            <p>Each person's fate is determined by four pillars derived from their birth year, month, day, and hour. These eight characters (팔자) reveal personality traits, career aptitude, relationship compatibility, and yearly fortune cycles.</p>
            <p>2026 is the Year of the <strong>Fire Horse (병오년, Byeong-o)</strong>. The combination of Fire energy with the Horse sign creates a year of dynamic change, passionate pursuits, and bold transformations. Each zodiac sign experiences this energy differently based on their elemental interactions.</p>
        </section>

        <!-- CTA -->
        <section class="cta-section" style="padding: var(--spacing-2xl) 0; text-align: center;">
            <h2 class="gold-text" style="font-size: var(--text-2xl);">Get Your Personalized Saju Reading</h2>
            <p>Enter your birth date and time for an in-depth Four Pillars analysis.</p>
            <a href="/" class="cta-btn">Free Saju Reading (Korean)</a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/en/zodiac/">Zodiac 2026</a>
                <a href="/en/compatibility/">Compatibility</a>
                <a href="/dream/">Dream Dictionary</a>
                <a href="/palm/">Palm Reading</a>
                <a href="/">Korean Version</a>
            </div>
            <p class="footer-copy">&copy; 2026 Saju Astrology. Traditional Korean Four Pillars fortune service.</p>
            <p class="footer-disclaimer">Horoscope readings are based on traditional East Asian astrology and are for entertainment and reference only. Please consult professionals for important life decisions.</p>
        </div>
    </footer>

</body>
</html>'''


def main():
    # Create directories
    os.makedirs(BASE, exist_ok=True)

    # Generate index page
    idx_path = os.path.join(BASE, 'index.html')
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(gen_index_page())
    print(f"Created: {idx_path}")

    # Generate animal pages
    for a in ANIMALS:
        d = os.path.join(BASE, a['slug'])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, 'index.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(gen_animal_page(a))
        print(f"Created: {p}")

    print(f"\nTotal: {1 + len(ANIMALS)} pages generated")


if __name__ == '__main__':
    main()
