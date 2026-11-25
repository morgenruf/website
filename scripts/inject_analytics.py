"""Put the analytics tag on every page, including the hand-written ones.

Generated pages get it from shell.head(). The pages that are not generated,
index.html and the blog among them, get it from here. Idempotent, so running
it after a build is safe and running it twice changes nothing.

Run: python3 scripts/inject_analytics.py
"""

from __future__ import annotations

import pathlib
import re
import sys

POSTHOG = '<script src="/assets/analytics.js" defer></script>'
# Google Analytics 4 and Microsoft Clarity, both consent gated. Must match
# the copy in scripts/site/shell.py.
GA4 = """<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
  try { if (localStorage.getItem('mr-consent') === 'accept') gtag('consent', 'update', { analytics_storage: 'granted' }); } catch (e) {}
  gtag('js', new Date());
  gtag('config', 'G-QM8RKPLDF4');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QM8RKPLDF4"></script>
<script>
  (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","zixuihjr17");
  var mrOk = false; try { mrOk = localStorage.getItem('mr-consent') === 'accept'; } catch (e) {}
  clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: mrOk ? 'granted' : 'denied' });
</script>"""
TAGS = (POSTHOG, GA4)
# Any earlier version of the GA4 block, so a changed snippet replaces the old
# one instead of landing next to it.
OLD_GA4 = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-QM8RKPLDF4"></script>\n<script>.*?</script>'
    r'|<script>\n  window\.dataLayer.*?</script>\n<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-QM8RKPLDF4"></script>\n<script>.*?</script>',
    re.S)
ROOT = pathlib.Path(__file__).resolve().parent.parent
# scripts/ holds the generators and their content fragments, .netlify the build
# plugins, og/ the internal page the share cards are drawn from. None is a
# page anyone loads.
SKIP = {"node_modules", ".git", ".netlify", "scripts", "og"}


def main() -> int:
    touched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP & set(path.parts):
            continue
        html = path.read_text()
        if GA4 not in html:
            html = OLD_GA4.sub(lambda _: GA4, html, count=1)
        missing = [t for t in TAGS if t not in html]
        if not missing:
            if html != path.read_text():
                path.write_text(html)
                print(f"updated {path.relative_to(ROOT)}")
                touched += 1
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
