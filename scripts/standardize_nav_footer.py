#!/usr/bin/env python3
"""
Standardize nav-links and footer-links across all sub-pages.
Preserves 'active' class based on page's section.
Skips the main index.html (different nav structure) and /en/ (English nav).

내비·푸터 정의는 SSR(/daily/)과 같은 api/_core/site_layout.py 한 곳에서 가져온다.
"""
import importlib.util
import os
import re
import glob

PUBLIC = os.path.join(os.path.dirname(__file__), '..', 'public')


def _load_site_layout():
    # _core 패키지 초기화(사주 계산기 로딩) 없이 파일 하나만 로드
    path = os.path.join(os.path.dirname(__file__), '..', 'api', '_core', 'site_layout.py')
    spec = importlib.util.spec_from_file_location('site_layout', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


site_layout = _load_site_layout()

# Section detection: path prefixes of the nav (except home)
SECTION_PREFIXES = [href for href, _label in site_layout.NAV_ITEMS if href != '/']


def detect_section(rel_path):
    """Detect which section a file belongs to based on its relative path.

    어느 섹션에도 속하지 않는 페이지(예: /privacy/)는 None → 활성 링크 없음.
    """
    rel_path = '/' + rel_path.replace('\\', '/')
    for href in SECTION_PREFIXES:
        if rel_path.startswith(href):
            return href
    return None


def build_nav_html(active_href):
    """Build standardized nav-links HTML."""
    return site_layout.nav_links_html(active_href)


def build_footer_html():
    """Build standardized footer-links HTML (no active class, 개인정보처리방침 포함).

    앞쪽 들여쓰기는 원래 줄의 것을 그대로 쓴다 (재실행해도 공백이 늘지 않도록).
    """
    return site_layout.footer_links_html()


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
