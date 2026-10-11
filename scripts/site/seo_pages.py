"""The keyword pages.

These existed as 320 to 420 word stubs with their own stylesheet, which is both
too thin to rank and visibly a different website. Same shell as everything
else, and enough substance to be worth landing on.
"""

from __future__ import annotations

import diagrams
from og_images import og_image
from product_pages import shot
from shell import (CTA_NOTE, INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, definition, faq,
                   footer, head, nav, webpage_schema)


def page(*, path, title, description, h1, lede, body, hero="", schema=(), trail=(), define="",
         og=None, reviewed=None):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = (list(schema) + ([crumb_schema] if crumb_schema else [])
               + [webpage_schema(path, title, reviewed)])
    head_in = f'''<div class="head-in">
  <div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="head-cta">
      <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
      <a class="btn btn-line" href="/setup/">Self-host in about 20 minutes</a>
    </div>
    {CTA_NOTE}
  </div>
  <div>{hero}</div>
</div>''' if hero else f'''<h1>{h1}</h1>
<p class="lede">{lede}</p>
<div class="head-cta">
  <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
  <a class="btn btn-line" href="/setup/">Self-host in about 20 minutes</a>
</div>
{CTA_NOTE}'''
    return (head(title=title, description=description, path=path, schema=schemas,
                 og_image=og_image(og) if og else "/og-image.png")
            + nav() + crumb_html
            + f'<main>\n<header class="page-head"><div class="wrap">{head_in}</div></header>\n'
            + (definition(define, reviewed) if define else "") + f'{body}\n</main>'
            + cta_band() + footer())


def project_facts():
    """What a visitor arriving from GitHub checks first: licence, how recent
    the last release is, and how to run it. Read from the changelog at build."""
    from changelog_page import latest_release
    version, date = latest_release()
    return f'''<div class="note"><p><strong>MIT licence</strong> &middot; latest release
<a href="{REPO}/releases/tag/v{version}">{version}</a>, {date} &middot;
<a href="https://charts.morgenruf.dev">Helm chart</a> &middot; <a href="/changelog/">every release</a></p>
<pre><code>git clone https://github.com/morgenruf/morgenruf.git
cd morgenruf/app &amp;&amp; cp .env.example .env   # add your Slack app values
docker compose up -d</code></pre>
<p style="margin:14px 0 0"><a class="btn btn-ink btn-sm" href="{REPO}">View on GitHub</a></p></div>'''


def guide(prose, toc):
    links = "".join(f'<a href="#{slug}">{label}</a>' for label, slug in toc)
    return (f'<section class="section"><div class="wrap"><div class="guide">'
            f'<nav class="toc" aria-label="On this page"><strong>On this page</strong>'
            f'<div class="toc-links">{links}</div></nav>'
            f'<div class="prose">{prose}</div></div></div></section>')


GEEKBOT_ROWS = [
    ("Async standups by DM, one channel summary", "Yes", "yes", "Yes", "yes"),
    ("Per-person timezones", "Yes", "yes", "Yes", "yes"),
    ("Polls and surveys", "No", "no", "Yes", "yes"),
    ("Microsoft Teams", "Planned", "no", "Yes", "yes"),
    ("Free plan", "Yes, any team size", "yes", "Up to 10 users", ""),
    ("Price above the free plan", "None", "yes", "$3 per user monthly, $2.50 billed annually", "no"),
    ("A 30 person team, per year", "$0 hosted", "yes", "$900 to $1,080", "no"),
    ("Runs on your own servers", "Yes", "yes", "No", "no"),
    ("Source you can read", "MIT", "yes", "Closed", "no"),
    ("Where answers are stored", "Your Postgres, or the hosted instance", "yes", "Geekbot's cloud", ""),
    ("Slack App Directory listing", "No", "no", "Yes", "yes"),
    ("Support contract", "Paid, from CloudDrove", "", "Included", "yes"),
]


def geekbot():
    from compare_pages import table
    geekbot_table = table(GEEKBOT_ROWS, "Geekbot")
    prose = f'''<h2 id="what-you-are-actually-comparing">What you are actually comparing</h2>
<p>Geekbot is a hosted async standup bot. It is mature, it works, and for a lot of teams the monthly
per-person fee is the right trade for never thinking about a server. Morgenruf is the same job,
plus coffee chats and recognition, for nothing per seat: free on the hosted instance CloudDrove runs,
or on your own infrastructure with the same MIT code. There is
<a href="/blog/geekbot-vs-morgenruf/">a longer and less tidy version of this comparison</a> on the
blog, written while switching a team across.</p>
<p>The decision is rarely about features. It is about where your team's answers live and whether you
want a subscription that grows with headcount. The same question applies to Donut, HeyTaco and
Standup &amp; Prosper, which is what <a href="/compare/">the comparison pages</a> work through.</p>

{diagrams.standup_flow("The shape of morning a Geekbot team already knows: a DM at each local hour, a private nudge, one summary.")}

<h2 id="morgenruf-and-geekbot-side-by-side">How do Morgenruf and Geekbot compare?</h2>
{geekbot_table}
<p class="shot-cap" style="margin-top:12px">Geekbot prices checked 2026-09-26 on
<a href="https://geekbot.com/pricing/">Geekbot's pricing page</a>. If something here is out of date,
please <a href="{REPO}/issues/new/choose">open an issue</a>.</p>

<h2 id="where-geekbot-wins">Where Geekbot wins</h2>
<ul>
  <li><strong>Nothing to run.</strong> No server, no database, no upgrade evenings. That is worth
  real money and this page is not going to pretend otherwise.</li>
  <li><strong>Years of edge cases.</strong> A hosted product that has been at this since 2015 has met
  situations a younger one has not.</li>
  <li><strong>Support with a contract behind it</strong> as part of the price, rather than an issue
  tracker and a maintainer's evening.</li>
  <li><strong>A free plan for small teams.</strong> Geekbot is free for up to 10 users, so a small
  team pays nothing either way.</li>
  <li><strong>Microsoft Teams.</strong> Geekbot runs there today; Teams support here is planned,
  not started.</li>
</ul>
<p>If you have no appetite for running anything, you do not have to: Add to Slack puts Morgenruf on
the free hosted instance in about two minutes. Most of what follows is about the other route,
<a href="/self-hosted-standup-bot/">two small containers and a Postgres of your own</a>.</p>

<h2 id="where-this-is-different">Where is Morgenruf different from Geekbot?</h2>
<h3>The price does not scale with hiring</h3>
<p>Per-seat pricing means the cost of asking your team three questions grows every time you hire.
Geekbot is free for up to 10 users, then $3 per user per month, or $2.50 per user per month billed
annually (prices checked 2026-09-26 on <a href="https://geekbot.com/pricing/">Geekbot's pricing
page</a>). A team of thirty pays $900 to $1,080 a year. On the Morgenruf hosted instance, thirty people and three hundred both cost nothing. Self-hosted, they cost
the same: one small server and a database.</p>

<h3>Your answers stay in your database</h3>
<p>Standup answers are a running commentary on your roadmap, your incidents and who is stuck. Some
teams do not want that in a third party's cloud, and for regulated ones it is not a preference.
Self-hosting keeps them in your own Postgres.</p>

<h3>Three rituals, one app</h3>
<p>Standups, <a href="/coffee-chats/">coffee chats</a> and <a href="/kudos/">kudos</a> share one
deployment and one database, which is also what makes the
<a href="/insights/">cross-signal questions</a> possible.</p>

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

<h2 id="what-geekbot-costs">What does Geekbot cost for 10, 30 or 100 people?</h2>
<p>Worked out from Geekbot's published prices on 2026-09-26, per year. Morgenruf's self-hosted figure
is the small server and Postgres it runs on, which does not move with headcount.</p>
<div class="scroll-x"><table>
<thead><tr><th>Team size</th><th>Geekbot, billed monthly</th><th>Geekbot, billed annually</th><th class="us">Morgenruf, hosted</th><th class="us">Morgenruf, self-hosted</th></tr></thead>
<tbody>
<tr><td>10 people</td><td>$0 (free plan)</td><td>$0 (free plan)</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>30 people</td><td>$1,080</td><td>$900</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>100 people</td><td>$3,600</td><td>$3,000</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
</tbody></table></div>
<p>At ten people or fewer, both are free and the choice is about everything else on this page.</p>

<h2 id="moving-across">Moving across from Geekbot</h2>
<p>There is no importer, and honestly the history is rarely what you miss. The usual path is to run
both for a week: same questions, same channel, and turn the old one off once the new summary looks
right. Nothing here has a contract to cancel.</p>
<ol>
  <li>Write down each Geekbot standup: its channel, questions, schedule, participants and
  timezone.</li>
  <li>Install Morgenruf: <a href="{INSTALL}">Add to Slack</a> for the free hosted instance, or
  <a href="/setup/docker/">run it with Docker</a> or <a href="/setup/kubernetes/">on Kubernetes</a>
  and <a href="/setup/slack-app/">create the Slack app</a>.</li>
  <li>Recreate each standup: channel, questions in your own words, hour, participants.</li>
  <li>Mark anyone on leave, so the first week's completion figure means something.</li>
  <li>Watch a week of mornings side by side.</li>
  <li>Keep whatever Geekbot history you want, then switch Geekbot off.</li>
</ol>'''
    body = guide(prose, [("What you are comparing", "what-you-are-actually-comparing"),
                         ("Side by side", "morgenruf-and-geekbot-side-by-side"),
                         ("Where Geekbot wins", "where-geekbot-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What decides it", "the-things-that-decide-it-in-practice"),
                         ("What Geekbot costs", "what-geekbot-costs"),
                         ("Moving across", "moving-across")])
    faq_html, faq_schema = faq([
        ("Is Morgenruf free compared with Geekbot?",
         "Yes, with no per-seat fee at all. The hosted instance is free. Self-hosted, you pay for the "
         "server and database you run it on, roughly $5 to $20 a month regardless of headcount."),
        ("Can I import my Geekbot history?",
         "No. Run both in parallel for a week and switch over once the summaries look right."),
        ("Does it do everything Geekbot does?",
         "For async standups, the everyday shape is the same: questions, schedules, timezones, "
         "summaries, reminders, analytics. Geekbot has more years of edge cases and a support "
         "contract; this has coffee chats and recognition in the same app, and your data in your "
         "own database."),
        ("How long does it take to set up?",
         "About two minutes on the free hosted instance. Self-hosted, about twenty minutes, most of it "
         "creating the Slack app."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Morgenruf and Geekbot</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/geekbot-alternative/",
                title="Free, open-source Geekbot alternative for Slack standups",
                description="A free, MIT-licensed Geekbot alternative for async Slack standups, "
                            "with coffee chats and recognition in the same app. Hosted free, or "
                            "self-hosted.",
                h1="A free, open-source Geekbot alternative for Slack",
                lede="The same morning questions and channel summary, free on the hosted instance or "
                     "on your own servers, with coffee chats and kudos included rather than sold "
                     "separately.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing who answered, who is blocked and recent recognition", "Your morning, on one screen.", lazy=False),
                trail=[("Home", "/"), ("Compare", "/compare/"), ("vs Geekbot", None)],
                og="geekbot-alternative",
        define='Morgenruf is a free, open-source (MIT) Geekbot alternative for Slack. Like Geekbot, it sends each person standup questions by DM and posts one summary to a channel. Unlike Geekbot (free up to 10 users, then $3 per user per month, checked 2026-09-26), it has no per-seat fee at any size, can run on your own servers, and adds coffee chats and kudos.')


SP_ROWS = [
    ("Async standups in Slack", "Yes", "yes", "Yes", "yes"),
    ("A hosted service with a free tier", "Yes, any team size", "yes", "Yes", "yes"),
    ("Runs on your own servers", "Yes", "yes", "No", "no"),
    ("Source you can read", "MIT", "yes", "Closed", "no"),
    ("Coffee chats and kudos in the same app", "Yes", "yes", "No, standups only", "no"),
]


def standup_prosper():
    from compare_pages import table
    sp_table = table(SP_ROWS, "Standup &amp; Prosper")
    prose = f'''<h2 id="the-short-version">The short version</h2>
<p>Standup &amp; Prosper is a hosted Slack standup bot with a generous free tier and a simple, well
made product. Morgenruf does the same job, free on its hosted instance or on your own
infrastructure, and adds coffee chats and recognition. If their free tier covers you and you have no
reason to move, that is a perfectly good answer, and <a href="/compare/">the other comparisons</a>
will not tell you anything different.</p>

{diagrams.standup_flow("What a Standup &amp; Prosper team would recognise: questions by DM, answers in their own time, one post.")}

<h2 id="side-by-side">How do Morgenruf and Standup &amp; Prosper compare?</h2>
{sp_table}
<p class="shot-cap" style="margin-top:12px">Checked against
<a href="https://standup-and-prosper.com/">Standup &amp; Prosper's own site</a> on 2026-09-27: a free
plan with unlimited standups and team members, and paid plans at $1 or $4 per standup user a
month.</p>

<h2 id="where-it-wins">Where Standup &amp; Prosper wins</h2>
<ul>
  <li><strong>Zero operations.</strong> Nothing to deploy, patch or back up.</li>
  <li><strong>A free plan with no user limit.</strong> Unlimited standups and team members, so for
  standups alone on Slack there is no cost argument at all.</li>
  <li><strong>Simplicity.</strong> It does one thing and does not ask you to think about modules,
  scopes or migrations.</li>
</ul>

<h2 id="where-this-is-different">Where this is different</h2>
<ul>
  <li><strong>Your data.</strong> Answers, blockers and participation live in Postgres you control.</li>
  <li><strong>The same day-to-day in Slack</strong>: DMs, a channel summary, slash commands and an
  App Home tab. <a href="/slack-standup-bot/">What the Slack app does</a> is the page for that.</li>
  <li><strong>No seat maths.</strong> The bill does not move when you hire.</li>
  <li><strong>Three rituals in one app</strong> rather than a standup tool plus two more
  subscriptions later.</li>
  <li><strong>Extensible</strong>: signed webhooks, automation rules, an MCP server for AI
  assistants, and the source itself.</li>
</ul>

<h2 id="what-you-take-on">What you take on</h2>
<p>Nothing, if you use the free hosted instance. Self-hosting is the trade for keeping the data in
your own database, and in practice that means a backend and a small frontend container, one database, an HTTPS URL,
and <code>docker compose pull</code> when there is a release. Migrations run in their own step
before the app starts.
<a href="/self-hosted-standup-bot/">Running it on your own servers</a> sets out the requirements, the
upgrade path and the backups in full. If that sounds like a chore rather than a Tuesday, a hosted
option is cheaper than your time.</p>

{shot("/screenshots/today.jpg", "The Today page showing answered, waiting and blocked counts", "What the morning looks like once it is running.")}

<h2 id="switching">Switching</h2>
<ol>
  <li><a href="/setup/">Pick a way to run it</a> and give Slack an HTTPS URL.</li>
  <li><a href="/setup/slack-app/">Create the app</a>, install it, invite the bot to your channel.</li>
  <li>Recreate the standup, run both for a few days, then turn the old one off.</li>
</ol>'''
    body = guide(prose, [("The short version", "the-short-version"), ("Side by side", "side-by-side"),
                         ("Where it wins", "where-it-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What you take on", "what-you-take-on"), ("Switching", "switching")])
    faq_html, faq_schema = faq([
        ("Is self-hosting worth it for a team of ten?",
         "Not for the price: Standup & Prosper's free plan has no user limit. It becomes worth it when "
         "standup answers cannot sit with a third party, when you want to keep full history in your "
         "own database, or when you want coffee chats and recognition too."),
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
    return page(path="/standup-prosper-alternative/",
                title="Free, open-source Standup &amp; Prosper alternative for Slack",
                description="An open-source, self-hosted Standup &amp; Prosper alternative for Slack "
                            "standups, with coffee chats and kudos in the same app and no per-seat "
                            "bill as you hire.",
                h1="A free, open-source Standup &amp; Prosper alternative",
                lede="Same async standups, run on your own infrastructure, with two more team "
                     "rituals included rather than sold separately.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Compare", "/compare/"), ("vs Standup & Prosper", None)],
                og="standup-prosper-alternative",
        define='Morgenruf is a free, open-source (MIT) alternative to Standup &amp; Prosper for Slack. Both run async standups by DM with one summary in the channel. Morgenruf is free at any team size on its hosted instance, can also run on your own servers, and adds coffee chats and kudos in the same app.')


def open_source():
    prose = f'''{project_facts()}
<h2 id="what-open-source-buys-you">What the licence actually says</h2>
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

{diagrams.architecture("The whole of what you would be running: the app and its frontend, one Postgres, and Slack on the other end.")}

<h2 id="the-honest-trade">The honest trade</h2>
<p>A licence does not run anything. Someone has to, and that is a backend and a small frontend container, a
Postgres and an HTTPS URL, with migrations applied as a step before each start.
<a href="/self-hosted-standup-bot/">What running it on your own servers involves</a> is a page of its
own, down to the backups. It is a small job, but it is not zero. The free hosted instance CloudDrove
runs removes it entirely, on the same code. Be clear which side of that you are on before
switching.</p>

<h2 id="what-morgenruf-includes">What is in the box</h2>
<ul>
  <li><a href="/standups/">Async standups</a> with per-person timezones, blockers, nudges and an edit
  window</li>
  <li><a href="/coffee-chats/">Random coffee chats</a> that agree a time and book a Zoom meeting</li>
  <li><a href="/kudos/">Peer recognition</a> with a daily allowance and your own emoji</li>
  <li><a href="/insights/">Insights</a> across both datasets</li>
  <li><a href="/celebrations/">Birthdays and work anniversaries</a> in a channel, from a member
  profile that keeps day and month only</li>
  <li>Signed webhooks, automation rules, an MCP server, CSV export, a Helm chart</li>
</ul>
<p>Every one of those is in the repository. There is no paid tier holding anything back, and
<a href="/slack-standup-bot/">what the bot does inside Slack</a> is the same whether you run the
published image or your own build of it.</p>

<h2 id="who-maintains-it">Who maintains it</h2>
<p>It is built and maintained by Anmol Nagpal and sponsored by CloudDrove, who run the free hosted
instance and also sell setup and hosting on your own infrastructure. Paid work funds the
project; it does not gate any of it. Issues and pull requests go to the same repository the releases
are cut from, and the Helm chart is published from it too.
<a href="/blog/why-i-built-morgenruf/">The weekend that produced it</a> explains why it is arranged
this way.</p>
<p>If that arrangement ends tomorrow, you keep the source, the chart and your own database. That is
the whole point of the licence, and it is worth checking a project can say the same before you put
a daily ritual on it.</p>

<h2 id="other-options">Other open-source options</h2>
<p>There are a few self-hosted standup tools around, mostly smaller scripts that post a message and
collect replies. They are fine for one team and one question set. The things that usually run out
are per-person timezones, vacation handling, a dashboard non-engineers will use, and anything beyond
standups. Pick by which of those you need rather than by star count. Against the hosted products,
<a href="/compare/">the comparison pages</a> are the more useful read.</p>

{shot("/screenshots/members.jpg", "Member cards in the dashboard showing which features each person runs", "Per-feature admin grants, so the team lead runs standups without holding the API keys.")}

<h2 id="getting-started">Getting started</h2>
<p><a href="/setup/">The setup guides</a> cover Docker Compose, Kubernetes and the Slack app. The
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
         "It is built and maintained by Anmol Nagpal and sponsored by CloudDrove, who also offer paid "
         "setup and hosting. Paid work "
         "funds it but never gates it."),
        ("What if the project stops?",
         "You have the source and your database. That is the point of the arrangement."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About the open-source side</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/open-source-standup-bot/",
                title="Open-source Slack standup bot, MIT licensed",
                description="An MIT-licensed Slack standup bot: one repository, no open-core split, "
                            "no paid tier. Read the source, fork it, and keep running it if the "
                            "project stops.",
                h1="An open-source standup bot: MIT, one repository, no paid tier",
                lede="What the licence covers, who maintains it, and what you are left holding if "
                     "the project ever stops. The hosting question has its own page.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Open-source standup bot", None)],
        define='Morgenruf is an open-source Slack standup bot under the MIT licence: one public repository, no open-core split and no paid tier. It asks standup questions by DM and posts one summary, and also runs coffee chats and kudos. Use the free hosted instance, or run the same code yourself.')


def self_hosted():
    prose = f'''{project_facts()}
<h2 id="why-teams-self-host-this">Why teams self-host a standup bot</h2>
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

{diagrams.architecture("Where the answers physically sit when you self-host: your Postgres, in the region you chose.")}

<h2 id="what-running-it-involves">What running it actually involves</h2>
<ul>
  <li><strong>Two small containers.</strong> A Python backend and a frontend that serves the
  dashboard. No queue and no worker pool. The Helm chart adds a small Redis that keeps
  in-progress standups across restarts.</li>
  <li><strong>One database.</strong> Postgres 13 or newer. Migrations run as a separate step before
  the app starts: a one-shot service in Compose, an init container in Helm.</li>
  <li><strong>An HTTPS URL.</strong> Slack posts events to it. A Cloudflare tunnel is enough and
  needs no open port.</li>
  <li><strong>Upgrades.</strong> Pull the image and restart, or <code>helm upgrade</code>.</li>
  <li><strong>Backups.</strong> <code>pg_dump</code>. There is no other state.</li>
</ul>

<h2 id="what-leaves-your-network">What leaves your network</h2>
<p>A self-hosted install talks to Slack only, plus Zoom, email (Resend), an AI provider or PostHog
analytics if the operator turns those on. By default that means <code>slack.com</code>: the app
calls it to read channel membership, open DMs and post the summary, and Slack calls your HTTPS URL
back with events. Answers, blockers, participation, coffee chat pairings and kudos are written to
your Postgres. There is no licence check. Each optional service stays silent until you configure
it: Zoom when someone links an account for coffee chats, Resend when you set up digest email, an AI
provider when you add a key for summaries, and PostHog when you set a PostHog key. You can watch
that on the egress rules, and since it is
<a href="/open-source-standup-bot/">MIT licensed and readable end to end</a> you can check the
claim rather than take it.</p>
<p>Which makes the residency answer short. The data lives in the region your database lives in,
under the retention your backups already have, and a deletion or subject access request is a query
against a schema you own.</p>

<h2 id="what-it-costs">What it costs</h2>
<p>A small VPS and a managed Postgres, or nothing extra if you already run both. There is no seat
component at any size, which is the whole economic argument: the difference between hosted and
self-hosted grows with your headcount, not with your usage.
<a href="/compare/">What the hosted standup bots charge per person</a> is on the comparison pages, if
you want to do the arithmetic for your own team.</p>

<h2 id="where-it-runs">Where it runs</h2>
<ul>
  <li><a href="/setup/kubernetes/">Kubernetes</a> with the published Helm chart, ingress, HTTPRoute or
  a tunnel</li>
  <li><a href="/setup/docker/">Docker Compose</a> on a VPS, a homelab box or a spare Mac mini</li>
  <li>Anywhere else a container and a Postgres can live</li>
</ul>
<p>The same image and the same database either way. <a href="/setup/">Every way of running it</a> is
written up step by step, and the choice is mostly about what your team already operates.</p>

{shot("/screenshots/standups.jpg", "Standups in the dashboard with completion sparklines", "The dashboard runs on your own domain, behind your own auth.")}

<h2 id="the-part-people-underestimate">The part people underestimate</h2>
<p>Not the install. The Slack app: scopes, a redirect URL, and the fact that a workspace which
installed before a feature existed has not granted that feature's scopes.
<a href="/setup/slack-app/">That page</a> exists because it is where setups actually stall. It helps
to read <a href="/slack-standup-bot/">what the bot does inside Slack</a> first, because the scopes
follow from it and half of them are for features you may not switch on. If you would rather hand
the whole job over, <a href="/support/">CloudDrove does paid setup and hosting</a> on your own
infrastructure.</p>'''
    body = guide(prose, [("Why teams self-host", "why-teams-self-host-this"),
                         ("What running it involves", "what-running-it-involves"),
                         ("What leaves your network", "what-leaves-your-network"),
                         ("What it costs", "what-it-costs"), ("Where it runs", "where-it-runs"),
                         ("The underestimated part", "the-part-people-underestimate")])
    faq_html, faq_schema = faq([
        ("What are the minimum requirements?",
         "Two small containers (backend and frontend) and a Postgres. A single vCPU with 512MB is enough for a team of "
         "dozens; the work is bursty and short."),
        ("Does it need a public IP?",
         "No. A Cloudflare tunnel gives Slack an HTTPS URL without opening a port or running an "
         "ingress controller."),
        ("How do upgrades work?",
         "Pull the new image and restart. Migrations run in an init container before the app starts, "
         "and are written to be safe against a live database."),
        ("Is there a hosted version?",
         "Yes. Add to Slack installs Morgenruf on a free hosted instance run by CloudDrove, in about "
         "two minutes. This page is about the other route: the same MIT code on your own servers."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About self-hosting</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/self-hosted-standup-bot/",
                title="Self-hosted standup bot: where your data lives",
                description="Run the standup bot on your own servers: two small containers, one Postgres, "
                            "one HTTPS URL. Docker or Kubernetes, in your region, answers in your "
                            "own database.",
                h1="A standup bot on your own servers, in your own region",
                lede="Two small containers, one database, one HTTPS URL Slack can reach. Where the answers "
                     "physically sit, and what it takes to keep them there.",
                body=body, schema=[faq_schema],
                trail=[("Home", "/"), ("Self-hosted standup bot", None)],
        define='Morgenruf is a self-hostable Slack standup bot: a backend, a small frontend and a Postgres database, deployed with Docker Compose or Helm, with every answer stored in a database you control. It is MIT licensed and free, and the same code also runs as a free hosted instance for teams that would rather not run it.')


def slack_bot():
    prose = f'''<h2 id="what-it-does-in-slack">What a Slack standup bot does, and what this one does</h2>
<p>A standup bot asks each person the same few questions every working morning and puts the answers
somewhere the team will actually read them. That is the whole category. Morgenruf does it entirely
inside Slack: a direct message at your local hour, a summary in the channel an hour later, and
nothing to log into. The dashboard is for whoever sets it up, and most weeks they do not open it
either.</p>
<p>This page is the general one. The two questions that follow it usually are the licence and the
hosting, which have pages of their own:
<a href="/open-source-standup-bot/">what the MIT licence covers</a> and
<a href="/self-hosted-standup-bot/">where the container and the database end up</a>.</p>
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

{diagrams.standup_flow("Everything a teammate sees happens in Slack: the DM, the nudge if they are late, and the summary.")}

<h2 id="the-scopes-it-asks-for">The scopes it asks for</h2>
<p>Standups need to read channel membership, write messages, and open DMs. Coffee chats add three
scopes for group DMs and timezones. Kudos needs emoji read access to use your own token. There is no
scope for reading channel history, because it never does.
<a href="/setup/slack-app/">Every scope, with the reason</a>.</p>

{shot("/screenshots/coffee-chat-settings.jpg", "Coffee chat settings with a live preview of the Slack message", "The settings page shows the Slack message it will produce, as you edit it.")}

<h2 id="what-it-is-not">What it is not</h2>
<ul>
  <li>Not a meeting recorder or a transcript bot.</li>
  <li>Not a productivity score. There is no ranking of people by output.</li>
  <li>Not something you have to run. The hosted instance is free; self-hosting is the option for
  teams that want the data in their own database.</li>
</ul>

<h2 id="adding-it">Adding it to your workspace</h2>
<p>The quick way is the Add to Slack button: it installs Morgenruf on the free hosted instance in
about two minutes. To self-host, create the app from the manifest, install it, invite the bot to a
channel, and make your first standup. <a href="/setup/">That route is about twenty minutes.</a>
Either way, the ten minutes after that go
on <a href="/standups/">the standup itself</a>: questions, hour, timezones, who is in it, what
happens when someone is on leave. If you are still deciding,
<a href="/compare/">how this lines up against the hosted standup bots</a> is the page for that.</p>'''
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
         "channel history scope."),
        ("What about Microsoft Teams or Google Chat?",
         "Google Chat is in beta; Teams as a platform is planned, not started. Slack is first class."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>About the Slack app</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/slack-standup-bot/",
                title="Free Slack standup bot: DMs, summaries, commands",
                description="A Slack standup bot that DMs each person their questions at their own "
                            "local hour and posts one summary to the channel. Slash commands, App "
                            "Home, MIT.",
                h1="A Slack standup bot, from the morning DM to the summary",
                lede="Questions by DM at each person's local hour, one summary in the channel, "
                     "slash commands and an App Home tab. Nobody opens a dashboard to take part.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing the morning's answers and blockers", "The dashboard is for whoever runs it. Everyone else stays in Slack.", lazy=False),
                trail=[("Home", "/"), ("Slack standup bot", None)],
        define='Morgenruf is a free Slack standup bot. It DMs each person your questions at their local hour, posts one summary to the channel, and adds slash commands and an App Home tab. It is open source (MIT), free on a hosted instance or self-hosted, and also runs coffee chats and kudos.')


# DailyBot and Standuply figures were read on their own pricing pages on this
# date. Standuply's prices are in the page source rather than the rendered
# text. Re-check both before changing a number.
CHECKED_2 = "2026-09-29"

DAILYBOT_ROWS = [
    ("Async standups by DM, one channel summary", "Yes", "yes", "Yes", "yes"),
    ("Kudos and recognition", "Yes", "yes", "Yes", "yes"),
    ("Coffee chat introductions", "Yes", "yes", "No", "no"),
    ("Forms and surveys", "No", "no", "Yes", "yes"),
    ("Chat apps", "Slack; Google Chat in beta", "", "Slack, Google Chat, Microsoft Teams, Discord",
     "yes"),
    ("Free plan", "Yes, any team size, no report cap", "yes",
     "Unlimited members, 50 compiled check-in reports a month, 14 days of history", ""),
    ("Price above the free plan", "None", "yes",
     "$3 or $6.50 per active user monthly, $2.40 or $5 billed annually", "no"),
    ("A 30 person team on the entry paid plan, per year", "$0 hosted", "yes", "$864 to $1,080", "no"),
    ("Runs on your own servers", "Yes", "yes", "No", "no"),
    ("Source you can read", "MIT, the whole app", "yes", "Closed; some side tools are MIT", "no"),
]


def dailybot():
    from compare_pages import table
    dailybot_table = table(DAILYBOT_ROWS, "DailyBot")
    prose = f'''<h2 id="what-you-are-actually-comparing">What you are actually comparing</h2>
<p>DailyBot is a hosted check-in and standup assistant that works across Slack, Google Chat,
Microsoft Teams and Discord, with AI reports, forms, kudos and workflow automation on top. Morgenruf
does the standup, plus coffee chats and recognition, for nothing per seat: free on the hosted
instance CloudDrove runs, or on your own infrastructure with the same MIT code.</p>
<p>The decision usually comes down to two things: which chat apps your company uses, and whether
you want a bill that grows with every active user. The same question applies to Geekbot and
Standup &amp; Prosper, which <a href="/compare/">the comparison pages</a> work through.</p>

{diagrams.standup_flow("The standup a DailyBot team already runs: a DM at each local hour, a private nudge, one summary.")}

<h2 id="side-by-side">How do Morgenruf and DailyBot compare?</h2>
{dailybot_table}
<p class="shot-cap" style="margin-top:12px">DailyBot plans and prices checked {CHECKED_2} on
<a href="https://www.dailybot.com/pricing">DailyBot's pricing page</a>, chat apps and features on
<a href="https://www.dailybot.com/">its homepage</a>. If something here is out of date, please
<a href="{REPO}/issues/new/choose">open an issue</a>.</p>

<h2 id="where-dailybot-wins">Where DailyBot wins</h2>
<ul>
  <li><strong>More chat apps.</strong> Slack, Google Chat, Microsoft Teams and Discord. If part of
  the company lives outside Slack, that settles it.</li>
  <li><strong>Forms, surveys and workflows.</strong> DailyBot does more than the morning check-in:
  forms, mood tracking, workflow automation and an AI assistant.</li>
  <li><strong>Nothing to run.</strong> No server, no database, no upgrade evenings.</li>
  <li><strong>A free plan with no member limit.</strong> The cap is on usage instead: 50 compiled
  check-in reports a month across the organisation, and 14 days of history.</li>
</ul>

<h2 id="where-this-is-different">Where is Morgenruf different from DailyBot?</h2>
<h3>No usage cap and no seat price</h3>
<p>DailyBot's free Starter plan allows 50 compiled check-in reports a month for the whole
organisation. Above that, Essentials is $3 per active user a month, or $2.40
billed annually, and Advanced is $6.50, or $5 billed annually (checked {CHECKED_2} on
<a href="https://www.dailybot.com/pricing">DailyBot's pricing page</a>). DailyBot counts an active
user by seat status, not by whether they used it that month. On the Morgenruf hosted instance there
is no report cap and no seat price at any size.</p>

<h3>History you keep</h3>
<p>The free DailyBot plan keeps 14 days of history. Morgenruf keeps every answer, and self-hosted it
keeps them in your own Postgres for as long as your backups do.</p>

<h3>Coffee chats in the same app</h3>
<p>DailyBot has kudos; Morgenruf has <a href="/kudos/">kudos</a> too, and adds
<a href="/coffee-chats/">coffee chats</a> that pair people and book the meeting, all in one
database, which is what makes the <a href="/insights/">cross-signal questions</a> possible.</p>

<h3>The whole app is open source</h3>
<p>DailyBot publishes some side tools under MIT, but the product itself is closed. Morgenruf is MIT
end to end: the bot, the dashboard and the Helm chart.</p>

{shot("/screenshots/standups.jpg", "Two standups in the dashboard, each with a completion sparkline and a health badge", "A standup that is quietly dying says so here before anyone notices in the channel.")}

<h2 id="what-dailybot-costs">What does DailyBot cost for 10, 30 or 100 people?</h2>
<p>Worked out from DailyBot's published Essentials price on {CHECKED_2}, per year, for teams that
have outgrown the free plan's report cap. Advanced costs a little over twice as much.</p>
<div class="scroll-x"><table>
<thead><tr><th>Team size</th><th>DailyBot Essentials, monthly</th><th>DailyBot Essentials, annual</th><th class="us">Morgenruf, hosted</th><th class="us">Morgenruf, self-hosted</th></tr></thead>
<tbody>
<tr><td>10 people</td><td>$360</td><td>$288</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>30 people</td><td>$1,080</td><td>$864</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>100 people</td><td>$3,600</td><td>$2,880</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
</tbody></table></div>

<h2 id="moving-across">Moving across from DailyBot</h2>
<p>There is no importer. Run both for a week with the same questions in the same channel, and turn
DailyBot off once the new summary looks right.</p>
<ol>
  <li>Write down each DailyBot check-in: its channel, questions, schedule, participants and
  timezone.</li>
  <li>Install Morgenruf: <a href="{INSTALL}">Add to Slack</a> for the free hosted instance, or
  <a href="/setup/docker/">run it with Docker</a> or <a href="/setup/kubernetes/">on Kubernetes</a>
  and <a href="/setup/slack-app/">create the Slack app</a>.</li>
  <li>Recreate each standup. <a href="/blog/standup-questions/">Thirty question templates</a> are
  there if you want to change the questions while you are at it.</li>
  <li>Mark anyone on leave, so the first week's completion figure means something.</li>
  <li>Watch a week of mornings side by side, then switch DailyBot off.</li>
</ol>'''
    body = guide(prose, [("What you are comparing", "what-you-are-actually-comparing"),
                         ("Side by side", "side-by-side"),
                         ("Where DailyBot wins", "where-dailybot-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What DailyBot costs", "what-dailybot-costs"),
                         ("Moving across", "moving-across")])
    faq_html, faq_schema = faq([
        ("Is DailyBot free?",
         "It has a free Starter plan with unlimited members, capped at 50 compiled check-in reports a "
         "month and 14 days of history. Paid plans are $3 or $6.50 per active user a month, or $2.40 "
         f"or $5 billed annually (checked {CHECKED_2})."),
        ("Is Morgenruf free compared with DailyBot?",
         "Yes, with no seat price and no report cap. The hosted instance is free. Self-hosted, you pay "
         "for the server and database, roughly $5 to $20 a month regardless of headcount."),
        ("Does Morgenruf work in Microsoft Teams or Discord?",
         "No. Slack is first class, Google Chat is in beta, and Teams is planned, not started. If you need "
         "Teams or Discord today, DailyBot is the better fit."),
        ("Can I import my DailyBot history?",
         "No. Run both in parallel for a week and switch over once the summaries look right."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Morgenruf and DailyBot</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/dailybot-alternative/",
                title="Free, open-source DailyBot alternative for Slack",
                description="A free, MIT-licensed DailyBot alternative for async Slack standups: no "
                            "report cap, no per-user price, coffee chats and kudos included. Hosted "
                            "free or self-hosted.",
                h1="A free, open-source DailyBot alternative for Slack",
                lede=f"Verdict: DailyBot charges $3 per active user a month once you pass its free "
                     f"plan's 50 reports (checked {CHECKED_2}), while Morgenruf runs the same Slack "
                     f"standup free at any size, so pick DailyBot only if you need Teams, Discord or "
                     f"its forms.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing who answered, who is blocked and recent recognition", "Your morning, on one screen.", lazy=False),
                trail=[("Home", "/"), ("Compare", "/compare/"), ("vs DailyBot", None)],
                og="dailybot-alternative", reviewed=CHECKED_2,
                define=f'Morgenruf is a free, open-source (MIT) DailyBot alternative for Slack. Like DailyBot, it sends each person standup questions by DM and posts one summary to a channel. Unlike DailyBot (free for 50 compiled reports a month, then $3 per active user per month, checked {CHECKED_2}), it has no report cap or seat price, can run on your own servers, and adds coffee chats.')


STANDUPLY_ROWS = [
    ("Async standups by DM, one channel summary", "Yes", "yes", "Yes", "yes"),
    ("Video and voice answers", "No", "no", "Yes", "yes"),
    ("Surveys", "No", "no", "Yes", "yes"),
    ("Coffee chats and kudos in the same app", "Yes", "yes", "No", "no"),
    ("Chat apps", "Slack; Google Chat in beta", "", "Slack, Microsoft Teams", "yes"),
    ("Free plan", "Yes, any team size", "yes", "Starter: automation for 3 users", "no"),
    ("Price above the free plan", "None", "yes",
     "Team $2 to $3.50 per user monthly, Business $4 to $5.50, less billed annually", "no"),
    ("A 30 person team on Team, per year", "$0 hosted", "yes", "$900 to $1,260", "no"),
    ("Runs on your own servers", "Yes", "yes", "No", "no"),
    ("Source you can read", "MIT", "yes", "Closed", "no"),
]


def standuply():
    from compare_pages import table
    standuply_table = table(STANDUPLY_ROWS, "Standuply")
    prose = f'''<h2 id="what-you-are-actually-comparing">What you are actually comparing</h2>
<p>Standuply is a hosted standup bot for Slack and Microsoft Teams with some extras most bots do not
have: answers by video or voice, surveys, and on its Business plan planning poker, backlog
refinement and 360 degree feedback. Morgenruf does the async standup, plus coffee chats and
recognition, for nothing per seat: free on the hosted instance CloudDrove runs, or on your own
infrastructure with the same MIT code.</p>
<p>If your team answers standups on video or runs its agile ceremonies through the bot, Standuply
does things this does not. If it is three written questions a morning, the difference is mostly the
bill. <a href="/compare/">The other comparisons</a> make the same trade for Geekbot, DailyBot and
Standup &amp; Prosper.</p>

{diagrams.standup_flow("The written standup both tools run: a DM at each local hour, a private nudge, one summary.")}

<h2 id="side-by-side">How do Morgenruf and Standuply compare?</h2>
{standuply_table}
<p class="shot-cap" style="margin-top:12px">Standuply plans and prices checked {CHECKED_2} on
<a href="https://standuply.com/pricing">Standuply's pricing page</a> (the figures are in the page
source; the price shown depends on the team size you pick), chat apps and features on
<a href="https://standuply.com/">its homepage</a>. If something here is out of date, please
<a href="{REPO}/issues/new/choose">open an issue</a>.</p>

<h2 id="where-standuply-wins">Where Standuply wins</h2>
<ul>
  <li><strong>Video and voice answers.</strong> Standuply lets people answer by video or voice
  message. Morgenruf is text only.</li>
  <li><strong>Microsoft Teams.</strong> Standuply runs there today; Teams support here is planned,
  not started.</li>
  <li><strong>Agile extras.</strong> Surveys, and on the Business plan planning poker, backlog
  refinement and 360 degree feedback.</li>
  <li><strong>Integrations.</strong> Standuply connects to Jira, Trello and Asana, and its Team plan
  adds GitHub, GitLab and Bitbucket.</li>
  <li><strong>A flat fee option.</strong> Team is also sold at $199 a month, or $149 billed
  annually, for up to 199 people, which caps the bill for a large company.</li>
</ul>

<h2 id="where-this-is-different">Where is Morgenruf different from Standuply?</h2>
<h3>Free for the whole team, not three people</h3>
<p>Standuply's free Starter plan covers automation for 3 users, then there is a 30 day trial of the
paid plans. Team costs $2 per user a month for 1 to 4 users, $3 for 5 to 29 and $3.50 from 30,
or $1.50, $2.25 and $2.50 billed annually. Business is $4, $5 and $5.50, or $3.50, $4.25 and $4.50
billed annually (checked {CHECKED_2} on <a href="https://standuply.com/pricing">Standuply's pricing
page</a>). On the Morgenruf hosted instance, every seat is free at any size.</p>

<h3>Your answers stay in your database</h3>
<p>Self-hosted, standup answers, blockers and participation live in Postgres you control. Standuply
is hosted only.</p>

<h3>Three rituals, one app</h3>
<p>Standups, <a href="/coffee-chats/">coffee chats</a> and <a href="/kudos/">kudos</a> share one
deployment and one database, which is also what makes the
<a href="/insights/">cross-signal questions</a> possible.</p>

<h3>It can be read and changed</h3>
<p>MIT licensed, the whole repository. If the summary format is wrong for you, the file is right
there.</p>

{shot("/screenshots/standups.jpg", "Two standups in the dashboard, each with a completion sparkline and a health badge", "A standup that is quietly dying says so here before anyone notices in the channel.")}

<h2 id="what-standuply-costs">What does Standuply cost for 10, 30 or 100 people?</h2>
<p>Worked out from Standuply's published Team prices on {CHECKED_2}, per year. At 100 people the
flat fee is cheaper than paying per user, so that is the figure shown.</p>
<div class="scroll-x"><table>
<thead><tr><th>Team size</th><th>Standuply Team, monthly</th><th>Standuply Team, annual</th><th class="us">Morgenruf, hosted</th><th class="us">Morgenruf, self-hosted</th></tr></thead>
<tbody>
<tr><td>10 people</td><td>$360</td><td>$270</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>30 people</td><td>$1,260</td><td>$900</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
<tr><td>100 people</td><td>$2,388 (flat fee)</td><td>$1,788 (flat fee)</td><td class="us yes">$0</td><td class="us">$60 to $240</td></tr>
</tbody></table></div>

<h2 id="moving-across">Moving across from Standuply</h2>
<p>There is no importer. Run both for a week with the same questions in the same channel, and turn
Standuply off once the new summary looks right.</p>
<ol>
  <li>Write down each Standuply standup: its channel, questions, schedule, participants and
  timezone.</li>
  <li>Install Morgenruf: <a href="{INSTALL}">Add to Slack</a> for the free hosted instance, or
  <a href="/setup/docker/">run it with Docker</a> or <a href="/setup/kubernetes/">on Kubernetes</a>
  and <a href="/setup/slack-app/">create the Slack app</a>.</li>
  <li>Recreate each standup. <a href="/blog/standup-questions/">Thirty question templates</a> are
  there if you want to change the questions while you are at it.</li>
  <li>Mark anyone on leave, so the first week's completion figure means something.</li>
  <li>Watch a week of mornings side by side, then switch Standuply off.</li>
</ol>'''
    body = guide(prose, [("What you are comparing", "what-you-are-actually-comparing"),
                         ("Side by side", "side-by-side"),
                         ("Where Standuply wins", "where-standuply-wins"),
                         ("Where this is different", "where-this-is-different"),
                         ("What Standuply costs", "what-standuply-costs"),
                         ("Moving across", "moving-across")])
    faq_html, faq_schema = faq([
        ("Is Standuply free?",
         "Its free Starter plan covers automation for 3 users, and paid plans have a 30 day trial. "
         "Team costs $2 to $3.50 per user a month depending on team size, or $1.50 to $2.50 billed "
         f"annually (checked {CHECKED_2})."),
        ("Is Morgenruf free compared with Standuply?",
         "Yes, for every seat. The hosted instance is free. Self-hosted, you pay for the server and "
         "database, roughly $5 to $20 a month regardless of headcount."),
        ("Can people answer by video or voice?",
         "Not in Morgenruf. Answers are written in Slack. If video or voice answers matter to your "
         "team, Standuply does that."),
        ("Can I import my Standuply history?",
         "No. Run both in parallel for a week and switch over once the summaries look right."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2>Morgenruf and Standuply</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(path="/standuply-alternative/",
                title="Free, open-source Standuply alternative for Slack",
                description="A free, MIT-licensed Standuply alternative for async Slack standups, "
                            "with coffee chats and kudos in the same app and no per-user price. "
                            "Hosted free or self-hosted.",
                h1="A free, open-source Standuply alternative for Slack",
                lede=f"Verdict: Standuply is free for 3 users and then $2 to $3.50 per user a month "
                     f"on Team (checked {CHECKED_2}), while Morgenruf runs written Slack standups free "
                     f"at any size, so stay on Standuply only for video answers, Teams or its agile "
                     f"extras.",
                body=body, schema=[faq_schema],
                hero=shot("/screenshots/today.jpg", "The Today page showing who answered, who is blocked and recent recognition", "Your morning, on one screen.", lazy=False),
                trail=[("Home", "/"), ("Compare", "/compare/"), ("vs Standuply", None)],
                og="standuply-alternative", reviewed=CHECKED_2,
                define=f'Morgenruf is a free, open-source (MIT) Standuply alternative for Slack. Both send standup questions by DM and post a summary to a channel. Standuply is free for 3 users, then $2 to $3.50 per user per month on Team (checked {CHECKED_2}); Morgenruf is free at any size, can run on your own servers, and adds coffee chats and kudos.')
