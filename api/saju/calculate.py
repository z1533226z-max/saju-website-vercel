"""
Vercel Function for Saju calculation - Production version
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for Saju calculation"""
        # Set CORS headers first
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Add paths for import
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            # Import modules
            from _core.saju_calculator import SajuCalculator
            from _core.elements import ElementsAnalyzer
            from _core.interpretation import Interpreter
            from _core.lunar_converter_improved import ImprovedLunarConverter
            
            # Initialize components
            saju_calculator = SajuCalculator()
            elements_analyzer = ElementsAnalyzer()
            interpreter = Interpreter()
            lunar_converter = ImprovedLunarConverter()
            
            # Extract and validate data
            year = data.get('year')
            month = data.get('month')
            day = data.get('day')
            hour = data.get('hour', '사시')
            gender = data.get('gender', 'male')
            is_lunar = data.get('isLunar', False)
            
            # Create birthDate string
            birth_date_str = f"{year}-{month:02d}-{day:02d}"
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            
            # Convert lunar to solar if needed
            if is_lunar:
                solar_date = lunar_converter.lunar_to_solar(year, month, day)
                birth_date = datetime(solar_date['year'], solar_date['month'], solar_date['day'])
            
            # Calculate Saju
            saju = saju_calculator.calculate_saju(
                birth_date=birth_date,
                birth_time=hour,
                gender=gender,
                is_lunar=is_lunar
            )
            
            # Analyze elements
            elements = elements_analyzer.analyze_elements(saju)
            
            # Generate interpretation
            interpretation = interpreter.generate_interpretation(saju, elements, gender)
            
            # Prepare response
            response_data = {
                'status': 'success',
                'saju': saju,
                'elements': elements,
                'interpretation': interpretation,
                'timestamp': datetime.now().isoformat()
            }
            
            # Send response
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'error': str(e),
                'type': 'calculation_error'
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(b'')