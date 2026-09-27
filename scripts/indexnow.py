"""Tell IndexNow (Bing, Yandex, Naver and others) which pages a push changed.

Run by CI after a push to main: python3 scripts/indexnow.py <before-sha> <after-sha>

The key is the one <32 hex>.txt file at the site root. IndexNow fetches it
from the live site to check the request is ours, so this waits until the
deploy that carries it is being served before sending anything.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://morgenruf.dev"


def key():
    files = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", p.name)]
    if len(files) != 1:
        sys.exit(f"expected one IndexNow key file at the site root, found {len(files)}")
    return files[0].stem


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())


def changed_urls(before, after):
    """Pages whose HTML changed in the push. A new branch or a rewritten
    history has no usable 'before', so every page is sent."""
    known = set(sitemap_urls())
    if not before or set(before) == {"0"}:
        return sorted(known)
    out = subprocess.run(["git", "diff", "--name-only", before, after], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode:
        return sorted(known)
    urls = set()
    for name in out.stdout.split():
        if name == "index.html":
            urls.add(SITE + "/")
        elif name.endswith("/index.html"):
            urls.add(f"{SITE}/{name[:-len('index.html')]}")
    return sorted(urls & known)


def wait_for_key(k, attempts=30, pause=20):
    url = f"{SITE}/{k}.txt"
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                if r.read().decode().strip() == k:
                    return
        except Exception:
            pass
        time.sleep(pause)
    sys.exit(f"{url} was not being served after {attempts * pause}s; skipping")


def main():
    before, after = (sys.argv[1:3] + ["", "HEAD"])[:2]
    urls = changed_urls(before, after)
    if not urls:
        print("no page changed; nothing to send")
        return
    k = key()
    wait_for_key(k)
    body = json.dumps({"host": "morgenruf.dev", "key": k, "keyLocation": f"{SITE}/{k}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow answered {r.status} for {len(urls)} URLs")


if __name__ == "__main__":
    main()
