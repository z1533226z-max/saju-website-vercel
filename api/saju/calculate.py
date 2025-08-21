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

from core.saju_calculator import SajuCalculator
from core.elements import ElementsAnalyzer
from core.interpretation import Interpreter
from core.lunar_converter_improved import ImprovedLunarConverter

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for Saju calculation"""
        try:
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
                    self.send_error(400, f'{field}가 필요합니다')
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
                        birth_date = converted_date
                except Exception:
                    pass  # Continue with original date if conversion fails
            
            # Calculate Saju
            saju = saju_calculator.calculate_saju(
                birth_date,
                birth_time,
                gender,
                is_lunar=False
            )
            
            # Analyze elements
            elements = elements_analyzer.analyze_elements(saju)
            balance = elements_analyzer.analyze_balance(elements)
            
            # Generate interpretation
            interpretation = interpreter.generate_interpretation(saju, elements, gender)
            
            # Try to calculate additional features
            major_fortune = None
            fortune_timeline = None
            ten_gods = None
            
            try:
                from core.major_fortune_calculator import MajorFortuneCalculator, analyze_major_fortune
                from core.ten_gods_calculator import TenGodsAnalyzer
                
                fortune_calculator = MajorFortuneCalculator()
                major_fortune = analyze_major_fortune(saju, birth_date, gender)
                fortune_timeline = fortune_calculator.generate_fortune_timeline(
                    saju, birth_date, gender
                )
                
                ten_gods_analyzer = TenGodsAnalyzer()
                ten_gods = ten_gods_analyzer.analyze(saju)
                
                if major_fortune:
                    interpretation['major_fortune'] = major_fortune
                if fortune_timeline:
                    interpretation['fortune_timeline'] = fortune_timeline
            except Exception:
                pass  # Continue without additional features
            
            # Build response
            response = {
                'saju': saju,
                'elements': elements,
                'balance': balance,
                'interpretation': interpretation,
                'ten_gods': ten_gods,
                'timestamp': datetime.now().isoformat()
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
