"""
Vercel Function for Saju information retrieval
Dynamic route handler for /api/saju/info/[type]
"""
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request for Saju information"""
        try:
            # Extract the info type from the path
            # Path format: /api/saju/info/[type]
            path_parts = self.path.split('/')
            info_type = path_parts[-1] if len(path_parts) > 0 else None
            
            # Remove query parameters if any
            if info_type and '?' in info_type:
                info_type = info_type.split('?')[0]
            
            # Map info types to data files
            info_map = {
                'heavenly_stems': 'heavenly_stems.json',
                'earthly_branches': 'earthly_branches.json',
                'elements': 'elements_mapping.json',
                'interpretations': 'interpretations.json',
                'patterns': 'patterns.json',
                'shinshal': 'shinshal.json',
                'ten_gods': 'ten_gods_rules.json'
            }
            
            if info_type not in info_map:
                self.send_error(404, f'잘못된 정보 타입: {info_type}')
                return
            
            # Read the data file
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_path, 'data', info_map[info_type])
            
            if not os.path.exists(file_path):
                self.send_error(404, f'데이터 파일을 찾을 수 없습니다: {info_map[info_type]}')
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.end_headers()
            
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
