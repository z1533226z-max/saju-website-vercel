"""/daily/ SSR: 표준 내비·푸터, 띠별 '함께 보면 좋은 운세' 링크 테스트."""
import os
import re
from datetime import datetime, timezone

import pytest

from _core import site_layout as sl
from _core.daily_fortune import KST, ZODIAC_DATA
from site_helpers import (
    ADSENSE_SCRIPT_RE, GENERIC_NOINDEX_RE, MANUAL_AD_SLOT_RE, PUBLIC, SIGNS,
    last_footer, load_module, parse, read_public, resolve_internal_href,
)

NOW = datetime(2026, 10, 5, 9, 0, tzinfo=KST)


@pytest.fixture(scope="module")
def index_mod():
    return load_module(os.path.join("api", "daily", "index.py"), "daily_index_layout_test")


@pytest.fixture(scope="module")
def fortune_mod():
    return load_module(os.path.join("api", "daily", "fortune.py"), "daily_fortune_layout_test")


def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def _related_block(html):
    m = re.search(r"<!-- DAILY_RELATED_V1 -->(.*?)<!-- /DAILY_RELATED_V1 -->", html, re.S)
    return m.group(1) if m else None


# ── 표준 내비·푸터 (정적 페이지와 같은 마크업) ──────────────────────
def test_layout_matches_standardize_script():
    script = load_module(os.path.join("scripts", "standardize_nav_footer.py"), "std_for_layout")
    assert list(sl.NAV_ITEMS) == script.NAV_ORDER
    assert list(sl.FOOTER_ITEMS) == script.NAV_ORDER + script.FOOTER_EXTRA
    for section in ("/daily/", "/zodiac/", None):
        assert sl.nav_links_html(section) == script.build_nav_html(section)
    assert sl.footer_links_html() == script.build_footer_html()


def test_ssr_nav_and_footer_equal_static_pages(index_mod, fortune_mod):
    static = read_public("daily/index.html")          # 같은 섹션(/daily/)의 정적 페이지
    static_nav = re.search(r'<nav class="nav-links">.*?</nav>', static, re.S).group(0)
    static_footer = re.search(r'<div class="footer-links">.*?</div>', last_footer(static), re.S).group(0)
    for html in (index_mod.render_index_html(NOW), fortune_mod.render_html("rat", NOW)):
        assert static_nav in html
        assert _norm(static_footer) in _norm(last_footer(html))
        assert 'href="/privacy/">개인정보처리방침</a>' in last_footer(html)


def test_ssr_pages_keep_single_auto_ads_tag_and_no_noindex(index_mod, fortune_mod):
    pages = [index_mod.render_index_html(NOW)] + [fortune_mod.render_html(s, NOW) for s in SIGNS]
    for html in pages:
        assert len(ADSENSE_SCRIPT_RE.findall(html)) == 1
        assert not MANUAL_AD_SLOT_RE.search(html)
        assert not GENERIC_NOINDEX_RE.search(html)
        assert "noindex" not in html.lower()


# ── '함께 보면 좋은 운세' ─────────────────────────────────────────
@pytest.mark.parametrize("sign", SIGNS)
def test_related_block_on_every_animal_page(fortune_mod, sign):
    html = fortune_mod.render_html(sign, NOW)
    block = _related_block(html)
    assert block is not None and "함께 보면 좋은 운세" in block
    hrefs = parse(block).hrefs
    assert 4 <= len(hrefs) <= sl.MAX_RELATED_LINKS
    assert f"/yearly/{sign}/#y2027" in hrefs
    assert f"/zodiac/{sign}/2026-10/" in hrefs
    assert f"/compatibility/{sign}/" in hrefs
    dreams = [h for h in hrefs if h.startswith("/dream/")]
    assert 1 <= len(dreams) <= 2
    name = ZODIAC_DATA[sign]["name"]
    assert f"{name} 2027 신년운세" in block and f"{name} 10월 운세" in block
    for href in hrefs:
        ok, why = resolve_internal_href(href)
        assert ok, (sign, href, why)


def test_related_block_order_puts_own_animal_dream_first():
    assert [h for h, _ in sl.related_links("snake", "뱀띠", NOW)][3:] == ["/dream/snake/", "/dream/dragon/"]
    assert [h for h, _ in sl.related_links("dragon", "용띠", NOW)][3:] == ["/dream/dragon/", "/dream/pig/"]
    assert [h for h, _ in sl.related_links("pig", "돼지띠", NOW)][3:] == ["/dream/pig/", "/dream/dragon/"]
    assert [h for h, _ in sl.related_links("rat", "쥐띠", NOW)][3:] == ["/dream/pig/", "/dream/dragon/"]


@pytest.mark.parametrize("now, expected", [
    (datetime(2026, 10, 5, 9, 0, tzinfo=KST), "/zodiac/rat/2026-10/"),
    (datetime(2026, 12, 31, 23, 0, tzinfo=KST), "/zodiac/rat/2026-12/"),
    (datetime(2026, 10, 31, 15, 30, tzinfo=timezone.utc), "/zodiac/rat/2026-11/"),   # = KST 11/1 00:30
    (datetime(2027, 1, 15, 12, 0, tzinfo=KST), "/zodiac/rat/"),                       # 2027 월별 페이지 없음
    (datetime(2026, 9, 15, 12, 0, tzinfo=KST), "/zodiac/rat/"),                       # 01~09월은 전 엔진 noindex
])
def test_month_link_uses_kst_month_or_falls_back(now, expected):
    hrefs = [h for h, _ in sl.related_links("rat", "쥐띠", now)]
    assert hrefs[1] == expected
    ok, why = resolve_internal_href(expected)
    assert ok, why


def test_month_link_label_for_fallback():
    links = sl.related_links("rat", "쥐띠", datetime(2027, 1, 15, tzinfo=KST))
    assert links[1] == ("/zodiac/rat/", "📅 쥐띠 운세 총정리")


def test_monthly_pages_constant_matches_public_files():
    """MONTHLY_PAGES = 12띠 모두에 있고 일반 robots noindex 가 아닌 달 (그 외 달은 없어야 함)."""
    linkable = None
    for sign in SIGNS:
        base = os.path.join(PUBLIC, "zodiac", sign)
        months = set()
        for ym in os.listdir(base):
            path = os.path.join(base, ym, "index.html")
            if re.fullmatch(r"\d{4}-\d{2}", ym) and os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    if not GENERIC_NOINDEX_RE.search(f.read()):
                        months.add(ym)
        linkable = months if linkable is None else linkable & months
        assert months == set(sl.MONTHLY_PAGES), (sign, sorted(months))
    assert linkable == set(sl.MONTHLY_PAGES)


def test_yearly_pages_have_2027_anchor():
    for sign in SIGNS:
        html = read_public(f"yearly/{sign}/index.html")
        assert f'id="{sl.YEARLY_2027_ANCHOR}"' in html, sign
        assert "Y2027_PREVIEW_V1" in html, sign


def test_dream_targets_are_deep_indexable_pages():
    for href, _label in sl.DREAM_PAGES.values():
        html = read_public(href.strip("/") + "/index.html")
        assert not GENERIC_NOINDEX_RE.search(html), href
        body = re.sub(r"<(script|style|head|header|footer|nav)\b.*?</\1>", "", html, flags=re.S)
        text = re.sub(r"\s+", "", re.sub(r"<[^>]+>", " ", body))
        assert len(text) >= 1500, (href, len(text))


def test_birth_year_upper_bound_is_current_year_in_js(index_mod):
    for html in (index_mod.render_index_html(NOW), read_public("daily/index.html")):
        assert 'id="birth-year"' in html
        assert "2025" not in html                          # 하드코딩된 상한 제거
        assert "BIRTH_YEAR_MAX = new Date().getFullYear()" in html
        assert "year > BIRTH_YEAR_MAX" in html


def test_every_internal_link_on_ssr_pages_resolves(index_mod, fortune_mod):
    pages = {"/daily/": index_mod.render_index_html(NOW)}
    pages.update({f"/daily/{s}/": fortune_mod.render_html(s, NOW) for s in SIGNS})
    for url, html in pages.items():
        p = parse(html)
        for href in p.hrefs:
            ok, why = resolve_internal_href(href, p.ids)
            assert ok, (url, href, why)
