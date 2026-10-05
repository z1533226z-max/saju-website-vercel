#!/usr/bin/env python3
"""
Standardize nav-links and footer-links across all sub-pages.
Adds /yearly/, /palm/, /dream/, /compatibility/ links where missing.
Preserves 'active' class based on page's section.
Skips the main index.html (different nav structure).
"""
import os
import re
import glob

PUBLIC = os.path.join(os.path.dirname(__file__), '..', 'public')

# Section detection: path prefix -> (href, label)
SECTIONS = [
    ('/zodiac/', '띠별 운세'),
    ('/daily/', '오늘의 운세'),
    ('/yearly/', '2026년 운세'),
    ('/compatibility/', '궁합'),
    ('/dream/', '꿈해몽'),
    ('/palm/', '손금 분석'),
    ('/guide/', '사주 가이드'),
]

NAV_ORDER = [
    ('/', '사주풀이'),
    ('/zodiac/', '띠별 운세'),
    ('/daily/', '오늘의 운세'),
    ('/yearly/', '2026년 운세'),
    ('/compatibility/', '궁합'),
    ('/dream/', '꿈해몽'),
    ('/palm/', '손금 분석'),
    ('/guide/', '사주 가이드'),
]

# 푸터에만 붙는 링크 (scripts/add_privacy_footer_link.py 로 넣은 것과 같은 모양)
FOOTER_EXTRA = [
    ('/privacy/', '개인정보처리방침'),
]


def detect_section(rel_path):
    """Detect which section a file belongs to based on its relative path.

    어느 섹션에도 속하지 않는 페이지(예: /privacy/)는 None → 활성 링크 없음.
    """
    rel_path = '/' + rel_path.replace('\\', '/')
    for href, label in SECTIONS:
        if rel_path.startswith(href):
            return href
    return None


def build_nav_html(active_href):
    """Build standardized nav-links HTML."""
    links = []
    for href, label in NAV_ORDER:
        if href == active_href:
            links.append(f'<a href="{href}" class="active">{label}</a>')
        else:
            links.append(f'<a href="{href}">{label}</a>')
    return '<nav class="nav-links">' + ''.join(links) + '</nav>'


def build_footer_html():
    """Build standardized footer-links HTML (no active class).

    앞쪽 들여쓰기는 원래 줄의 것을 그대로 쓴다 (재실행해도 공백이 늘지 않도록).
    """
    links = []
    for href, label in NAV_ORDER + FOOTER_EXTRA:
        links.append(f'\n                <a href="{href}">{label}</a>')
    return '<div class="footer-links">' + ''.join(links) + '\n            </div>'


# Regex patterns
NAV_PATTERN = re.compile(
    r'<nav class="nav-links">.*?</nav>',
    re.DOTALL
)
FOOTER_PATTERN = re.compile(
    r'<div class="footer-links">.*?</div>',
    re.DOTALL
)


def process_file(filepath, rel_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    section = detect_section(rel_path)

    # Replace nav-links
    new_nav = build_nav_html(section)
    content = NAV_PATTERN.sub(new_nav, content)

    # Replace footer-links
    new_footer = build_footer_html()
    content = FOOTER_PATTERN.sub(new_footer, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = glob.glob(os.path.join(PUBLIC, '**', 'index.html'), recursive=True)
    updated = 0
    skipped = 0

    for filepath in sorted(html_files):
        rel_path = os.path.relpath(filepath, PUBLIC).replace('\\', '/')

        # Skip main index.html (different nav structure with anchors)
        if rel_path == 'index.html':
            skipped += 1
            continue

        # Skip English pages (/en/ has its own English nav/footer)
        if rel_path.startswith('en/'):
            skipped += 1
            continue

        # Skip if file doesn't have nav-links
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'class="nav-links"' not in content:
            skipped += 1
            continue

        if process_file(filepath, rel_path):
            updated += 1
            print(f'  Updated: {rel_path}')
        else:
            skipped += 1

    print(f'\nDone: {updated} files updated, {skipped} skipped')


if __name__ == '__main__':
    main()
