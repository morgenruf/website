"""Privacy, terms, 404 and the blog index, on the same shell as everything else.

Their content was fine. Their stylesheet was a different website.
"""

from __future__ import annotations

import pathlib
import re

from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, footer, head, nav

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def _extract(name):
    """The prose for a legal page, kept beside the generator.

    This used to read the old hand-written page and strip its chrome, which
    worked exactly once: the build then deleted that file and could never run
    again. The copy lives in content/ now.

    The stored copy is still a whole HTML document, head and all. Returning it
    whole put a second <title>, a second meta description and a second
    canonical inside the body of the built page, so only the body comes back,
    without the back-link that the real nav and breadcrumbs already provide.
    """
    raw = (pathlib.Path(__file__).resolve().parent / "content" / name).read_text()
    body = re.search(r"<body[^>]*>(.*)</body>", raw, re.S)
    inner = body[1] if body else raw
    inner = re.sub(r'\s*<a href="/">[^<]*morgenruf\.dev</a>\s*', "\n", inner, count=1)
    return inner.strip()


def _page(*, path, title, description, h1, lede, prose, trail, noindex=False):
    crumb_html, crumb_schema = breadcrumbs(trail)
    extra = '\n<meta name="robots" content="noindex, follow"/>' if noindex else ""
    html = head(title=title, description=description, path=path,
                schema=[crumb_schema] if crumb_schema else [], extra_head=extra)
    if noindex:
        html = html.replace('<meta name="robots" content="index, follow"/>', "")
    return (html + nav() + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></header>
<section class="section"><div class="wrap"><div class="prose">{prose}</div></div></section>
</main>''' + footer())


def privacy():
    return _page(path="/privacy",
                 title="Privacy: what Morgenruf stores and what it never sends",
                 description="What Morgenruf stores, what leaves your infrastructure (almost "
                             "nothing), the two optional services that do make outbound calls, and "
                             "the sub-processors involved.",
                 h1="Privacy",
                 lede="Short version: self-hosted, your database, no telemetry. The longer version "
                      "is below, including the two optional services that do make outbound calls.",
                 prose=_extract("privacy.html"),
                 trail=[("Home", "/"), ("Privacy", None)])


def terms():
    return _page(path="/terms",
                 title="Terms: morgenruf.dev and the hosted demo",
                 description="Terms covering this website and the hosted demo, including what the "
                             "demo is for and what it is not. The software itself is MIT licensed "
                             "and yours to run.",
                 h1="Terms",
                 lede="These cover this website and the hosted demo. The software is MIT licensed, "
                      "and running it yourself is governed by that licence, not by this page.",
                 prose=_extract("terms.html"),
                 trail=[("Home", "/"), ("Terms", None)])


def not_found():
    prose = f'''<p>The page you were after is not here. It may have moved when the site was
rebuilt, or the link may have been wrong to begin with.</p>
<h2 id="the-useful-links">Where you were probably going</h2>
<div class="tiles" style="margin:24px 0">
  <a class="tile" href="/setup"><h3>Set it up</h3><p>Docker, Kubernetes and the Slack app, in about
  twenty minutes.</p><span class="go">Start here →</span></a>
  <a class="tile" href="/standups"><h3>Standups</h3><p>What the daily check-in does and how it
  behaves.</p><span class="go">Read →</span></a>
  <a class="tile" href="/support"><h3>Help</h3><p>Issues, discussions and commercial support.</p>
  <span class="go">Get help →</span></a>
</div>
<p>If a link on this site brought you here, that is a bug:
<a href="{REPO}/issues/new/choose">please report it</a>.</p>'''
    return _page(path="/404", title="Page not found on morgenruf.dev",
                 description="That page does not exist, so here are the ones people are usually "
                             "looking for. Morgenruf is an open-source, self-hosted Slack app for "
                             "standups and kudos.",
                 h1="That page does not exist",
                 lede="Here is where most people are heading.",
                 prose=prose, trail=[("Home", "/"), ("Not found", None)], noindex=True)


POSTS = [
    ("/blog/why-i-built-morgenruf", "Why I built a free Geekbot alternative",
     "A Saturday at a Tim Hortons in Kitchener, a monthly SaaS bill, and one line on it: $2.50 per "
     "person per month for a bot that DMs three questions and pastes the answers into a channel. "
     "The post works through how small the core loop really is, what the weekend produced, and "
     "which features went in afterwards because they cost nothing once the foundation existed: "
     "mood tracking, webhooks, CSV export and an MCP server."),
    ("/blog/async-standups-slack-free", "Async standups in Slack, for free",
     "The arithmetic first: a quarter hour a day is 75 minutes a week per person, and 12.5 hours a "
     "week for a team of ten, most of it spent listening. Then what replaces it. A scheduled DM, "
     "short written answers, one summary in a channel, and the five steps to get there. It ends on "
     "the per-seat maths, which is where the case for async stops being about meetings."),
    ("/blog/geekbot-vs-morgenruf", "Geekbot and Morgenruf, compared honestly",
     "A feature table, then the section that matters: where Geekbot wins. Zero operations, a Slack "
     "App Directory listing your IT admin already knows how to approve, years of edge cases, and a "
     "funded team behind it. After that, the parts self-hosting wins, and a straight answer on who "
     "should choose which. If you only read one of these before switching, read this one."),
]


def blog_index():
    cards = "".join(
        f'<a class="tile" href="{href}"><h3>{title}</h3><p>{blurb}</p>'
        f'<span class="go">Read the post →</span></a>' for href, title, blurb in POSTS)
    prose = f'''<p>Three posts so far. They get written when something is concrete enough to be
worth a stranger's time: a decision with a number behind it, a cost that turned out to be real, or
a comparison that is easier to make in long form than in a table. Nothing here is on a schedule,
which is why there are three of them and not thirty.</p>

<h2 id="the-posts">The posts</h2>
<div class="tiles" style="margin:24px 0 8px">{cards}</div>

<h2 id="what-gets-written">What gets written here, and what does not</h2>
<p>The subjects are the ones this project keeps running into: async standups and whether they
actually replace the meeting, what self-hosting a small Slack app costs in money and in evenings,
and the parts of building an alternative to per-seat software that turned out harder than expected.
Where a post compares Morgenruf with something people pay for, it says where the paid tool wins,
for the same reason the <a href="/compare">comparison pages</a> do: a page that claims the
competitor is bad at everything convinces nobody.</p>
<p>What you will not find is a list of the ten best standup bots of the year, a post written to
hold a keyword, or an announcement dressed as an essay. Releases go in the
<a href="/changelog">changelog</a>, and how each part of the app behaves is documented on the
<a href="/standups">standups</a>, <a href="/coffee-chats">coffee chats</a> and
<a href="/kudos">kudos</a> pages rather than being rewritten here.</p>
<p>New posts are announced in <a href="{REPO}/discussions">GitHub discussions</a>, which is also
where to say that one of them is wrong.</p>'''
    return _page(path="/blog", title="Blog: async standups, self-hosting and team rituals",
                 description="Writing about async standups, self-hosting Slack tools and building "
                             "an open-source alternative to per-seat team software. Three posts so "
                             "far, no listicles.",
                 h1="Writing",
                 lede="On async standups, self-hosting, and what building the alternative actually "
                      "involves.",
                 prose=prose, trail=[("Home", "/"), ("Blog", None)])
