"""Support: where to go, and what each route actually gets you.

Two audiences with different questions. Somebody stuck at 2am wants the issue
tracker and a search box. Somebody deciding whether to self-host at all wants
to know there is a company behind it who will pick up the phone.

Email comes first for both. Slack's Marketplace asks for a support address that
works without an account and a reply within two business days, and that is
also the simplest promise to make to anybody.
"""

from __future__ import annotations

from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav

EMAIL = "hello@morgenruf.dev"
MAILTO = f"mailto:{EMAIL}?subject=Morgenruf%20support"
ISSUES = REPO + "/issues"
DISCUSSIONS = REPO + "/discussions"

SUPPORT_FAQ = [
    ("How do I contact support?",
     "Email hello@morgenruf.dev. It is free, it needs no account or signup, and it covers the "
     "hosted Slack app and self-hosted installs alike. We reply within 2 business days."),
    ("Is there paid support?",
     "Yes, from CloudDrove, who sponsor Morgenruf. Installation, a managed cluster, "
     "upgrades and a contracted response time. Write to hello@morgenruf.dev. You do not need it "
     "to get an answer: free support is by email too, at the same address."),
    ("Does paying get me features other people do not have?",
     "No. Everything is MIT and everything is in the repository. Paid work funds the project and "
     "buys you somebody else's time, never a private build."),
    ("How fast will I hear back?",
     "We reply to email within 2 business days. GitHub issues and discussions are read by the same "
     "person and usually get an answer about as quickly. Bugs with a clear reproduction get fixed "
     "fastest, because the hard part is already done."),
    ("Something is broken in production. What do I do first?",
     "Check the app logs and the migrate init container's logs; they say more than the dashboard "
     "does. Then open an issue with the version, how it is deployed, and what the logs said, or email "
     "hello@morgenruf.dev with the same three things. You do not need a support agreement to email."),
    ("Can I ask for a feature?",
     "Yes, in Discussions under Ideas. The roadmap order follows what people ask for, and a "
     "well-argued request from one person has moved it before."),
    ("Is there a security contact?",
     "Report privately through the security policy in the repository rather than opening an issue."),
]


def support():
    body = f'''<section class="section"><div class="wrap">
  <div class="prose">
    <span class="eyebrow">Support by email</span>
    <h2 id="email">Email {EMAIL}</h2>
    <p>This is the support address for Morgenruf, for everybody: people using the free hosted Slack
    app, people running it on their own servers, and people who have not installed it yet. You do not
    need an account, a GitHub login or a support agreement to use it. <strong>We reply within 2
    business days.</strong></p>
    <p>Say which workspace or install you mean, and for anything broken, the three things listed
    under "Before you open an issue" below. It saves a round trip.</p>
    <p><a class="btn btn-ink" href="{MAILTO}">Email {EMAIL}</a></p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <span class="eyebrow">Also free</span>
  <h2 id="where-to-start" style="margin-bottom:24px">Three more places to start</h2>
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
      <li><a href="{MAILTO}">{EMAIL}</a>, for anything at all. We reply within 2 business days.</li>
      <li><a href="{ISSUES}">Issues</a>, for bugs and anything with a reproduction.</li>
      <li><a href="{DISCUSSIONS}">Discussions</a>, for questions, ideas, and "is this supposed to happen".</li>
      <li><a href="https://status.morgenruf.dev">Status</a>, for the free hosted instance. Self-hosted
      instances are yours to monitor.</li>
      <li><a href="{REPO}/security/policy">Security policy</a>. Please report privately rather than in an
      issue.</li>
    </ul>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="band" style="text-align:left">
    <span class="eyebrow" style="color:var(--sun)">Commercial support</span>
    <h2>Or have CloudDrove run it</h2>
    <p class="lede" style="margin:14px 0 22px">Morgenruf is built by Anmol Nagpal and sponsored by
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
      <a class="btn btn-sun" href="mailto:hello@morgenruf.dev?subject=Morgenruf%20support">Email hello@morgenruf.dev</a>
      <a class="btn btn-ghost" href="https://clouddrove.com">About CloudDrove</a>
    </div>
    <p style="margin:22px 0 0;font-size:14px;color:var(--on-ink-muted)">Paid support funds the work
    but never gates it. Free support is by email too, at the same address, with the same 2 business
    day reply. A bug is a bug, and it gets fixed for everybody.</p>
  </div>
</div></section>
'''
    faq_html, faq_schema = faq(SUPPORT_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Getting help</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return (head(title="Morgenruf support: email, issues and paid help",
                 description="Email hello@morgenruf.dev for free Morgenruf support, no signup "
                             "needed, with a reply within 2 business days. Also GitHub issues, "
                             "discussions, the docs, and paid help from CloudDrove.",
                 path="/support/", schema=[faq_schema, breadcrumbs(
                     [("Home", "/"), ("Support", None)])[1]])
            + nav() + breadcrumbs([("Home", "/"), ("Support", None)])[0]
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>Getting help</h1>
  <p class="lede">Email <a href="{MAILTO}">{EMAIL}</a>. It is free, needs no signup, and we reply
  within 2 business days. GitHub issues and discussions work too, and CloudDrove will run the whole
  thing for you if you would rather pay.</p>
  <div class="head-cta">
    <a class="btn btn-ink" href="{MAILTO}">Email {EMAIL}</a>
    <a class="btn btn-line" href="{ISSUES}">Open an issue</a>
  </div>
</div></header>
{body}
</main>''' + cta_band() + footer())
