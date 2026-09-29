"""Render each card in og/index.html that has an id to og/<id>.png.

Run: python3 scripts/site/og_images.py [id ...]

Uses headless Chrome, which is on the machines that build this site. The PNGs
are committed, so the page build does not need Chrome, and pages point their
og:image at /og/<id>.png through og_image() below.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
GENERATOR = ROOT / "og/index.html"
CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def card_ids():
    return re.findall(r'<div class="card-wrapper" id="([a-z0-9-]+)">', GENERATOR.read_text())


def og_image(card_id):
    """The og:image path for a card, or the site-wide image if the card has
    not been rendered yet, so a page never points at a missing file."""
    if (ROOT / "og" / f"{card_id}.png").exists():
        return f"/og/{card_id}.png"
    return "/og-image.png"


def main(ids):
    chrome = next((c for c in CHROME if c and pathlib.Path(c).exists()), None)
    if not chrome:
        sys.exit("Chrome not found; the committed PNGs are left as they are.")
    for card_id in ids or card_ids():
        out = ROOT / "og" / f"{card_id}.png"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,630",
                        "--virtual-time-budget=5000", f"--screenshot={out}",
                        GENERATOR.as_uri() + f"?card={card_id}"],
                       check=True, capture_output=True)
        print(f"og/{card_id}.png written")


if __name__ == "__main__":
    main(sys.argv[1:])
