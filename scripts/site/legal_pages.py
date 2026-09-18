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
    """
    return (pathlib.Path(__file__).resolve().parent / "content" / name).read_text().strip()


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
                 title="Privacy — what Morgenruf stores and what it never sends",
                 description="What Morgenruf stores, what leaves your infrastructure (almost "
                             "nothing), and what self-hosting means for your team's standup data.",
                 h1="Privacy",
                 lede="Short version: self-hosted, your database, no telemetry. The longer version "
                      "is below, including the two optional services that do make outbound calls.",
                 prose=_extract("privacy.html"),
                 trail=[("Home", "/"), ("Privacy", None)])


def terms():
    return _page(path="/terms",
                 title="Terms — morgenruf.dev and the hosted demo",
                 description="Terms covering this website and the hosted demo. The software itself "
                             "is MIT licensed and yours to run.",
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
    return _page(path="/404", title="Page not found — Morgenruf",
                 description="That page does not exist. Morgenruf is an open-source, self-hosted "
                             "Slack app for standups, coffee chats and kudos.",
                 h1="That page does not exist",
                 lede="Here is where most people are heading.",
                 prose=prose, trail=[("Home", "/"), ("Not found", None)], noindex=True)


POSTS = [
    ("/blog/why-i-built-morgenruf", "Why I built a free Geekbot alternative",
     "What was annoying enough about per-seat standup pricing to spend a weekend on it."),
    ("/blog/async-standups-slack-free", "Async standups in Slack, for free",
     "How to run a daily standup that people actually fill in, without paying per person."),
    ("/blog/geekbot-vs-morgenruf", "Geekbot and Morgenruf, compared honestly",
     "Where the hosted product is the better answer, and where self-hosting wins."),
]


def blog_index():
    cards = "".join(
        f'<a class="tile" href="{href}"><h3>{title}</h3><p>{blurb}</p>'
        f'<span class="go">Read →</span></a>' for href, title, blurb in POSTS)
    prose = f'''<div class="tiles" style="margin-bottom:34px">{cards}</div>
<p>Occasional writing about running team rituals without a per-seat subscription, and about the
parts of building this that turned out to be harder than expected. New posts are announced in
<a href="{REPO}/discussions">discussions</a>.</p>'''
    return _page(path="/blog", title="Blog — async standups, self-hosting and team rituals",
                 description="Writing about async standups, self-hosting Slack tools, and building "
                             "an open-source alternative to per-seat team software.",
                 h1="Writing",
                 lede="On async standups, self-hosting, and what building the alternative actually "
                      "involves.",
                 prose=prose, trail=[("Home", "/"), ("Blog", None)])
