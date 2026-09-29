"""The changelog, generated from the app repository's CHANGELOG.md.

The hand-written one stopped at 1.2.0 while the product shipped 1.8.4, which is
worse than not having the page: it tells a visitor the project stalled.
"""

from __future__ import annotations

import functools
import pathlib
import re

from shell import REPO, breadcrumbs, cta_band, faq, footer, head, nav

# One source for the version everywhere on the site: the changelog on the app
# repository's main branch, read at build time. The local checkout is the
# fallback, since it can sit on an older branch, and a clone that is behind
# kept the site on 1.8.13 while 1.9.4 was out.
SOURCE_URL = "https://raw.githubusercontent.com/morgenruf/morgenruf/main/CHANGELOG.md"
SOURCE = pathlib.Path.home() / "workspace/morgenruf/morgenruf/CHANGELOG.md"
# The last release a build saw, committed, so a build with no network and no
# local checkout still states a version rather than failing or printing none.
LAST_KNOWN = pathlib.Path(__file__).resolve().parent / "latest_release.json"
BUILT = pathlib.Path(__file__).resolve().parent.parent.parent / "changelog/index.html"
KIND = {"Added": "state done", "Fixed": "state", "Changed": "state", "Removed": "state",
        "Security": "state"}


@functools.lru_cache(maxsize=None)
def _source_text():
    import urllib.request
    try:
        with urllib.request.urlopen(SOURCE_URL, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        pass
    if SOURCE.exists():
        return SOURCE.read_text()
    return ""


@functools.lru_cache(maxsize=None)
def _published_tags():
    """Versions that have a tag on the app repository. A tag is what builds
    the Docker image, so a tagged version is a released one. GitHub releases
    stopped being cut after 1.8.13, and counting only those held every page
    on 1.8.13. git ls-remote needs no token and uses no API quota."""
    import subprocess
    try:
        out = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", REPO + ".git"],
            capture_output=True, text=True, timeout=30).stdout
        tags = set(re.findall(r"refs/tags/v?([0-9]+\.[0-9]+\.[0-9]+)$", out, re.M))
    except Exception:
        tags = set()
    if not tags and BUILT.exists():
        # Offline: keep the links the last build found rather than silently
        # dropping every one of them.
        tags = set(re.findall(r"/releases/tag/v([0-9.]+)", BUILT.read_text()))
    return tags


@functools.lru_cache(maxsize=None)
def latest_release():
    """The newest version in the changelog that has been tagged, and its date.

    Falls back to the last value a build recorded when neither the changelog
    nor the tags can be read, and records the value whenever it can."""
    import json
    entries = _entries()
    published = _published_tags()
    found = next(((v, d) for v, d, _ in entries if v in published), None)
    if found is None and entries and not published:
        found = (entries[0][0], entries[0][1])
    known = json.loads(LAST_KNOWN.read_text()) if LAST_KNOWN.exists() else None

    def newer(a, b):
        return tuple(map(int, a.split("."))) > tuple(map(int, b.split(".")))

    # A local checkout on an old branch must not move the version backwards.
    if known and (not found or newer(known["version"], found[0])):
        return known["version"], known["date"]
    if found:
        record = json.dumps({"version": found[0], "date": found[1]}, indent=2) + "\n"
        if not LAST_KNOWN.exists() or LAST_KNOWN.read_text() != record:
            LAST_KNOWN.write_text(record)
        return found
    return "", ""


@functools.lru_cache(maxsize=None)
def _entries():
    text = _source_text()
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
    if not entries and BUILT.exists():
        # No changelog to read: keep the page the last build wrote.
        return BUILT.read_text()
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
    latest, _ = latest_release()
    body = f'''<section class="section"><div class="wrap">
  <div class="note" style="margin-bottom:34px"><p>Every release is tagged, published with notes, and
  built from the same commit that is on <a href="{REPO}">GitHub</a>. Docker images carry the
  revision they were built from, so you can check what you are running matches what you read here.</p></div>
  {rows}
</div></section>'''
    faq_html, faq_schema = faq([
        ("How often are there releases?",
         "Whenever something is ready. Some months see several in a week and others none; the dates "
         "above are the record. Fixes have gone out within an hour of being reported."),
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
                 path="/changelog/", schema=[faq_schema, crumb_schema])
            + nav() + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>Changelog</h1>
  <p class="lede">Every release, what changed in it, and why. Currently on
  <strong>{latest}</strong>, with {len(entries)} releases documented.</p>
</div></header>
{body}
</main>''' + cta_band() + footer())
