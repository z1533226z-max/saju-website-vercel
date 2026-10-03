"""SajuCalculator 기준값 회귀 테스트 (만세력 대조값)."""
from datetime import datetime

import pytest

from _core.saju_calculator import SajuCalculator


@pytest.fixture(scope="module")
def calc():
    return SajuCalculator()


def _hanja(pillar):
    return pillar["heavenly_hanja"] + pillar["earthly_hanja"]


# ── 일주: 1900-01-01 = 甲戌일 기준 ──────────────────────────────
@pytest.mark.parametrize("ymd, expected", [
    ((1900, 1, 1), "甲戌"),
    ((1899, 12, 31), "癸酉"),   # 1900년 이전 역산 경로
    ((1949, 10, 1), "甲子"),
    ((1990, 5, 15), "庚辰"),
    ((2000, 1, 1), "戊午"),
    ((2026, 10, 3), "庚戌"),
])
def test_day_pillar(calc, ymd, expected):
    assert _hanja(calc.calculate_day_pillar(datetime(*ymd))) == expected


def test_day_pillar_ignores_time_of_day(calc):
    assert _hanja(calc.calculate_day_pillar(datetime(2026, 10, 3, 15, 30))) == "庚戌"


# ── 년주: 입춘(2월 4일경) 이전 출생은 전년도 ─────────────────────
@pytest.mark.parametrize("ymd, expected_year, expected_zodiac", [
    ((2000, 1, 1), "己卯", "토끼"),
    ((2000, 2, 3), "己卯", "토끼"),
    ((2000, 2, 4), "庚辰", "용"),
    ((2000, 12, 31), "庚辰", "용"),
    ((1990, 5, 15), "庚午", "말"),
    ((2026, 10, 3), "丙午", "말"),
])
def test_year_pillar_uses_ipchun_boundary(calc, ymd, expected_year, expected_zodiac):
    saju = calc.calculate_saju(datetime(*ymd), "12:00", "male")
    assert _hanja(saju["year"]) == expected_year
    assert saju["year"]["zodiac"] == expected_zodiac


# ── 월주: 월간은 입춘 기준 년간으로 계산 ─────────────────────────
@pytest.mark.parametrize("ymd, expected", [
    ((2000, 1, 1), "丙子"),    # 소한 전 → 己卯년 자월
    ((2000, 1, 10), "丁丑"),   # 소한 후·입춘 전 → 己卯년 축월
    ((2000, 2, 3), "丁丑"),    # 입춘 전 → 己卯년 축월
    ((2000, 2, 10), "戊寅"),   # 입춘 후 → 庚辰년 인월
    ((1990, 5, 15), "辛巳"),
    ((2026, 10, 3), "丁酉"),   # 한로(10/8) 전 → 유월
])
def test_month_pillar(calc, ymd, expected):
    saju = calc.calculate_saju(datetime(*ymd), "12:00", "male")
    assert _hanja(saju["month"]) == expected


def test_hour_pillar_follows_day_stem(calc):
    # 庚일 오시 → 壬午시 (乙庚일 丙子시 기준)
    saju = calc.calculate_saju(datetime(2026, 10, 3), "12:00", "female")
    assert _hanja(saju["day"]) == "庚戌"
    assert _hanja(saju["hour"]) == "壬午"


def test_saju_year_helper(calc):
    assert calc.get_saju_year(2000, 1, 1) == 1999
    assert calc.get_saju_year(2000, 2, 3) == 1999
    assert calc.get_saju_year(2000, 2, 4) == 2000
    assert calc.get_saju_year(2000, 11, 30) == 2000
