"""SSR 핸들러 HEAD 지원: GET 과 같은 상태·헤더를 돌려주고 본문은 보내지 않는다 (이전: 501)."""
import http.client
import os
import threading
from http.server import HTTPServer

import pytest

from site_helpers import load_module

FIXED_CACHE = "public, s-maxage=600, max-age=300, stale-while-revalidate=60"


@pytest.fixture(scope="module")
def servers():
    started = {}
    for key, rel in (("index", ("api", "daily", "index.py")), ("fortune", ("api", "daily", "fortune.py"))):
        mod = load_module(os.path.join(*rel), f"daily_{key}_head_test")
        mod.cache_control_until_midnight = lambda now=None: FIXED_CACHE   # GET/HEAD 사이 초 단위 차이 제거
        mod.handler.log_message = lambda *args, **kwargs: None
        srv = HTTPServer(("127.0.0.1", 0), mod.handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        started[key] = srv
    yield {k: s.server_port for k, s in started.items()}
    for srv in started.values():
        srv.shutdown()
        srv.server_close()


def _request(port, method, path):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
    try:
        conn.request(method, path)
        resp = conn.getresponse()
        body = resp.read()
        headers = {k.lower(): v for k, v in resp.getheaders() if k.lower() not in ("date", "server")}
        return resp.status, headers, body
    finally:
        conn.close()


@pytest.mark.parametrize("server, path, status", [
    ("index", "/daily/", 200),
    ("fortune", "/daily/rat/?sign=rat", 200),
    ("fortune", "/api/daily/fortune.py?sign=pig", 200),
    ("fortune", "/daily/cat/?sign=cat", 404),
    ("fortune", "/daily/rat/", 404),          # sign 쿼리 없음 (기존 동작 유지)
])
def test_head_matches_get_without_body(servers, server, path, status):
    port = servers[server]
    get_status, get_headers, get_body = _request(port, "GET", path)
    head_status, head_headers, head_body = _request(port, "HEAD", path)
    assert get_status == head_status == status
    assert head_headers == get_headers
    assert head_body == b""
    assert int(get_headers["content-length"]) == len(get_body) > 0
    assert get_headers["content-type"] == "text/html; charset=utf-8"
    if status == 200:
        assert get_headers["cache-control"] == FIXED_CACHE
        assert b"</html>" in get_body
    else:
        assert "cache-control" not in get_headers
