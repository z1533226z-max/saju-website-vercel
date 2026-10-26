"""KASI calculator samples from research541 (2026-10-26), not generated baselines.

Source: https://astro.kasi.re.kr/life/lunc?yyyy=YYYY&mm=MM&dd=DD
An absent leap-month row means invalid; never substitute its regular-month row.
"""
from datetime import datetime

import pytest

from _core.lunar_converter_improved import ImprovedLunarConverter
from saju import calculate, compatibility
from test_calculation_regression import post


KASI_SAMPLES = [
    (1914, 5, 1, True, "1914-06-24"),
    (1919, 10, 24, False, "1919-12-16"),
    (1928, 9, 19, False, "1928-11-01"),
    (1943, 11, 14, False, "1943-12-11"),
    (1954, 1, 8, False, "1954-02-11"),
    (1972, 12, 3, False, "1973-01-07"),
    (1987, 5, 27, False, "1987-06-23"),
    (1997, 1, 22, False, "1997-03-01"),
    (2012, 7, 15, False, "2012-09-01"),
    (2026, 9, 10, False, "2026-10-20"),
    (2036, 11, 5, False, "2036-12-22"),
    (2050, 2, 29, False, "2050-03-22"),
    (1914, 5, 30, True, None),
    (1914, 5, 30, False, "1914-06-23"),
    (2023, 2, 1, True, "2023-03-22"),
    (2025, 6, 1, True, "2025-07-25"),
    (2024, 1, 1, False, "2024-02-10"),
    (2025, 1, 1, False, "2025-01-29"),
    (2026, 1, 1, False, "2026-02-17"),
    (2012, 4, 1, False, "2012-05-21"),
    (2012, 7, 1, False, "2012-08-18"),
]

# All 37 leap months in 1930–2030, including Korean leap 3/2012 and 5/2017.
LEAP_MONTHS = [
    (1930, 6), (1933, 5), (1936, 3), (1938, 7), (1941, 6), (1944, 4),
    (1947, 2), (1949, 7), (1952, 5), (1955, 3), (1957, 8), (1960, 6),
    (1963, 4), (1966, 3), (1968, 7), (1971, 5), (1974, 4), (1976, 8),
    (1979, 6), (1982, 4), (1984, 10), (1987, 6), (1990, 5), (1993, 3),
    (1995, 8), (1998, 5), (2001, 4), (2004, 2), (2006, 7), (2009, 5),
    (2012, 3), (2014, 9), (2017, 5), (2020, 4), (2023, 2), (2025, 6),
    (2028, 5),
]


@pytest.mark.parametrize("year,month,day,leap,expected", KASI_SAMPLES)
def test_kasi_samples(year, month, day, leap, expected):
    converter = ImprovedLunarConverter()
    assert converter.validate_lunar_date(year, month, day, leap) == (expected is not None)
    actual = converter.lunar_to_solar(year, month, day, leap)
    assert actual == (datetime.fromisoformat(expected) if expected else None)
    if actual:
        assert converter.solar_to_lunar(actual) == {
            "year": year, "month": month, "day": day,
            "is_leap_month": leap, "success": True,
        }


@pytest.mark.parametrize("year,month", LEAP_MONTHS)
def test_all_37_korean_leap_months(year, month):
    converter = ImprovedLunarConverter()
    assert converter.get_leap_month(year) == month
    last_day = converter.get_lunar_month_days(year, month, True)
    for day in (1, 29, last_day):
        solar = converter.lunar_to_solar(year, month, day, True)
        assert solar is not None
        assert converter.solar_to_lunar(solar) == {
            "year": year, "month": month, "day": day,
            "is_leap_month": True, "success": True,
        }
    assert converter.validate_lunar_date(year, month, last_day + 1, True) is False


@pytest.mark.parametrize("lunar,solar", [
    ((1900, 1, 1), "1900-01-31"), ((2050, 11, 18), "2050-12-31"),
])
def test_lunar_range_boundaries(lunar, solar):
    assert ImprovedLunarConverter().lunar_to_solar(*lunar) == datetime.fromisoformat(solar)


@pytest.mark.parametrize("solar,lunar", [
    ("1900-01-01", (1899, 12, 1)), ("2050-12-31", (2050, 11, 18)),
])
def test_solar_range_boundaries(solar, lunar):
    assert ImprovedLunarConverter().solar_to_lunar(datetime.fromisoformat(solar)) == {
        "year": lunar[0], "month": lunar[1], "day": lunar[2],
        "is_leap_month": False, "success": True,
    }


@pytest.mark.parametrize("solar", ["1899-12-31", "2051-01-01", "2100-01-01"])
def test_solar_out_of_range_returns_explicit_failure(solar):
    result = ImprovedLunarConverter().solar_to_lunar(datetime.fromisoformat(solar))
    assert result["success"] is False
    assert result["error"]


@pytest.mark.parametrize("module,person_key", [
    (calculate, None), (compatibility, "person1"), (compatibility, "person2"),
])
@pytest.mark.parametrize("date,leap,expected", [
    ("2012-03-01", True, "2012-04-21"),
    ("2012-04-01", False, "2012-05-21"),
    ("2017-05-01", True, "2017-06-24"),
    ("1900-01-01", False, "1900-01-31"),
    ("2050-11-18", False, "2050-12-31"),
    ("2012-04-01", True, None), ("2017-06-01", True, None),
    ("1914-05-30", True, None), ("2023-01-30", False, None),
    ("2050-11-19", False, None), ("2050-12-01", False, None),
    ("1899-12-01", False, None), ("2051-01-01", False, None),
    ("2100-01-01", False, None),
])
def test_korean_dates_reach_both_apis(module, person_key, date, leap, expected):
    person = {"birthDate": date, "isLunar": True, "isLeapMonth": leap}
    payload = person
    if person_key:
        payload = {"person1": {"birthDate": "1990-05-15"},
                   "person2": {"birthDate": "1992-08-20"}, person_key: person}
    response = post(module, payload, 200 if expected else 400)
    if expected:
        saju = response[person_key]["saju"] if person_key else response["saju"]
        assert saju["birth_info"]["date"] == expected
        solar_person = {"birthDate": expected, "isLunar": False}
        if person_key:
            payload[person_key] = solar_person
        else:
            payload = solar_person
        solar_response = post(module, payload)
        solar_saju = solar_response[person_key]["saju"] if person_key else solar_response["saju"]
        for pillar in ("year", "month", "day", "hour"):
            assert saju[pillar] == solar_saju[pillar]
    else:
        assert response["error"]
