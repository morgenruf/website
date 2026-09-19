"""The keyword pages.

These existed as 320 to 420 word stubs with their own stylesheet, which is both
too thin to rank and visibly a different website. Same shell as everything
else, and enough substance to be worth landing on.
"""

from __future__ import annotations

import diagrams
from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav


def page(*, path, title, description, h1, lede, body, hero="", schema=(), trail=()):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = list(schema) + ([crumb_schema] if crumb_schema else [])
    head_in = f'''<div class="head-in">
  <div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="head-cta">
      <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
      <a class="btn btn-line" href="/setup">Set it up yourself</a>
    </div>
  </div>
  <div>{hero}</div>
</div>''' if hero else f'''<h1>{h1}</h1>
<p class="lede">{lede}</p>
<div class="head-cta">
  <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
  <a class="btn btn-line" href="/setup">Set it up yourself</a>
</div>'''
    return (head(title=title, description=description, path=path, schema=schemas)
            + nav() + crumb_html
            + f'<main>\n<header class="page-head"><div class="wrap">{head_in}</div></header>\n{body}\n</main>'
            + cta_band() + footer())


def guide(prose, toc):
    links = "".join(f'<a href="#{slug}">{label}</a>' for label, slug in toc)
    return (f'<section class="section"><div class="wrap"><div class="guide">'
            f'<nav class="toc" aria-label="On this page"><strong>On this page</strong>'
            f'<div class="toc-links">{links}</div></nav>'
            f'<div class="prose">{prose}</div></div></div></section>')


def shot(src, alt, caption):
    from PIL import Image
    import pathlib
    with Image.open(pathlib.Path(__file__).resolve().parent.parent.parent / src.lstrip("/")) as im:
        w, h = im.size
    return (f'<div class="shot"><img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}"/></div>'
            f'<p class="shot-cap">{caption}</p>')


def geekbot():
    prose = f'''<h2 id="what-you-are-actually-comparing">What you are actually comparing</h2>
<p>Geekbot is a hosted async standup bot. It is mature, it works, and for a lot of teams the monthly
per-person fee is the right trade for never thinking about a server. Morgenruf is the same job done
on your own infrastructure, plus coffee chats and recognition, for nothing per seat. There is
<a href="/blog/geekbot-vs-morgenruf">a longer and less tidy version of this comparison</a> on the
blog, written while switching a team across.</p>
<p>The decision is rarely about features. It is about where your team's answers live and whether you
want a subscription that grows with headcount. The same question applies to Donut, HeyTaco and
Standup &amp; Prosper, which is what <a href="/compare">the comparison pages</a> work through.</p>

{diagrams.standup_flow()}

<h2 id="where-geekbot-wins">Where Geekbot wins</h2>
<ul>
  <li><strong>Nothing to run.</strong> No server, no database, no upgrade evenings. That is worth
  real money and this page is not going to pretend otherwise.</li>
  <li><strong>Years of edge cases.</strong> A hosted product that has been at this since 2015 has met
  situations a younger one has not.</li>
  <li><strong>Support with a contract behind it</strong> as part of the price, rather than an issue
  tracker and a maintainer's evening.</li>
</ul>
<p>If you have no appetite for running anything, stop here and use Geekbot. Everything below assumes
you are willing to run <a href="/self-hosted-standup-bot">one container and a Postgres of your
own</a>.</p>

<h2 id="where-this-is-different">Where this is different</h2>
<h3>The price does not scale with hiring</h3>
<p>Per-seat pricing means the cost of asking your team three questions grows every time you hire.
Self-hosted, thirty people and three hundred cost the same: one small server and a database.</p>

<h3>Your answers stay in your database</h3>
<p>Standup answers are a running commentary on your roadmap, your incidents and who is stuck. Some
teams do not want that in a third party's cloud, and for regulated ones it is not a preference.</p>

<h3>Three rituals, one app</h3>
<p>Standups, <a href="/coffee-chats">coffee chats</a> and <a href="/kudos">kudos</a> share one
deployment and one database, which is also what makes the
<a href="/insights">cross-signal questions</a> possible.</p>

<h3>It can be read and changed</h3>
<p>MIT licensed. If the summary format is wrong for you, the file is right there.</p>

<h2 id="the-things-that-decide-it-in-practice">The things that decide it in practice</h2>
<ul>
  <li><strong>Timezones per person</strong>, so a Toronto standup does not arrive at 19:00 in
  Kolkata.</li>
  <li><strong>Leave</strong> that skips people rather than nagging them, and does not drag the
  completion figure down.</li>
  <li><strong>A private nudge</strong> for whoever has not filed, instead of a public callout.</li>
  <li><strong>An edit window</strong>, because people send early and remember something a minute
  later.</li>
  <li><strong>Knowing it is working</strong>: fourteen days of completion on the card and a badge
  when it slips.</li>
</ul>

{shot("/screenshots/standups.jpg", "Two standups in the dashboard, each with a completion sparkline and a health badge", "A standup that is quietly dying says so here before anyone notices in the channel.")}

<h2 id="moving-across">Moving across</h2>
<p>There is no importer, and honestly the history is rarely what you miss. The usual path is to run
both for a week: same questions, same channel, and turn the old one off once the new summary looks
right. Nothing here has a contract to cancel.</p>
<ol>
  <li><a href="/setup/docker">Run it with Docker</a> or <a href="/setup/kubernetes">on Kubernetes</a>.</li>
  <li><a href="/setup/slack-app">Create the Slack app</a> and install it.</li>
  <li>Recreate your standup: channel, questions, hour, participants.</li>
  <li>Watch one morning. Then switch the other one off.</li>
</ol>'''
    body = guide(prose, [("What you are comparing", "what-you-are-actually-comparing"),
                         ("Where Geekbot wins", "where-geekbot-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What decides it", "the-things-that-decide-it-in-practice"),
                         ("Moving across", "moving-across")])
    faq_html, faq_schema = faq([
        ("Is Morgenruf free compared with Geekbot?",
         "There is no per-seat fee at all. You pay for the server and database you run it on, which "
         "for most teams is a few dollars a month regardless of headcount."),
        ("Can I import my Geekbot history?",
         "No. Run both in parallel for a week and switch over once the summaries look right."),
        ("Does it do everything Geekbot does?",
         "For async standups, the everyday shape is the same: questions, schedules, timezones, "
         "summaries, reminders, analytics. Geekbot has more years of edge cases and a support "
         "contract; this has coffee chats and recognition in the same app, and your data in your "
         "own database."),
        ("How long does it take to set up?",
         "About twenty minutes, most of it creating the Slack app."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Morgenruf and Geekbot</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/geekbot-alternative",
                title="Open-source Geekbot alternative, self-hosted",
                description="A self-hosted, MIT-licensed Geekbot alternative for async Slack "
                            "standups, with coffee chats and recognition in the same app. No "
                            "per-seat fee, your Postgres.",
                h1="An open-source Geekbot alternative you host yourself",
                lede="The same morning questions and channel summary, on your own servers, with "
                     "coffee chats and kudos included rather than sold separately.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing who answered, who is blocked and recent recognition", "Your morning, on one screen."),
                trail=[("Home", "/"), ("Compare", "/compare"), ("vs Geekbot", None)])


def standup_prosper():
    prose = f'''<h2 id="the-short-version">The short version</h2>
<p>Standup &amp; Prosper is a hosted Slack standup bot with a generous free tier and a simple, well
made product. Morgenruf does the same job on your own infrastructure and adds coffee chats and
recognition. If the hosted free tier covers you and you have no interest in running software, that
is a perfectly good answer, and <a href="/compare">the other comparisons</a> will not tell you
anything different.</p>

{diagrams.standup_flow()}

<h2 id="where-it-wins">Where Standup &amp; Prosper wins</h2>
<ul>
  <li><strong>Zero operations.</strong> Nothing to deploy, patch or back up.</li>
  <li><strong>A free tier</strong> that genuinely fits small teams, so the cost argument only starts
  to bite as you grow.</li>
  <li><strong>Simplicity.</strong> It does one thing and does not ask you to think about modules,
  scopes or migrations.</li>
</ul>

<h2 id="where-this-is-different">Where this is different</h2>
<ul>
  <li><strong>Your data.</strong> Answers, blockers and participation live in Postgres you control.</li>
  <li><strong>The same day-to-day in Slack</strong>: DMs, a channel summary, slash commands and an
  App Home tab. <a href="/slack-standup-bot">What the Slack app does</a> is the page for that.</li>
  <li><strong>No seat maths.</strong> The bill does not move when you hire.</li>
  <li><strong>Three rituals in one app</strong> rather than a standup tool plus two more
  subscriptions later.</li>
  <li><strong>Extensible</strong>: signed webhooks, automation rules, an MCP server for AI
  assistants, and the source itself.</li>
</ul>

<h2 id="what-you-take-on">What you take on</h2>
<p>Running it is the trade. In practice that means one container, one database, an HTTPS URL, and
<code>docker compose pull</code> when there is a release. Migrations apply themselves on start.
<a href="/self-hosted-standup-bot">Running it on your own servers</a> sets out the requirements, the
upgrade path and the backups in full. If that sounds like a chore rather than a Tuesday, the hosted
option is cheaper than your time.</p>

{shot("/screenshots/today.jpg", "The Today page showing answered, waiting and blocked counts", "What the morning looks like once it is running.")}

<h2 id="switching">Switching</h2>
<ol>
  <li><a href="/setup">Pick a way to run it</a> and give Slack an HTTPS URL.</li>
  <li><a href="/setup/slack-app">Create the app</a>, install it, invite the bot to your channel.</li>
  <li>Recreate the standup, run both for a few days, then turn the old one off.</li>
</ol>'''
    body = guide(prose, [("The short version", "the-short-version"), ("Where it wins", "where-it-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What you take on", "what-you-take-on"), ("Switching", "switching")])
    faq_html, faq_schema = faq([
        ("Is self-hosting worth it for a team of ten?",
         "If the hosted free tier covers ten people and you have nowhere to run a container, probably "
         "not. It becomes worth it when you outgrow the free tier, when standup answers cannot sit in "
         "a third party, or when you want coffee chats and recognition too."),
        ("What does it cost to run?",
         "A small VPS and a Postgres. Many teams run it beside things they already have, in which "
         "case the marginal cost is close to nothing."),
        ("Can I keep using Slack the same way?",
         "Yes. It is a Slack app: DMs for questions, a channel for the summary, slash commands, and "
         "an App Home tab."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Morgenruf and Standup &amp; Prosper</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/standup-prosper-alternative",
                title="Self-hosted Standup &amp; Prosper alternative",
                description="An open-source, self-hosted Standup &amp; Prosper alternative for Slack "
                            "standups, with coffee chats and kudos in the same app and no per-seat "
                            "bill as you hire.",
                h1="A self-hosted Standup &amp; Prosper alternative",
                lede="Same async standups, run on your own infrastructure, with two more team "
                     "rituals included rather than sold separately.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Compare", "/compare"), ("vs Standup & Prosper", None)])


def open_source():
    prose = f'''<h2 id="what-open-source-buys-you">What the licence actually says</h2>
<p>MIT, on the whole repository. Not open core, not source available, not a community edition with
the useful half behind a sales call. One licence file, one repository, and the same code in the
image that runs in production. Read it in about a minute: you may use, copy, modify, merge, publish,
distribute, sublicense and sell it, including inside a company, as long as the copyright notice
travels with it. There is no contributor agreement assigning your changes to anyone.</p>
<p>In practice that buys three things:</p>
<ul>
  <li><strong>You can read it.</strong> A standup bot sees everything your team is stuck on. Being
  able to check what it does with that is not paranoia.</li>
  <li><strong>You can change it.</strong> Summary format, question types, the wording of a nudge.
  Fork it and run your fork; nothing checks that you did.</li>
  <li><strong>It cannot be taken away.</strong> No price change, no acquisition, no sunset email.</li>
</ul>

{diagrams.architecture()}

<h2 id="the-honest-trade">The honest trade</h2>
<p>A licence does not run anything. Someone has to, and that is one container, a Postgres and an
HTTPS URL, with migrations that apply themselves.
<a href="/self-hosted-standup-bot">What running it on your own servers involves</a> is a page of its
own, down to the backups. It is a small job, but it is not zero, and a hosted tool removes it
entirely. Be clear which side of that you are on before switching.</p>

<h2 id="what-morgenruf-includes">What is in the box</h2>
<ul>
  <li><a href="/standups">Async standups</a> with per-person timezones, blockers, nudges and an edit
  window</li>
  <li><a href="/coffee-chats">Random coffee chats</a> that agree a time and book a Zoom meeting</li>
  <li><a href="/kudos">Peer recognition</a> with a daily allowance and your own emoji</li>
  <li><a href="/insights">Insights</a> across both datasets</li>
  <li>Signed webhooks, automation rules, an MCP server, CSV export, a Helm chart</li>
</ul>
<p>Every one of those is in the repository. There is no paid tier holding anything back, and
<a href="/slack-standup-bot">what the bot does inside Slack</a> is the same whether you run the
published image or your own build of it.</p>

<h2 id="who-maintains-it">Who maintains it</h2>
<p>It is built and maintained at CloudDrove, who also sell setup and hosting. Paid work funds the
project; it does not gate any of it. Issues and pull requests go to the same repository the releases
are cut from, and the Helm chart is published from it too.
<a href="/blog/why-i-built-morgenruf">The weekend that produced it</a> explains why it is arranged
this way.</p>
<p>If that arrangement ends tomorrow, you keep the source, the chart and your own database. That is
the whole point of the licence, and it is worth checking a project can say the same before you put
a daily ritual on it.</p>

<h2 id="other-options">Other open-source options</h2>
<p>There are a few self-hosted standup tools around, mostly smaller scripts that post a message and
collect replies. They are fine for one team and one question set. The things that usually run out
are per-person timezones, vacation handling, a dashboard non-engineers will use, and anything beyond
standups. Pick by which of those you need rather than by star count. Against the hosted products,
<a href="/compare">the comparison pages</a> are the more useful read.</p>

{shot("/screenshots/members.jpg", "Member cards in the dashboard showing which features each person runs", "Per-feature admin grants, so the team lead runs standups without holding the API keys.")}

<h2 id="getting-started">Getting started</h2>
<p><a href="/setup">The setup guides</a> cover Docker Compose, Kubernetes and the Slack app. The
whole thing takes about twenty minutes, most of it in Slack's settings.</p>'''
    body = guide(prose, [("What the licence says", "what-open-source-buys-you"),
                         ("The honest trade", "the-honest-trade"),
                         ("What is in the box", "what-morgenruf-includes"),
                         ("Who maintains it", "who-maintains-it"),
                         ("Other options", "other-options"), ("Getting started", "getting-started")])
    faq_html, faq_schema = faq([
        ("Is it really MIT, all of it?",
         "Yes. One repository, one licence, no open-core split and no feature held back for a paid "
         "tier."),
        ("Can I run it commercially?",
         "Yes, including inside a company, without asking anyone."),
        ("Who maintains it?",
         "It is built and maintained at CloudDrove, who also offer paid setup and hosting. Paid work "
         "funds it but never gates it."),
        ("What if the project stops?",
         "You have the source and your database. That is the point of the arrangement."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About the open-source side</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/open-source-standup-bot",
                title="Open-source Slack standup bot, MIT licensed",
                description="An MIT-licensed Slack standup bot: one repository, no open-core split, "
                            "no paid tier. Read the source, fork it, and keep running it if the "
                            "project stops.",
                h1="An open-source standup bot: MIT, one repository, no paid tier",
                lede="What the licence covers, who maintains it, and what you are left holding if "
                     "the project ever stops. The hosting question has its own page.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Compare", "/compare"), ("Open source", None)])


def self_hosted():
    prose = f'''<h2 id="why-teams-self-host-this">Why teams self-host a standup bot</h2>
<p>Self-hosting decides one thing before anything else: which machine, in which country, holds the
answers. Everything else on this page follows from that. Three reasons come up, in this order:</p>
<ul>
  <li><strong>The answers are sensitive.</strong> A standup is a daily log of what is broken, what is
  late and who is stuck. Plenty of companies are fine with that in a vendor's cloud. Regulated ones
  are not, and it is not a preference they can be argued out of. Here the answers sit in whatever
  Postgres you point it at, in whatever region that database is in.</li>
  <li><strong>The bill grows with the team.</strong> Per-seat pricing means the cost of three
  questions a morning rises every time you hire.</li>
  <li><strong>They already run things.</strong> If you have a cluster and a Postgres, adding one more
  small service is an afternoon.</li>
</ul>

{diagrams.architecture()}

<h2 id="what-running-it-involves">What running it actually involves</h2>
<ul>
  <li><strong>One container.</strong> A Python process. Not a queue, a worker pool and a cache.</li>
  <li><strong>One database.</strong> Postgres 13 or newer. Migrations run themselves on start.</li>
  <li><strong>An HTTPS URL.</strong> Slack posts events to it. A Cloudflare tunnel is enough and
  needs no open port.</li>
  <li><strong>Upgrades.</strong> Pull the image and restart, or <code>helm upgrade</code>.</li>
  <li><strong>Backups.</strong> <code>pg_dump</code>. There is no other state.</li>
</ul>

<h2 id="what-leaves-your-network">What leaves your network</h2>
<p>Slack's API, and nothing else. The app calls <code>slack.com</code> to read channel membership,
open DMs and post the summary, and Slack calls your HTTPS URL back with events. Answers, blockers,
participation, coffee chat pairings and kudos are written to your Postgres and stay there. No
telemetry, no analytics endpoint, no licence check phoning home. You can watch that on the egress
rules, and since it is <a href="/open-source-standup-bot">MIT licensed and readable end to end</a>
you can check the claim rather than take it.</p>
<p>Which makes the residency answer short. The data lives in the region your database lives in,
under the retention your backups already have, and a deletion or subject access request is a query
against a schema you own.</p>

<h2 id="what-it-costs">What it costs</h2>
<p>A small VPS and a managed Postgres, or nothing extra if you already run both. There is no seat
component at any size, which is the whole economic argument: the difference between hosted and
self-hosted grows with your headcount, not with your usage.
<a href="/compare">What the hosted standup bots charge per person</a> is on the comparison pages, if
you want to do the arithmetic for your own team.</p>

<h2 id="where-it-runs">Where it runs</h2>
<ul>
  <li><a href="/setup/kubernetes">Kubernetes</a> with the published Helm chart, ingress, HTTPRoute or
  a tunnel</li>
  <li><a href="/setup/docker">Docker Compose</a> on a VPS, a homelab box or a spare Mac mini</li>
  <li>Anywhere else a container and a Postgres can live</li>
</ul>
<p>The same image and the same database either way. <a href="/setup">Every way of running it</a> is
written up step by step, and the choice is mostly about what your team already operates.</p>

{shot("/screenshots/standups.jpg", "Standups in the dashboard with completion sparklines", "The dashboard runs on your own domain, behind your own auth.")}

<h2 id="the-part-people-underestimate">The part people underestimate</h2>
<p>Not the install. The Slack app: scopes, a redirect URL, and the fact that a workspace which
installed before a feature existed has not granted that feature's scopes.
<a href="/setup/slack-app">That page</a> exists because it is where setups actually stall. It helps
to read <a href="/slack-standup-bot">what the bot does inside Slack</a> first, because the scopes
follow from it and half of them are for features you may not switch on.</p>'''
    body = guide(prose, [("Why teams self-host", "why-teams-self-host-this"),
                         ("What running it involves", "what-running-it-involves"),
                         ("What leaves your network", "what-leaves-your-network"),
                         ("What it costs", "what-it-costs"), ("Where it runs", "where-it-runs"),
                         ("The underestimated part", "the-part-people-underestimate")])
    faq_html, faq_schema = faq([
        ("What are the minimum requirements?",
         "One small container and a Postgres. A single vCPU with 512MB is enough for a team of "
         "dozens; the work is bursty and short."),
        ("Does it need a public IP?",
         "No. A Cloudflare tunnel gives Slack an HTTPS URL without opening a port or running an "
         "ingress controller."),
        ("How do upgrades work?",
         "Pull the new image and restart. Migrations run in an init container before the app starts, "
         "and are written to be safe against a live database."),
        ("Is there a hosted version?",
         "There is a demo, and CloudDrove will run it for you commercially, but the product is "
         "designed to be yours."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About self-hosting</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/self-hosted-standup-bot",
                title="Self-hosted standup bot: where your data lives",
                description="Run the standup bot on your own servers: one container, one Postgres, "
                            "one HTTPS URL. Docker or Kubernetes, in your region, answers in your "
                            "own database.",
                h1="A standup bot on your own servers, in your own region",
                lede="One container, one database, one HTTPS URL Slack can reach. Where the answers "
                     "physically sit, and what it takes to keep them there.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Compare", "/compare"), ("Self-hosted", None)])


def slack_bot():
    prose = f'''<h2 id="what-it-does-in-slack">What a Slack standup bot does, and what this one does</h2>
<p>A standup bot asks each person the same few questions every working morning and puts the answers
somewhere the team will actually read them. That is the whole category. This one does it entirely
inside Slack: a direct message at your local hour, a summary in the channel an hour later, and
nothing to log into. The dashboard is for whoever sets it up, and most weeks they do not open it
either.</p>
<p>This page is the general one. The two questions that follow it usually are the licence and the
hosting, which have pages of their own:
<a href="/open-source-standup-bot">what the MIT licence covers</a> and
<a href="/self-hosted-standup-bot">where the container and the database end up</a>.</p>
<ul>
  <li><strong>A direct message</strong> at your local hour with your team's questions.</li>
  <li><strong>A summary in the channel</strong>, grouped by person or by question, blockers pulled
  out, optionally in a thread.</li>
  <li><strong>Slash commands</strong>: <code>/standup</code>, <code>/skip</code>,
  <code>/kudos @teammate a reason</code>, <code>/help</code>.</li>
  <li><strong>An App Home tab</strong> with your standups, your streak, your remaining kudos, and
  buttons for vacation and pausing coffee chats.</li>
  <li><strong>Group introductions</strong> for coffee chats, with the time vote in the message.</li>
</ul>

{diagrams.standup_flow()}

<h2 id="the-scopes-it-asks-for">The scopes it asks for</h2>
<p>Standups need to read channel membership, write messages, and open DMs. Coffee chats add three
scopes for group DMs and timezones. Kudos needs emoji read access to use your own token. There is no
scope for reading channel history, because it never does.
<a href="/setup/slack-app">Every scope, with the reason</a>.</p>

{shot("/screenshots/coffee-chat-settings.jpg", "Coffee chat settings with a live preview of the Slack message", "The settings page shows the Slack message it will produce, as you edit it.")}

<h2 id="what-it-is-not">What it is not</h2>
<ul>
  <li>Not a meeting recorder or a transcript bot.</li>
  <li>Not a productivity score. There is no ranking of people by output.</li>
  <li>Not a hosted service you sign up for. You run it, which is the trade.</li>
</ul>

<h2 id="adding-it">Adding it to your workspace</h2>
<p>Create the app from the manifest, install it, invite the bot to a channel, and make your first
standup. <a href="/setup">The whole thing is about twenty minutes.</a> The ten minutes after that go
on <a href="/standups">the standup itself</a>: questions, hour, timezones, who is in it, what
happens when someone is on leave. If you are still deciding,
<a href="/compare">how this lines up against the hosted standup bots</a> is the page for that.</p>'''
    body = guide(prose, [("What a standup bot does", "what-it-does-in-slack"),
                         ("The scopes", "the-scopes-it-asks-for"),
                         ("What it is not", "what-it-is-not"), ("Adding it", "adding-it")])
    faq_html, faq_schema = faq([
        ("Does it work on Slack's free plan?",
         "Yes. It uses standard app APIs available on the free plan."),
        ("Can it post to a different channel from the one it asks in?",
         "Yes. Questions go by DM, and the summary can post anywhere the bot has been invited."),
        ("Does it read our channel messages?",
         "No. It reads replies to its own DMs and channel membership where you point it. It has no "
         "history scope."),
        ("What about Microsoft Teams or Google Chat?",
         "Google Chat is in beta; Teams as a platform is in progress. Slack is first class."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About the Slack app</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/slack-standup-bot",
                title="Slack standup bot: DMs, summaries, commands",
                description="A Slack standup bot that DMs each person their questions at their own "
                            "local hour and posts one summary to the channel. Slash commands, App "
                            "Home, MIT licensed.",
                h1="A Slack standup bot, from the morning DM to the summary",
                lede="Questions by DM at each person's local hour, one summary in the channel, "
                     "slash commands and an App Home tab. Nobody opens a dashboard to take part.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing the morning's answers and blockers", "The dashboard is for whoever runs it. Everyone else stays in Slack."),
                trail=[("Home", "/"), ("Slack standup bot", None)])
