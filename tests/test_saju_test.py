"""사주 오행 캐릭터 테스트(/saju-test/): 계산 일치 · 궁합 규칙 · 생성 페이지 · 개인정보 · 공유 설정."""
import datetime
import json
import os
import re
import shutil
import subprocess

import pytest

from site_helpers import (
    ADSENSE_SCRIPT_RE, GA4_RE, GENERIC_NOINDEX_RE, MANUAL_AD_SLOT_RE, PUBLIC, ROOT,
    last_footer, load_module, parse, read_public, resolve_internal_href,
)

SITE = "https://saju.gon.ai.kr"
CORE_JS = os.path.join(PUBLIC, "js", "share-test", "saju-test-core.js")
APP_JS = os.path.join(PUBLIC, "js", "share-test", "saju-test-app.js")
STANDARD_NAV = ('<nav class="nav-links"><a href="/">사주풀이</a><a href="/zodiac/">띠별 운세</a>'
                '<a href="/daily/">오늘의 운세</a><a href="/yearly/">2026년 운세</a>'
                '<a href="/compatibility/">궁합</a><a href="/dream/">꿈해몽</a>'
                '<a href="/palm/">손금 분석</a><a href="/guide/">사주 가이드</a></nav>')

NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="node 가 없어 JS 계산을 돌릴 수 없음")


@pytest.fixture(scope="module")
def gen():
    return load_module(os.path.join("scripts", "generate_saju_test.py"), "generate_saju_test")


def run_core(js_body, payload=None):
    """saju-test-core.js 를 node 로 불러 js_body(c=모듈, input=payload)를 실행하고 JSON 결과를 돌려준다."""
    script = ("const c = require(process.argv[1]);"
              "const input = JSON.parse(require('fs').readFileSync(0, 'utf8') || 'null');"
              f"console.log(JSON.stringify((() => {{ {js_body} }})()));")
    out = subprocess.run([NODE, "-e", script, CORE_JS], input=json.dumps(payload), capture_output=True,
                         text=True, encoding="utf-8", check=True, timeout=60)
    return json.loads(out.stdout)


def _type_pages():
    return [f"saju-test/{slug}/index.html" for slug in (
        "gap-wood", "eul-wood", "byeong-fire", "jeong-fire", "mu-earth",
        "gi-earth", "gyeong-metal", "sin-metal", "im-water", "gye-water")]


TYPE_PAGES = _type_pages()
ALL_PAGES = ["saju-test/index.html"] + TYPE_PAGES


# ── 계산: 홈 사주풀이(파이썬)와 같은 기둥 ───────────────────────────────
def _sample_dates():
    dates, d = [], datetime.date(1900, 1, 1)
    while d.year <= 2100:
        dates.append(d)
        d += datetime.timedelta(days=11)
    # 경계일: 입춘·소한·각 절기 전날/당일
    for y in (1950, 1999, 2000, 2024, 2026):
        for m, day in ((1, 5), (1, 6), (2, 3), (2, 4), (3, 5), (3, 6), (4, 4), (4, 5), (5, 5), (5, 6), (6, 5), (6, 6),
                       (7, 6), (7, 7), (8, 7), (8, 8), (9, 7), (9, 8), (10, 7), (10, 8), (11, 6), (11, 7), (12, 6), (12, 7),
                       (12, 31)):
            dates.append(datetime.date(y, m, day))
    return dates


@needs_node
def test_core_pillars_match_python_calculator():
    from _core.saju_calculator import SajuCalculator
    calc = SajuCalculator()
    stems = [s["name_ko"] for s in calc.heavenly_stems]
    branches = [b["name_ko"] for b in calc.earthly_branches]
    dates = _sample_dates()
    js = run_core("return input.map(([y, m, d]) => c.pillars(y, m, d));", [[d.year, d.month, d.day] for d in dates])
    mismatches = []
    for d, p in zip(dates, js):
        py = calc.calculate_saju(datetime.datetime(d.year, d.month, d.day), "12:00", "male")
        for k in ("year", "month", "day"):
            if (stems[p[k]["stem"]], branches[p[k]["branch"]]) != (py[k]["heavenly"], py[k]["earthly"]):
                mismatches.append((d.isoformat(), k))
    assert len(dates) > 6000
    assert not mismatches, mismatches[:10]


@needs_node
def test_core_rejects_invalid_dates():
    res = run_core("return input.map(([y, m, d]) => c.isValidDate(y, m, d));",
                   [[2001, 2, 29], [2000, 2, 29], [1899, 12, 31], [2101, 1, 1], [1990, 13, 1], [1990, 4, 31]])
    assert res == [False, True, False, False, False, False]


@needs_node
def test_type_code_roundtrip_and_validation():
    res = run_core("""
        const ok = [];
        for (let s = 0; s < 10; s++) for (let b = 0; b < 12; b++) {
            const code = c.typeCode(s, b), back = c.parseCode(code);
            ok.push([code, back && back.stem === s && back.branch === b]);
        }
        return {ok, bad: ['01', '1a', 'zz', '', '123', '0c', 'ab', null].map(x => c.parseCode(x))};
    """)
    valid = [code for code, good in res["ok"] if good]
    assert len(valid) == 60                       # 60갑자 = 음양이 같은 조합만
    assert all(re.fullmatch(r"[0-9][0-9ab]", c) for c in valid)
    assert res["bad"] == [None] * 8


@needs_node
def test_compatibility_is_symmetric_bounded_and_deterministic():
    res = run_core("""
        const codes = [];
        for (let s = 0; s < 10; s++) for (let b = s % 2; b < 12; b += 2) codes.push({stem: s, branch: b});
        const out = [];
        for (const a of codes) for (const b of codes) out.push([c.compatibility(a, b).score, c.compatibility(b, a).score]);
        return {out, min: c.MIN_SCORE, max: c.MAX_SCORE,
                hap: c.compatibility({stem: 0, branch: 0}, {stem: 5, branch: 1}),
                chung: c.compatibility({stem: 0, branch: 0}, {stem: 1, branch: 6})};
    """)
    assert len(res["out"]) == 3600
    assert all(a == b for a, b in res["out"])
    assert all(res["min"] <= a <= res["max"] for a, _ in res["out"])
    assert res["max"] < 100                           # '100% 궁합' 같은 단정 표현 없음
    assert res["hap"]["stemRel"] == "hap" and res["hap"]["branchRel"] == "yukhap" and res["hap"]["score"] == 97
    assert res["chung"]["branchRel"] == "chung"


@needs_node
def test_analyze_code_is_day_pillar_only():
    res = run_core("const r = c.analyze(1995, 3, 15); return [r.code, r.pillars.day, r.counts.reduce((a, b) => a + b)];")
    code, day, total = res
    assert code == f"{day['stem']}{'0123456789ab'[day['branch']]}"
    assert total == 6


# ── 개인정보: 생년월일이 페이지 밖으로 나가지 않는다 ────────────────────────
def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_share_test_js_sends_and_stores_nothing_personal():
    for path in (CORE_JS, APP_JS):
        src = _read(path)
        assert "localStorage" not in src and "sessionStorage" not in src and "indexedDB" not in src, path
        assert "XMLHttpRequest" not in src and "sendBeacon" not in src, path
    app = _read(APP_JS)
    assert re.findall(r"fetch\(([^,)]+)", app) == ["'/api/share/config'"]
    # 초대·궁합 링크는 유형 코드와 별명만으로 만든다
    invite = re.search(r"function inviteUrl\(code, nick\) \{(.*?)\n    \}", app, re.S).group(1)
    pair = re.search(r"function pairUrl\(codeA, nickA, codeB, nickB\) \{(.*?)\n    \}", app, re.S).group(1)
    for body in (invite, pair):
        assert not re.search(r"year|month|day|pillars|counts", body)
    # GA 이벤트에 생년월일·별명을 넣지 않는다
    for params in re.findall(r"track\('[a-z_]+',\s*(\{[^}]*\})", app):
        assert not re.search(r"year|month|day\b|nick|birth", params), params


def test_privacy_policy_mentions_share_test():
    html = read_public("privacy/index.html")
    assert "오행 캐릭터 테스트" in html and 'href="/saju-test/"' in html


# ── 생성 파일이 최신 ──────────────────────────────────────────────────
def test_generated_files_are_up_to_date(gen):
    built = gen.build_all()
    assert set(built) == {"js/share-test/saju-test-data.js", *ALL_PAGES}
    for rel, content in built.items():
        assert read_public(rel) == content, f"{rel} 가 생성기와 다름 — python scripts/generate_saju_test.py 실행"


def test_thin_type_page_falls_back_to_noindex(gen, monkeypatch):
    monkeypatch.setattr(gen, "MIN_INDEX_TEXT", 10 ** 6)
    html = gen.build_type_page(0, gen.load_details())
    assert '<meta name="robots" content="noindex, follow">' in html


# ── 페이지 템플릿 ──────────────────────────────────────────────────────
@pytest.mark.parametrize("rel", ALL_PAGES)
def test_page_uses_site_template(rel):
    html = read_public(rel)
    url = SITE + "/" + rel[: -len("index.html")]
    assert len(ADSENSE_SCRIPT_RE.findall(html)) == 1               # 자동 광고 태그만
    assert not MANUAL_AD_SLOT_RE.search(html)                     # 수동 광고 칸 없음
    assert GA4_RE.search(html)
    assert STANDARD_NAV in html
    assert f'<link rel="canonical" href="{url}">' in html
    assert f'<meta property="og:url" content="{url}">' in html
    assert not GENERIC_NOINDEX_RE.search(html)
    assert 'href="/privacy/">개인정보처리방침</a>' in last_footer(html)
    assert html.count("<h1") == 1


@pytest.mark.parametrize("rel", ALL_PAGES)
def test_page_links_and_og_image_resolve(rel):
    html = read_public(rel)
    p = parse(html)
    for href in p.hrefs:
        ok, why = resolve_internal_href(href, p.ids)
        assert ok, (rel, href, why)
    og = re.search(r'<meta property="og:image" content="https://saju\.gon\.ai\.kr(/[^"]+)">', html).group(1)
    assert os.path.isfile(os.path.join(PUBLIC, og.lstrip("/"))), og
    for src in re.findall(r'<(?:script|link)[^>]+(?:src|href)="(/[^"?]+)', html):
        assert os.path.isfile(os.path.join(PUBLIC, src.lstrip("/"))), (rel, src)


@pytest.mark.parametrize("rel", TYPE_PAGES)
def test_type_pages_have_enough_unique_text(rel, gen):
    html = read_public(rel)
    main = re.search(r"<main.*?</main>", html, re.S).group(0)
    text = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", main))
    assert len(text) >= gen.MIN_INDEX_TEXT


def test_type_pages_are_not_duplicates():
    bodies = []
    for rel in TYPE_PAGES:
        main = re.search(r"<main.*?</main>", read_public(rel), re.S).group(0)
        pieces = re.split(r"[.\n]", re.sub(r"<[^>]+>", "\n", main))          # 태그·마침표 단위 문장
        bodies.append({p for p in (re.sub(r"\s+", " ", x).strip() for x in pieces) if len(p) >= 15})
    # 안내 문구 몇 줄은 공통 틀이지만, 겹치는 문장 글자가 각 페이지 문장의 15% 를 넘으면 복제 페이지로 본다
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            shared = sum(len(x) for x in bodies[i] & bodies[j])
            ratio = shared / min(sum(len(x) for x in bodies[i]), sum(len(x) for x in bodies[j]))
            assert ratio < 0.15, (TYPE_PAGES[i], TYPE_PAGES[j], round(ratio, 3))


def test_all_og_images_exist(gen):
    names = ["og-main.jpg"] + [f"og-{t['slug']}.jpg" for t in gen.TYPES]
    for name in names:
        path = os.path.join(PUBLIC, "assets", "images", "saju-test", name)
        assert os.path.isfile(path) and os.path.getsize(path) < 300_000, name
    app = _read(APP_JS)
    assert "'og-' + t.slug + '.jpg'" in app and "'og-main.jpg'" in app


def test_main_page_loads_scripts_in_order():
    html = read_public("saju-test/index.html")
    order = [m.group(1) for m in re.finditer(r'<script src="/js/share-test/(saju-test-[a-z]+)\.js\?v=', html)]
    assert order == ["saju-test-core", "saju-test-data", "saju-test-app"]
    for marker in ("st-form", "st-result", "st-compat", "st-pair", "st-invite"):
        assert f'id="{marker}"' in html


# ── 진입 링크 ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("rel", ["index.html", "guide/day-master/index.html", "compatibility/index.html"])
def test_entry_links_point_to_test(rel):
    html = read_public(rel)
    assert html.count("<!-- SAJU_TEST_ENTRY_V1") == 1
    assert 'href="/saju-test/"' in html


# ── 카카오 공유 설정 ──────────────────────────────────────────────────
@pytest.fixture()
def share_config():
    return load_module(os.path.join("api", "share", "config.py"), "share_config")


def test_share_config_exposes_only_a_well_formed_kakao_key(share_config, monkeypatch):
    monkeypatch.delenv("KAKAO_JS_KEY", raising=False)
    assert share_config.public_config() == {"kakaoJsKey": None}
    for bad in ("", "abc", "sk_live_" + "x" * 30, "0123456789abcdef0123456789abcdeg"):
        monkeypatch.setenv("KAKAO_JS_KEY", bad)
        assert share_config.public_config() == {"kakaoJsKey": None}, bad
    monkeypatch.setenv("KAKAO_JS_KEY", " 0123456789abcdef0123456789ABCDEF ")
    assert share_config.public_config() == {"kakaoJsKey": "0123456789abcdef0123456789ABCDEF"}


def test_vercel_routes_share_config_before_catch_all():
    with open(os.path.join(ROOT, "vercel.json"), encoding="utf-8") as f:
        routes = json.load(f)["routes"]
    srcs = [r["src"] for r in routes]
    i = srcs.index("/api/share/config")
    assert routes[i]["dest"] == "/api/share/config.py"
    assert i < srcs.index("/(.*)")


def test_kakao_sdk_is_pinned_with_integrity():
    app = _read(APP_JS)
    assert re.search(r"kakao_js_sdk/\d+\.\d+\.\d+/kakao\.min\.js", app)
    assert re.search(r"integrity: 'sha384-[A-Za-z0-9+/=]{64}'", app)
    assert "hidden: true" in app                     # 키가 없으면 카카오 버튼은 숨긴 채로
