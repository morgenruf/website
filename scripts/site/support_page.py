"""Support: where to go, and what each route actually gets you.

Two audiences with different questions. Somebody stuck at 2am wants the issue
tracker and a search box. Somebody deciding whether to self-host at all wants
to know there is a company behind it who will pick up the phone.
"""

from __future__ import annotations

from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav

ISSUES = REPO + "/issues"
DISCUSSIONS = REPO + "/discussions"

SUPPORT_FAQ = [
    ("Is there paid support?",
     "Yes, from CloudDrove, who build and maintain Morgenruf. Installation, a managed cluster, "
     "upgrades and a contracted response time. Write to hello@clouddrove.com."),
    ("Does paying get me features other people do not have?",
     "No. Everything is MIT and everything is in the repository. Paid work funds the project and "
     "buys you somebody else's time, never a private build."),
    ("How fast do community issues get answered?",
     "Usually within a day or two, by one person who also has a job. Bugs with a clear reproduction "
     "get fixed fastest, because the hard part is already done."),
    ("Something is broken in production. What do I do first?",
     "Check the app logs and the migrate init container's logs; they say more than the dashboard "
     "does. Then open an issue with the version, how it is deployed, and what the logs said. If you "
     "have a support agreement, email instead and include the same three things."),
    ("Can I ask for a feature?",
     "Yes, in Discussions under Ideas. The roadmap order follows what people ask for, and a "
     "well-argued request from one person has moved it before."),
    ("Is there a security contact?",
     "Report privately through the security policy in the repository rather than opening an issue."),
]


def support():
    body = f'''<section class="section"><div class="wrap">
  <div class="tiles">
    <a class="tile" href="{ISSUES}"><h3>Report a bug</h3>
      <p>The issue tracker. Templates for bugs, and the fastest route to a fix if you can say how to
      reproduce it.</p><span class="go">Open an issue →</span></a>
    <a class="tile" href="{DISCUSSIONS}"><h3>Ask a question</h3>
      <p>Discussions, for "how do I", "should this work like this", and feature ideas. Searchable,
      so the answer helps the next person.</p><span class="go">Start a discussion →</span></a>
    <a class="tile" href="https://docs.morgenruf.dev"><h3>Read the docs</h3>
      <p>Configuration, every environment variable, the webhook payloads and the MCP tools.</p>
      <span class="go">Open the documentation →</span></a>
  </div>

  <div class="prose" style="margin-top:54px">
    <h2>Before you open an issue</h2>
    <p>Three things turn a report into a fix, and leaving them out is what makes a thread take a
    week:</p>
    <ul>
      <li><strong>The version.</strong> The footer of your dashboard, or the image tag you deployed.</li>
      <li><strong>How it is running.</strong> Docker Compose, Helm, or from source.</li>
      <li><strong>What the logs said.</strong> The app container, and the migrate init container if
      it happened during a deploy.</li>
    </ul>
    <p>If it is a Slack message that went wrong, the timestamp helps, because the log line for that
    send will be next to it.</p>

    <h2>Where things get answered</h2>
    <ul>
      <li><a href="{ISSUES}">Issues</a> — bugs, and anything with a reproduction.</li>
      <li><a href="{DISCUSSIONS}">Discussions</a> — questions, ideas, and "is this supposed to happen".</li>
      <li><a href="https://status.morgenruf.dev">Status</a> — for the hosted demo. Self-hosted
      instances are yours to monitor.</li>
      <li><a href="{REPO}/security/policy">Security policy</a> — please report privately, not in an
      issue.</li>
    </ul>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="band" style="text-align:left">
    <span class="eyebrow" style="color:var(--sun)">Commercial support</span>
    <h2>Or have CloudDrove run it</h2>
    <p class="lede" style="margin:14px 0 22px">Morgenruf is built and maintained at
    <a style="color:var(--sun)" href="https://clouddrove.com">CloudDrove</a>, a DevOps consultancy
    that runs Kubernetes for other people for a living. If you would rather not run this yourself,
    they will.</p>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:26px;margin-bottom:26px" class="support-grid">
      <div>
        <h3 style="color:var(--on-ink);margin-bottom:8px">What they do</h3>
        <ul style="list-style:none;padding:0;margin:0;color:var(--on-ink-muted);font-size:15.5px">
          <li style="margin-bottom:7px">Install it in your cloud account, on your infrastructure</li>
          <li style="margin-bottom:7px">Run the cluster and the database, with backups</li>
          <li style="margin-bottom:7px">Upgrades and migrations, so a release is not your evening</li>
          <li style="margin-bottom:7px">Slack app setup, scopes and workspace rollout</li>
          <li style="margin-bottom:7px">A contracted response time rather than best effort</li>
        </ul>
      </div>
      <div>
        <h3 style="color:var(--on-ink);margin-bottom:8px">What does not change</h3>
        <ul style="list-style:none;padding:0;margin:0;color:var(--on-ink-muted);font-size:15.5px">
          <li style="margin-bottom:7px">The licence: MIT, every feature, nothing held back</li>
          <li style="margin-bottom:7px">The data: your cloud account, your database</li>
          <li style="margin-bottom:7px">The code: same repository everybody else gets</li>
          <li style="margin-bottom:7px">Leaving: it is already yours, so there is nothing to migrate</li>
        </ul>
      </div>
    </div>
    <div class="band-cta" style="justify-content:flex-start">
      <a class="btn btn-sun" href="mailto:hello@clouddrove.com?subject=Morgenruf%20support">Email hello@clouddrove.com</a>
      <a class="btn btn-ghost" href="https://clouddrove.com">About CloudDrove</a>
    </div>
    <p style="margin:22px 0 0;font-size:14px;color:var(--on-ink-muted)">Paid support funds the work
    but never gates it. A bug is a bug, and it gets fixed for everybody.</p>
  </div>
</div></section>
'''
    faq_html, faq_schema = faq(SUPPORT_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Getting help</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return (head(title="Support: issues, discussions and commercial help — Morgenruf",
                 description="Where to get help with Morgenruf: the GitHub issue tracker, "
                             "discussions, documentation, and paid setup and hosting from "
                             "CloudDrove, who build it.",
                 path="/support", schema=[faq_schema, breadcrumbs(
                     [("Home", "/"), ("Support", None)])[1]])
            + nav() + breadcrumbs([("Home", "/"), ("Support", None)])[0]
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>Getting help</h1>
  <p class="lede">Two routes, and both are real: a public issue tracker where the maintainer answers,
  and a company that will run the whole thing for you.</p>
  <div class="head-cta">
    <a class="btn btn-ink" href="{ISSUES}">Open an issue</a>
    <a class="btn btn-line" href="mailto:hello@clouddrove.com?subject=Morgenruf%20support">Ask about paid support</a>
  </div>
</div></header>
{body}
</main>''' + cta_band() + footer())
