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

PALM_ANALYSIS_PROMPT = """당신은 수상학(palmistry)에 정통한 전문 손금 분석가입니다.

먼저 이 사진이 손바닥 사진인지 판단하세요. 손바닥이 아니면 is_palm을 false로 설정하세요.

당신은 동양 수상학과 서양 수상학 모두에 대한 깊은 지식을 갖추고 있습니다.
이 사진 속 손바닥을 직접 관찰하고, 당신의 수상학 지식을 바탕으로 자유롭게 해석해주세요.

분석 방법:
1. 사진에서 각 손금선의 물리적 특징을 관찰하세요.
2. 관찰한 특징을 당신의 수상학 지식에 비추어 자유롭게 판단하고 해석하세요.
3. 정해진 매뉴얼이 아닌, 이 손금에서 실제로 보이는 것을 근거로 당신만의 전문적 견해를 말하세요.
4. 특수 기호(별, 삼각형, 사각형, 십자, 섬, 갈래 등)가 보이면 반드시 special_marks에 기록하세요.

다음 JSON 형식으로만 응답하세요 (마크다운 코드블록 없이 순수 JSON만):

{
  "is_palm": true 또는 false,
  "rejection_reason": "손바닥이 아닌 경우 이유 (한국어). 손바닥이면 빈 문자열",
  "hand": "왼손" 또는 "오른손",
  "lines": {
    "heart_line": {
      "name": "감정선",
      "description": "관찰한 물리적 특징 + 수상학적 해석을 자유롭게 서술 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "head_line": {
      "name": "두뇌선",
      "description": "관찰한 물리적 특징 + 수상학적 해석 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "life_line": {
      "name": "생명선",
      "description": "관찰한 물리적 특징 + 수상학적 해석 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "fate_line": {
      "name": "운명선",
      "description": "관찰한 물리적 특징 + 수상학적 해석 (3-4문장, 한국어). 보이지 않으면 그 의미도 해석",
      "score": 50~100 사이의 정수 (보이지 않으면 50~60),
      "keywords": ["키워드1", "키워드2", "키워드3"]
    }
  },
  "special_marks": [
    {
      "type": "기호 유형 (별/삼각형/사각형/십자/섬/갈래 등)",
      "location": "발견 위치 (예: 감정선 위, 목성구 등)",
      "meaning": "수상학적 의미 (1-2문장, 한국어)"
    }
  ],
  "overall": "4개 선의 전체적 조화와 이 손금만의 특이점을 종합 (4-5문장, 한국어, 긍정적 톤)",
  "personality": "손금에서 읽히는 성격 특성 (3-4문장, 한국어)",
  "love": "연애운 해석 (2-3문장, 한국어)",
  "career": "직업운/재물운 해석 (2-3문장, 한국어)",
  "health": "건강운 해석 (1-2문장, 한국어)",
  "advice": "이 손금에 맞는 조언 (1-2문장, 한국어, 격려하는 톤)"
}

special_marks: 특수 기호가 없으면 빈 배열 []. 있으면 발견한 만큼 추가.
4개 선의 score가 모두 같으면 안 됩니다. 반드시 위 JSON 형식만 출력하세요."""


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
    candidates = result.get('candidates', [])
    if not candidates:
        raise ValueError(f"No candidates in Gemini response: {json.dumps(result, ensure_ascii=False)[:200]}")

    parts = candidates[0].get('content', {}).get('parts', [])
    if not parts or 'text' not in parts[0]:
        raise ValueError("No text in Gemini response")

    text = parts[0]['text'].strip()

    # Clean markdown code blocks if present
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()

    if not text:
        raise ValueError("Empty text from Gemini")

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

            # Check if image is actually a palm
            if not result.get('is_palm', True):
                reason = result.get('rejection_reason', '손바닥 사진이 아닌 것 같습니다.')
                self._json_response(400, {
                    'error': 'not_palm',
                    'message': f'🤚 {reason}\n손바닥이 잘 보이는 사진을 올려주세요.',
                    'remaining': remaining
                })
                return

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
