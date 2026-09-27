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
    "compare/index.html": compare_pages.hub,
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


def refresh_chrome(html):
    html = re.sub(r'<nav class="nav">.*?</nav>\n', lambda _: shell.nav(), html, count=1, flags=re.S)
    html = re.sub(r"</main>.*\Z", lambda _: "</main>" + shell.cta_band() + shell.footer(), html,
                  count=1, flags=re.S)
    return html


def refresh_home_footer(html):
    """The homepage keeps its own nav (in-page anchors) and closing band, but
    its footer is the shared one."""
    return re.sub(r"<footer>.*?</footer>\n", lambda _: shell.footer_block(), html, count=1, flags=re.S)


def main():
    for rel, render in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = render()
        out.write_text(html)
        print(f"{rel:38s} {len(html.split()):5d} words")
    for rel in HAND_WRITTEN:
        path = ROOT / rel
        before = path.read_text()
        after = refresh_chrome(before)
        if after != before:
            path.write_text(after)
        print(f"{rel:38s} chrome {'refreshed' if after != before else 'unchanged'}")
    home = ROOT / "index.html"
    before = home.read_text()
    after = refresh_home_footer(before)
    if after != before:
        home.write_text(after)
    print(f"{'index.html':38s} footer {'refreshed' if after != before else 'unchanged'}")


if __name__ == "__main__":
    main()
