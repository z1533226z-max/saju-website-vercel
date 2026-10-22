"""Fixed calculation regressions; no network, clock, or production services.

Pillars/scores characterize the checked-in implementation, not an astronomical
almanac certification. Solar terms currently use approximate fixed calendar
days; midnight follows the existing civil-date (not late-zi next-day) rule.
Lunar conversion cases include the formerly reported D231 defects.
"""
from datetime import datetime, timezone
from io import BytesIO
import json

import pytest

from _core import daily_fortune as df
from _core.lunar_converter_improved import ImprovedLunarConverter
from _core.saju_calculator import SajuCalculator
from daily.fortune import render_html
from saju import calculate, compatibility


def pillars(saju):
    return tuple(
        saju[key]["heavenly_hanja"] + saju[key]["earthly_hanja"]
        for key in ("year", "month", "day", "hour")
    )


def post(module, payload, expected_status=200):
    """Run the real POST parsing/calculation/JSON path using in-memory streams."""
    raw = json.dumps(payload).encode("utf-8")
    handler = object.__new__(module.handler)
    handler.headers = {"Content-Length": str(len(raw))}
    handler.rfile = BytesIO(raw)
    handler.wfile = BytesIO()
    statuses, headers = [], {}
    handler.send_response = statuses.append
    handler.send_header = lambda key, value: headers.update({key: value})
    handler.end_headers = lambda: None
    handler.do_POST()
    assert statuses == [expected_status], handler.wfile.getvalue().decode("utf-8")
    assert headers["Content-Type"] == "application/json; charset=utf-8"
    response = json.loads(handler.wfile.getvalue())
    assert response["status"] == ("success" if expected_status == 200 else "error")
    return response


@pytest.mark.parametrize("date,time,expected", [
    ("2000-01-05", "12:00", ("己卯", "丙子", "壬戌", "丙午")),
    ("2000-01-06", "12:00", ("己卯", "丁丑", "癸亥", "戊午")),
    ("2000-02-03", "23:59", ("己卯", "丁丑", "辛卯", "戊子")),
    ("2000-02-04", "00:00", ("庚辰", "戊寅", "壬辰", "庚子")),
    ("2026-10-07", "12:00", ("丙午", "丁酉", "甲寅", "庚午")),
    ("2026-10-08", "12:00", ("丙午", "戊戌", "乙卯", "壬午")),
    ("2026-10-03", "22:59", ("丙午", "丁酉", "庚戌", "丁亥")),
    ("2026-10-03", "23:00", ("丙午", "丁酉", "庚戌", "丙子")),
    ("2026-10-03", "23:59", ("丙午", "丁酉", "庚戌", "丙子")),
    ("2026-10-04", "00:00", ("丙午", "丁酉", "辛亥", "戊子")),
    ("2026-10-04", "00:59", ("丙午", "丁酉", "辛亥", "戊子")),
    ("2026-10-04", "01:00", ("丙午", "丁酉", "辛亥", "己丑")),
])
def test_saju_solar_terms_and_midnight(date, time, expected):
    result = post(calculate, {
        "birthDate": date, "birthTime": time, "gender": "male",
    })
    assert pillars(result["saju"]) == expected
    assert result["saju"]["birth_info"]["date"] == date
    assert result["saju"]["birth_info"]["time"] == time


@pytest.mark.parametrize("lunar_date,leap,solar_date,expected", [
    ((2024, 1, 1), False, "2024-02-10", ("甲辰", "丙寅", "甲辰", "庚午")),
    ((2023, 2, 1), False, "2023-02-20", ("癸卯", "甲寅", "己酉", "庚午")),
    ((2023, 2, 1), True, "2023-03-22", ("癸卯", "乙卯", "己卯", "庚午")),
    ((2023, 2, 29), True, "2023-04-19", ("癸卯", "丙辰", "丁未", "丙午")),
])
def test_lunar_round_trip_and_pillars(lunar_date, leap, solar_date, expected):
    converter = ImprovedLunarConverter()
    converted = converter.lunar_to_solar(*lunar_date, is_leap_month=leap)
    assert converted == datetime.fromisoformat(solar_date)
    assert converter.solar_to_lunar(converted) == {
        "year": lunar_date[0], "month": lunar_date[1], "day": lunar_date[2],
        "is_leap_month": leap, "success": True,
    }
    assert pillars(SajuCalculator().calculate_saju(converted, "12:00", "male")) == expected


def test_saju_api_lunar_and_solar_inputs_reach_same_result():
    common = {"birthTime": "12:00", "gender": "male"}
    lunar = post(calculate, dict(common, birthDate="2024-01-01", isLunar=True))
    solar = post(calculate, dict(common, birthDate="2024-02-10", isLunar=False))
    assert pillars(lunar["saju"]) == ("甲辰", "丙寅", "甲辰", "庚午")
    for key in ("saju", "elements", "interpretation", "pattern", "shinshal", "yongshin"):
        assert lunar[key] == solar[key], key


@pytest.mark.parametrize("date1,date2,expected1,expected2,scores", [
    ("1990-05-15", "1992-08-20", ("庚午", "辛巳", "庚辰", "壬午"),
     ("壬申", "戊申", "戊辰", "辛酉"), (60.1, 34, 65, 75.0, "보통 (Average)")),
    ("2000-01-01", "2000-02-04", ("己卯", "丙子", "戊午", "戊午"),
     ("庚辰", "戊寅", "壬辰", "己酉"), (83.0, 94, 86.2, 56.2, "매우 좋음 (Excellent)")),
])
def test_compatibility_fixed_birth_inputs(date1, date2, expected1, expected2, scores):
    result = post(compatibility, {
        "person1": {"birthDate": date1, "birthTime": "12:00", "gender": "male"},
        "person2": {"birthDate": date2, "birthTime": "18:30", "gender": "female"},
    })
    assert pillars(result["person1"]["saju"]) == expected1
    assert pillars(result["person2"]["saju"]) == expected2
    assert tuple(result["compatibility"][key] for key in (
        "overall_score", "element_compatibility", "heavenly_stem_compatibility",
        "earthly_branch_compatibility", "compatibility_level",
    )) == scores


@pytest.mark.parametrize("person_key", ["person1", "person2"])
def test_compatibility_lunar_input_converted_for_either_person(person_key):
    payload = {
        "person1": {"birthDate": "2024-02-10", "birthTime": "12:00", "gender": "male"},
        "person2": {"birthDate": "2024-02-10", "birthTime": "12:00", "gender": "female"},
    }
    solar = post(compatibility, payload)
    payload[person_key].update(birthDate="2024-01-01", isLunar=True)
    lunar = post(compatibility, payload)
    assert lunar[person_key]["saju"]["birth_info"]["date"] == "2024-02-10"
    assert pillars(lunar[person_key]["saju"]) == ("甲辰", "丙寅", "甲辰", "庚午")
    for key in ("person1", "person2"):
        assert lunar[key]["elements"] == solar[key]["elements"]
    # Existing policy adds two points for one lunar input, even for the same birthday.
    assert lunar["compatibility"]["overall_score"] == min(
        100, solar["compatibility"]["overall_score"] + 2,
    )


@pytest.mark.parametrize("sign,expected,relation", [
    ("rat", (70, 65, 71, 70, "28, 45", "분홍", "동북쪽", "10시"), "pyeong"),
    ("ox", (61, 56, 56, 67, "6, 28", "하늘색", "서남쪽", "3시"), "hyeong"),
    ("tiger", (93, 87, 91, 96, "16, 27", "노랑", "북쪽", "2시"), "samhap"),
    ("rabbit", (88, 82, 80, 97, "20, 40", "파랑", "동남쪽", "12시"), "yukhap"),
    ("dragon", (54, 48, 61, 48, "9, 26", "보라", "동남쪽", "6시"), "chung"),
    ("snake", (65, 59, 55, 58, "36, 39", "은색", "동쪽", "4시"), "wonjin"),
    ("horse", (82, 75, 82, 73, "10, 12", "파랑", "동남쪽", "9시"), "samhap"),
    ("goat", (58, 51, 57, 63, "14, 45", "남색", "동북쪽", "10시"), "hyeong"),
    ("monkey", (75, 68, 67, 85, "12, 35", "파랑", "동북쪽", "9시"), "pyeong"),
    ("rooster", (56, 49, 63, 55, "12, 36", "갈색", "동북쪽", "12시"), "hae"),
    ("dog", (68, 61, 58, 63, "21, 40", "금색", "동남쪽", "4시"), "pyeong"),
    ("pig", (73, 65, 78, 73, "21, 42", "초록", "서북쪽", "2시"), "pyeong"),
])
def test_all_zodiacs_fixed_scores_and_rendered_result(sign, expected, relation):
    now = datetime(2026, 10, 3, 12, tzinfo=df.KST)
    fortune = df.generate_fortune(sign, now)
    assert fortune["ilji"]["hanja"] == "庚戌"
    assert fortune["relation"]["key"] == relation
    assert tuple(fortune[key] for key in (
        "overall", "money", "love", "health", "lucky_number",
        "lucky_color", "lucky_dir", "lucky_time",
    )) == expected
    html = render_html(sign, now)
    assert f'{expected[0]}<small>점</small>' in html
    assert expected[4] in html
    assert fortune["overall_msg"] in html


@pytest.mark.parametrize("utc_time,expected_day,expected", [
    ("2026-10-03T14:59:59+00:00", "庚戌", (88, 82, 80, 97, "20, 40")),
    ("2026-10-03T15:00:00+00:00", "辛亥", (93, 90, 98, 94, "23, 40")),
])
def test_fortune_kst_midnight_fixed_results(utc_time, expected_day, expected):
    utc = datetime.fromisoformat(utc_time)
    assert utc.tzinfo == timezone.utc
    fortune = df.generate_fortune("rabbit", utc)
    assert fortune == df.generate_fortune("rabbit", utc.astimezone(df.KST))
    assert fortune["ilji"]["hanja"] == expected_day
    assert tuple(fortune[key] for key in (
        "overall", "money", "love", "health", "lucky_number",
    )) == expected


def test_core_lunar_conversion():
    result = SajuCalculator().calculate_saju(
        datetime(2024, 1, 1), "12:00", "male", is_lunar=True,
    )
    assert result["birth_info"]["date"] == "2024-02-10"
    assert pillars(result) == ("甲辰", "丙寅", "甲辰", "庚午")


@pytest.mark.parametrize("module,person_key", [
    (calculate, None), (compatibility, "person1"), (compatibility, "person2"),
])
def test_api_leap_month(module, person_key):
    person = {
        "birthDate": "2023-02-01", "birthTime": "12:00", "gender": "male",
        "isLunar": True, "isLeapMonth": True,
    }
    if person_key:
        payload = {
            "person1": {"birthDate": "1990-05-15"},
            "person2": {"birthDate": "1992-08-20"},
        }
        payload[person_key] = person
        saju = post(module, payload)[person_key]["saju"]
    else:
        saju = post(module, person)["saju"]
    assert saju["birth_info"]["date"] == "2023-03-22"
    assert pillars(saju) == ("癸卯", "乙卯", "己卯", "庚午")


def test_invalid_leap_month_day_is_rejected():
    converter = ImprovedLunarConverter()
    assert converter.validate_lunar_date(2023, 2, 30, True) is False
    assert converter.lunar_to_solar(2023, 2, 30, True) is None


@pytest.mark.parametrize("date,leap", [
    ((2023, 3, 1), True), ((2024, 2, 1), True),
    ((2023, 1, 30), False), ((2023, 2, 30), True),
])
def test_converter_rejects_invalid_lunar_dates_without_correction(date, leap):
    converter = ImprovedLunarConverter()
    assert converter.validate_lunar_date(*date, leap) is False
    assert converter.lunar_to_solar(*date, leap) is None


@pytest.mark.parametrize("leap,expected", [(False, "2023-02-20"), (True, "2023-03-22")])
def test_core_distinguishes_regular_and_leap_month(leap, expected):
    result = SajuCalculator().calculate_saju(
        datetime(2023, 2, 1), "12:00", "male", is_lunar=True, is_leap_month=leap,
    )
    assert result["birth_info"]["date"] == expected
    assert result["birth_info"]["is_lunar"] is True


def test_core_rejects_invalid_lunar_date():
    with pytest.raises(ValueError, match="음력"):
        SajuCalculator().calculate_saju(datetime(2023, 1, 30), "12:00", "male", True)


@pytest.mark.parametrize("module,person_key", [
    (calculate, None), (compatibility, "person1"), (compatibility, "person2"),
])
@pytest.mark.parametrize("date,leap,expected", [
    ("2023-02-01", False, "2023-02-20"),
    ("2023-02-30", False, "2023-03-21"),
    ("2023-02-29", True, "2023-04-19"),
    ("2023-02-30", True, None),
    ("2023-03-01", True, None),
    ("2024-02-01", True, None),
    ("2023-01-30", False, None),
])
def test_api_lunar_calendar_validation(module, person_key, date, leap, expected):
    person = {"birthDate": date, "isLunar": True, "isLeapMonth": leap}
    payload = person
    if person_key:
        payload = {"person1": {"birthDate": "1990-05-15"},
                   "person2": {"birthDate": "1992-08-20"}, person_key: person}
    response = post(module, payload, expected_status=200 if expected else 400)
    if expected:
        saju = response[person_key]["saju"] if person_key else response["saju"]
        assert saju["birth_info"]["date"] == expected
    else:
        assert "음력" in response["error"]


def test_saju_numeric_lunar_date_is_validated_before_gregorian_date():
    response = post(calculate, {"year": 2023, "month": 2, "day": 30, "isLunar": True})
    assert response["saju"]["birth_info"]["date"] == "2023-03-21"
