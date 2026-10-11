"""The parts every page shares: head, navigation, footer, structured data.

One shell means a nav link added here appears on twenty pages, and a page
cannot quietly ship without a canonical or an OG image, which is how the five
older landing pages ended up thin and inconsistent.
"""

from __future__ import annotations

import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://morgenruf.dev"
INSTALL = "https://api.morgenruf.dev/install"
REPO = "https://github.com/morgenruf/morgenruf"

MARK = '<img class="mark" src="/logo-mark-68.png" width="34" height="34" alt="Morgenruf"/>' 

SLACK_MARK = ('<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" style="flex:0 0 17px">'
  '<path fill="#E01E5A" d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313z"/>'
  '<path fill="#36C5F0" d="M8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312z"/>'
  '<path fill="#2EB67D" d="M18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312z"/>'
  '<path fill="#ECB22E" d="M15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"/></svg>')

NAV = [
    ("Standups", "/standups/"),
    ("Coffee chats", "/coffee-chats/"),
    ("Kudos", "/kudos/"),
    ("Celebrations", "/celebrations/"),
    ("Set up", "/setup/"),
    ("Compare", "/compare/"),
    ("Docs", "https://docs.morgenruf.dev"),
]

FOOTER = [
    ("Product", [("Standups", "/standups/"), ("Coffee chats", "/coffee-chats/"),
                 ("Kudos", "/kudos/"), ("Celebrations", "/celebrations/"),
                 ("Insights", "/insights/"),
                 ("Roadmap", "/#roadmap"), ("Changelog", "/changelog/")]),
    ("Set up", [("All the ways", "/setup/"), ("Docker Compose", "/setup/docker/"),
                ("Kubernetes and Helm", "/setup/kubernetes/"), ("The Slack app", "/setup/slack-app/"),
                ("Documentation", "https://docs.morgenruf.dev")]),
    ("Compare", [("All comparisons", "/compare/"), ("Standup bots compared", "/compare/standup-bots/"),
                 ("vs Geekbot", "/geekbot-alternative/"),
                 ("vs Donut", "/donut-alternative/"), ("vs HeyTaco", "/heytaco-alternative/"),
                 ("vs Standup &amp; Prosper", "/standup-prosper-alternative/"),
                 ("vs DailyBot", "/dailybot-alternative/"), ("vs Standuply", "/standuply-alternative/"),
                 ("Open-source standup bot", "/open-source-standup-bot/"),
                 ("Self-hosted standup bot", "/self-hosted-standup-bot/"),
                 ("Slack standup bot", "/slack-standup-bot/")]),
    ("Project", [("GitHub", REPO), ("Helm charts", "https://charts.morgenruf.dev"),
                 ("Status", "https://status.morgenruf.dev"), ("Blog", "/blog/"),
                 ("Support", "/support/"),
                 ("LinkedIn", "https://www.linkedin.com/company/morgenruf"),
                 ("X", "https://x.com/morgenruf_dev")]),
]


# The day the comparison and product pages were last checked against the
# product and the competitors' public pages. Shown on the page and in schema.
REVIEWED = "2026-09-26"
REVIEWED_TEXT = "September 26, 2026"

CTA_NOTE = ('<p class="cta-note">Add to Slack installs Morgenruf on the free hosted instance '
            'CloudDrove runs. Self-hosting is the same MIT code.</p>')


def webpage_schema(path, title, reviewed=None):
    """A WebPage node with the review date, pointing at the product entity
    the homepage declares."""
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": SITE + path,
                       "name": title, "dateModified": reviewed or REVIEWED,
                       "about": {"@id": SITE + "/#software"},
                       "publisher": {"@id": SITE + "/#organization"}})


def definition(text, reviewed=None):
    """One self-contained sentence or three that names the product, so a
    passage lifted out of the page still says what it is about."""
    import datetime
    when = (datetime.date.fromisoformat(reviewed).strftime("%B %-d, %Y") if reviewed
            else REVIEWED_TEXT)
    return (f'<section class="section define"><div class="wrap">'
            f'<p class="lede">{text}</p>'
            f'<p class="reviewed">Last reviewed {when}</p></div></section>\n')


def asset(path):
    """A static asset URL carrying a hash of its contents.

    /assets/* is served with a year-long immutable cache, so an edited
    site.css under the same URL would never reach a returning visitor. The
    query string changes whenever the file does."""
    digest = hashlib.sha256((ROOT / path.lstrip("/")).read_bytes()).hexdigest()[:10]
    return f"{path}?v={digest}"


def head(*, title, description, path, og_image="/og-image.png", schema=None, extra_head=""):
    url = SITE + path
    blocks = "".join(f'\n<script type="application/ld+json">{s}</script>' for s in (schema or []))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{description}"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{url}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:image" content="{SITE}{og_image}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{description}"/>
<meta name="twitter:image" content="{SITE}{og_image}"/>
<meta name="theme-color" content="#12131f"/>
<link rel="icon" type="image/png" sizes="512x512" href="/icon-512.png"/>
<link rel="icon" type="image/x-icon" href="/favicon.ico"/>
<link rel="apple-touch-icon" href="/icon-512.png"/>
<link rel="preload" href="/assets/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin/>
<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin/>
<link rel="stylesheet" href="{asset("/assets/site.css")}"/>
<script src="/assets/analytics.js" defer></script>
<script src="{asset("/assets/nav.js")}" defer></script>{extra_head}{blocks}
</head>
<body>
'''


def nav_menu(links):
    """The links the desktop bar shows, for screens too narrow to show them.

    A details element opens and closes without any script, so the menu works
    even if nav.js never loads; the script only closes it after a tap.
    """
    return f'''<details class="nav-menu">
      <summary aria-label="Menu"><span class="burger" aria-hidden="true"></span></summary>
      <div class="nav-menu-panel">{links}<a href="{REPO}">GitHub</a></div>
    </details>'''


def nav(current=""):
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == current else ""}>{label}</a>'
        for label, href in NAV)
    return f'''<nav class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="/">{MARK} morgenruf</a>
    <div class="nav-links">{links}</div>
    <div class="nav-cta">
      <a class="btn btn-ghost btn-sm" href="{REPO}">GitHub</a>
      <a class="btn btn-sun btn-sm" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
    </div>
    {nav_menu(links)}
  </div>
</nav>
'''


def breadcrumbs(trail):
    """Visible trail plus the schema, which is what shows under a search result."""
    if not trail:
        return "", None
    crumbs = " ".join(
        f'<a href="{href}">{label}</a><span aria-hidden="true">›</span>' if href else f'<span>{label}</span>'
        for label, href in trail)
    items = ",".join(
        '{"@type":"ListItem","position":%d,"name":"%s"%s}' % (
            i + 1, label, f',"item":"{SITE}{href}"' if href else "")
        for i, (label, href) in enumerate(trail))
    schema = '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}' % items
    return f'<div class="crumbs wrap">{crumbs}</div>', schema


def footer():
    return footer_block() + "</body>\n</html>\n"


def footer_block():
    """The footer element alone, for the hand-written homepage, which has
    schema after it and so cannot take the closing tags as well."""
    cols = ""
    for heading, links in FOOTER:
        rows = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
        cols += f'<div><h3>{heading}</h3>{rows}</div>'
    return f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/" style="margin-bottom:12px">{MARK} morgenruf</a>
        <p style="max-width:34ch;font-size:14.5px">One open-source Slack app for standups, coffee
        chats and recognition. Free on the hosted instance, or self-host it and keep your own
        data.</p>
        <p style="font-size:13.5px;color:var(--dim)">Built over a weekend at a Tim Hortons in
        Kitchener, Ontario 🇨🇦</p>
      </div>
      {cols}
    </div>
    <div class="foot-bottom">
      <span>MIT licensed. Built by Anmol Nagpal, sponsored by <a style="color:var(--sun)" href="https://clouddrove.com">CloudDrove</a>.</span>
      <span class="foot-legal"><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></span>
    </div>
  </div>
</footer>
'''


def cta_band(title="Free for every seat, and that is the whole pricing page",
             body="Add to Slack puts Morgenruf on the free hosted instance CloudDrove runs, in about "
                  "two minutes. Or self-host the same MIT code with Docker Compose or Helm and pay "
                  "only for the server."):
    return f'''<section class="section">
  <div class="wrap">
    <div class="band">
      <h2>{title}</h2>
      <p class="lede">{body}</p>
      <div class="band-cta">
        <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
        <a class="btn btn-ghost" href="{REPO}">Read the source</a>
      </div>
    </div>
  </div>
</section>
'''


def faq(pairs):
    """Rendered questions and the FAQPage schema from one list, so they agree."""
    html = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(pairs))
    import json
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs],
    })
    return html, schema
