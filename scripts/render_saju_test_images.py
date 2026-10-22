#!/usr/bin/env python3
"""
사주 오행 캐릭터 테스트 공유 이미지(OG) 만들기 — public/assets/images/saju-test/og-*.jpg

카톡·페이스북 미리보기는 자바스크립트를 실행하지 않으므로 이미지 파일이 미리 있어야 한다.
화면의 결과 카드와 같은 그림이 되도록 saju-test-app.js 의 SajuTestCard.draw() 를
헤드리스 Chromium(playwright)에서 그대로 실행해 저장한다. 개인 정보 없이 유형별 대표 그림만 만든다.

    pip install playwright && python -m playwright install chromium
    python scripts/render_saju_test_images.py
"""
import base64
import functools
import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
OUT_DIR = os.path.join(PUBLIC, "assets", "images", "saju-test")

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from generate_saju_test import TYPES  # noqa: E402


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    from playwright.sync_api import sync_playwright

    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_QuietHandler, directory=PUBLIC))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}/saju-test/"
    os.makedirs(OUT_DIR, exist_ok=True)
    jobs = [("og-main.jpg", "og-main", None)] + [(f"og-{t['slug']}.jpg", "og", i) for i, t in enumerate(TYPES)]
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.wait_for_function("window.SajuTestCard && window.SAJU_TEST_DATA")
            text = "".join(t["name"] for t in TYPES) + "사주오행캐릭터테스트나는어떤자연일까생년월일만넣으면초가지친구궁합너는이야일간"
            page.evaluate("t => window.SajuTestCard.fontsReady(t)", text)
            for name, kind, stem in jobs:
                data_url = page.evaluate(
                    "([k, s]) => window.SajuTestCard.draw(document.createElement('canvas'), k, {stem: s}).toDataURL('image/jpeg', 0.9)",
                    [kind, stem])
                with open(os.path.join(OUT_DIR, name), "wb") as f:
                    f.write(base64.b64decode(data_url.split(",", 1)[1]))
                print("wrote", name)
            browser.close()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
