"""
Vercel Function for Compatibility calculation
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
from core.compatibility import CompatibilityAnalyzer
from core.lunar_converter_improved import ImprovedLunarConverter

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for compatibility calculation"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Initialize components
            saju_calculator = SajuCalculator()
            elements_analyzer = ElementsAnalyzer()
            compatibility_analyzer = CompatibilityAnalyzer()
            lunar_converter = ImprovedLunarConverter()
            
            # Parse dates
            person1_date = datetime.strptime(data['person1']['birthDate'], '%Y-%m-%d')
            person2_date = datetime.strptime(data['person2']['birthDate'], '%Y-%m-%d')
            
            # Convert lunar to solar if needed
            if data['person1'].get('isLunar', False):
                try:
                    person1_date = lunar_converter.lunar_to_solar(
                        person1_date.year, 
                        person1_date.month, 
                        person1_date.day
                    )
                except:
                    pass
            
            if data['person2'].get('isLunar', False):
                try:
                    person2_date = lunar_converter.lunar_to_solar(
                        person2_date.year,
                        person2_date.month,
                        person2_date.day
                    )
                except:
                    pass
            
            # Get gender info
            gender1 = data['person1'].get('gender', 'neutral')
            gender2 = data['person2'].get('gender', 'neutral')
            
            # Calculate Saju for both people
            person1_saju = saju_calculator.calculate_saju(
                person1_date,
                data['person1']['birthTime'],
                gender1
            )
            
            person2_saju = saju_calculator.calculate_saju(
                person2_date,
                data['person2']['birthTime'],
                gender2
            )
            
            # Analyze elements for both
            person1_elements = elements_analyzer.analyze_elements(person1_saju)
            person2_elements = elements_analyzer.analyze_elements(person2_saju)
            
            # Calculate compatibility
            compatibility = compatibility_analyzer.analyze_compatibility(
                person1_saju, person2_saju,
                person1_elements, person2_elements,
                gender1, gender2,
                data['person1'].get('isLunar', False),
                data['person2'].get('isLunar', False)
            )
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.end_headers()
            
            response = {
                'status': 'success',
                'compatibility': compatibility
            }
            
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
