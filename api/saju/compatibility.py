"""
Vercel Function for Compatibility calculation
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime
import logging

logger = logging.getLogger('saju')

# Add parent directory to path for imports (module level)
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from _core.saju_calculator import SajuCalculator
from _core.elements import ElementsAnalyzer
from _core.compatibility import CompatibilityAnalyzer
from _core.lunar_converter_improved import ImprovedLunarConverter

# Module-level initialization for cold start optimization
_saju_calculator = SajuCalculator()
_elements_analyzer = ElementsAnalyzer()
_compatibility_analyzer = CompatibilityAnalyzer()
_lunar_converter = ImprovedLunarConverter()


_ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '*')


def _send_json(handler, status_code, data):
    """Send JSON response with proper headers"""
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
    handler.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for compatibility calculation"""
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

            # Validate person data exists
            if 'person1' not in data or 'person2' not in data:
                _send_json(self, 400, {'status': 'error', 'error': 'person1, person2 데이터가 필요합니다.'})
                return

            # Process both persons
            persons = []
            for person_key in ['person1', 'person2']:
                person_data = data[person_key]

                # Parse date
                birth_date_str = person_data.get('birthDate', '')
                if not birth_date_str:
                    _send_json(self, 400, {
                        'status': 'error',
                        'error': f'{person_key}의 birthDate가 필요합니다.'
                    })
                    return

                try:
                    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                except ValueError:
                    _send_json(self, 400, {
                        'status': 'error',
                        'error': f'{person_key}의 birthDate 형식이 올바르지 않습니다. (YYYY-MM-DD)'
                    })
                    return

                birth_time = person_data.get('birthTime', '12:00')
                gender = person_data.get('gender', 'neutral')
                is_lunar = person_data.get('isLunar', False)

                # Convert lunar to solar if needed
                if is_lunar:
                    try:
                        converted_date = _lunar_converter.lunar_to_solar(
                            birth_date.year, birth_date.month, birth_date.day
                        )
                        if converted_date is not None:
                            # lunar_to_solar returns datetime object
                            birth_date = converted_date
                    except Exception:
                        pass  # Use original date if conversion fails

                # Calculate Saju with correct signature
                saju_result = _saju_calculator.calculate_saju(
                    birth_date=birth_date,
                    birth_time=birth_time,
                    gender=gender,
                    is_lunar=is_lunar
                )

                # Analyze elements
                elements_result = _elements_analyzer.analyze_elements(saju_result)

                persons.append({
                    'saju': saju_result,
                    'elements': elements_result,
                    'gender': gender,
                    'is_lunar': is_lunar
                })

            # Calculate compatibility with full parameters
            compatibility_result = _compatibility_analyzer.analyze_compatibility(
                persons[0]['saju'],
                persons[1]['saju'],
                persons[0]['elements'],
                persons[1]['elements'],
                gender1=persons[0]['gender'],
                gender2=persons[1]['gender'],
                is_lunar1=persons[0]['is_lunar'],
                is_lunar2=persons[1]['is_lunar']
            )

            # Format response
            response_data = {
                'status': 'success',
                'person1': {
                    'saju': persons[0]['saju'],
                    'elements': persons[0]['elements'],
                    'gender': persons[0]['gender']
                },
                'person2': {
                    'saju': persons[1]['saju'],
                    'elements': persons[1]['elements'],
                    'gender': persons[1]['gender']
                },
                'compatibility': compatibility_result
            }

            _send_json(self, 200, response_data)

        except Exception as e:
            logger.error(f'Compatibility error: {str(e)}')
            _send_json(self, 500, {
                'status': 'error',
                'error': '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
            })

    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
