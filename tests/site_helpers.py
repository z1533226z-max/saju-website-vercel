"""테스트 공용: public/ 정적 파일과 SSR 라우트로 내부 링크가 실제로 열리는지 확인하는 도우미."""
import importlib.util
import os
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
API_DIR = os.path.join(ROOT, "api")

SIGNS = ("rat", "ox", "tiger", "rabbit", "dragon", "snake",
         "horse", "goat", "monkey", "rooster", "dog", "pig")
# vercel.json 의 SSR 라우트: /daily/ → api/daily/index.py, /daily/<띠>/ → api/daily/fortune.py
SSR_ROUTE_RE = re.compile(r"^/daily/(?:(?:%s)/)?$" % "|".join(SIGNS))

ADSENSE_SCRIPT_RE = re.compile(
    r'<script[^>]+src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js'
    r'\?client=ca-pub-7479840445702290"')
MANUAL_AD_SLOT_RE = re.compile(r'<ins[^>]+class="[^"]*adsbygoogle')
GA4_RE = re.compile(r"gtag\('config',\s*'G-BNRL6FRMMM'\)")
GENERIC_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)


def load_module(rel_path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_public(rel):
    with open(os.path.join(PUBLIC, rel), encoding="utf-8") as f:
        return f.read()


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href") is not None:
            self.hrefs.append(a["href"])


def parse(html):
    p = LinkParser()
    p.feed(html)
    return p


def public_file_for(path):
    """URL 경로 → public/ 아래 파일 경로 (없으면 None)."""
    rel = path.lstrip("/")
    candidate = os.path.join(PUBLIC, rel, "index.html") if (rel == "" or path.endswith("/")) \
        else os.path.join(PUBLIC, rel)
    return candidate if os.path.isfile(candidate) else None


def resolve_internal_href(href, page_ids=()):
    """내부 링크 하나를 검사. (ok, 설명) — 외부 링크는 (True, 'external')."""
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith(("mailto:", "tel:", "javascript:")):
        return True, "external"
    if not parts.path:                       # '#id' 같은 페이지 내부 이동
        return (parts.fragment in page_ids), f"in-page #{parts.fragment}"
    if not parts.path.startswith("/"):
        return False, f"relative link {href!r}"
    if SSR_ROUTE_RE.match(parts.path):
        return True, "ssr"
    target = public_file_for(parts.path)
    if target is None:
        return False, f"missing file for {parts.path}"
    if parts.fragment:
        with open(target, encoding="utf-8") as f:
            ids = parse(f.read()).ids
        if parts.fragment not in ids:
            return False, f"missing id #{parts.fragment} in {parts.path}"
    return True, "file"


def last_footer(html):
    found = re.findall(r"<footer\b[^>]*>.*?</footer>", html, re.S)
    return found[-1] if found else ""


def public_html_files():
    out = []
    for dirpath, _dirs, files in os.walk(PUBLIC):
        for name in files:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), PUBLIC).replace("\\", "/"))
    return sorted(out)
