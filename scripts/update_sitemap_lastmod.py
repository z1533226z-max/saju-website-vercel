#!/usr/bin/env python3
"""사이트맵 lastmod 를 '그 페이지 내용이 실제로 바뀐 날'로 맞춘다 (멱등).

배경: public/sitemap.xml 177개 중 176개가 6/17·10/3 고정값이라, 이후 고친 페이지도
구글에는 '안 바뀐 페이지'로 보였다. 반대로 오늘 날짜를 일괄로 찍으면 구글이 lastmod 를 불신한다.

규칙
- 정적 페이지(public/<경로>/index.html): git 이력에서 '본문'이 마지막으로 바뀐 커밋 날짜.
  본문 = <title> + meta description·robots + JSON-LD(정규화) + <body> 글자·링크 href·이미지 src/alt
  (내비·푸터·스크립트·스타일 제외).
  전 페이지 푸터 링크 추가 같은 공통 틀 변경은 날짜를 올리지 않는다.
  커밋 전 작업 중 변경이 있으면 오늘 날짜.
- 서버 렌더 페이지(/daily/, /daily/<띠>/): 매일 내용이 바뀌어 고정 날짜가 틀리므로 lastmod 를 넣지 않는다.

사용:
  python scripts/update_sitemap_lastmod.py          # 두 사이트맵 갱신
  python scripts/update_sitemap_lastmod.py --check  # 바꿀 것이 있으면 목록 출력 후 종료코드 1
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://saju.gon.ai.kr"
SITEMAPS = ("sitemap.xml", "sitemap-naver.xml")
SSR_PATH_RE = re.compile(r"^/daily/(?:[a-z]+/)?$")
URL_BLOCK_RE = re.compile(r"(<url>\s*<loc>([^<]+)</loc>)(\s*<lastmod>[^<]*</lastmod>)?")
SKIP_TAGS = {"nav", "footer", "script", "style", "noscript", "template"}


class _ContentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip = 0
        self._in_title = False
        self._in_body = False
        self._ld = None                                  # JSON-LD <script> 안이면 글자를 모으는 리스트

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._ld = []                                # 구조화 데이터 변경도 의미 있는 변경
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name", "").lower() == "description":
            self.parts.append("DESC:" + a.get("content", ""))
        elif tag == "meta" and a.get("name", "").lower() in ("robots", "googlebot", "bingbot", "yeti"):
            # 색인 허용 여부가 바뀐 것도 그 로봇에게는 의미 있는 변경 (예: 10/3 네이버 색인 복구)
            self.parts.append(f"ROBOTS:{a['name'].lower()}={a.get('content', '')}")
        elif tag == "body":
            self._in_body = True
        elif tag in SKIP_TAGS:
            self._skip += 1
        if self._in_body and not self._skip:
            if tag == "a" and a.get("href"):
                self.parts.append("HREF:" + a["href"])
            elif tag == "img":
                self.parts.append(f"IMG:{a.get('src', '')}|{a.get('alt', '')}")

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            raw = "".join(self._ld).strip()
            self._ld = None
            try:                                         # 키 순서·공백 차이는 무시
                raw = json.dumps(json.loads(raw), sort_keys=True, ensure_ascii=False)
            except ValueError:
                pass
            self.parts.append("LD:" + raw)
        if tag == "title":
            self._in_title = False
        elif tag in SKIP_TAGS and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)
        elif self._in_title:
            self.parts.append("TITLE:" + data)
        elif self._in_body and not self._skip:
            self.parts.append(data)


def content_signature(html):
    """페이지 본문만 남긴 비교용 문자열 (공백 정규화)."""
    p = _ContentParser()
    p.feed(html)
    return re.sub(r"\s+", " ", " ".join(p.parts)).strip()


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def today_kst():
    return datetime.now(timezone(timedelta(hours=9))).date().isoformat()


def content_lastmod(rel):
    """rel(예: public/zodiac/rat/index.html) 본문이 마지막으로 바뀐 날짜(YYYY-MM-DD). 이력 없으면 None."""
    history = [line.split(" ", 1) for line in _git("log", "--format=%H %cs", "--", rel).splitlines() if line]
    if not history:
        return None
    working = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    newer_sig = content_signature(working)
    if newer_sig != content_signature(_git("show", f"{history[0][0]}:{rel}")):
        return today_kst()
    for (sha, day), older in zip(history, history[1:] + [None]):
        if older is None:
            return day                                   # 처음 만든 커밋
        older_sig = content_signature(_git("show", f"{older[0]}:{rel}"))
        if older_sig != newer_sig:
            return day
        newer_sig = older_sig
    return history[-1][1]


def page_file(path):
    return "public" + path + ("index.html" if path.endswith("/") else "")


def expected_lastmod(loc):
    """None = lastmod 를 넣지 않는다(서버 렌더 페이지)."""
    path = loc.replace(SITE, "", 1)
    if SSR_PATH_RE.match(path):
        return None
    lastmod = content_lastmod(page_file(path))
    if lastmod is None:
        raise FileNotFoundError(f"{loc}: {page_file(path)} 가 git 에 없음")
    return lastmod


def update_sitemap(text, newline):
    changes = []

    def repl(m):
        head, loc, old = m.group(1), m.group(2), m.group(3)
        old_value = re.search(r"<lastmod>([^<]*)</lastmod>", old).group(1) if old else None
        new_value = expected_lastmod(loc)
        if new_value != old_value:
            changes.append((loc, old_value, new_value))
        if new_value is None:
            return head
        indent = re.match(r"\s*", old).group(0) if old else newline + "    "
        return f"{head}{indent}<lastmod>{new_value}</lastmod>"

    return URL_BLOCK_RE.sub(repl, text), changes


def main(check=False):
    all_changes = []
    for name in SITEMAPS:
        path = PUBLIC / name
        raw = path.read_bytes().decode("utf-8")
        newline = "\r\n" if "\r\n" in raw else "\n"
        new_text, changes = update_sitemap(raw, newline)
        all_changes += [(name, *c) for c in changes]
        if changes and not check:
            path.write_bytes(new_text.encode("utf-8"))
        print(f"{name}: {len(changes)}개 lastmod 변경{' 필요' if check else ''}")
    for name, loc, old, new in all_changes[:20]:
        print(f"  {name} {loc}: {old} -> {new}")
    return 1 if (check and all_changes) else 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
