"""KST rollover, server-rendered previews and query isolation regressions."""
import http.client
import json
import re
import threading
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer

import pytest

from _core import daily_fortune as df
from site_helpers import load_module

NOW = datetime(2026, 10, 22, 23, 59, 59, tzinfo=df.KST)


@pytest.fixture
def detail():
    return load_module("api/daily/fortune.py", "rollover_detail")


@pytest.fixture
def index():
    return load_module("api/daily/index.py", "rollover_index")


def _schema(html):
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])


def test_renderers_normalize_utc_to_kst(detail, index):
    utc = datetime(2026, 10, 22, 15, 0, 1, tzinfo=timezone.utc)
    for html in (detail.render_html("dog", utc), index.render_index_html(utc)):
        assert "2026년 10월 23일" in html
        assert 'data-daily-date="2026-10-23"' in html
        assert 'data-daily-refresh-at="2026-10-24T00:00:00+09:00"' in html


@pytest.mark.parametrize("sign", df.ZODIAC_ORDER)
def test_preview_is_next_day_fortune_in_server_html(detail, sign):
    html = detail.render_html(sign, NOW, day="tomorrow")
    target = NOW + timedelta(days=1)
    fortune = df.generate_fortune(sign, target)
    assert "2026년 10월 23일" in html
    assert f"{fortune['overall']}<small>점</small>" in html
    assert fortune["overall_msg"] in html
    assert fortune["money_msg"] in html
    assert fortune["ilji"]["display"] in html
    assert 'name="robots" content="noindex,follow"' in html
    assert f'<link rel="canonical" href="https://saju.gon.ai.kr/daily/{sign}/">' in html
    assert f'href="/daily/{sign}/?day=tomorrow" aria-current="page"' in html
    # Preview dates are not publication/modification timestamps in the future.
    schema = _schema(html)
    assert schema["dateModified"] == "2026-10-22T00:00:00+09:00"
    assert "datePublished" not in schema


@pytest.mark.parametrize("now", [
    NOW,
    datetime(2026, 12, 31, 23, 59, 59, tzinfo=df.KST),
    datetime(2028, 2, 28, 23, 59, 59, tzinfo=df.KST),
    datetime(2028, 2, 29, 23, 59, 59, tzinfo=df.KST),
])
def test_midnight_date_and_content_rollover(detail, index, now):
    after = now + timedelta(seconds=2)
    for sign in df.ZODIAC_ORDER:
        before_html = detail.render_html(sign, now)
        after_html = detail.render_html(sign, after)
        assert f'data-daily-date="{now:%Y-%m-%d}"' in before_html
        assert f'data-daily-date="{after:%Y-%m-%d}"' in after_html
        assert df.generate_fortune(sign, now) != df.generate_fortune(sign, after)
        preview = detail.render_html(sign, now, day="tomorrow")
        fortune = df.generate_fortune(sign, after)
        for category in ("overall_msg", "money_msg", "love_msg", "health_msg"):
            assert fortune[category] in preview and fortune[category] in after_html
        assert _schema(after_html)["dateModified"] == after.replace(
            hour=0, minute=0, second=0, microsecond=0).isoformat()
    assert f'data-daily-date="{after:%Y-%m-%d}"' in index.render_index_html(after)


def test_same_kst_day_has_same_html_and_content(detail):
    morning = NOW.replace(hour=0, minute=0, second=1)
    assert detail.render_html("dog", morning) == detail.render_html("dog", NOW)
    assert df.generate_fortune("dog", morning) == df.generate_fortune("dog", NOW)
    # Different UTC calendar dates, same KST date.
    assert detail.render_html("dog", morning.astimezone(timezone.utc)) == detail.render_html("dog", NOW)


def test_adjacent_days_do_not_repeat_entire_message_bundle():
    for sign in df.ZODIAC_ORDER:
        previous = None
        for offset in range(366):
            fortune = df.generate_fortune(sign, NOW + timedelta(days=offset))
            bundle = tuple(fortune[k] for k in ("overall_msg", "money_msg", "love_msg", "health_msg"))
            assert bundle != previous, (sign, offset)
            previous = bundle


def test_cache_cannot_serve_previous_day_or_other_query():
    for now in (NOW, NOW + timedelta(seconds=2)):
        assert df.cache_control_until_midnight(now) == "no-store, max-age=0"


def test_http_handler_uses_one_clock_and_keeps_query_isolated(detail, monkeypatch):
    class Clock:
        @staticmethod
        def now(tz):
            return NOW.astimezone(tz)

    monkeypatch.setattr(detail, "datetime", Clock)
    monkeypatch.setattr(detail.handler, "log_message", lambda *args: None)
    server = HTTPServer(("127.0.0.1", 0), detail.handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        def request(path, method="GET"):
            conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=10)
            try:
                conn.request(method, path)
                response = conn.getresponse()
                return response.status, dict(response.getheaders()), response.read().decode()
            finally:
                conn.close()

        for _ in range(2):
            for day, date in (("today", "2026-10-22"), ("tomorrow", "2026-10-23")):
                status, headers, body = request(f"/api/daily/fortune.py?sign=dog&day={day}")
                assert status == 200
                assert f'data-daily-date="{date}"' in body
                assert headers["Cache-Control"] == "no-store, max-age=0"
                assert headers["CDN-Cache-Control"] == headers["Vercel-CDN-Cache-Control"] == "no-store"
                status, head, body = request(f"/api/daily/fortune.py?sign=dog&day={day}", "HEAD")
                assert status == 200 and body == ""
                assert head["Content-Length"] == headers["Content-Length"]
        for invalid in ("yesterday", "2026-10-25", "%3Cscript%3E", "today&day=tomorrow"):
            assert request(f"/api/daily/fortune.py?sign=dog&day={invalid}")[0] == 400
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_today_has_indexable_links_and_no_preview_robots(detail):
    html = detail.render_html("dog", NOW)
    assert 'name="robots"' not in html
    assert 'href="/daily/dog/" aria-current="page"' in html
    assert 'href="/daily/dog/?day=tomorrow"' in html
    assert "한국 시간 매일 자정 갱신" in html
