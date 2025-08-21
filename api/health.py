"""
Health check endpoint for Vercel deployment
"""
from datetime import datetime

def handler(req, res):
    """Handle request for health check"""
    
    # Handle CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    
    if req.method == 'OPTIONS':
        return res.status(200).send('')
    
    # Response data
    response = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'saju-backend-vercel',
        'version': '2.0.0',
        'environment': 'vercel'
    }
    
    return res.status(200).json(response)
