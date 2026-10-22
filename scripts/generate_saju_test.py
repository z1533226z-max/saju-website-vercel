#!/usr/bin/env python3
"""
사주 오행 캐릭터 테스트(/saju-test/) 생성기.

만드는 것
  - public/js/share-test/saju-test-data.js : 화면·카드가 쓰는 10유형 자료 (window.SAJU_TEST_DATA)
  - public/saju-test/<slug>/index.html     : 일간 10유형 고정 소개 페이지 (본문 충분한 것만 색인)

입력
  - 아래 TYPES (캐릭터 이름·문구·그림: 이 사이트 자체 창작, 남의 캐릭터·상표 없음)
  - api/data/day_stems_detailed/*.json (기존 일간 상세 풀이 — 홈 사주풀이와 같은 원문)

/saju-test/index.html(테스트 본 화면)은 손으로 관리하고, 여기서는 표시 블록 두 곳
(ST_HERO_ICONS, ST_TYPE_GRID)의 안쪽만 다시 채운다.
tests/test_saju_test.py 가 이 스크립트를 메모리에서 돌려 결과가 커밋된 파일과 같은지 확인한다.

    python scripts/generate_saju_test.py
"""
import html
import importlib.util
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
DETAIL_DIR = os.path.join(ROOT, "api", "data", "day_stems_detailed")
SITE = "https://saju.gon.ai.kr"
BASE = "/saju-test/"
DATA_JS = os.path.join("js", "share-test", "saju-test-data.js")
OG_DIR = "/assets/images/saju-test/"
ASSET_VERSION = "20261022a"

# 본문(<main> 안, 태그·공백 뺀 글자)이 이보다 짧으면 noindex 로 낸다 — 얇은 페이지를 색인에 올리지 않는 안전장치.
# 기준: 색인 중인 /zodiac/rat/ 본문 약 2,000자, /guide/day-master/ 약 1,500자 (2026-10-22 측정)
MIN_INDEX_TEXT = 2000

ELEMENTS = ["목", "화", "토", "금", "수"]
ELEMENTS_HANJA = ["木", "火", "土", "金", "水"]
ELEMENT_WORD = ["나무", "불", "흙", "쇠", "물"]
STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
STEMS_HANJA = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ELEMENT_COLORS = ["#3f9b5a", "#e2573b", "#c99a4a", "#aab4c0", "#3b7dd8"]

TEN_GOD_KEYS = ["비견_겁재", "식신_상관", "정재_편재", "정관_편관", "정인_편인"]
TEN_GODS = [
    ("비겁", "자기 확신·뚝심", "비견·겁재 — 나와 같은 기운"),
    ("식상", "표현력·재능", "식신·상관 — 내가 만들어 내는 기운"),
    ("재성", "현실 감각·실행력", "정재·편재 — 내가 다루는 기운"),
    ("관성", "책임감·원칙", "정관·편관 — 나를 다듬는 기운"),
    ("인성", "배움·통찰", "정인·편인 — 나를 돕는 기운"),
]
LACKING_TIPS = [
    "새로운 일을 시작해 보기, 아침 산책, 초록색 소품이 부족한 나무 기운을 채워 준다고 봅니다.",
    "햇볕 쬐기, 사람 만나기, 붉은색 포인트가 부족한 불 기운을 채워 준다고 봅니다.",
    "규칙적인 생활, 정리 정돈, 노란색·갈색 계열이 부족한 흙 기운을 채워 준다고 봅니다.",
    "하던 일 마무리하기, 물건 정리, 흰색·금속 소품이 부족한 쇠 기운을 채워 준다고 봅니다.",
    "충분한 휴식과 수면, 독서, 물 자주 마시기, 남색 계열이 부족한 물 기운을 채워 준다고 봅니다.",
]


def _circle(cx, cy, r):
    return f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0z"


def _drop(x, y):
    return f"M{x} {y - 10}C{x + 7} {y} {x + 7} {y + 8} {x} {y + 8}C{x - 7} {y + 8} {x - 7} {y} {x} {y - 10}z"


def _sun_rays():
    parts = []
    for k in range(12):
        a = math.radians(k * 30)
        a1, a2 = a - math.radians(7), a + math.radians(7)
        pts = [(50 + 30 * math.cos(a1), 50 + 30 * math.sin(a1)),
               (50 + 44 * math.cos(a), 50 + 44 * math.sin(a)),
               (50 + 30 * math.cos(a2), 50 + 30 * math.sin(a2))]
        parts.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "z")
    return "".join(parts)


# 그림: viewBox 0 0 100 100, [{d, fill} 또는 {d, stroke, w}] — 화면 SVG 와 카드 canvas(Path2D) 공용
TYPES = [
    dict(slug="gap-wood", file="gap_wood.json", name="곧은 소나무",
         tagline="한번 정한 길은 끝까지 가는 리더",
         keywords=["#리더십", "#정직", "#추진력"], heard="믿고 따라가도 되는 사람",
         icon=[dict(d="M45 68h10v24H45z", fill="#7a4f2a"),
               dict(d="M50 6L20 44h14L16 70h68L66 44h14z", fill="#3f9b5a"),
               dict(d="M50 6L34 27h32z", fill="#6cc48a")]),
    dict(slug="eul-wood", file="eul_wood.json", name="바람 타는 덩굴꽃",
         tagline="어디서든 길을 찾아 피어나는 적응왕",
         keywords=["#유연함", "#친화력", "#센스"], heard="같이 있으면 분위기가 부드러워져",
         icon=[dict(d="M50 94C38 76 62 64 50 42", stroke="#3f9b5a", w=4),
               dict(d="M48 74C34 74 28 64 30 56C40 56 48 64 48 74z", fill="#6cc48a"),
               dict(d="M53 62C66 60 72 50 70 42C60 42 53 50 53 62z", fill="#3f9b5a"),
               dict(d=_circle(50, 22, 9) + _circle(61, 30, 9) + _circle(57, 43, 9)
                    + _circle(43, 43, 9) + _circle(39, 30, 9), fill="#f29bb7"),
               dict(d=_circle(50, 34, 7), fill="#ffd166")]),
    dict(slug="byeong-fire", file="byeong_fire.json", name="한낮의 태양",
         tagline="있는 곳마다 환해지는 분위기 메이커",
         keywords=["#열정", "#솔직함", "#에너지"], heard="너 오면 분위기가 확 살아",
         icon=[dict(d=_sun_rays(), fill="#fb8500"),
               dict(d=_circle(50, 50, 25), fill="#ffb703"),
               dict(d=_circle(43, 43, 8), fill="#ffd56b")]),
    dict(slug="jeong-fire", file="jeong_fire.json", name="밤을 밝히는 촛불",
         tagline="조용히 오래 타오르는 따뜻한 감성파",
         keywords=["#섬세함", "#배려", "#집중력"], heard="내 마음을 제일 잘 알아주는 사람",
         icon=[dict(d=_circle(50, 30, 26), fill="rgba(255,183,3,0.18)"),
               dict(d="M38 52h24v40H38z", fill="#f1e3c8"),
               dict(d="M49 44h2v8h-2z", fill="#4a3b2a"),
               dict(d="M50 10C59 25 63 34 50 46C37 34 41 25 50 10z", fill="#ff7b29"),
               dict(d="M50 25C55 32 56 38 50 44C44 38 45 32 50 25z", fill="#ffd166")]),
    dict(slug="mu-earth", file="mu_earth.json", name="든든한 큰 산",
         tagline="흔들리지 않는 믿음직한 버팀목",
         keywords=["#포용력", "#안정감", "#뚝심"], heard="힘들 때 제일 먼저 생각나는 사람",
         icon=[dict(d="M6 88L40 28L60 58L72 42L96 88z", fill="#b07d3a"),
               dict(d="M40 28L31 44L39 40L45 46L50 42z", fill="#f5efe0"),
               dict(d="M18 88L52 48L82 88z", fill="#8c5a2b")]),
    dict(slug="gi-earth", file="gi_earth.json", name="생명을 키우는 정원",
         tagline="작은 것도 꼼꼼히 키워 내는 살림꾼",
         keywords=["#꼼꼼함", "#실속", "#보살핌"], heard="너한테 맡기면 안심이야",
         icon=[dict(d=_circle(80, 20, 8), fill="#ffd166"),
               dict(d="M6 70Q50 58 94 70V92H6z", fill="#b98a4b"),
               dict(d="M14 82Q50 72 86 82", stroke="#8c5a2b", w=3),
               dict(d="M50 66V44", stroke="#3f9b5a", w=4),
               dict(d="M50 52C40 52 33 44 33 35C43 35 50 42 50 52z", fill="#6cc48a"),
               dict(d="M50 47C61 47 68 38 68 28C56 28 50 37 50 47z", fill="#3f9b5a")]),
    dict(slug="gyeong-metal", file="gyeong_metal.json", name="단단한 강철 바위",
         tagline="불의를 못 참는 결단력의 해결사",
         keywords=["#결단력", "#의리", "#강단"], heard="결정이 필요할 땐 너야",
         icon=[dict(d="M12 86L22 46L46 26L74 32L90 60L84 86z", fill="#8d99a6"),
               dict(d="M46 26L52 54L22 46z", fill="#c3ced8"),
               dict(d="M52 54L90 60L84 86z", fill="#66717e"),
               dict(d="M52 54L84 86H38z", fill="#7a8694")]),
    dict(slug="sin-metal", file="sin_metal.json", name="빛나는 보석",
         tagline="디테일까지 완벽한 감각파",
         keywords=["#완벽주의", "#감각", "#자존심"], heard="취향이 확실하고 멋있어",
         icon=[dict(d="M30 30H70L88 47L50 90L12 47z", fill="#9fd8f0"),
               dict(d="M30 30H70L60 47H40z", fill="#d8f3ff"),
               dict(d="M30 30L40 47H12z", fill="#eefaff"),
               dict(d="M70 30L88 47H60z", fill="#eefaff"),
               dict(d="M40 47H60L50 90z", fill="#7cc4e6"),
               dict(d="M82 8L85 16L93 19L85 22L82 30L79 22L71 19L79 16z", fill="#ffffff")]),
    dict(slug="im-water", file="im_water.json", name="끝없는 바다",
         tagline="크게 보고 넓게 품는 자유로운 전략가",
         keywords=["#포용", "#지혜", "#자유로움"], heard="생각의 스케일이 달라",
         icon=[dict(d="M4 50C16 40 28 40 40 50S64 60 76 50S94 42 96 42V92H4z", fill="#2f6fb8"),
               dict(d="M4 66C16 56 28 56 40 66S64 76 76 66S94 58 96 58V92H4z", fill="#3b8ee0"),
               dict(d="M4 80C16 72 28 72 40 80S64 88 76 80S94 74 96 74V92H4z", fill="#6fb3f0")]),
    dict(slug="gye-water", file="gye_water.json", name="촉촉한 이슬비",
         tagline="작은 변화도 알아채는 직관의 예술가",
         keywords=["#직관", "#감수성", "#상상력"], heard="말 안 해도 다 알아채더라",
         icon=[dict(d="M26 48a14 14 0 0 1 6-27a19 19 0 0 1 35 5a12 12 0 0 1 5 22z", fill="#cfe3f7"),
               dict(d=_drop(34, 64) + _drop(52, 76) + _drop(70, 62), fill="#5aa9e6")]),
]


def _load_site_layout():
    path = os.path.join(ROOT, "api", "_core", "site_layout.py")
    spec = importlib.util.spec_from_file_location("site_layout", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


site_layout = _load_site_layout()


def load_details():
    out = []
    for t in TYPES:
        with open(os.path.join(DETAIL_DIR, t["file"]), encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def e(text):
    return html.escape(str(text), quote=True)


def stem_label(i):
    return f"{STEMS[i]}{ELEMENTS[i // 2]}({STEMS_HANJA[i]}{ELEMENTS_HANJA[i // 2]})"


def matches_for(i):
    """일간 기준 잘 맞는 유형: 천간합 1, 나를 돕는(인성) 1, 내가 돕는(식상) 1 — 같은 음양 짝 우선."""
    me = i // 2
    hap = (i + 5) % 10
    feeds_me = ((me + 4) % 5) * 2 + (i % 2)
    i_feed = ((me + 1) % 5) * 2 + (i % 2)
    return [("찰떡 짝꿍(천간합)", hap), ("나를 채워 주는 사이", feeds_me), ("내가 키워 주는 사이", i_feed)]


def icon_svg(icon, size=120, label=""):
    parts = []
    for p in icon:
        if "stroke" in p:
            parts.append(f'<path d="{p["d"]}" fill="none" stroke="{p["stroke"]}" stroke-width="{p["w"]}" stroke-linecap="round"/>')
        else:
            parts.append(f'<path d="{p["d"]}" fill="{p["fill"]}"/>')
    aria = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="st-icon" viewBox="0 0 100 100" width="{size}" height="{size}" {aria}>{"".join(parts)}</svg>'


# ── saju-test-data.js ────────────────────────────────────────────────
def build_data_js(details):
    types = []
    for i, (t, d) in enumerate(zip(TYPES, details)):
        b = d["basic"]
        types.append({
            "slug": t["slug"], "name": t["name"], "tagline": t["tagline"],
            "keywords": t["keywords"], "heard": t["heard"], "icon": t["icon"],
            "label": stem_label(i), "element": i // 2, "yang": i % 2 == 0,
            "color": ELEMENT_COLORS[i // 2],
            "nature": b["nature"], "strengths": b["strengths"][:3], "weaknesses": b["weaknesses"][:2],
            "tenGods": [d["ten_gods_interpretation"][k]["positive"] for k in TEN_GOD_KEYS],
            "love": d["love_marriage"]["romantic_style"]["approach"],
        })
    data = {
        "version": ASSET_VERSION,
        "types": types,
        "tenGods": [{"key": k, "power": p} for k, p, _ in TEN_GODS],
        "elements": [{"name": n, "hanja": h, "word": w, "color": c}
                     for n, h, w, c in zip(ELEMENTS, ELEMENTS_HANJA, ELEMENT_WORD, ELEMENT_COLORS)],
        "lackingTips": LACKING_TIPS,
    }
    body = json.dumps(data, ensure_ascii=False, indent=1)
    return ("// 자동 생성 파일 — scripts/generate_saju_test.py 로 다시 만들 것 (직접 고치지 말 것)\n"
            f"window.SAJU_TEST_DATA = {body};\n")


# ── 유형 소개 페이지 ──────────────────────────────────────────────────
def _ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def _dl(pairs):
    return "".join(f"<p><strong>{e(k)}</strong> — {e(v)}</p>" for k, v in pairs)


LABELS = {
    "leadership": "리더십", "integrity": "정직함", "independence": "독립심", "vision": "통찰력",
    "persistence": "끈기", "expression": "감정 표현", "stress_response": "스트레스 반응",
    "joy_triggers": "기쁨을 느낄 때", "anger_triggers": "화가 날 때", "coping_mechanisms": "푸는 방법",
    "decision_making": "결정 방식", "communication": "소통 방식", "conflict_resolution": "갈등 대처",
    "work_style": "일하는 방식", "social_interaction": "사람 사귀는 방식",
    "approach": "다가가는 방식", "commitment": "마음을 정하면", "expectations": "상대에게 바라는 것",
    "personality": "잘 맞는 성격", "values": "통하는 가치관",
    "ideal": "잘 맞는 환경", "challenging": "힘든 환경", "team_dynamics": "팀에서의 모습",
    "early_career": "사회 초년", "mid_career": "중견 시기", "late_career": "무르익은 시기",
    "retirement": "은퇴 뒤", "strengths": "좋은 점", "challenges": "부딪히는 점",
    "family_dynamics": "가족 안에서", "conflict_areas": "다툼이 생기는 곳",
    "teamwork": "팀워크", "mediation": "중재", "networking": "인맥", "reputation": "평판",
    "mentoring": "후배를 대할 때", "parental_role": "부모로서", "sibling_relations": "형제자매와",
    "extended_family": "집안 어른·친척과", "generational_bridge": "세대 사이에서", "emotional_support": "마음 챙김",
    "caregiving": "돌봄", "traditions": "전통", "freedom": "자유", "responsibility": "책임감", "healing": "위로",
    "protection": "지켜 주기", "standards": "기준",
    "quality": "친구 관계", "loyalty": "의리", "selection": "친구를 고르는 기준", "maintenance": "관계 유지",
}


def _label(key):
    return LABELS.get(key, None)


def _labeled(section):
    """영문 키를 한국어 제목으로 바꿀 수 있는 항목만 (모르는 키는 제목 없이 문장만)."""
    out = []
    for k, v in section.items():
        if not isinstance(v, str):
            continue
        lab = _label(k)
        out.append(f"<p><strong>{e(lab)}</strong> — {e(v)}</p>" if lab else f"<p>{e(v)}</p>")
    return "".join(out)


def build_type_page(i, details):
    t, d = TYPES[i], details[i]
    b, pd = d["basic"], d["personality_detailed"]
    label = stem_label(i)
    url = f"{SITE}{BASE}{t['slug']}/"
    title = f"{STEMS[i]}{ELEMENTS[i // 2]} 일간 '{t['name']}' 유형 — 성격·연애·궁합 | 사주 오행 캐릭터"
    desc = (f"{label} 일간은 '{t['name']}' 유형입니다. {t['tagline']}. "
            f"강점·약점, 십신으로 본 재능, 일·연애 스타일, 잘 맞는 유형까지 한 번에 정리했습니다.")
    og_image = f"{SITE}{OG_DIR}og-{t['slug']}.jpg"

    tg_html = []
    for (key, power, sub), jk in zip(TEN_GODS, TEN_GOD_KEYS):
        x = d["ten_gods_interpretation"][jk]
        tg_html.append(
            f'<div class="info-box"><h3>{e(key)} — {e(power)}</h3>'
            f'<p>{e(x["positive"])}</p><p><strong>조심할 점</strong> — {e(x["negative"])}</p>'
            f'<p><strong>살리는 법</strong> — {e(x["advice"])}</p></div>')

    match_html = []
    for why, j in matches_for(i):
        tj = TYPES[j]
        match_html.append(
            f'<a href="{BASE}{tj["slug"]}/" class="related-card">{icon_svg(tj["icon"], 56)}'
            f'<span class="related-title">{e(tj["name"])}</span>'
            f'<span class="st-sub">{e(why)} · {e(stem_label(j))}</span></a>')

    others = "".join(
        f'<a href="{BASE}{TYPES[j]["slug"]}/">{e(TYPES[j]["name"])}</a>'
        for j in range(10) if j != i)

    love = d["love_marriage"]
    career = d["career_detailed"]
    social = d.get("social_relations", {})
    yinyang = "양(陽)" if i % 2 == 0 else "음(陰)"

    body = f"""
    <main class="guide-page st-type-page">
        <a href="{BASE}" class="back-link">&larr; 사주 오행 캐릭터 테스트</a>
        <section class="guide-hero st-type-hero" style="--st-color:{ELEMENT_COLORS[i // 2]}">
            {icon_svg(t["icon"], 140, t["name"])}
            <p class="st-type-label">{e(label)} 일간 · {yinyang}의 {ELEMENT_WORD[i // 2]}</p>
            <h1 class="hero-title"><span class="gold-text">'{e(t["name"])}' 유형</span></h1>
            <p class="hero-subtitle">{e(t["tagline"])}</p>
            <p class="st-keywords">{" ".join(e(k) for k in t["keywords"])}</p>
            <a href="{BASE}" class="cta-button">내 유형도 확인하기 →</a>
        </section>

        <section class="guide-section">
            <h2>'{e(t["name"])}' 유형은 이런 사람</h2>
            <p>태어난 날의 천간(일간)이 <strong>{e(label)}</strong>인 사람은 사주에서 <strong>{e(b["nature"])}</strong>에 비유합니다.
            주변에서 <strong>"{e(t["heard"])}"</strong>라는 말을 자주 듣는 편입니다
            (<a href="/guide/day-master/">일간이란?</a>).</p>
            {_ul(b["characteristics"])}
        </section>

        <section class="guide-section">
            <h2>강점과 조심할 점</h2>
            <div class="st-two-col">
                <div class="info-box"><h3>강점</h3>{_ul(b["strengths"])}</div>
                <div class="info-box"><h3>조심할 점</h3>{_ul(b["weaknesses"])}</div>
            </div>
        </section>

        <section class="guide-section">
            <h2>성격 깊이 보기</h2>
            {_labeled(pd["core_traits"])}
            <h3>감정이 움직이는 방식</h3>
            {_labeled(pd["emotional_patterns"])}
            <h3>행동 습관</h3>
            {_labeled(pd["behavioral_tendencies"])}
        </section>

        <section class="guide-section">
            <h2>다섯 가지 무기 — 십신으로 본 '{e(t["name"])}'</h2>
            <p>같은 {e(label)} 일간이라도 어떤 십신이 강한지에 따라 '{e(t["name"])}'의 장점이 드러나는 방식이 달라집니다
            (<a href="/guide/ten-gods/">십성 가이드</a>).</p>
            {"".join(tg_html)}
        </section>

        <section class="guide-section">
            <h2>일과 진로</h2>
            {_ul(career["suitable_fields"])}
            {_labeled(career["work_environment"])}
            <h3>커리어 흐름</h3>
            {_labeled(career["career_development"])}
            {"<h3>함께 일할 때</h3>" + _labeled(social["professional_relationships"]) if "professional_relationships" in social else ""}
        </section>

        <section class="guide-section">
            <h2>연애와 관계</h2>
            {_labeled(love["romantic_style"])}
            {_labeled(love["ideal_partner"])}
            <h3>함께 살 때</h3>
            {_labeled(love["marriage_life"])}
            <h3>관계를 오래 가게 하는 팁</h3>
            {_ul([v for v in love["relationship_advice"].values() if isinstance(v, str)])}
            {"<h3>친구 관계</h3>" + _labeled(social["friendship_patterns"]) if "friendship_patterns" in social else ""}
            {"<h3>가족 안에서</h3>" + _labeled(social["family_dynamics"]) if "family_dynamics" in social else ""}
        </section>

        <section class="guide-section">
            <h2>더 성장하려면</h2>
            {_ul([v for v in pd["growth_areas"].values() if isinstance(v, str)])}
        </section>

        <section class="guide-section related-section">
            <h2>'{e(t["name"])}'와 잘 맞는 유형</h2>
            <div class="related-grid">{"".join(match_html)}</div>
        </section>

        <section class="guide-cta">
            <h2>친구는 어떤 자연일까?</h2>
            <a href="{BASE}" class="cta-button">무료 테스트 하러 가기 →</a>
        </section>

        <section class="guide-section">
            <h2>다른 9가지 유형</h2>
            <nav class="st-type-list" aria-label="다른 오행 캐릭터 유형">{others}</nav>
            <p class="st-disclaimer">전통 일간 해석을 바탕으로 한 재미용 풀이 · 정밀 풀이는 <a href="/">무료 사주풀이</a></p>
        </section>
    </main>"""

    text_len = len(re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", body)))
    robots = ("index, follow, max-snippet:-1, max-image-preview:large" if text_len >= MIN_INDEX_TEXT
              else "noindex, follow")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": f"{label} 일간 '{t['name']}' 유형 — 성격·연애·궁합",
        "description": desc, "url": url, "image": og_image, "inLanguage": "ko",
        "datePublished": "2026-10-22", "dateModified": "2026-10-22",
        "publisher": {"@type": "Organization", "name": "사주명리", "url": f"{SITE}/"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "사주 오행 캐릭터 테스트", "item": f"{SITE}{BASE}"},
            {"@type": "ListItem", "position": 3, "name": t["name"], "item": url},
        ]},
    }, ensure_ascii=False, indent=1)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="{robots}">
    <meta name="description" content="{e(desc)}">
    <title>{e(title)}</title>
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="나는 '{e(t["name"])}' 유형 — 사주 오행 캐릭터 테스트">
    <meta property="og:description" content="{e(t["tagline"])}. 너는 어떤 자연이야? 생년월일로 1초 테스트 + 친구 궁합">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="나는 '{e(t["name"])}' 유형 — 사주 오행 캐릭터 테스트">
    <meta name="twitter:description" content="{e(t["tagline"])}">
    <meta name="twitter:image" content="{og_image}">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/guide.css">
    <link rel="stylesheet" href="/css/saju-test.css?v={ASSET_VERSION}">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290"
         crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-BNRL6FRMMM');
    </script>
    <script type="application/ld+json">
{jsonld}
    </script>
</head>
<body>
    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration:none;">
                <span class="st-logo"><span class="gold-text">사주명리</span></span>
            </a>
            {site_layout.nav_links_html(None)}
        </nav>
    </header>
{body}

    <footer class="site-footer">
        <div class="container">
            {site_layout.footer_links_html()}
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>
</body>
</html>
"""


def _fill_block(page, marker, inner, indent):
    pat = re.compile(rf"(<!-- {marker} -->)(.*?)(\n[ \t]*<!-- /{marker} -->)", re.S)
    if not pat.search(page):
        raise ValueError(f"marker {marker} not found")
    return pat.sub(lambda m: m.group(1) + "\n" + indent + inner + m.group(3), page, count=1)


def build_main_page(page):
    icons = "".join(icon_svg(t["icon"], 40) for t in TYPES)
    grid = "".join(
        f'<a href="{BASE}{t["slug"]}/">{icon_svg(t["icon"], 56)}<strong>{e(t["name"])}</strong>'
        f'<span>{e(stem_label(i))}</span></a>' for i, t in enumerate(TYPES))
    page = _fill_block(page, "ST_HERO_ICONS", f'<div class="st-hero-icons">{icons}</div>', " " * 12)
    return _fill_block(page, "ST_TYPE_GRID", f'<nav class="st-type-grid" aria-label="10가지 오행 캐릭터">{grid}</nav>', " " * 12)


def build_all():
    """{public 기준 상대경로: 내용} — 테스트가 커밋된 파일과 비교한다."""
    details = load_details()
    out = {DATA_JS.replace("\\", "/"): build_data_js(details)}
    with open(os.path.join(PUBLIC, "saju-test", "index.html"), encoding="utf-8") as f:
        out["saju-test/index.html"] = build_main_page(f.read())
    for i, t in enumerate(TYPES):
        out[f"saju-test/{t['slug']}/index.html"] = build_type_page(i, details)
    return out


def main():
    for rel, content in build_all().items():
        path = os.path.join(PUBLIC, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("wrote", rel)


if __name__ == "__main__":
    main()
