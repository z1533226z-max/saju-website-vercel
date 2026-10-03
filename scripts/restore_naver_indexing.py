#!/usr/bin/env python3
"""네이버 색인 복구: 일반 robots noindex → 구글/빙 전용 noindex 로 교체 (멱등).

대상 (168장):
  - public/zodiac/<띠>/2026-10/, 2026-11/, 2026-12/   (36장)
  - public/compatibility/<띠>/<띠>/                   (132장)

2026-07-05 에 붙인 <meta name="robots" content="noindex, ..."> 때문에 네이버 유입까지
끊겼다. 구글·빙은 계속 제외하고 네이버(Yeti)만 색인되도록
<meta name="googlebot" content="noindex, follow"> + <meta name="bingbot" ...> 로 바꾼다.
지난 달(2026-01~09) 페이지는 건드리지 않는다.

또한 public/sitemap-naver.xml 을 생성한다 (robots.txt·sitemap.xml 에는 넣지 않음,
네이버 서치어드바이저에 수동 제출용).

사용: python scripts/restore_naver_indexing.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://saju.gon.ai.kr"
LASTMOD = "2026-10-03"

ANIMALS = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
           "horse", "goat", "monkey", "rooster", "dog", "pig"]
MONTHS = ["2026-10", "2026-11", "2026-12"]

ROBOTS_NOINDEX = re.compile(r'^([ \t]*)<meta name="robots" content="noindex[^"]*">', re.MULTILINE)
GOOGLEBOT = '<meta name="googlebot" content="noindex, follow">'
BINGBOT = '<meta name="bingbot" content="noindex, follow">'
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)"')


def target_paths():
    paths = [f"zodiac/{a}/{m}/" for a in ANIMALS for m in MONTHS]
    paths += [f"compatibility/{a}/{b}/" for a in ANIMALS for b in ANIMALS if a != b]
    return paths


def status(text):
    if ROBOTS_NOINDEX.search(text):
        return "robots-noindex"
    if GOOGLEBOT in text and BINGBOT in text:
        return "crawler-specific"
    return "other"


def main():
    paths = target_paths()
    before = {"robots-noindex": 0, "crawler-specific": 0, "other": 0}
    after = dict(before)
    changed = 0
    errors = []

    for rel in paths:
        f = PUBLIC / rel / "index.html"
        if not f.is_file():
            errors.append(f"missing file: {f}")
            continue
        with open(f, encoding="utf-8", newline="") as fh:
            text = fh.read()
        before[status(text)] += 1

        canon = CANONICAL.search(text)
        if not canon or canon.group(1) != f"{SITE}/{rel}":
            errors.append(f"canonical mismatch: {rel} -> {canon.group(1) if canon else None}")

        nl = "\r\n" if "\r\n" in text else "\n"
        new = ROBOTS_NOINDEX.sub(lambda m: f"{m.group(1)}{GOOGLEBOT}{nl}{m.group(1)}{BINGBOT}", text, count=1)
        if new != text:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            changed += 1
        after[status(new)] += 1

    urls = "\n".join(
        f"  <url>\n    <loc>{SITE}/{rel}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>"
        for rel in paths
    )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}\n</urlset>\n")
    with open(PUBLIC / "sitemap-naver.xml", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(sitemap)

    print(f"targets: {len(paths)}  files changed this run: {changed}")
    print(f"before: {before}")
    print(f"after : {after}")
    print(f"sitemap-naver.xml: {len(paths)} URLs")
    if errors:
        print("ERRORS:", *errors, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
