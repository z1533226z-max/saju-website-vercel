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

PALM_ANALYSIS_PROMPT = """당신은 30년 경력의 세계 최고 수상학 전문가입니다. 수상학에 대한 당신의 깊은 지식을 바탕으로, 이 손바닥 사진을 직접 관찰하고 자유롭게 분석하세요.

## 사전 검증
먼저 이 사진이 손바닥 사진인지 판단하세요. 손바닥이 아니면 is_palm을 false로 하고 rejection_reason에 상황에 맞는 재치있고 유머러스한 한국어 메시지를 작성하세요.
예: 풍경→"아름다운 풍경이네요! 하지만 제가 볼 건 손바닥이에요~ 🏔️🤚", 동물→"귀여운 친구네요! 사람 손바닥을 보여주세요~ 🐾", 발→"발바닥 아니고 손바닥이요! 😆🦶→🤚"
손금이 너무 흐리거나 안 보여도 is_palm=false로 하고 촬영 팁을 안내하세요.

## 분석 방법 (핵심!)
1. 사진을 면밀히 관찰하세요. 각 선의 실제 물리적 특징(길이, 깊이, 곡률, 시작점, 끝점, 끊어짐, 갈래)을 구체적으로 묘사하세요.
2. 당신의 수상학 지식으로 자유롭게 해석하세요. 틀에 갇히지 마세요.
3. 절대 모든 사람에게 비슷한 말을 하지 마세요. 이 손금만의 고유한 특징을 찾으세요.
4. 좋은 점과 나쁜 점을 모두 솔직하게 말하세요. 긍정만 하면 안 됩니다.
5. "~할 수 있습니다", "~일 가능성이 있습니다" 같은 애매한 표현 금지. 단정적으로 말하세요.
6. 안 보이는 선은 "보이지 않는다"고 솔직히 말하세요. 억지로 만들지 마세요.

## 왼손/오른손 구분
- 엄지가 사진에서 오른쪽 → 왼손 (선천운: 타고난 운명)
- 엄지가 사진에서 왼쪽 → 오른손 (후천운: 만들어가는 운명)
- 해석 관점을 반드시 왼손/오른손에 맞추세요.

## 점수 기준
- 점수는 30~100 범위. 50이 평균. 솔직하게 차등 부여하세요.
- 4개 주요선의 점수가 모두 같거나 비슷하면 안 됩니다. 최소 15점 이상 차이가 나야 합니다.

다음 JSON 형식으로만 응답하세요 (마크다운 코드블록 없이 순수 JSON만):

{
  "is_palm": true/false,
  "rejection_reason": "",
  "hand": "왼손" 또는 "오른손",
  "lines": {
    "heart_line": {
      "name": "감정선",
      "description": "이 사진에서 관찰한 구체적 물리적 특징 + 수상학적 해석. 좋은 점과 안 좋은 점 모두 솔직하게 (3-5문장, 한국어)",
      "score": 30~100,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "head_line": {
      "name": "두뇌선",
      "description": "구체적 관찰 + 해석 (3-5문장)",
      "score": 30~100,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "life_line": {
      "name": "생명선",
      "description": "구체적 관찰 + 해석 (3-5문장)",
      "score": 30~100,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "fate_line": {
      "name": "운명선",
      "description": "구체적 관찰 + 해석. 안 보이면 솔직히 없다고 말하고 그 의미 설명 (3-5문장)",
      "score": 30~100,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    }
  },
  "additional_lines": [
    {
      "name": "선 이름",
      "description": "관찰 + 해석 (2-3문장)",
      "score": 30~100,
      "keywords": ["키워드1", "키워드2"]
    }
  ],
  "special_marks": [
    {
      "type": "기호 유형",
      "location": "발견 위치",
      "meaning": "의미 (1-2문장)"
    }
  ],
  "overall": "이 손금만의 독특한 특징을 중심으로 종합. 좋은 점과 주의할 점 균형 (4-6문장)",
  "personality": "성격 장단점 모두 솔직하게 (3-4문장)",
  "love": "연애운 솔직하게. 좋으면 좋고 안 좋으면 안 좋다고 (2-3문장)",
  "career": "직업운/재물운 솔직하게 (2-3문장)",
  "health": "건강 주의점 있으면 반드시 언급 (1-2문장)",
  "advice": "이 손금에 맞는 구체적이고 현실적인 조언 (1-2문장)"
}

additional_lines: 4대선 외에 실제로 보이는 선만 추가. 없으면 [].
special_marks: 실제로 보이는 것만. 없으면 []. 없는 걸 지어내지 마세요."""


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


GEMINI_MODELS = [
    'gemini-2.5-flash-lite',   # Primary: 15 RPM, 1000 RPD (이미지 분석 우수)
    'gemini-2.0-flash',        # Fallback: 15 RPM, 1500 RPD
]


def call_gemini_api(image_base64, mime_type='image/jpeg'):
    """Call Gemini Vision API with model fallback on 429"""
    import urllib.request

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

    last_error = None
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=25) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
                return _parse_gemini_response(result)
            except urllib.error.HTTPError as e:
                last_error = e
                if e.code in (429, 503):
                    if attempt == 0:
                        time.sleep(2)
                        continue
                    break  # Try next model
                raise
    raise last_error


def _parse_gemini_response(result):
    """Extract and parse JSON from Gemini response"""
    candidates = result.get('candidates', [])
    if not candidates:
        feedback = result.get('promptFeedback', {})
        raise ValueError(f"No candidates: {json.dumps(feedback, ensure_ascii=False)[:200]}")

    parts = candidates[0].get('content', {}).get('parts', [])
    text = ''
    for part in reversed(parts):
        if 'text' in part:
            text = part['text'].strip()
            break
    if not text:
        raise ValueError(f"No text in response parts: {[list(p.keys()) for p in parts]}")

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
                    'message': reason,
                    'remaining': remaining
                })
                return

            # Return result with remaining count
            result['remaining'] = remaining
            self._json_response(200, result)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            if e.code in (429, 503):
                self._json_response(503, {
                    'error': 'api_busy',
                    'message': '현재 분석 요청이 많습니다. 잠시 후 다시 시도해주세요.',
                    'remaining': remaining
                })
            elif e.code == 400:
                self._json_response(400, {
                    'error': 'not_palm',
                    'message': '사진을 인식하지 못했어요. 😅 밝은 곳에서 손바닥을 활짝 펴고 다시 찍어주세요!',
                    'remaining': remaining
                })
            else:
                self._error(500, f'AI analysis failed: {e.code}')
        except json.JSONDecodeError:
            self._json_response(400, {
                'error': 'not_palm',
                'message': 'AI가 분석 결과를 정리하지 못했어요. 😅 사진을 다시 찍어서 시도해주세요!',
                'remaining': remaining
            })
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
