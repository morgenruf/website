"""Render every generated page. Run: python3 scripts/site/build.py"""

from __future__ import annotations

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import changelog_page  # noqa: E402
import compare_pages  # noqa: E402
import legal_pages  # noqa: E402
import product_pages  # noqa: E402
import seo_pages  # noqa: E402
import setup_pages  # noqa: E402
import shell  # noqa: E402
import support_page  # noqa: E402

PAGES = {
    "setup/index.html": setup_pages.hub,
    "setup/docker/index.html": setup_pages.docker,
    "setup/kubernetes/index.html": setup_pages.kubernetes,
    "setup/slack-app/index.html": setup_pages.slack_app,
    "standups/index.html": product_pages.standups,
    "coffee-chats/index.html": product_pages.coffee_chats,
    "kudos/index.html": product_pages.kudos,
    "insights/index.html": product_pages.insights,
    "celebrations/index.html": product_pages.celebrations,
    "compare/index.html": compare_pages.hub,
    "compare/standup-bots/index.html": compare_pages.standup_bots,
    "donut-alternative/index.html": compare_pages.donut,
    "heytaco-alternative/index.html": compare_pages.heytaco,
    "support/index.html": support_page.support,
    "geekbot-alternative/index.html": seo_pages.geekbot,
    "standup-prosper-alternative/index.html": seo_pages.standup_prosper,
    "open-source-standup-bot/index.html": seo_pages.open_source,
    "self-hosted-standup-bot/index.html": seo_pages.self_hosted,
    "slack-standup-bot/index.html": seo_pages.slack_bot,
    "changelog/index.html": changelog_page.changelog,
    "privacy/index.html": legal_pages.privacy,
    "terms/index.html": legal_pages.terms,
    "blog/index.html": legal_pages.blog_index,
    "404.html": legal_pages.not_found,
}

# Written by hand, but they carry the same nav, closing band and footer as
# every generated page. Those parts are refreshed from shell.py on each build,
# so a footer link added there reaches the posts too. Everything between the
# nav and </main> is left alone.
HAND_WRITTEN = [
    "blog/why-i-built-morgenruf/index.html",
    "blog/async-standups-slack-free/index.html",
    "blog/geekbot-vs-morgenruf/index.html",
]


def refresh_assets(html):
    """Point a hand-written page at the current versions of the shared assets."""
    for path in ("/assets/site.css", "/assets/nav.js"):
        html = re.sub(re.escape(path) + r'(\?v=[0-9a-f]+)?"', shell.asset(path) + '"', html)
    return html


def refresh_chrome(html):
    html = re.sub(r'<nav class="nav">.*?</nav>\n', lambda _: shell.nav(), html, count=1, flags=re.S)
    html = re.sub(r"</main>.*\Z", lambda _: "</main>" + shell.cta_band() + shell.footer(), html,
                  count=1, flags=re.S)
    return html


def refresh_home_footer(html):
    """The homepage keeps its own nav (in-page anchors) and closing band, but
    its footer is the shared one, and its schema states the version the
    changelog says was released last. A hand-typed version went stale twice."""
    html = re.sub(r"<footer>.*?</footer>\n", lambda _: shell.footer_block(), html, count=1, flags=re.S)
    version, _ = changelog_page.latest_release()
    html = re.sub(r'"softwareVersion":"[^"]*",\n', "", html)
    if version:
        html = html.replace('"downloadUrl":', f'"softwareVersion":"{version}",\n"downloadUrl":', 1)
    return html


def refresh_webp():
    """A WebP copy beside each screenshot and the mascot, which pages offer
    first through <picture>. Made again whenever the original is newer, so a
    replaced screenshot cannot keep serving its old WebP."""
    from PIL import Image
    sources = [(p, None) for p in sorted((ROOT / "screenshots").glob("*.jpg"))]
    sources.append((ROOT / "mascot.png", 660))  # shown at most 330px wide
    for src, width in sources:
        dst = src.with_suffix(".webp")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        with Image.open(src) as im:
            if width and im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=82, method=6)
        print(f"{dst.relative_to(ROOT)!s:38s} written")


def _lastmod(rel):
    """The day this page last changed: today if it has uncommitted edits
    (the build runs before the commit), otherwise its last commit."""
    import datetime
    import subprocess
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if not dirty:
        day = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        if day:
            return day
    return datetime.date.today().isoformat()


def write_sitemap():
    """Every indexable page, with the date it last changed.

    Hand-kept, this carried one date for every URL and would have gone stale
    on the first single-page edit. The changelog also counts the date of its
    newest release, since that page changes when the app repository does."""
    rels = ["index.html"] + [r for r in PAGES if r != "404.html"] + HAND_WRITTEN
    entries = []
    for rel in rels:
        path = "/" if rel == "index.html" else "/" + rel[: -len("index.html")]
        day = _lastmod(rel)
        if rel == "changelog/index.html":
            newest = re.search(r'<time datetime="([0-9-]{10})"', (ROOT / rel).read_text())
            if newest and newest.group(1) > day:
                day = newest.group(1)
        entries.append((path, day))
    entries.sort(key=lambda e: (e[0] != "/", e[0]))
    urls = "".join(f"  <url>\n    <loc>{shell.SITE}{p}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n"
                   for p, d in entries)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml)
    print(f"{'sitemap.xml':38s} {len(entries):5d} urls")


def refresh_llms():
    """Keep the version line in llms.txt current, and write llms-full.txt:
    the main text of the product, comparison and setup pages as plain text,
    for assistants that would rather read one file than follow twenty links."""
    import html as html_lib
    version, date = changelog_page.latest_release()
    llms = ROOT / "llms.txt"
    text = llms.read_text()
    text = re.sub(r"^- Current version: .*$", f"- Current version: {version}, released {date}", text, flags=re.M)
    llms.write_text(text)

    parts = [f"# Morgenruf: the full text of the main pages\n\nGenerated from the site on each build. "
             f"Current version {version}, released {date}. Summary and index: {shell.SITE}/llms.txt\n"]
    for rel in ["standups/index.html", "coffee-chats/index.html", "kudos/index.html",
                "insights/index.html", "celebrations/index.html", "compare/index.html", "compare/standup-bots/index.html", "geekbot-alternative/index.html",
                "donut-alternative/index.html", "heytaco-alternative/index.html",
                "standup-prosper-alternative/index.html", "open-source-standup-bot/index.html",
                "self-hosted-standup-bot/index.html", "slack-standup-bot/index.html",
                "setup/index.html", "setup/docker/index.html", "setup/kubernetes/index.html",
                "setup/slack-app/index.html"]:
        page = (ROOT / rel).read_text()
        title = html_lib.unescape(re.search(r"<title>(.*?)</title>", page)[1])
        main = re.search(r"<main>(.*?)</main>", page, re.S)[1]
        main = re.sub(r"<(script|style|svg|figure)\b.*?</\1>", " ", main, flags=re.S)
        main = re.sub(r"<nav class=\"toc\".*?</nav>", " ", main, flags=re.S)
        main = " ".join(main.split())
        main = re.sub(r"</(p|h[1-6]|li|tr|pre|summary|details|div|section)>", "\n", main)
        main = re.sub(r"<[^>]+>", "", main)
        lines = [" ".join(line.split()) for line in html_lib.unescape(main).splitlines()]
        body = "\n".join(line for line in lines if line)
        url = shell.SITE + "/" + rel[: -len("index.html")]
        parts.append(f"\n## {title}\n{url}\n\n{body}\n")
    (ROOT / "llms-full.txt").write_text("".join(parts))
    print(f"{'llms.txt, llms-full.txt':38s} written")


def main():
    refresh_webp()
    for rel, render in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = render()
        out.write_text(html)
        print(f"{rel:38s} {len(html.split()):5d} words")
    for rel in HAND_WRITTEN:
        path = ROOT / rel
        before = path.read_text()
        after = refresh_assets(refresh_chrome(before))
        if after != before:
            path.write_text(after)
        print(f"{rel:38s} chrome {'refreshed' if after != before else 'unchanged'}")
    home = ROOT / "index.html"
    before = home.read_text()
    after = refresh_assets(refresh_home_footer(before))
    if after != before:
        home.write_text(after)
    print(f"{'index.html':38s} shared parts {'refreshed' if after != before else 'unchanged'}")
    refresh_llms()
    write_sitemap()


if __name__ == "__main__":
    main()
