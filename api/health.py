"""
Health check endpoint for Saju API
"""
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import json
import os
import sys

_ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '*')

# Fixed synthetic inputs; pillar baselines also live in test_saju_calculator.py.
_SOLAR_CASES = (
    ('solar_2000_01_01', datetime(2000, 1, 1), ('己卯', '丙子', '戊午', '戊午')),
    ('solar_2026_10_03', datetime(2026, 10, 3), ('丙午', '丁酉', '庚戌', '壬午')),
)


def _pillars_match(calculator, birth_date, expected):
    saju = calculator.calculate_saju(birth_date, '12:00', 'male', is_lunar=False)
    actual = tuple(
        saju[pillar]['heavenly_hanja'] + saju[pillar]['earthly_hanja']
        for pillar in ('year', 'month', 'day', 'hour')
    )
    return actual == expected


def _calculation_checks():
    checks = []
    name = 'saju_calculation'
    try:
        # Import and load data inside the check so cold-start failures return 503.
        api_dir = os.path.dirname(os.path.abspath(__file__))
        if api_dir not in sys.path:
            sys.path.insert(0, api_dir)
        from _core.saju_calculator import SajuCalculator
        from _core.lunar_converter_improved import ImprovedLunarConverter

        calculator = SajuCalculator()
        for name, birth_date, expected in _SOLAR_CASES:
            passed = _pillars_match(calculator, birth_date, expected)
            checks.append({'name': name, 'status': 'passed' if passed else 'failed'})

        name = 'lunar_1999_11_25'
        converted = ImprovedLunarConverter().lunar_to_solar(1999, 11, 25)
        passed = converted == datetime(2000, 1, 1) and _pillars_match(
            calculator, converted, _SOLAR_CASES[0][2]
        )
        checks.append({'name': name, 'status': 'passed' if passed else 'failed'})
    except Exception:
        # Never publish exception text, paths, or internal configuration.
        checks.append({'name': name, 'status': 'failed'})
    return checks


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        checks = _calculation_checks()
        healthy = all(check['status'] == 'passed' for check in checks)
        self.send_response(200 if healthy else 503)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
        self.end_headers()

        response = {
            'status': 'ok' if healthy else 'error',
            'service': 'saju-api',
            'version': '2.0.0',
            'checks': checks,
        }

        self.wfile.write(json.dumps(response).encode('utf-8'))
