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
DAILY_LIMIT = 100

PALM_ANALYSIS_PROMPT = """당신은 수상학(palmistry)에 정통한 전문 손금 분석가입니다.

먼저 이 사진이 손바닥 사진인지 판단하세요. 손바닥이 아니면 is_palm을 false로 설정하세요.

## 왼손과 오른손의 차이 (중요!)
- 왼손(비주력손) = 선천운: 태어날 때 타고난 잠재력, 성격, 운명
- 오른손(주력손) = 후천운: 노력과 환경으로 만들어진 현재의 모습
- 왼손이면 "타고난 운명"의 관점에서, 오른손이면 "현재 만들어가는 운명"의 관점에서 해석하세요.
- 왼손/오른손을 정확히 구별하세요: 엄지가 오른쪽에 있으면 왼손, 왼쪽에 있으면 오른손입니다.

## 전문 수상학 해석 기준 (참고)

【감정선(Heart Line)】새끼손가락 아래에서 시작하여 검지 방향으로 뻗음.
- 검지 아래까지 닿음 → 이상주의적 사랑관, 높은 기준
- 중지 아래에서 끝남 → 자기중심적, 현실적 사랑
- 직선형 → 감정 표현이 절제됨, 이성적
- 곡선형 → 감정 표현이 풍부, 정열적
- 짧고 곧음 → 실용적, 로맨스보다 안정 중시
- 끊어짐/사슬형 → 감정적 상처, 관계의 어려움
- 깊고 선명 → 감정에 충실, 헌신적

【두뇌선(Head Line)】검지 아래에서 시작하여 손바닥을 가로지름.
- 길고 직선 → 논리적, 분석적, 체계적 사고
- 아래로 휘어짐 → 창의적, 예술적, 상상력 풍부
- 짧음 → 직관적 판단, 실행력 강함
- 생명선과 붙어서 시작 → 신중하고 조심스러움
- 생명선과 떨어져 시작 → 독립적, 모험적
- 갈래(작가의 포크) → 상상력과 현실감각 겸비
- 끊어짐 → 사고방식의 큰 전환점

【생명선(Life Line)】엄지와 검지 사이에서 시작, 손목 방향으로 호를 그림.
- 수명의 길이가 아닌 생명력/활력/건강을 나타냄
- 길고 깊음 → 강인한 체력, 풍부한 활력
- 짧거나 얕음 → 에너지를 타인에게 의존하기 쉬움
- 큰 호를 그림 → 에너지 넘침, 열정적
- 직선에 가까움 → 조심스럽고 신중함
- 끊어짐 → 생활의 큰 변화, 건강 전환점
- 이중선 → 보호력이 강함, 추가적 생명력

【운명선(Fate Line)】손목에서 중지 방향으로 세로로 뻗음.
- 모든 사람에게 있는 것은 아님
- 깊고 뚜렷 → 강한 의지, 목표 지향적
- 생명선에서 시작 → 자수성가형
- 손목에서 시작 → 어릴 때부터 진로 뚜렷
- 중간에 끊어짐 → 직업/인생 방향 전환
- 없음 → 자유로운 삶, 정해진 운명보다 선택에 따름

【결혼선(Marriage Line)】새끼손가락 아래, 감정선 위의 짧은 가로선.
- 뚜렷한 선 하나 → 중요한 관계/결혼 하나
- 여러 개 → 여러 번의 중요한 관계
- 위로 휘어짐 → 결혼에 대한 긍정적 전망
- 아래로 휘어짐 → 관계에서의 실망이나 어려움
- 갈래로 끝남 → 별거나 이혼의 가능성

【태양선(Sun Line/Apollo Line)】약지 아래로 세로로 뻗는 선.
- 있으면 → 명예, 성공, 예술적 재능, 대중적 인정
- 뚜렷함 → 성공과 명성의 징조
- 희미함 → 재능은 있으나 아직 발현되지 않음

【건강선(Health Line)】새끼손가락 아래에서 손목 방향으로 비스듬히 뻗음.
- 없는 것이 오히려 건강한 징조
- 뚜렷함 → 건강에 관심이 많거나 건강 관련 직업
- 끊어짐/물결형 → 소화기 등 건강 주의

【특수 기호】
- 별(Star) ☆: 행운과 성공 (위치에 따라 의미 다름)
- 삼각형(Triangle) △: 지적 성취, 학문적 재능
- 사각형(Square) □: 보호, 위기 극복의 힘
- 십자(Cross) ✕: 시련과 변화, 정신적 성장
- 섬(Island) ◯: 에너지 분산, 스트레스, 약화
- 갈래(Fork) ⑃: 다양성, 풍부한 경험

위 기준은 참고용이며, 당신의 전문적 판단으로 자유롭게 해석하세요.

## 핵심 원칙
1. 사실적으로 해석하세요. 좋은 점은 좋다고, 안 좋은 점은 안 좋다고 솔직하게 말하세요.
2. 모든 것을 긍정적으로만 포장하지 마세요.
3. 4대 주요선 외에도 보이는 선이 있으면 additional_lines에 추가 분석하세요.
4. 특수 기호는 실제로 보이는 것만 기록하세요. 없으면 빈 배열 []. 없는 기호를 만들어내지 마세요.

다음 JSON 형식으로만 응답하세요 (마크다운 코드블록 없이 순수 JSON만):

{
  "is_palm": true 또는 false,
  "rejection_reason": "손바닥이 아닌 경우 이유 (한국어). 손바닥이면 빈 문자열",
  "hand": "왼손" 또는 "오른손",
  "lines": {
    "heart_line": {
      "name": "감정선",
      "description": "관찰한 물리적 특징 + 수상학적 해석. 좋은 점과 안 좋은 점 모두 솔직하게 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "head_line": {
      "name": "두뇌선",
      "description": "관찰한 물리적 특징 + 수상학적 해석. 솔직하게 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "life_line": {
      "name": "생명선",
      "description": "관찰한 물리적 특징 + 수상학적 해석. 솔직하게 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2", "키워드3"]
    },
    "fate_line": {
      "name": "운명선",
      "description": "관찰한 물리적 특징 + 수상학적 해석. 보이지 않으면 그 의미도 솔직히 (3-4문장, 한국어)",
      "score": 50~100 사이의 정수 (보이지 않으면 50~60),
      "keywords": ["키워드1", "키워드2", "키워드3"]
    }
  },
  "additional_lines": [
    {
      "name": "선 이름 (예: 결혼선, 태양선, 건강선, 직감선, 금성대 등)",
      "description": "관찰한 특징 + 수상학적 해석 (2-3문장, 한국어)",
      "score": 50~100 사이의 정수,
      "keywords": ["키워드1", "키워드2"]
    }
  ],
  "special_marks": [
    {
      "type": "기호 유형 (별/삼각형/사각형/십자/섬/갈래 등)",
      "location": "발견 위치",
      "meaning": "수상학적 의미 (1-2문장, 한국어)"
    }
  ],
  "overall": "전체적 종합. 좋은 점과 주의할 점을 균형 있게 (4-5문장, 한국어)",
  "personality": "손금에서 읽히는 성격 특성. 장단점 모두 (3-4문장, 한국어)",
  "love": "연애운. 솔직하게 (2-3문장, 한국어)",
  "career": "직업운/재물운. 솔직하게 (2-3문장, 한국어)",
  "health": "건강운. 주의점 있으면 언급 (1-2문장, 한국어)",
  "advice": "이 손금에 맞는 현실적 조언 (1-2문장, 한국어)"
}

additional_lines: 4대선 외에 보이는 선이 있으면 추가. 없으면 빈 배열 [].
special_marks: 실제로 보이는 것만 기록. 없으면 빈 배열 [].
4개 주요선의 score가 모두 같으면 안 됩니다. 반드시 위 JSON 형식만 출력하세요."""


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
