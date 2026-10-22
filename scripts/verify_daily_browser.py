"""Local-only HTTP/browser proof; never connects to production or loads .env.

Run with the repository requirements plus playwright installed:
python scripts/verify_daily_browser.py --output <evidence directory>
The HTTP server is always shut down, including on assertion failures.
"""
import argparse
import importlib.util
import json
import re
import sys
import threading
from datetime import datetime, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))
from _core.daily_fortune import KST, ZODIAC_ORDER, generate_fortune  # noqa: E402


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(output):
    from playwright.sync_api import expect, sync_playwright

    output.mkdir(parents=True, exist_ok=True)
    detail = load("api/daily/fortune.py", "browser_detail")
    index = load("api/daily/index.py", "browser_index")
    before = datetime(2026, 10, 22, 23, 59, 59, tzinfo=KST)
    after = before + timedelta(seconds=2)

    class Clock:
        current = before

        @classmethod
        def now(cls, tz):
            return cls.current.astimezone(tz)

    detail.datetime = index.datetime = Clock
    routes = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))["routes"]
    daily_routes = [r for r in routes if r["dest"].startswith("/api/daily/")]

    class LocalHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT / "public"), **kwargs)

        def log_message(self, *args):
            pass

        def respond(self, include_body):
            original = self.path
            parts = urlsplit(original)
            for route in daily_routes:
                match = re.fullmatch(route["src"], parts.path)
                if match:
                    destination = route["dest"]
                    for i, group in enumerate(match.groups(), 1):
                        destination = destination.replace(f"${i}", group)
                    target = urlsplit(destination)
                    # Preserve the incoming query, as Vercel rewrites do.
                    query = parse_qs(parts.query, keep_blank_values=True)
                    query.update(parse_qs(target.query, keep_blank_values=True))
                    self.path = target.path + "?" + urlencode(query, doseq=True)
                    module = index if target.path.endswith("index.py") else detail
                    try:
                        module.handler._respond(self, include_body)
                    finally:
                        self.path = original
                    return
            if include_body:
                super().do_GET()
            else:
                super().do_HEAD()

        def do_GET(self):
            self.respond(True)

        def do_HEAD(self):
            self.respond(False)

    server = ThreadingHTTPServer(("127.0.0.1", 0), LocalHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    rows = []
    page_errors = []
    try:
        # Raw HTTP responses: bots receive dates, scores and prose without JS.
        for now in (before, after):
            Clock.current = now
            for sign in ZODIAC_ORDER:
                for day in ("today", "tomorrow"):
                    url = f"{base}/daily/{sign}/" + ("?day=tomorrow" if day == "tomorrow" else "")
                    with urlopen(url, timeout=10) as response:
                        html = response.read().decode("utf-8")
                        headers = dict(response.headers)
                    target = now + timedelta(days=day == "tomorrow")
                    fortune = generate_fortune(sign, target)
                    assert f'data-daily-date="{target:%Y-%m-%d}"' in html
                    assert fortune["overall_msg"] in html
                    assert headers["Cache-Control"] == "no-store, max-age=0"
                    assert headers["CDN-Cache-Control"] == headers["Vercel-CDN-Cache-Control"] == "no-store"
                    assert ('content="noindex,follow"' in html) == (day == "tomorrow")
                    if sign == "dog":
                        (output / f"after-dog-asof-{now:%Y-%m-%d}-{day}.html").write_text(html, encoding="utf-8")
                        rows.append({"asof": now.isoformat(), "day": day, "date": target.date().isoformat(),
                                     "overall": fortune["overall"], "ilji": fortune["ilji"]["display"],
                                     "overall_msg": fortune["overall_msg"], "headers": headers})

        Clock.current = before
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=True)

            def local_only(route):
                if urlsplit(route.request.url).hostname == "127.0.0.1":
                    route.continue_()
                else:
                    route.abort()

            try:
                # JS disabled: dates and both tabs still work on every zodiac.
                context = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
                context.route("**/*", local_only)
                page = context.new_page()
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                for sign in ZODIAC_ORDER:
                    page.goto(f"{base}/daily/{sign}/", wait_until="networkidle")
                    expect(page.locator("time")).to_have_attribute("datetime", "2026-10-22")
                    page.get_by_role("link", name="내일의 운세", exact=True).click()
                    expect(page.locator("time")).to_have_attribute("datetime", "2026-10-23")
                    expect(page.locator(".daily-day-nav [aria-current=page]")).to_have_text("내일의 운세")
                    if not page.evaluate("document.documentElement.scrollWidth <= innerWidth"):
                        page.screenshot(path=str(output / "mobile-overflow-before-fix.png"), full_page=True)
                        print(page.evaluate("""Array.from(document.querySelectorAll('body *')).map(e => ({
                            tag: e.tagName, cls: e.className, left: e.getBoundingClientRect().left,
                            right: e.getBoundingClientRect().right
                        })).filter(e => e.right > innerWidth || e.left < 0)"""))
                        raise AssertionError(f"mobile overflow: {sign}")
                context.close()

                for width, height in ((390, 844), (1440, 1000)):
                    context = browser.new_context(viewport={"width": width, "height": height}, timezone_id="America/Los_Angeles")
                    context.route("**/*", local_only)
                    page = context.new_page()
                    page.on("pageerror", lambda error: page_errors.append(str(error)))
                    page.clock.install(time=before - timedelta(seconds=1))
                    page.clock.pause_at(before)
                    for day in ("today", "tomorrow"):
                        page.goto(f"{base}/daily/dog/" + ("?day=tomorrow" if day == "tomorrow" else ""), wait_until="networkidle")
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                        page.screenshot(path=str(output / f"dog-{day}-{width}.png"), full_page=True)
                    # Preview must retain its query at midnight and advance one date.
                    Clock.current = after
                    page.clock.run_for(2000)
                    expect(page.locator("time")).to_have_attribute("datetime", "2026-10-24")
                    assert "day=tomorrow" in page.url
                    page.screenshot(path=str(output / f"dog-midnight-preview-{width}.png"), full_page=True)
                    Clock.current = before
                    context.close()

                # Today and index also refresh when held open across midnight.
                for path, expected_date in (("/daily/dog/", "2026-10-23"), ("/daily/", "2026-10-23")):
                    context = browser.new_context()
                    context.route("**/*", local_only)
                    page = context.new_page()
                    page.clock.install(time=before - timedelta(seconds=1))
                    page.clock.pause_at(before)
                    page.goto(base + path, wait_until="networkidle")
                    Clock.current = after
                    page.clock.run_for(2000)
                    expect(page.locator("body")).to_have_attribute("data-daily-date", expected_date)
                    Clock.current = before
                    context.close()

                # Simulate a sleeping/history-restored tab with timers not fired.
                for event in ("pageshow", "visibilitychange"):
                    context = browser.new_context()
                    context.route("**/*", local_only)
                    page = context.new_page()
                    page.clock.install(time=before - timedelta(seconds=1))
                    page.clock.pause_at(before)
                    page.goto(base + "/daily/dog/", wait_until="networkidle")
                    Clock.current = after
                    page.clock.set_system_time(after)
                    if event == "pageshow":
                        page.evaluate("window.dispatchEvent(new Event('pageshow'))")
                    else:
                        page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
                    expect(page.locator("body")).to_have_attribute("data-daily-date", "2026-10-23")
                    Clock.current = before
                    context.close()
                assert not page_errors, page_errors
            finally:
                browser.close()
        result = {"raw_http_pages": 48, "no_js_zodiac_switches": 12, "viewports": [390, 1440],
                  "midnight": ["today", "tomorrow", "index"], "restore_events": ["pageshow", "visibilitychange"],
                  "page_errors": page_errors, "external_requests": "blocked", "responses": rows}
        (output / "browser-proof.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PASS: 48 raw HTTP pages, 12 no-JS tab switches, 390/1440px, midnight and restore events")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        print(f"Local server stopped: {base}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    verify(parser.parse_args().output.resolve())
