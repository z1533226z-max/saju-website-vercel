"""
Vercel Function for Saju calculation - Production version
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime
from dataclasses import asdict
import logging

logger = logging.getLogger('saju')

# Add parent directory to path for imports (module level)
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from _core.saju_calculator import SajuCalculator
from _core.elements import ElementsAnalyzer
from _core.interpretation import Interpreter
from _core.lunar_converter_improved import ImprovedLunarConverter
from _core.pattern_analyzer import PatternAnalyzer
from _core.shinshal_calculator import ShinshalCalculator
from _core.yongshin_analyzer import YongshinAnalyzer

# Module-level initialization for cold start optimization
_saju_calculator = SajuCalculator()
_elements_analyzer = ElementsAnalyzer()
_interpreter = Interpreter()
_lunar_converter = ImprovedLunarConverter()
_pattern_analyzer = PatternAnalyzer()
_shinshal_calculator = ShinshalCalculator()
_yongshin_analyzer = YongshinAnalyzer()


def _json_serializer(obj):
    """Custom JSON serializer for dataclasses and datetime objects"""
    if hasattr(obj, '__dataclass_fields__'):
        return asdict(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


_ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '*')


def _send_json(handler, status_code, data):
    """Send JSON response with proper headers"""
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
    handler.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False, default=_json_serializer).encode('utf-8'))


def _validate_input(data):
    """Validate input data, returns (cleaned_data, error_message)

    Accepts two formats:
    1. { year, month, day, hour } - direct fields
    2. { birthDate: "YYYY-MM-DD", birthTime: "HH:MM" } - frontend format
    """
    errors = []

    # Support both input formats
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour') or data.get('birthTime', '12:00')
    gender = data.get('gender', 'male')
    is_lunar = data.get('isLunar', False)

    # If year/month/day not provided, try parsing birthDate
    if year is None or month is None or day is None:
        birth_date_str = data.get('birthDate', '')
        if birth_date_str:
            try:
                parts = birth_date_str.split('-')
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
            except (ValueError, IndexError):
                return None, 'birthDate 형식이 올바르지 않습니다. (YYYY-MM-DD)'
        else:
            return None, 'year/month/day 또는 birthDate 필드가 필요합니다.'

    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except (ValueError, TypeError):
        return None, 'year, month, day는 숫자여야 합니다.'

    if not (1900 <= year <= 2100):
        errors.append(f'year는 1900~2100 범위여야 합니다. (입력값: {year})')
    if not (1 <= month <= 12):
        errors.append(f'month는 1~12 범위여야 합니다. (입력값: {month})')
    if not (1 <= day <= 31):
        errors.append(f'day는 1~31 범위여야 합니다. (입력값: {day})')
    if gender not in ('male', 'female'):
        gender = 'male'

    if errors:
        return None, ' '.join(errors)

    return {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'gender': gender,
        'is_lunar': bool(is_lunar),
    }, None


def _serialize_dataclass(obj):
    """Convert dataclass to dict safely"""
    try:
        return asdict(obj)
    except Exception:
        # Fallback: convert to dict manually
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if isinstance(value, list):
                result[field] = [
                    asdict(item) if hasattr(item, '__dataclass_fields__') else item
                    for item in value
                ]
            elif isinstance(value, dict):
                result[field] = value
            else:
                result[field] = value
        return result


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for Saju calculation"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                _send_json(self, 400, {'status': 'error', 'error': '요청 본문이 비어있습니다.'})
                return

            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                _send_json(self, 400, {'status': 'error', 'error': '잘못된 JSON 형식입니다.'})
                return

            # Validate input
            validated, error = _validate_input(data)
            if error:
                _send_json(self, 400, {'status': 'error', 'error': error})
                return

            year = validated['year']
            month = validated['month']
            day = validated['day']
            hour = validated['hour']
            gender = validated['gender']
            is_lunar = validated['is_lunar']

            # Build birth_date
            birth_date_str = f"{year}-{month:02d}-{day:02d}"
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

            # Convert lunar to solar if needed
            if is_lunar:
                solar_date = _lunar_converter.lunar_to_solar(year, month, day)
                if solar_date is not None:
                    # lunar_to_solar returns datetime object
                    birth_date = solar_date
                # If conversion fails, use original date as-is

            # Calculate Saju
            saju = _saju_calculator.calculate_saju(
                birth_date=birth_date,
                birth_time=hour,
                gender=gender,
                is_lunar=is_lunar
            )

            # Analyze elements
            elements = _elements_analyzer.analyze_elements(saju)

            # Generate interpretation
            interpretation = _interpreter.generate_interpretation(saju, elements, gender)

            # Pattern analysis (격국)
            try:
                pattern_result = _pattern_analyzer.analyze(saju)
                pattern_data = _serialize_dataclass(pattern_result)
            except Exception:
                pattern_data = None

            # Shinshal analysis (신살)
            try:
                shinshal_result = _shinshal_calculator.calculate_shinshal(saju)
                shinshal_data = {}
                for category, items in shinshal_result.items():
                    shinshal_data[category] = [
                        _serialize_dataclass(item) if hasattr(item, '__dataclass_fields__') else item
                        for item in items
                    ]
            except Exception:
                shinshal_data = None

            # Yongshin analysis (용신)
            try:
                yongshin_result = _yongshin_analyzer.analyze(saju, elements)
                yongshin_data = _serialize_dataclass(yongshin_result)
            except Exception:
                yongshin_data = None

            # Prepare response
            response_data = {
                'status': 'success',
                'saju': saju,
                'elements': elements,
                'interpretation': interpretation,
                'pattern': pattern_data,
                'shinshal': shinshal_data,
                'yongshin': yongshin_data,
                'timestamp': datetime.now().isoformat()
            }

            _send_json(self, 200, response_data)

        except Exception as e:
            # 서버 로그에만 상세 에러 기록
            logger.error(f'Calculation error: {str(e)}')
            _send_json(self, 500, {
                'status': 'error',
                'error': '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
                'type': 'calculation_error'
            })

    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
