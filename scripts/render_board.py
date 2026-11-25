#!/usr/bin/env python3
"""Render an HTML analysis board into a crisp 16:9 PNG via Playwright + Chrome.

Usage:
    python render_board.py --html board.html --out board.png \
        [--width 1920] [--height 1080] [--scale 2]

Uses the locally installed Chrome (auto-detected, override with --chrome or
CHROME_PATH env). Waits for all images and fonts before capturing.
"""
from __future__ import annotations

import argparse
import os
import sys


def find_chrome(explicit: str | None) -> str | None:
    candidates = [
        explicit,
        os.environ.get("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\lenovo\AppData\Local\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Screenshot an HTML board to 16:9 PNG")
    ap.add_argument("--html", required=True, help="path to board HTML file")
    ap.add_argument("--out", required=True, help="output PNG path")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--scale", type=int, default=2, help="device scale factor for crisp text")
    ap.add_argument("--chrome", default=None, help="explicit Chrome executable path")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    html_path = os.path.abspath(args.html)
    out_path = os.path.abspath(args.out)
    if not os.path.isfile(html_path):
        print(f"ERROR: html not found: {html_path}", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    chrome = find_chrome(args.chrome)
    if not chrome:
        print("ERROR: Chrome not found. Set CHROME_PATH or pass --chrome.", file=sys.stderr)
        return 3

    url = "file:///" + html_path.replace("\\", "/")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome, headless=True,
                                    args=["--allow-file-access-from-files"])
        context = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page = context.new_page()
        page.goto(url, wait_until="load", timeout=60000)
        try:
            page.evaluate("""async () => {
                await document.fonts.ready;
                const imgs = Array.from(document.images);
                await Promise.all(imgs.map(img => img.complete ? null :
                    new Promise(res => { img.onload = img.onerror = res; })));
            }""")
        except Exception:
            pass
        page.screenshot(path=out_path, full_page=False, animations="disabled")
        browser.close()

    size_kb = os.path.getsize(out_path) // 1024
    print(f"OK: {out_path} ({args.width * args.scale}x{args.height * args.scale}, {size_kb} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
