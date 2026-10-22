"""구글용 sitemap.xml · 네이버용 sitemap-naver.xml · robots.txt 정합성, lastmod 규칙, 홈에서의 크롤 경로."""
import os
import re
import xml.etree.ElementTree as ET
from collections import deque
from datetime import date, timedelta
from urllib.parse import urlsplit

import pytest

from site_helpers import PUBLIC, SSR_ROUTE_RE, GENERIC_NOINDEX_RE, load_module, parse, public_file_for

SITE = "https://saju.gon.ai.kr"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
GOOGLEBOT_NOINDEX_RE = re.compile(r'<meta\s+name="googlebot"\s+content="[^"]*noindex', re.I)
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')


def _entries(name):
    root = ET.parse(os.path.join(PUBLIC, name)).getroot()
    out = []
    for url in root.findall("s:url", NS):
        lastmod = url.find("s:lastmod", NS)
        out.append((url.find("s:loc", NS).text, lastmod.text if lastmod is not None else None))
    return out


def _path(loc):
    assert loc.startswith(SITE + "/"), loc
    return loc[len(SITE):]


def _html(path):
    f = public_file_for(path)
    assert f, f"no file for {path}"
    with open(f, encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def google():
    return _entries("sitemap.xml")


@pytest.fixture(scope="module")
def naver():
    return _entries("sitemap-naver.xml")


@pytest.fixture(scope="module")
def lastmod_script():
    return load_module(os.path.join("scripts", "update_sitemap_lastmod.py"), "update_sitemap_lastmod")


def test_robots_txt_points_google_to_sitemap_only():
    with open(os.path.join(PUBLIC, "robots.txt"), encoding="utf-8") as f:
        robots = f.read()
    assert f"Sitemap: {SITE}/sitemap.xml" in robots
    assert "sitemap-naver.xml" not in robots          # 네이버용(구글 noindex 페이지)은 서치어드바이저에 직접 제출


def test_sitemaps_do_not_overlap_or_repeat(google, naver):
    g = [loc for loc, _ in google]
    n = [loc for loc, _ in naver]
    assert len(g) == len(set(g)) and len(n) == len(set(n))
    assert not set(g) & set(n)


def test_google_sitemap_lists_only_indexable_self_canonical_pages(google):
    bad = []
    for loc, _ in google:
        path = _path(loc)
        if SSR_ROUTE_RE.match(path):
            continue                                  # 서버 렌더 — test_daily_head.py 가 따로 확인
        html = _html(path)
        canonical = CANONICAL_RE.search(html)
        if GENERIC_NOINDEX_RE.search(html) or GOOGLEBOT_NOINDEX_RE.search(html):
            bad.append((loc, "noindex"))
        elif not canonical or canonical.group(1) != loc:
            bad.append((loc, canonical.group(1) if canonical else "no canonical"))
    assert not bad, bad[:10]


def test_naver_sitemap_lists_google_only_noindex_pages(naver):
    bad = []
    for loc, _ in naver:
        html = _html(_path(loc))
        if not GOOGLEBOT_NOINDEX_RE.search(html) or GENERIC_NOINDEX_RE.search(html):
            bad.append(loc)                           # 네이버는 색인돼야 하고 구글만 빠져야 함
    assert not bad, bad[:10]


def test_lastmod_rules(google, naver):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    for loc, lastmod in google + naver:
        if SSR_ROUTE_RE.match(_path(loc)):
            assert lastmod is None, loc               # 매일 바뀌는 페이지에 고정 날짜를 주지 않는다
        else:
            assert lastmod and re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod), loc
            assert lastmod <= tomorrow, loc


def test_content_signature_ignores_shared_footer_but_not_body(lastmod_script):
    sig = lastmod_script.content_signature
    page = ('<html><head><title>T</title><meta name="description" content="D"></head><body>'
            '<nav><a href="/">홈</a></nav><main>본문</main><footer>{}</footer></body></html>')
    assert sig(page.format("ⓒ")) == sig(page.format('<a href="/privacy/">개인정보처리방침</a>'))
    assert sig(page.format("ⓒ")) != sig(page.format("ⓒ").replace("본문", "새 본문"))
    assert sig(page) != sig(page.replace("<title>T", "<title>T2"))
    noindex = page.replace("</head>", '<meta name="googlebot" content="noindex, follow"></head>')
    assert sig(page) != sig(noindex)


def test_content_signature_tracks_structured_data_links_and_images(lastmod_script):
    sig = lastmod_script.content_signature
    ld = '<script type="application/ld+json">{{"@type":"Article","headline":"{}"}}</script>'
    page = ('<html><head><title>T</title>' + ld + '</head><body><nav><a href="/n/">홈</a></nav>'
            '<main><a href="/old/">풀이</a><img src="old.jpg" alt="옛">본문</main>'
            '<footer><a href="/f1/">푸터</a></footer></body></html>')
    base = page.format("A")
    assert sig(base) != sig(page.format("New"))                                  # JSON-LD 값
    assert sig(base) != sig(base.replace("/old/", "/new/"))                      # 본문 링크
    assert sig(base) != sig(base.replace("old.jpg", "new.jpg"))                  # 이미지 src
    assert sig(base) != sig(base.replace('alt="옛"', 'alt="새"'))                 # 이미지 alt
    assert sig(base) == sig(base.replace("/f1/", "/f2/").replace("/n/", "/m/"))  # 공통 nav/footer 링크 제외
    reordered = base.replace('{"@type":"Article","headline":"A"}', '{ "headline": "A", "@type": "Article" }')
    assert sig(base) == sig(reordered)                                           # JSON-LD 키 순서·공백 정규화


@pytest.mark.parametrize("loc", [f"{SITE}/", f"{SITE}/palm/", f"{SITE}/yearly/rat/"])
def test_sample_lastmod_matches_last_content_change(google, lastmod_script, loc):
    """전체(약 80초)는 `python scripts/update_sitemap_lastmod.py --check` 로 확인."""
    assert dict(google)[loc] == lastmod_script.expected_lastmod(loc)


def test_every_google_url_is_reachable_from_home_without_javascript(google):
    """홈에서 정적 HTML 의 <a href> 만 따라가 사이트맵 URL 전부에 닿는다 (서버 렌더 페이지는 도착만 확인)."""
    seen, queue = {"/"}, deque([("/", 0)])
    depth = {"/": 0}
    while queue:
        path, d = queue.popleft()
        if SSR_ROUTE_RE.match(path) or public_file_for(path) is None:
            continue
        for href in parse(_html(path)).hrefs:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or not parts.path.startswith("/"):
                continue
            nxt = parts.path
            if nxt not in seen and (SSR_ROUTE_RE.match(nxt) or public_file_for(nxt)):
                seen.add(nxt)
                depth[nxt] = d + 1
                queue.append((nxt, d + 1))
    missing = [loc for loc, _ in google if _path(loc) not in seen]
    assert not missing, missing[:10]
    assert max(depth[_path(loc)] for loc, _ in google) <= 3
