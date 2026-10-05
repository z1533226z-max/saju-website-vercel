#!/usr/bin/env python3
"""
모든 공개 HTML 페이지 푸터에 '개인정보처리방침'(/privacy/) 링크를 넣는다.

- 멱등: 푸터에 이미 href="/privacy/" 가 있으면 그 파일은 건드리지 않는다 (여러 번 실행해도 같음).
- 푸터 형태별 처리
  1) <div class="footer-links"> 세로 목록 (한국어 표준 푸터, /en/ 영어 푸터)
     → 마지막 링크 뒤에 같은 들여쓰기로 한 줄 추가
  2) ' · ' 로 이어진 한 줄 링크 (/guide/, /palm/, 홈)
     → 마지막 링크 뒤에 ' · <a href="/privacy/">…</a>' 추가 (마지막 링크의 style 속성을 그대로 따름)
- 위 형태가 아닌 푸터는 고치지 않고 보고하며 종료 코드 1.
- additional-features.html 은 홈 화면 조각(HTML fragment)이라 제외한다.

실행: python scripts/add_privacy_footer_link.py [--dry-run]
"""
import argparse
import glob
import os
import re
import sys

PUBLIC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public"))
HREF = "/privacy/"
LABEL_KO = "개인정보처리방침"
LABEL_EN = "Privacy Policy (개인정보처리방침)"
SKIP = {"additional-features.html"}

FOOTER_RE = re.compile(r"<footer\b[^>]*>.*?</footer>", re.S)
LIST_RE = re.compile(r'<div class="footer-links">(?P<inner>.*?)(?P<tail>\r?\n[ \t]*)</div>', re.S)
ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>.*?</a>", re.S)
STYLE_RE = re.compile(r'\sstyle="[^"]*"')


def _add_to_list(footer, rel, nl):
    m = LIST_RE.search(footer)
    if not m:
        return None
    indents = re.findall(r"\n([ \t]*)<a\b", m.group("inner"))
    if not indents:
        return None
    if rel.startswith("en/"):
        link = f'<a href="{HREF}" hreflang="ko">{LABEL_EN}</a>'
    else:
        link = f'<a href="{HREF}">{LABEL_KO}</a>'
    pos = m.start("tail")
    return footer[:pos] + nl + indents[-1] + link + footer[pos:]


def _add_inline(footer):
    anchors = list(ANCHOR_RE.finditer(footer))
    if not anchors or " · <a" not in footer:
        return None
    last = anchors[-1]
    style = STYLE_RE.search(last.group("attrs"))
    link = f' · <a href="{HREF}"{style.group(0) if style else ""}>{LABEL_KO}</a>'
    return footer[:last.end()] + link + footer[last.end():]


def add_privacy_link(html, rel):
    """(새 html, 상태) — 상태: 'list' | 'inline' | 'already' | 'no-footer' | 'unknown'."""
    footers = list(FOOTER_RE.finditer(html))
    if not footers:
        return html, "no-footer"
    fm = footers[-1]
    footer = fm.group(0)
    if f'href="{HREF}"' in footer:
        return html, "already"
    nl = "\r\n" if "\r\n" in html else "\n"
    new_footer, kind = _add_to_list(footer, rel, nl), "list"
    if new_footer is None:
        new_footer, kind = _add_inline(footer), "inline"
    if new_footer is None:
        return html, "unknown"
    return html[:fm.start()] + new_footer + html[fm.end():], kind


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않고 결과만 출력")
    args = parser.parse_args()

    counts = {"list": 0, "inline": 0, "already": 0}
    problems = []
    for path in sorted(glob.glob(os.path.join(PUBLIC, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, PUBLIC).replace("\\", "/")
        if rel in SKIP:
            continue
        with open(path, encoding="utf-8", newline="") as f:
            html = f.read()
        new_html, status = add_privacy_link(html, rel)
        if status in ("no-footer", "unknown"):
            problems.append(f"{rel}: {status}")
            continue
        counts[status] += 1
        if new_html != html and not args.dry_run:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_html)

    changed = counts["list"] + counts["inline"]
    mode = " (dry-run, 저장 안 함)" if args.dry_run else ""
    print(f"changed={changed} (list={counts['list']}, inline={counts['inline']}), "
          f"already={counts['already']}, skipped={sorted(SKIP)}{mode}")
    for p in problems:
        print("  !! " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
