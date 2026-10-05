"""개인정보처리방침 페이지 · 전 페이지 푸터 링크 · 사이트맵 테스트."""
import os
import re
import xml.etree.ElementTree as ET

import pytest

from site_helpers import (
    ADSENSE_SCRIPT_RE, GA4_RE, GENERIC_NOINDEX_RE, MANUAL_AD_SLOT_RE, PUBLIC,
    last_footer, load_module, parse, public_html_files, read_public, resolve_internal_href,
)

SITE = "https://saju.gon.ai.kr"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
STANDARD_NAV = ('<nav class="nav-links"><a href="/">사주풀이</a><a href="/zodiac/">띠별 운세</a>'
                '<a href="/daily/">오늘의 운세</a><a href="/yearly/">2026년 운세</a>'
                '<a href="/compatibility/">궁합</a><a href="/dream/">꿈해몽</a>'
                '<a href="/palm/">손금 분석</a><a href="/guide/">사주 가이드</a></nav>')


@pytest.fixture(scope="module")
def privacy_html():
    return read_public("privacy/index.html")


# ── /privacy/ 페이지 ──────────────────────────────────────────────
def test_privacy_page_uses_site_template(privacy_html):
    assert len(ADSENSE_SCRIPT_RE.findall(privacy_html)) == 1     # 자동광고 태그 1개
    assert not MANUAL_AD_SLOT_RE.search(privacy_html)            # 수동 광고 슬롯 없음
    assert GA4_RE.search(privacy_html)
    assert STANDARD_NAV in privacy_html
    assert '<link rel="canonical" href="https://saju.gon.ai.kr/privacy/">' in privacy_html
    assert not GENERIC_NOINDEX_RE.search(privacy_html)
    assert 'href="/privacy/">개인정보처리방침</a>' in last_footer(privacy_html)


def test_privacy_page_discloses_what_the_code_does(privacy_html):
    required = [
        "2026년 10월 5일",                                            # 시행일
        "Google을 포함한 제3자 광고 사업자는 쿠키를 사용하여",          # 애드센스 필수 고지
        "https://adssettings.google.com",
        "https://policies.google.com/technologies/ads",
        "Google 애널리틱스",
        "_ga",
        "Gemini API",
        "Google LLC",
        "저장하지 않습니다",                                           # 입력값·사진 비저장
        "IP 주소",                                                    # 손금 이용 횟수 제한(메모리)
        "localStorage",
        "Vercel",
        "쿠키를 거부하는 방법",
    ]
    for phrase in required:
        assert phrase in privacy_html, phrase


def test_privacy_page_has_no_email_address(privacy_html):
    assert not EMAIL_RE.search(privacy_html)


def test_privacy_page_internal_links_resolve(privacy_html):
    p = parse(privacy_html)
    for href in p.hrefs:
        ok, why = resolve_internal_href(href, p.ids)
        assert ok, (href, why)


def test_saju_and_palm_handlers_do_not_persist_inputs():
    """방침 문구('서버에 저장하지 않습니다')의 근거: 핸들러에 파일 쓰기·DB 저장이 없다."""
    for rel in ("api/saju/calculate.py", "api/saju/compatibility.py", "api/palm/analyze.py"):
        with open(os.path.join(os.path.dirname(PUBLIC), rel), encoding="utf-8") as f:
            src = f.read()
        assert not re.search(r"open\([^)]*['\"][wa]b?['\"]", src), rel
        assert "sqlalchemy" not in src and "database" not in src.lower(), rel


# ── 전 페이지 푸터 링크 ────────────────────────────────────────────
def test_every_public_page_footer_links_privacy():
    missing = []
    for rel in public_html_files():
        if rel == "additional-features.html":          # 홈 화면 조각(fragment) — 푸터 없음
            continue
        if 'href="/privacy/"' not in last_footer(read_public(rel)):
            missing.append(rel)
    assert not missing, missing[:10]


def test_privacy_footer_script_is_idempotent():
    script = load_module(os.path.join("scripts", "add_privacy_footer_link.py"), "privacy_footer_script")
    for rel in ("index.html", "yearly/rat/index.html", "en/index.html", "guide/index.html",
                "palm/index.html", "privacy/index.html"):
        html = read_public(rel)
        new_html, status = script.add_privacy_link(html, rel)
        assert status == "already" and new_html == html, rel


def test_privacy_footer_script_handles_each_footer_shape():
    script = load_module(os.path.join("scripts", "add_privacy_footer_link.py"), "privacy_footer_script2")
    ko = ('<footer class="site-footer">\r\n            <div class="footer-links">\r\n'
          '                <a href="/">사주풀이</a>\r\n            </div>\r\n    </footer>')
    out, status = script.add_privacy_link(ko, "zodiac/rat/index.html")
    assert status == "list"
    assert '<a href="/">사주풀이</a>\r\n                <a href="/privacy/">개인정보처리방침</a>\r\n            </div>' in out
    en_out, _ = script.add_privacy_link(ko, "en/index.html")
    assert '<a href="/privacy/" hreflang="ko">Privacy Policy (개인정보처리방침)</a>' in en_out
    inline = '<footer><p>&copy; <a href="/" style="color: red;">홈</a> · <a href="/guide/" style="color: red;">가이드</a></p></footer>'
    out, status = script.add_privacy_link(inline, "guide/index.html")
    assert status == "inline"
    assert '가이드</a> · <a href="/privacy/" style="color: red;">개인정보처리방침</a></p>' in out
    assert script.add_privacy_link(out, "guide/index.html")[1] == "already"
    assert script.add_privacy_link("<footer><p>no links</p></footer>", "x.html")[1] == "unknown"


def test_standardize_script_keeps_privacy_link_in_footer():
    """standardize_nav_footer.py 를 다시 돌려도 개인정보처리방침 링크가 지워지지 않아야 한다."""
    script = load_module(os.path.join("scripts", "standardize_nav_footer.py"), "standardize_script")
    footer = script.build_footer_html()
    assert footer.startswith('<div class="footer-links">')
    assert '<a href="/privacy/">개인정보처리방침</a>' in footer
    assert script.build_nav_html(script.detect_section("privacy/index.html")) == STANDARD_NAV
    std = read_public("yearly/rat/index.html")
    assert script.FOOTER_PATTERN.search(std).group(0) == footer


# ── sitemap.xml ───────────────────────────────────────────────────
@pytest.fixture(scope="module")
def sitemap_locs():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.parse(os.path.join(PUBLIC, "sitemap.xml")).getroot()
    return [e.text.strip() for e in root.findall("s:url/s:loc", ns)]


def test_sitemap_lists_privacy_once(sitemap_locs):
    assert sitemap_locs.count(f"{SITE}/privacy/") == 1
    assert len(sitemap_locs) == len(set(sitemap_locs))
