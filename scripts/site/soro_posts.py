"""Soro posts as pages of their own, at /blog/<slug>/.

Soro's embed used to draw each post into /blog/ in the browser, at
/blog/?post=<slug>. Search engines saw one page for all of them. The build
now reads the same public data the embed reads and writes a static page per
post. The ?post= URLs redirect here (netlify.toml).

The fetched posts are kept in content/soro_posts.json, so a build without
network, or with Soro down, still writes every page. A post only reaches the
site when the build runs again: there is no scheduled rebuild.

Everything from Soro is data. Post HTML goes through an allowlist: known tags,
no attributes except a checked href.
"""

from __future__ import annotations

import datetime
import hashlib
import html as html_lib
import io
import json
import pathlib
import re
import urllib.request
from html.parser import HTMLParser

from shell import SITE

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SNAPSHOT = HERE / "content" / "soro_posts.json"
TOKEN = "8bb533f4-55ea-4c1e-b09a-843dcf0f3f55"
API = "https://app.trysoro.com/api/embed/" + TOKEN
UA = {"User-Agent": "morgenruf-site-build"}

ALLOWED = {"p", "h2", "h3", "h4", "ul", "ol", "li", "a", "strong", "em", "b", "i", "blockquote",
           "code", "pre", "br", "hr", "table", "thead", "tbody", "tr", "th", "td"}
VOID = {"br", "hr"}
POST_LINK = re.compile(r"^https://(?:www\.)?morgenruf\.dev/blog/?(?:index\.html)?\?post=([a-z0-9-]+)$")


class _Clean(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe"):
            self.skip += 1
        if self.skip:
            return
        tag = {"h1": "h2"}.get(tag, tag)  # the page has its own H1
        if tag not in ALLOWED:
            return
        if tag == "a":
            href = _href(dict(attrs).get("href") or "")
            self.out.append(f'<a href="{html_lib.escape(href)}">' if href else "<a>")
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe"):
            self.skip = max(0, self.skip - 1)
            return
        tag = {"h1": "h2"}.get(tag, tag)
        if not self.skip and tag in ALLOWED and tag not in VOID:
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html_lib.escape(data, quote=False))


def _href(href):
    """Links to other posts point at their new pages, links on this site
    become root-relative, and anything that is not http(s) is dropped."""
    href = href.strip()
    m = POST_LINK.match(href)
    if m:
        return f"/blog/{m.group(1)}/"
    if re.match(r"^https://(?:www\.)?morgenruf\.dev/", href):
        return re.sub(r"^https://(?:www\.)?morgenruf\.dev", "", href)
    return href if re.match(r"^(https?://|/)", href) else ""


def clean(content):
    p = _Clean()
    p.feed(content or "")
    p.close()
    return "".join(p.out).strip()


def describe(text, low=140, high=158):
    """The excerpt as a meta description: whole if it fits, else cut at the
    last sentence end that keeps it in range, else at a word."""
    text = " ".join(text.split())
    if len(text) <= high:
        return text
    ends = [m.end() for m in re.finditer(r"[.!?](?=\s)", text[: high + 1])]
    fits = [e for e in ends if low <= e <= high]
    if fits:
        return text[: fits[-1]]
    cut = text[: high].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "."


def short_title(title, limit=60):
    if len(title) <= limit:
        return title
    return title[: limit].rsplit(" ", 1)[0].rstrip(",;:")


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return r.read()


def _image_size(url):
    from PIL import Image
    with Image.open(io.BytesIO(_get(url))) as im:
        return im.size


def refresh():
    """Read the post list and each post from Soro and update the snapshot.
    A post whose text changed since the last snapshot gets today as its
    modified date; a new one starts with its publish date."""
    old = {p["slug"]: p for p in load()}
    try:
        js = _get(API).decode()
        found = re.search(r"var SORO_ARTICLES = (\[.*?\]);\n", js, re.S)
        listed = json.loads(found.group(1))
        posts = []
        for a in listed:
            if not re.fullmatch(r"[a-z0-9-]+", a.get("slug", "")):
                continue
            body = clean(json.loads(_get(f"{API}/article/{a['id']}"))["content"])
            digest = hashlib.sha256((a["title"] + a["excerpt"] + body).encode()).hexdigest()
            prev = old.get(a["slug"], {})
            published = a["isoDate"][:10]
            if prev.get("hash") == digest:
                modified = prev["modified"]
            else:
                modified = datetime.date.today().isoformat() if prev else published
            image = a.get("image") or ""
            if image and not image.startswith("https://"):
                image = ""
            size = prev.get("image_size") if prev.get("image") == image else None
            if image and not size:
                size = list(_image_size(image))
            posts.append({"slug": a["slug"], "title": a["title"], "excerpt": a["excerpt"],
                          "published": published, "modified": modified, "image": image,
                          "image_size": size, "hash": digest, "body": body})
    except Exception as exc:  # Soro down or changed shape: keep the last good copy
        print(f"{'soro posts':38s} fetch failed ({exc}), using the snapshot")
        return
    posts.sort(key=lambda p: p["published"], reverse=True)
    SNAPSHOT.write_text(json.dumps(posts, indent=1, ensure_ascii=False) + "\n")
    print(f"{'soro posts':38s} {len(posts):5d} fetched")


# One closing call to action per post, matched to its topic (owner decision
# 2026-11-25, every post ends with one). Kept here rather than in Soro so a
# refresh of the post text from Soro does not drop it.
GITHUB = "https://github.com/morgenruf/morgenruf"
CTA = {
    "granular-admin-permissions":
        "Morgenruf is open source under the MIT license, so your security team can read the source before you add it to your workspace:",
    "google-chat-standups":
        "Morgenruf is a free, open-source standup bot for Slack that also supports Google Chat for some of its features, so trying it with one team costs nothing:",
    "zoom-coffee-chat-scheduling":
        "Morgenruf pairs people on a cadence, avoids repeat matches and can add a Zoom link to each pair, free and open source:",
    "cross-team-employee-introductions":
        "Morgenruf runs these introductions as coffee chats in Slack, pairing people on a cadence and avoiding repeat matches, with no seat limit:",
    "random-coffee-chat-pairing":
        "To start a modest cadence without a per-seat bill, Morgenruf pairs people in Slack and avoids repeat matches, free and open source:",
    "time-zone-friendly-team-check-ins":
        "Morgenruf sends each person the standup questions by Slack DM at their own local time and posts one summary to the channel, free and open source:",
    "automated-slack-standup-summaries":
        "Morgenruf collects standup answers by Slack DM and posts the summary to a channel with blockers called out, with no per-seat pricing:",
    "how-to-replace-daily-standups":
        "When you are ready to cancel the recurring meeting, Morgenruf runs the async standup in Slack for free, on the hosted instance or on your own servers:",
    "free-slack-standup-bot":
        "Morgenruf is a free Slack standup bot with no paid tier and no seat limit, and it works on the free Slack plan:",
}


def cta(slug):
    if slug not in CTA:
        return ""
    return f'<p>{html_lib.escape(CTA[slug], quote=False)} <a href="{GITHUB}">Quick start on GitHub</a>.</p>\n'


def load():
    return json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else []


def _people():
    """Author and publisher, as the hand-written posts state them."""
    page = (ROOT / "blog/standup-questions/index.html").read_text()
    found = re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org",'
                      r'"@type":"BlogPosting".*?)</script>', page, re.S)
    post = json.loads(found.group(1))
    return post["author"], post["publisher"]


def render(post):
    from legal_pages import _page  # imported late: legal_pages imports this module

    path = f"/blog/{post['slug']}/"
    title = html_lib.escape(short_title(post["title"]))
    description = html_lib.escape(describe(post["excerpt"]))
    author, publisher = _people()
    schema = {"@context": "https://schema.org", "@type": "BlogPosting",
              "headline": post["title"], "description": describe(post["excerpt"]),
              "url": SITE + path, "mainEntityOfPage": SITE + path,
              "datePublished": post["published"], "dateModified": post["modified"],
              "author": author, "publisher": publisher, "inLanguage": "en"}
    if post["image"]:
        schema["image"] = post["image"]
    day = datetime.date.fromisoformat(post["published"])
    img = ""
    if post["image"]:
        w, h = post["image_size"]
        img = (f'<p><img src="{html_lib.escape(post["image"])}" alt="" width="{w}" height="{h}" '
               f'style="width:100%;height:auto;border-radius:12px"/></p>\n')
    prose = (f'<p class="byline">By <strong>Anmol Nagpal</strong>, creator of Morgenruf &middot; '
             f'<time datetime="{post["published"]}">{day:%B} {day.day}, {day.year}</time></p>\n'
             f'{img}{post["body"]}\n'
             f'{cta(post["slug"])}'
             f'<p><a href="/blog/">More posts on the Morgenruf blog</a></p>')
    page = _page(path=path, title=title, description=description, h1=html_lib.escape(post["title"]),
                 lede=html_lib.escape(post["excerpt"]), prose=prose,
                 trail=[("Home", "/"), ("Blog", "/blog/"), (title, None)],
                 schema=[json.dumps(schema, separators=(",", ":"), ensure_ascii=False)
                         .replace("</", "<\\/")])
    page = page.replace('<meta property="og:type" content="website"/>',
                        '<meta property="og:type" content="article"/>', 1)
    if post["image"]:
        page = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*"',
                      lambda m: m.group(1) + html_lib.escape(post["image"]) + '"', page)
    return page


def pages():
    return {f"blog/{p['slug']}/index.html": (lambda p=p: render(p)) for p in load()}


if __name__ == "__main__":
    assert describe("a" * 150) == "a" * 150
    long = "First sentence is here and runs on for quite a while to pass the low bound of the range. " \
           "Second sentence keeps going so the whole thing is longer than one hundred fifty eight chars."
    d = describe(long)
    assert 140 <= len(d) <= 158 or d.endswith("."), d
    assert clean('<h1 onclick="x">T</h1><script>bad()</script><a href="javascript:x">l</a>'
                 '<a href="https://morgenruf.dev/blog/?post=foo-bar">p</a>') == \
        '<h2>T</h2><a>l</a><a href="/blog/foo-bar/">p</a>'
    print("ok")
