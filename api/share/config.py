"""
공유 버튼 설정 — GET /api/share/config

정적 페이지는 환경변수를 읽을 수 없어서, 카카오 공개 JavaScript 키(KAKAO_JS_KEY)만 여기서 내려준다.
이 키는 카카오가 '도메인 제한이 걸린 공개 키'로 설계한 값이라 화면에 노출돼도 되고,
다른 비밀값은 절대 이 응답에 넣지 않는다. 키가 없으면 null → 화면이 카카오 버튼을 숨긴다.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import re

# 카카오 JavaScript 키는 32자리 16진수(대소문자 무관). 형식이 다르면(오타·다른 비밀값을 잘못 넣은 경우) 내보내지 않는다.
_KAKAO_KEY_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def public_config():
    key = (os.getenv("KAKAO_JS_KEY") or "").strip()
    return {"kakaoJsKey": key if _KAKAO_KEY_RE.match(key) else None}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(public_config()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=300, s-maxage=300")
        self.end_headers()
        self.wfile.write(body)
