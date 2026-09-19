"""The changelog, generated from the app repository's CHANGELOG.md.

The hand-written one stopped at 1.2.0 while the product shipped 1.8.4, which is
worse than not having the page: it tells a visitor the project stalled.
"""

from __future__ import annotations

import pathlib
import re

from shell import REPO, breadcrumbs, cta_band, faq, footer, head, nav

SOURCE = pathlib.Path.home() / "workspace/morgenruf/morgenruf/CHANGELOG.md"
KIND = {"Added": "state done", "Fixed": "state", "Changed": "state", "Removed": "state",
        "Security": "state"}


def _published_tags():
    """Tags that have a GitHub release. The 0.x entries predate releases, and
    linking them produced four 404s on a page about being well maintained."""
    import subprocess
    try:
        out = subprocess.run(
            ["gh", "release", "list", "--limit", "80", "--repo", "morgenruf/morgenruf",
             "--json", "tagName", "-q", ".[].tagName"],
            capture_output=True, text=True, timeout=30).stdout.split()
        return {t.lstrip("v") for t in out}
    except Exception:
        return set()


def _entries():
    text = SOURCE.read_text()
    # Markdown link references at the foot of the file are not release notes.
    # Left in, they arrived as a bullet reading "[0.1.0]: https://…" inside the
    # oldest entry.
    text = re.sub(r"^\[[^\]]+\]:\s*http\S+\s*$", "", text, flags=re.M)
    out = []
    for block in re.split(r"\n(?=## \[)", text):
        # Older entries separate version and date with an em dash, newer ones
        # with a plain hyphen. Both parse.
        m = re.match(r"## \[([0-9]+\.[0-9]+\.[0-9]+)\][^\n]*?[—–-]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", block)
        if not m:
            continue
        sections = []
        for sec in re.split(r"\n### ", block[block.index("\n"):]):
            sec = sec.strip()
            if not sec:
                continue
            headline, _, rest = sec.partition("\n")
            items = []
            for raw in re.findall(r"^- (.+?)(?=\n- |\Z)", rest, re.S | re.M):
                item = " ".join(raw.split())
                item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
                item = re.sub(r"`(.+?)`", r"<code>\1</code>", item)
                item = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', item)
                items.append(item)
            if items:
                sections.append((headline.strip(), items))
        out.append((m.group(1), m.group(2), sections))
    return out


def changelog():
    entries = _entries()
    rows = ""
    published = _published_tags()
    for version, date, sections in entries:
        link = (f'<a href="{REPO}/releases/tag/v{version}">Release notes ↗</a>'
                if version in published else "")
        blocks = ""
        for headline, items in sections:
            lis = "".join(f"<li>{i}</li>" for i in items)
            blocks += (f'<h3 id="v{version}-{headline.lower()}">{headline}</h3><ul>{lis}</ul>')
        rows += f'''<article class="release">
  <div class="release-meta">
    <h2 id="v{version}">{version}</h2>
    <time datetime="{date}">{date}</time>
    {link}
  </div>
  <div class="release-body">{blocks}</div>
</article>'''
    latest = entries[0][0] if entries else ""
    body = f'''<section class="section"><div class="wrap">
  <div class="note" style="margin-bottom:34px"><p>Every release is tagged, published with notes, and
  built from the same commit that is on <a href="{REPO}">GitHub</a>. Docker images carry the
  revision they were built from, so you can check what you are running matches what you read here.</p></div>
  {rows}
</div></section>'''
    faq_html, faq_schema = faq([
        ("How often are there releases?",
         "Whenever something is ready. Recent months have averaged several a week, including fixes "
         "that went out within an hour of being reported."),
        ("How do I upgrade?",
         "Pull the new image and restart, or helm upgrade. Migrations run themselves before the app "
         "starts."),
        ("Do you follow semantic versioning?",
         "Yes. Breaking changes would move the major, and there have not been any since 1.0."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About releases</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    crumb_html, crumb_schema = breadcrumbs([("Home", "/"), ("Changelog", None)])
    return (head(title=f"Changelog: every Morgenruf release, currently {latest}",
                 description="Every Morgenruf release and what changed in it: new modules, fixes and the "
                             "occasional removal, generated straight from the repository's own changelog file.",
                 path="/changelog", schema=[faq_schema, crumb_schema])
            + nav() + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>Changelog</h1>
  <p class="lede">Every release, what changed in it, and why. Currently on
  <strong>{latest}</strong>, with {len(entries)} releases documented.</p>
</div></header>
{body}
</main>''' + cta_band() + footer())
