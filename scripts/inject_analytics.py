"""Put the analytics tag on every page, including the hand-written ones.

Generated pages get it from shell.head(). The pages that are not generated,
index.html and the blog among them, get it from here. Idempotent, so running
it after a build is safe and running it twice changes nothing.

Run: python3 scripts/inject_analytics.py
"""

from __future__ import annotations

import pathlib
import sys

POSTHOG = '<script src="/assets/analytics.js" defer></script>'
# Google Analytics 4. Must match the copy in scripts/site/shell.py.
GA4 = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-QM8RKPLDF4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
  gtag('config', 'G-QM8RKPLDF4');
</script>"""
TAGS = (POSTHOG, GA4)
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
        missing = [t for t in TAGS if t not in html]
        if not missing:
            continue
        if "</head>" not in html:
            print(f"no head, skipped: {path.relative_to(ROOT)}", file=sys.stderr)
            continue
        if missing == [GA4]:
            # Right after the PostHog tag, where shell.head() puts it.
            html = html.replace(POSTHOG, f"{POSTHOG}\n{GA4}", 1)
        else:
            html = html.replace("</head>", "\n".join(missing) + "\n</head>", 1)
        path.write_text(html)
        print(f"tagged {path.relative_to(ROOT)}")
        touched += 1
    print(f"{touched} page{'s' if touched != 1 else ''} tagged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
