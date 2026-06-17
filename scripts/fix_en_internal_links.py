#!/usr/bin/env python3
"""EN 페이지 내부링크 KR 누수 교정 (exp: EN 색인/응집도 개선, 2026-06-17)

문제: /en/ 영문 페이지 40개의 nav/footer/CTA가 한국어 페이지로 링크를 보내
      영어 검색 유입자를 한국어 페이지로 이탈시키고, EN 섹션 링크주스가 누수됨.

교정:
  - /dream/ (Dreams, Dream Dictionary) → /en/five-elements/ (Five Elements)
  - /palm/  (Palm Reading)             → /en/four-pillars/ (Four Pillars)
  - href="/" CTA (앵커 텍스트에 'Korean' 미포함) → /en/ (EN 홈)
  - 'Korean Ver.' / 'Korean Version' / '...(Korean)' (의도적 언어전환) → 유지

부가효과: nav/footer에 없던 Five Elements·Four Pillars 섹션이 40개 페이지에
          노출되어 발견성(crawl/색인) 향상.

멱등: 이미 교정된 파일에 재실행해도 안전(변경 없음).
"""
import re
import glob
import os

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
files = sorted(glob.glob(os.path.join(PUB, 'en', '**', 'index.html'), recursive=True))

# 텍스트까지 함께 교체 (EN 대응 페이지가 없는 KR 전용 섹션)
LITERAL = [
    ('<a href="/dream/">Dreams</a>',           '<a href="/en/five-elements/">Five Elements</a>'),
    ('<a href="/dream/">Dream Dictionary</a>', '<a href="/en/five-elements/">Five Elements</a>'),
    ('<a href="/palm/">Palm Reading</a>',      '<a href="/en/four-pillars/">Four Pillars</a>'),
]

HOME_A = re.compile(r'<a ([^>]*?)href="/"([^>]*?)>([^<]*)</a>')


def fix_home(m):
    """href="/" CTA 중 앵커 텍스트에 'Korean'이 없으면 EN 홈(/en/)으로."""
    text = m.group(3)
    if 'Korean' in text:
        return m.group(0)  # 의도적 언어전환 링크 유지
    return f'<a {m.group(1)}href="/en/"{m.group(2)}>{text}</a>'


stats = {'files_changed': 0, 'dream_palm': 0, 'cta': 0}
for fp in files:
    with open(fp, encoding='utf-8') as f:
        c = f.read()
    orig = c

    for a, b in LITERAL:
        n = c.count(a)
        stats['dream_palm'] += n
        c = c.replace(a, b)

    # CTA 변경 수를 정확히 세기 위해 직접 카운트
    def _count_and_fix(m):
        if 'Korean' in m.group(3):
            return m.group(0)
        stats['cta'] += 1
        return f'<a {m.group(1)}href="/en/"{m.group(2)}>{m.group(3)}</a>'

    c = HOME_A.sub(_count_and_fix, c)

    if c != orig:
        stats['files_changed'] += 1
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)

print(stats)
