"""
Health check endpoint for Vercel deployment
"""
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request for health check"""
        # Set response headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()
        
        # Response data
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'saju-backend-vercel',
            'version': '2.0.0',
            'environment': 'vercel'
        }
        
        # Send response
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        return
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
