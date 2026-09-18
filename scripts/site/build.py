"""Render every generated page. Run: python3 scripts/site/build.py"""

from __future__ import annotations

import pathlib
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


def main():
    for rel, render in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = render()
        out.write_text(html)
        print(f"{rel:38s} {len(html.split()):5d} words")


if __name__ == "__main__":
    main()
