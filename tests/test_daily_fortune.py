"""/daily/ 오늘의 운세: 일진 + 지지 관계 기반 점수 테스트."""
import importlib.util
import os
import re
from datetime import datetime, timedelta
from html.parser import HTMLParser

import pytest

from _core import daily_fortune as df

API_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api")
NOW = datetime(2026, 10, 3, 9, 0, tzinfo=df.KST)   # 庚戌일


def _load(rel_path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(API_DIR, rel_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def index_mod():
    return _load(os.path.join("daily", "index.py"), "daily_index_under_test")


@pytest.fixture(scope="module")
def fortune_mod():
    return _load(os.path.join("daily", "fortune.py"), "daily_fortune_under_test")


# ── 일진 ────────────────────────────────────────────────────────
def test_day_ilji_2026_10_03():
    il = df.get_day_ilji(NOW)
    assert il["hanja"] == "庚戌"
    assert il["name_ko"] == "경술"
    assert il["branch_index"] == 10
    assert il["element"] == "금"


def test_day_ilji_uses_kst_date():
    # UTC 2026-10-02 20:00 == KST 2026-10-03 05:00
    from datetime import timezone
    utc = datetime(2026, 10, 2, 20, 0, tzinfo=timezone.utc)
    assert df.get_day_ilji(utc)["hanja"] == "庚戌"


# ── 지지 관계 (子0 丑1 寅2 卯3 辰4 巳5 午6 未7 申8 酉9 戌10 亥11) ─────
@pytest.mark.parametrize("mine, day, key", [
    # 오늘(戌) 기준 12띠
    (3, 10, "yukhap"), (2, 10, "samhap"), (6, 10, "samhap"),
    (4, 10, "chung"), (1, 10, "hyeong"), (7, 10, "hyeong"),
    (9, 10, "hae"), (5, 10, "wonjin"),
    (0, 10, "pyeong"), (8, 10, "pyeong"), (11, 10, "pyeong"), (10, 10, "pyeong"),
    # 기타 대표 관계
    (0, 1, "yukhap"), (2, 11, "yukhap"), (5, 8, "yukhap"),
    (0, 6, "chung"), (6, 6, "hyeong"), (0, 3, "hyeong"), (2, 5, "hyeong"),
    (0, 7, "wonjin"), (1, 6, "wonjin"), (2, 9, "wonjin"),
    (0, 9, "pa"), (3, 6, "pa"), (3, 4, "hae"), (8, 11, "hae"),
])
def test_branch_relation(mine, day, key):
    assert df.branch_relation(mine, day)["key"] == key


def test_branch_relation_is_symmetric():
    for a in range(12):
        for b in range(12):
            assert df.branch_relation(a, b)["key"] == df.branch_relation(b, a)["key"]


def test_branch_relation_lists_secondary():
    rel = df.branch_relation(5, 8)   # 巳申: 육합 + 형 + 파
    assert rel["key"] == "yukhap"
    assert set(rel["also"]) == {"hyeong", "pa"}


def test_every_relation_has_plain_korean_explanation():
    for a in range(12):
        for b in range(12):
            rel = df.branch_relation(a, b)
            assert rel["label"] and rel["explain"]
            assert re.search(r"[가-힣]", rel["explain"])


# ── 점수: 관계가 범위를 결정 ──────────────────────────────────────
def test_scores_bounded_by_relation_today():
    for key in df.ZODIAC_ORDER:
        f = df.generate_fortune(key, NOW)
        lo, hi = df.RELATIONS[f["relation"]["key"]]["band"]
        assert lo <= f["overall"] <= hi, (key, f["overall"], f["relation"]["key"])
    assert df.generate_fortune("rabbit", NOW)["overall"] > df.generate_fortune("dragon", NOW)["overall"]


def test_scores_bounded_and_lucky_numbers_distinct_over_a_year():
    for d in range(400):
        now = NOW + timedelta(days=d)
        for key in df.ZODIAC_ORDER:
            f = df.generate_fortune(key, now)
            lo, hi = df.RELATIONS[f["relation"]["key"]]["band"]
            assert lo <= f["overall"] <= hi
            for k in ("money", "love", "health"):
                assert 40 <= f[k] <= 99
            a, b = (int(x) for x in f["lucky_number"].split(", "))
            assert 1 <= a < b <= 45, (now, key, f["lucky_number"])


def test_fortune_is_deterministic_per_day():
    assert df.generate_fortune("tiger", NOW) == df.generate_fortune("tiger", NOW)


def test_cache_control_expires_at_kst_midnight():
    from datetime import timezone
    utc_2300_kst = datetime(2026, 10, 3, 14, 0, tzinfo=timezone.utc)   # KST 23:00
    assert df.cache_control_until_midnight(utc_2300_kst) == \
        "public, s-maxage=3600, max-age=300, stale-while-revalidate=60"


# ── 전체 운세 지수: 일진 ↔ 월주 ─────────────────────────────────
def test_month_pillar_uses_solar_term_month():
    assert df.get_month_pillar(NOW)["hanja"] == "丁酉"                        # 한로(10/8) 전
    assert df.get_month_pillar(NOW + timedelta(days=5))["hanja"] == "戊戌"    # 10/8 한로 후


@pytest.mark.parametrize("day_el, month_el, key", [
    ("금", "금", "wang"), ("수", "금", "sang"), ("화", "토", "hyu"),
    ("목", "토", "su"), ("목", "금", "sa"), ("토", "목", "sa"), ("화", "수", "sa"),
])
def test_season_strength(day_el, month_el, key):
    assert df.season_strength(day_el, month_el) == key


def test_day_energy_today_is_explained():
    e = df.day_energy(NOW)   # 庚 in 酉월 = 왕, 戌↔酉 = 해
    assert (e["strength"], e["relation"]) == ("wang", "hae")
    assert e["score"] == df.DAY_ENERGY_BASE + 10 - 5 == 73
    for part in ("정유(丁酉)월", "기본 68", "왕(旺) +10", "해(害) −5"):
        assert part in e["reason"], part


def test_day_energy_varies_and_matches_its_reason_over_a_year():
    scores = []
    for d in range(365):
        e = df.day_energy(NOW + timedelta(days=d))
        expected = (df.DAY_ENERGY_BASE + df.SEASON_STRENGTH[e["strength"]][1]
                    + df.MONTH_RELATION_POINTS[e["relation"]])
        assert e["score"] == expected
        assert 40 <= e["score"] <= 95
        scores.append(e["score"])
    assert max(scores) - min(scores) >= 30
    assert len(set(scores)) >= 15
    assert sum(1 for a, b in zip(scores, scores[1:]) if a != b) > 300


# ── 렌더링 ──────────────────────────────────────────────────────
class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href"))


def test_index_renders_ilji_relations_and_links(index_mod):
    html = index_mod.render_index_html(NOW)
    assert "경술(庚戌)" in html
    assert "육합" in html and "충(沖)" in html
    p = _Parser()
    p.feed(html)
    for href in ("/yearly/", "/dream/", "/compatibility/", "/palm/"):
        assert href in p.hrefs, href
    assert "{f[" not in html and "{z[" not in html
    e = df.day_energy(NOW)
    assert f"{e['score']}<small>/100</small>" in html and e["reason"] in html
    assert "12띠 총운 평균" not in html


def test_detail_page_matches_index_scores(index_mod, fortune_mod):
    for key in ("rabbit", "dragon"):
        a = index_mod.generate_fortune(key, NOW)
        b = fortune_mod.generate_fortune(key, NOW)
        assert a == b
    html = fortune_mod.render_html("rabbit", NOW)
    f = df.generate_fortune("rabbit", NOW)
    assert "경술(庚戌)" in html and "육합" in html
    assert f"{f['overall']}<small>점</small>" in html
    assert "오늘 일진과 육합(六合) 관계, 총운" in html
