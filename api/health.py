"""
Health check endpoint for Saju API
"""
from http.server import BaseHTTPRequestHandler
import json
import os

_ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '*')


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
        self.end_headers()

        response = {
            'status': 'ok',
            'service': 'saju-api',
            'version': '2.0.0'
        }

        self.wfile.write(json.dumps(response).encode('utf-8'))
