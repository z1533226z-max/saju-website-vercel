"""홈 사주 계산기: 결과 아래 내 띠·일간 링크, '더 알아보기' 카드의 가이드 링크."""
import os
import re

import pytest

from site_helpers import PUBLIC, SIGNS, parse, read_public, resolve_internal_href


@pytest.fixture(scope="module")
def home():
    return read_public("index.html")


@pytest.fixture(scope="module")
def form_js():
    with open(os.path.join(PUBLIC, "js", "saju-form-enhanced.js"), encoding="utf-8") as f:
        return f.read()


def _section(html, start_marker, end_marker):
    i = html.find(start_marker)
    j = html.find(end_marker, i + len(start_marker))
    assert 0 <= i < j, (start_marker, end_marker)
    return html[i:j]


def test_learn_more_cards_link_to_real_guide_pages(home):
    section = _section(home, '<section id="additional-section">', "</section>")
    assert 'data-action="showInfoModal"' not in section
    hrefs = [h for h in parse(section).hrefs]
    assert hrefs == ["/guide/heavenly-stems/", "/guide/earthly-branches/", "/guide/five-elements/"]
    for href in hrefs:
        ok, why = resolve_internal_href(href)
        assert ok, (href, why)


def test_result_links_block_sits_inside_alpine_results(home):
    alpine_root = _section(home, '<div x-data="sajuForm()">', "<!-- End of Alpine.js component -->")
    results = _section(alpine_root, '<section id="results-section"', "<!-- 공유 버튼 -->")
    block = _section(results, "<!-- RESULT_NEXT_LINKS_V1", "<!-- /RESULT_NEXT_LINKS_V1 -->")
    assert 'x-show="zodiacKey"' in block
    assert ":href=\"'/yearly/' + zodiacKey + '/#y2027'\"" in block
    assert ":href=\"'/daily/' + zodiacKey + '/'\"" in block
    assert 'x-text="zodiacName"' in block and 'x-text="dayStemLabel"' in block
    # JS 가 꺼져 있어도 깨지지 않는 기본 링크 + 일간 가이드
    for href in parse(block).hrefs:
        ok, why = resolve_internal_href(href)
        assert ok, (href, why)
    assert "/guide/day-master/" in parse(block).hrefs


def test_form_component_defines_link_getters(form_js):
    for getter in ("get zodiacKey()", "get zodiacName()", "get dayStemLabel()"):
        assert getter in form_js, getter
    m = re.search(r"branchZodiacKeys:\s*\{(.*?)\}", form_js, re.S)
    mapping = dict(re.findall(r"'(.)':\s*'([a-z]+)'", m.group(1)))
    assert list(mapping) == list("자축인묘진사오미신유술해")
    assert tuple(mapping.values()) == SIGNS
    for sign in SIGNS:                       # 계산 결과로 만들어질 수 있는 모든 링크가 열리는지
        for href in (f"/yearly/{sign}/#y2027", f"/daily/{sign}/"):
            ok, why = resolve_internal_href(href)
            assert ok, (href, why)


def test_home_loads_updated_form_script(home):
    m = re.search(r'<script src="js/saju-form-enhanced\.js\?v=([^"]+)"></script>', home)
    assert m and m.group(1) != "20260218h"      # 캐시된 예전 JS(게터 없음)를 쓰지 않도록
