"""Render docs/img/share.png, the 1200x630 link-preview image, from the built page.

    pip install playwright && playwright install chromium
    python docs/build_case_study.py && python docs/make_share_image.py

It is a screenshot of the real hero, so the preview can never show a number the
page does not. The README uses the same image. Re-run after the hero changes.
"""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent
OUT = DOCS / "img" / "share.png"

# Fonts load over http, not file://, so serve docs/ on a free port for the shot.
handler = partial(SimpleHTTPRequestHandler, directory=str(DOCS))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # 1600x840 at 0.75 scale is exactly 1200x630, the ratio link previews expect
        page = browser.new_page(viewport={"width": 1600, "height": 840},
                                device_scale_factor=0.75, color_scheme="light")
        page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(OUT))
        browser.close()
finally:
    server.shutdown()

from PIL import Image  # noqa: E402  (installed with matplotlib)
size = Image.open(OUT).size
assert size == (1200, 630), f"share image is {size}, link previews expect 1200x630"
print(f"wrote {OUT.relative_to(DOCS.parent)} {size[0]}x{size[1]}, {OUT.stat().st_size // 1024} KB")
