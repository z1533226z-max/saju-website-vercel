"""
Vercel Function for Saju calculation
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _core.saju_calculator import SajuCalculator
from _core.elements import ElementsAnalyzer
from _core.interpretation import Interpreter
from _core.lunar_converter_improved import ImprovedLunarConverter

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for Saju calculation"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Initialize components
            saju_calculator = SajuCalculator()
            elements_analyzer = ElementsAnalyzer()
            interpreter = Interpreter()
            lunar_converter = ImprovedLunarConverter()
            
            # Input validation
            required_fields = ['birthDate', 'birthTime', 'gender']
            for field in required_fields:
                if field not in data:
                    error_response = {'error': f'{field}가 필요합니다'}
                    self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
                    return
            
            # Parse date
            birth_date = datetime.strptime(data['birthDate'], '%Y-%m-%d')
            birth_time = data['birthTime']
            gender = data['gender']
            is_lunar = data.get('isLunar', False)
            
            # Convert lunar to solar if needed
            if is_lunar:
                try:
                    converted_date = lunar_converter.lunar_to_solar(
                        birth_date.year, birth_date.month, birth_date.day
                    )
                    if converted_date:
                        birth_date = datetime(converted_date[0], converted_date[1], converted_date[2])
                except:
                    pass  # Use original date if conversion fails
            
            # Calculate Saju
            saju_result = saju_calculator.calculate_saju(
                birth_date.year,
                birth_date.month,
                birth_date.day,
                birth_time
            )
            
            # Analyze elements
            elements_result = elements_analyzer.analyze_elements(saju_result)
            
            # Get interpretation
            interpretation_result = interpreter.interpret(saju_result, elements_result)
            
            # Format response
            response_data = {
                'saju': saju_result,
                'elements': elements_result['percentages'],
                'elements_detail': elements_result,
                'interpretation': interpretation_result,
                'input': {
                    'birthDate': data['birthDate'],
                    'birthTime': birth_time,
                    'gender': gender,
                    'isLunar': is_lunar
                }
            }
            
            # Send response
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            print(f"Error in calculate handler: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
