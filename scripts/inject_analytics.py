"""Put the analytics tag on every page, including the hand-written ones.

Generated pages get it from shell.head(). The pages that are not generated,
index.html and the blog among them, get it from here. Idempotent, so running
it after a build is safe and running it twice changes nothing.

Run: python3 scripts/inject_analytics.py
"""

from __future__ import annotations

import pathlib
import sys

TAG = '<script src="/assets/analytics.js" defer></script>'
ROOT = pathlib.Path(__file__).resolve().parent.parent
# scripts/ holds the generators and their content fragments, .netlify the build
# plugins. Neither is a page anyone loads.
SKIP = {"node_modules", ".git", ".netlify", "scripts"}


def main() -> int:
    touched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP & set(path.parts):
            continue
        html = path.read_text()
        if TAG in html:
            continue
        if "</head>" not in html:
            print(f"no head, skipped: {path.relative_to(ROOT)}", file=sys.stderr)
            continue
        path.write_text(html.replace("</head>", f"{TAG}\n</head>", 1))
        print(f"tagged {path.relative_to(ROOT)}")
        touched += 1
    print(f"{touched} page{'s' if touched != 1 else ''} tagged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
