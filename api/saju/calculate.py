"""
Vercel Function for Saju calculation - Debug version
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
            
            # Debug: Check import paths
            debug_info = {
                'current_dir': os.path.dirname(os.path.abspath(__file__)),
                'parent_dir': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'sys_path_before': sys.path[:3]
            }
            
            # Add paths for import
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            # Add both parent and current to path
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            debug_info['sys_path_after'] = sys.path[:5]
            
            # Try import
            try:
                from _core.saju_calculator import SajuCalculator
                from _core.elements import ElementsAnalyzer
                from _core.interpretation import Interpreter
                from _core.lunar_converter_improved import ImprovedLunarConverter
                
                debug_info['import_success'] = True
                
                # Initialize components
                saju_calculator = SajuCalculator()
                elements_analyzer = ElementsAnalyzer()
                interpreter = Interpreter()
                lunar_converter = ImprovedLunarConverter()
                
                # Simple test response
                response_data = {
                    'status': 'success',
                    'message': 'Import successful!',
                    'debug': debug_info,
                    'input': data
                }
                
            except ImportError as e:
                debug_info['import_error'] = str(e)
                debug_info['import_success'] = False
                
                # Check if files exist
                core_path = os.path.join(current_dir, '_core')
                debug_info['core_exists'] = os.path.exists(core_path)
                if os.path.exists(core_path):
                    debug_info['core_files'] = os.listdir(core_path)[:5]
                
                response_data = {
                    'status': 'error',
                    'error': f'Import failed: {str(e)}',
                    'debug': debug_info
                }
            
            # Send response
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'error': str(e),
                'type': 'general_error'
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
