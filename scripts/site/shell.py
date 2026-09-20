"""The parts every page shares: head, navigation, footer, structured data.

One shell means a nav link added here appears on twenty pages, and a page
cannot quietly ship without a canonical or an OG image, which is how the five
older landing pages ended up thin and inconsistent.
"""

from __future__ import annotations

SITE = "https://morgenruf.dev"
INSTALL = "https://api.morgenruf.dev/install"
REPO = "https://github.com/morgenruf/morgenruf"

MARK = '<img class="mark" src="/logo-mark.png" width="34" height="34" alt="Morgenruf"/>' 

SLACK_MARK = ('<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" style="flex:0 0 17px">'
  '<path fill="#E01E5A" d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313z"/>'
  '<path fill="#36C5F0" d="M8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312z"/>'
  '<path fill="#2EB67D" d="M18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312z"/>'
  '<path fill="#ECB22E" d="M15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"/></svg>')

NAV = [
    ("Standups", "/standups"),
    ("Coffee chats", "/coffee-chats"),
    ("Kudos", "/kudos"),
    ("Set up", "/setup"),
    ("Compare", "/compare"),
    ("Docs", "https://docs.morgenruf.dev"),
]

FOOTER = [
    ("Product", [("Standups", "/standups"), ("Coffee chats", "/coffee-chats"),
                 ("Kudos", "/kudos"), ("Insights", "/insights"),
                 ("Roadmap", "/#roadmap"), ("Changelog", "/changelog")]),
    ("Set up", [("All the ways", "/setup"), ("Docker Compose", "/setup/docker"),
                ("Kubernetes and Helm", "/setup/kubernetes"), ("The Slack app", "/setup/slack-app"),
                ("Documentation", "https://docs.morgenruf.dev")]),
    ("Compare", [("All comparisons", "/compare"), ("vs Geekbot", "/geekbot-alternative"),
                 ("vs Donut", "/donut-alternative"), ("vs HeyTaco", "/heytaco-alternative"),
                 ("vs Standup & Prosper", "/standup-prosper-alternative")]),
    ("Project", [("GitHub", REPO), ("Helm charts", "https://charts.morgenruf.dev"),
                 ("Status", "https://status.morgenruf.dev"), ("Blog", "/blog"),
                 ("Support", "/support")]),
]


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
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/site.css"/>
<script src="/assets/analytics.js" defer></script>{extra_head}{blocks}
</head>
<body>
'''


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
        chats and recognition. Self-host it and keep your own data.</p>
        <p style="font-size:13.5px;color:var(--dim)">Built over a weekend at a Tim Hortons in
        Kitchener, Ontario 🇨🇦</p>
      </div>
      {cols}
    </div>
    <div class="foot-bottom">
      <span>MIT licensed. Built and maintained at <a style="color:var(--sun)" href="https://clouddrove.com">CloudDrove</a>.</span>
      <span class="foot-legal"><a href="/privacy">Privacy</a><a href="/terms">Terms</a></span>
    </div>
  </div>
</footer>
</body>
</html>
'''


def cta_band(title="Free for every seat, and that is the whole pricing page",
             body="MIT licensed, no paid tier, nothing held back from the repository. You pay for a "
                  "server and a database, which you were paying for anyway."):
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
