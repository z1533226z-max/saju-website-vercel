"""Exercise the health handler over real local HTTP, including fault injection."""
import builtins
from datetime import datetime
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import json
from threading import Thread

import pytest

import health
from _core.lunar_converter_improved import ImprovedLunarConverter
from _core.saju_calculator import SajuCalculator


@pytest.fixture
def get_health():
    server = ThreadingHTTPServer(('127.0.0.1', 0), health.handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def request():
        connection = HTTPConnection(*server.server_address, timeout=5)
        try:
            connection.request('GET', '/api/health')
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), json.loads(response.read())
        finally:
            connection.close()

    yield request
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()


def test_health_runs_real_calculations_on_every_request(get_health, monkeypatch):
    calls = []
    calculate = SajuCalculator.calculate_saju

    def record(self, *args, **kwargs):
        calls.append((args, kwargs))
        return calculate(self, *args, **kwargs)

    monkeypatch.setattr(SajuCalculator, 'calculate_saju', record)
    for _ in range(2):
        status, headers, body = get_health()
        assert status == 200
        assert headers['Cache-Control'] == 'no-store'
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        assert body['status'] == 'ok'
        assert body['service'] == 'saju-api'
        assert body['version'] == '2.0.0'
        assert body['checks'] == [
            {'name': 'solar_2000_01_01', 'status': 'passed'},
            {'name': 'solar_2026_10_03', 'status': 'passed'},
            {'name': 'lunar_1999_11_25', 'status': 'passed'},
        ]
    assert len(calls) == 6


@pytest.mark.parametrize('date', [datetime(2000, 1, 1), datetime(2026, 10, 3)])
@pytest.mark.parametrize('pillar', ['year', 'month', 'day', 'hour'])
def test_health_detects_each_pillar_mismatch(get_health, monkeypatch, date, pillar):
    calculate = SajuCalculator.calculate_saju

    def wrong(self, birth_date, *args, **kwargs):
        result = calculate(self, birth_date, *args, **kwargs)
        if birth_date == date:
            result[pillar]['heavenly_hanja'] = 'wrong'
        return result

    monkeypatch.setattr(SajuCalculator, 'calculate_saju', wrong)
    status, headers, body = get_health()
    assert status == 503
    assert headers['Cache-Control'] == 'no-store'
    assert body['status'] == 'error'
    assert any(check['status'] == 'failed' for check in body['checks'])


@pytest.mark.parametrize('method', ['calculate_saju', 'load_data'])
def test_health_hides_internal_errors(get_health, monkeypatch, method):
    def broken(*args, **kwargs):
        raise RuntimeError('internal-sensitive-detail')

    monkeypatch.setattr(SajuCalculator, method, broken)
    status, _, body = get_health()
    assert status == 503
    assert body['status'] == 'error'
    assert body['checks'][-1]['status'] == 'failed'
    assert 'internal-sensitive-detail' not in json.dumps(body)


def test_health_reports_calculator_import_failure(get_health, monkeypatch):
    import_module = builtins.__import__

    def broken(name, *args, **kwargs):
        if name == '_core.saju_calculator':
            raise ImportError('internal-sensitive-detail')
        return import_module(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', broken)
    status, _, body = get_health()
    assert status == 503
    assert body['status'] == 'error'
    assert 'internal-sensitive-detail' not in json.dumps(body)


@pytest.mark.parametrize('converted', [None, datetime(1999, 11, 25), datetime(2000, 1, 2)])
def test_health_rejects_lunar_failure_or_wrong_date(get_health, monkeypatch, converted):
    monkeypatch.setattr(ImprovedLunarConverter, 'lunar_to_solar', lambda *args: converted)
    status, _, body = get_health()
    assert status == 503
    assert body['status'] == 'error'
    assert body['checks'][-1] == {'name': 'lunar_1999_11_25', 'status': 'failed'}


def test_health_recovers_after_transient_failure(get_health, monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(SajuCalculator, 'calculate_saju', lambda *args, **kwargs: {})
        assert get_health()[0] == 503
    assert get_health()[0] == 200
