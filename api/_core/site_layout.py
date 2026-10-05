# -*- coding: utf-8 -*-
"""
SSR 페이지(/daily/, /daily/<띠>/) 공용 레이아웃 조각: 상단 내비 · 푸터 · '함께 보면 좋은 운세'.

- 내비(.nav-links)·푸터(.footer-links)는 정적 페이지와 같은 마크업이다.
  정적 페이지 쪽은 scripts/standardize_nav_footer.py · scripts/add_privacy_footer_link.py 가
  만든 것이고, tests/test_site_layout.py 가 public/ 실제 페이지와 비교한다.
- public/ 은 서버리스 함수 번들에 들어간다는 보장이 없어 런타임에 파일을 읽지 않는다.
  링크 대상(월별 운세 목록, 2027 섹션 id, 꿈해몽 페이지)은 아래 상수로 두고,
  테스트가 public/ 실제 파일·robots 메타와 대조한다.
"""
from datetime import timedelta, timezone

KST = timezone(timedelta(hours=9))

# 정적 페이지 표준 내비 순서 (scripts/standardize_nav_footer.py 의 NAV_ORDER 와 같아야 함)
NAV_ITEMS = (
    ("/", "사주풀이"),
    ("/zodiac/", "띠별 운세"),
    ("/daily/", "오늘의 운세"),
    ("/yearly/", "2026년 운세"),
    ("/compatibility/", "궁합"),
    ("/dream/", "꿈해몽"),
    ("/palm/", "손금 분석"),
    ("/guide/", "사주 가이드"),
)
PRIVACY_ITEM = ("/privacy/", "개인정보처리방침")
FOOTER_ITEMS = NAV_ITEMS + (PRIVACY_ITEM,)


def nav_links_html(active_href=None):
    """정적 페이지와 같은 한 줄짜리 <nav class="nav-links">."""
    links = "".join(
        f'<a href="{href}" class="active">{label}</a>' if href == active_href
        else f'<a href="{href}">{label}</a>'
        for href, label in NAV_ITEMS
    )
    return f'<nav class="nav-links">{links}</nav>'


def footer_links_html():
    """정적 페이지와 같은 <div class="footer-links"> (개인정보처리방침 포함)."""
    links = "".join(f'\n                <a href="{href}">{label}</a>' for href, label in FOOTER_ITEMS)
    return f'<div class="footer-links">{links}\n            </div>'


# ── '함께 보면 좋은 운세' (/daily/<띠>/) ───────────────────────────────────
RELATED_MARKER = "DAILY_RELATED_V1"
MAX_RELATED_LINKS = 6

# public/yearly/<띠>/index.html 의 2027 정미년 섹션 id (Y2027_PREVIEW_V1 블록)
YEARLY_2027_ANCHOR = "y2027"

# 12띠 공통으로 있고 일반 robots noindex 가 아닌 월별 운세 (/zodiac/<띠>/YYYY-MM/).
# 2026-01~09 는 모든 검색엔진 noindex 라 빼고, 2026-10~12 는 네이버 색인용이라 넣는다.
MONTHLY_PAGES = frozenset({"2026-10", "2026-11", "2026-12"})

# 본문이 깊은 꿈해몽 페이지 (68개 중 상위)
DREAM_PAGES = {
    "pig": ("/dream/pig/", "🐷 돼지꿈 해몽"),
    "dragon": ("/dream/dragon/", "🐉 용꿈 해몽"),
    "snake": ("/dream/snake/", "🐍 뱀꿈 해몽"),
}

# 템플릿의 <style> 안에 '    {RELATED_LINKS_CSS}' 형태로 넣는다 (첫 줄은 들여쓰기 없이 시작).
RELATED_LINKS_CSS = """.daily-more-links {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.6rem;
        margin-top: 1rem;
    }
    .daily-more-links a {
        display: block;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        color: inherit;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.2);
        transition: border-color 0.2s;
    }
    .daily-more-links a:hover { border-color: var(--color-gold); color: var(--color-gold); }"""


def _kst_date(now):
    return now.astimezone(KST) if now.tzinfo is not None else now


def monthly_page_href(sign, now):
    """이번 달(KST) 월별 운세 경로. 링크할 수 있는 달이 아니면 None."""
    now = _kst_date(now)
    ym = f"{now.year:04d}-{now.month:02d}"
    return f"/zodiac/{sign}/{ym}/" if ym in MONTHLY_PAGES else None


def dream_keys_for(sign):
    """띠와 같은 동물의 깊은 꿈해몽이 있으면 그것부터, 나머지는 대표 길몽(돼지꿈·용꿈)."""
    first = sign if sign in DREAM_PAGES else "pig"
    second = "dragon" if first != "dragon" else "pig"
    return [first, second]


def related_links(sign, zodiac_name, now):
    """[(href, label), ...] — 최대 MAX_RELATED_LINKS 개."""
    now = _kst_date(now)
    links = [(f"/yearly/{sign}/#{YEARLY_2027_ANCHOR}", f"🎍 {zodiac_name} 2027 신년운세")]
    month_href = monthly_page_href(sign, now)
    if month_href:
        links.append((month_href, f"📅 {zodiac_name} {now.month}월 운세"))
    else:
        links.append((f"/zodiac/{sign}/", f"📅 {zodiac_name} 운세 총정리"))
    links.append((f"/compatibility/{sign}/", f"💞 {zodiac_name} 궁합"))
    links.extend(DREAM_PAGES[k] for k in dream_keys_for(sign))
    return links[:MAX_RELATED_LINKS]


def related_links_html(sign, zodiac_name, now):
    items = "".join(
        f'\n                <a href="{href}">{label}</a>' for href, label in related_links(sign, zodiac_name, now)
    )
    return (
        f'<!-- {RELATED_MARKER} -->\n'
        f'            <h2 class="section-title" style="margin-top:2rem;"><span class="gold-text">함께 보면 좋은 운세</span></h2>\n'
        f'            <nav class="daily-more-links" aria-label="{zodiac_name} 함께 보면 좋은 운세">{items}\n'
        f'            </nav>\n'
        f'            <!-- /{RELATED_MARKER} -->'
    )
