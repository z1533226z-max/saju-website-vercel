"""
Palm reading analysis endpoint using Gemini Vision API
POST /api/palm/analyze
- Accepts base64 encoded palm image
- Returns palm line analysis in Korean
- Rate limited: 5 requests per IP per day
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import base64
import hashlib
import time
import urllib.error

_ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '*')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# In-memory rate limit store (resets on cold start, but good enough for basic protection)
# For production, use Vercel KV or similar
_rate_limit_store = {}
DAILY_LIMIT = 5

PALM_ANALYSIS_PROMPT = """당신은 전문 손금 분석가입니다. 이 손바닥 사진을 분석하여 손금을 읽어주세요.

다음 JSON 형식으로만 응답하세요 (마크다운 코드블록 없이 순수 JSON만):

{
  "hand": "왼손" 또는 "오른손",
  "lines": {
    "heart_line": {
      "name": "감정선",
      "description": "감정선에 대한 상세 분석 (2-3문장, 한국어)",
      "rating": "강함" 또는 "보통" 또는 "약함",
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "head_line": {
      "name": "두뇌선",
      "description": "두뇌선에 대한 상세 분석 (2-3문장, 한국어)",
      "rating": "강함" 또는 "보통" 또는 "약함",
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "life_line": {
      "name": "생명선",
      "description": "생명선에 대한 상세 분석 (2-3문장, 한국어)",
      "rating": "강함" 또는 "보통" 또는 "약함",
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "fate_line": {
      "name": "운명선",
      "description": "운명선에 대한 상세 분석 (2-3문장, 한국어)",
      "rating": "강함" 또는 "보통" 또는 "약함",
      "keywords": ["키워드1", "키워드2", "키워드3"]
    }
  },
  "overall": "종합 손금 해석 (4-5문장, 한국어, 긍정적이고 희망적인 톤)",
  "personality": "성격 분석 (3-4문장, 한국어)",
  "love": "연애운 (2-3문장, 한국어)",
  "career": "직업운/재물운 (2-3문장, 한국어)",
  "health": "건강운 (1-2문장, 한국어)",
  "advice": "오늘의 조언 (1-2문장, 한국어, 격려하는 톤)"
}

반드시 위 JSON 형식을 정확히 지켜주세요. 한국어로 작성하고, 긍정적이고 재미있는 톤으로 분석해주세요."""


def get_client_ip(headers):
    """Extract client IP from request headers"""
    forwarded = headers.get('x-forwarded-for', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    real_ip = headers.get('x-real-ip', '')
    if real_ip:
        return real_ip
    return 'unknown'


def check_rate_limit(ip):
    """Check if IP has exceeded daily limit. Returns (allowed, remaining)"""
    today = time.strftime('%Y-%m-%d')
    key = f"{ip}:{today}"

    if key not in _rate_limit_store:
        _rate_limit_store[key] = 0

    # Clean old entries
    old_keys = [k for k in _rate_limit_store if not k.endswith(today)]
    for k in old_keys:
        del _rate_limit_store[k]

    count = _rate_limit_store[key]
    if count >= DAILY_LIMIT:
        return False, 0

    _rate_limit_store[key] = count + 1
    return True, DAILY_LIMIT - count - 1


def call_gemini_api(image_base64, mime_type='image/jpeg'):
    """Call Gemini Vision API for palm analysis"""
    import urllib.request

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [
                {"text": PALM_ANALYSIS_PROMPT},
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": image_base64
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=25) as resp:
        result = json.loads(resp.read().decode('utf-8'))

    # Extract text from response
    text = result['candidates'][0]['content']['parts'][0]['text']

    # Clean markdown code blocks if present
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()

    return json.loads(text)


class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', _ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        """Handle palm analysis request"""
        remaining = 0
        try:
            # Check API key
            if not GEMINI_API_KEY:
                self._error(500, 'Server configuration error')
                return

            # Rate limit check
            client_ip = get_client_ip(self.headers)
            allowed, remaining = check_rate_limit(client_ip)

            if not allowed:
                self._json_response(429, {
                    'error': 'daily_limit_exceeded',
                    'message': '오늘의 무료 손금 분석 횟수(5회)를 모두 사용했습니다. 내일 다시 이용해주세요!',
                    'remaining': 0
                })
                return

            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0 or content_length > 10 * 1024 * 1024:  # 10MB max
                self._error(400, 'Invalid request body')
                return

            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                self._error(400, 'Invalid request JSON')
                return

            # Extract image
            image_data = data.get('image', '')
            if not image_data:
                self._error(400, 'No image provided')
                return

            # Handle data URL format (data:image/jpeg;base64,...)
            mime_type = 'image/jpeg'
            if image_data.startswith('data:'):
                header, image_data = image_data.split(',', 1)
                if 'png' in header:
                    mime_type = 'image/png'
                elif 'webp' in header:
                    mime_type = 'image/webp'

            # Call Gemini API
            result = call_gemini_api(image_data, mime_type)

            # Return result with remaining count
            result['remaining'] = remaining
            self._json_response(200, result)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            if e.code == 429:
                self._json_response(503, {
                    'error': 'api_busy',
                    'message': '현재 분석 요청이 많습니다. 잠시 후 다시 시도해주세요.',
                    'remaining': remaining
                })
            else:
                self._error(500, f'AI analysis failed: {e.code}')
        except Exception as e:
            self._error(500, f'Internal error: {str(e)}')

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _error(self, status, message):
        self._json_response(status, {'error': message})

    def log_message(self, format, *args):
        pass  # Suppress default logging
