"""
Test Health check - Debug version
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Debug info
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # Check if _core exists
        core_path = os.path.join(current_dir, '_core')
        core_exists = os.path.exists(core_path)
        core_files = []
        if core_exists:
            try:
                core_files = os.listdir(core_path)
            except:
                pass
        
        response = {
            'status': 'debug',
            'current_dir': current_dir,
            'parent_dir': parent_dir,
            'sys_path': sys.path[:5],
            'core_exists': core_exists,
            'core_path': core_path,
            'core_files': core_files[:5] if core_files else []
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
