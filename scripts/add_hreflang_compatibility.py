"""Add reciprocal hreflang links to KR compatibility pages + KR home.

Mirrors scripts/add_hreflang_zodiac.py. The /en/ counterparts already point
back to these KR pages via hreflang; this completes the bidirectional
(reciprocal) signal so Google treats the /en/ pages as the canonical English
alternates instead of ignoring the one-sided hreflang.

Idempotent: skips any file that already contains a hreflang tag.
"""
import os
import re

ANIMALS = ['rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake',
           'horse', 'goat', 'monkey', 'rooster', 'dog', 'pig']
PUBLIC = os.path.join(os.path.dirname(__file__), '..', 'public')


def add_hreflang(file_path, links_block):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'hreflang' in content:
        print(f"  Skip (already has hreflang): {file_path}")
        return False
    content, n = re.subn(
        r'(<link rel="canonical"[^>]+>)',
        lambda m: m.group(1) + links_block,
        content,
        count=1,
    )
    if n == 0:
        print(f"  WARN no canonical found: {file_path}")
        return False
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Updated: {file_path}")
    return True


def pair(ko_url, en_url):
    return (f'\n    <link rel="alternate" hreflang="ko" href="{ko_url}">'
            f'\n    <link rel="alternate" hreflang="en" href="{en_url}">')


count = 0

# KR home: ko + en + x-default (mirrors /en/ home, which carries all three)
home = os.path.join(PUBLIC, 'index.html')
if os.path.exists(home):
    block = (pair('https://saju.gon.ai.kr/', 'https://saju.gon.ai.kr/en/')
             + '\n    <link rel="alternate" hreflang="x-default" '
               'href="https://saju.gon.ai.kr/">')
    if add_hreflang(home, block):
        count += 1

# Compatibility index
idx = os.path.join(PUBLIC, 'compatibility', 'index.html')
if os.path.exists(idx):
    if add_hreflang(idx, pair('https://saju.gon.ai.kr/compatibility/',
                              'https://saju.gon.ai.kr/en/compatibility/')):
        count += 1

# Individual animal compatibility pages
for animal in ANIMALS:
    p = os.path.join(PUBLIC, 'compatibility', animal, 'index.html')
    if os.path.exists(p):
        if add_hreflang(p, pair(f'https://saju.gon.ai.kr/compatibility/{animal}/',
                                f'https://saju.gon.ai.kr/en/compatibility/{animal}/')):
            count += 1

print(f"\nUpdated {count} KR pages with hreflang links")
