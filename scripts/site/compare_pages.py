"""Comparison pages.

Written to be useful to somebody weighing the choice, including the cases where
the answer is "keep paying them". A comparison page that says the competitor is
bad at everything convinces nobody and ranks badly, because people bounce.
"""

from __future__ import annotations

from shell import (CTA_NOTE, INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, definition, faq,
                   footer, head, nav, webpage_schema)


def page(*, path, title, description, h1, lede, body, schema=(), trail=(), current="/compare/",
         define=""):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = list(schema) + ([crumb_schema] if crumb_schema else []) + [webpage_schema(path, title)]
    return (head(title=title, description=description, path=path, schema=schemas)
            + nav(current) + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="head-cta">
    <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
    <a class="btn btn-line" href="/setup/">Self-host in about 20 minutes</a>
  </div>
  {CTA_NOTE}
</div></header>
{definition(define) if define else ""}{body}
</main>''' + cta_band() + footer())


def table(rows, them):
    head_row = f'<thead><tr><th></th><th class="us">Morgenruf</th><th>{them}</th></tr></thead>'
    body = "".join(
        f'<tr><td>{label}</td><td class="us {a_cls}">{a}</td><td class="{b_cls}">{b}</td></tr>'
        for label, a, a_cls, b, b_cls in rows)
    return f'<div class="scroll-x"><table>{head_row}<tbody>{body}</tbody></table></div>'


HONEST = '''<div class="note"><p><strong>Where they win.</strong> %s</p></div>'''


def donut():
    rows = [
        ("Random pairings from a channel", "Yes", "yes", "Yes", "yes"),
        ("Avoids repeat matches", "Yes", "yes", "Yes", "yes"),
        ("Suggests a time both people can make", "Yes, voted on in the message", "yes", "Varies", "no"),
        ("Creates the meeting", "Zoom, at the agreed hour", "yes", "Varies by plan", "no"),
        ("Async standups in the same app", "Yes", "yes", "No", "no"),
        ("Peer recognition in the same app", "Yes", "yes", "Shoutouts", "yes"),
        ("Birthdays and work anniversaries", "Yes, around your working days and holidays", "yes",
         "Yes", "yes"),
        ("Runs on your own servers", "Yes", "yes", "No", "no"),
        ("Source you can read", "MIT", "yes", "Closed", "no"),
        ("Your pairing data lives in", "your database", "yes", "their cloud", "no"),
        ("Microsoft Teams", "In progress", "no", "Yes", "yes"),
        ("Price", "Free, any team size", "yes", "Free plan; paid plans from about $74 a month", ""),
    ]
    body = f'''<section class="section"><div class="wrap">
{table(rows, "Donut")}
<p class="shot-cap" style="margin-top:12px">Prices checked 2026-09-26 against
<a href="https://www.donut.com/pricing/">Donut's pricing page</a>. Their plans change; if something
here is out of date, please
<a href="{REPO}/issues/new/choose">tell me and I will fix it</a>.</p>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
<h2 id="the-honest-version">The honest version</h2>
<p>Donut is a good product and the one that made this category. It has years of polish, a Teams
version that works today, and a wider surface than this: journeys for onboarding, channel prompts,
video facilitation.</p>
{HONEST % ("If you need Microsoft Teams today, or onboarding journeys, or a video facilitation layer, "
           "Donut is the better answer and you should use it.")}

<h2 id="where-this-is-different">Where this is different</h2>
<h3>It is one app, not three subscriptions</h3>
<p>Most teams that pay for pairing also pay for standups and recognition. Morgenruf runs all three
against one database, which is also what makes the cross-signal questions possible: who answers
every standup and is thanked by nobody.</p>

<h3>Birthdays and work anniversaries, too</h3>
<p>Donut celebrates birthdays and anniversaries, and so does Morgenruf: posted in a channel you
pick, grouped into one message per kind a day, and moved to the last working day before a weekend
or a company holiday on your own list. Only the day and month of a birthday are kept, and anyone can
opt out with one checkbox. Donut imports dates straight from an HRIS; here HR uploads a CSV export
instead. <a href="/celebrations/">Celebrations</a> has the details.</p>

<h3>The introduction carries a meeting</h3>
<p>Two people being told to meet is the easy part. This proposes hours that fall inside both working
days, each of them presses one, and a matching pair becomes a Zoom meeting at that hour, hosted on
the account of whoever connected theirs.</p>

<h3>Your data stays yours</h3>
<p>Self-hosted, who met whom and who quietly opted out lives in Postgres you control. The install
talks to Slack only, plus Zoom, email (Resend), an AI provider or PostHog analytics if the operator
turns those on. Leaving is not a migration because the data is already yours.</p>

<h3>The price</h3>
<p>Free for every seat, at any size: on the free hosted instance, or self-hosted, where a thirty
person team pays for a small server and a database instead of a subscription that grows with
hiring.</p>

<h2 id="for-people-teams">For people teams: nothing to install on a server</h2>
<p>Add to Slack puts Morgenruf on the free hosted instance, so a people ops lead can start coffee
chats without anyone running a server. Each round closes by asking whether the pair met, and the
answer is recorded four ways: met, did not meet, never replied, and never delivered. If your company
needs the data in-house, this is the line to forward to engineering: "Morgenruf is one container
and a Postgres, MIT licensed, about twenty minutes to set up: morgenruf.dev/setup/".</p>

<h2 id="switching">Switching</h2>
<p>There is no importer, and pairing history is the one thing worth not losing, so the sensible move
is to run both for a fortnight: point Morgenruf at the same channel with a different cadence, see
whether the introductions land, then turn Donut off. Nothing here needs a contract to be cancelled.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq([
        ("Is Morgenruf a drop-in Donut replacement?",
         "For random pairings from a Slack channel, yes. For Teams, journeys or Gatheround's video "
         "facilitation, no, and pretending otherwise would waste your afternoon."),
        ("Can I import our Donut history?",
         "No. Run both for a couple of weeks instead and let the new pairings build their own history."),
        ("Does Morgenruf do birthdays and work anniversaries like Donut?",
         "Yes. Celebrations posts both in a channel, on the last working day before any weekend or "
         "company holiday, from dates people add themselves or HR imports as a CSV. Birthdays are "
         "day and month only. It has no weekly or monthly roundups."),
        ("Does it need Zoom?",
         "No. Without it a pairing uses whatever room link you set on the programme, or none. Zoom "
         "only adds a real meeting at the agreed hour."),
        ("What does it cost for 200 people?",
         "Nothing per seat. On the hosted instance, nothing at all. Self-hosted, the server and "
         "database you run it on, which for 200 people is a small instance."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="morgenruf-and-donut">Morgenruf and Donut</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/donut-alternative/",
        title="Free, open-source Donut alternative for Slack coffee chats",
        description="A free Donut alternative for random coffee chats in Slack, plus standups and "
                    "kudos in the same app. MIT licensed, no per-seat fee, hosted or self-hosted.",
        h1="A free, open-source Donut alternative for Slack",
        lede="Random introductions from a channel, a time both people actually pick, and the meeting "
             "booked at that hour. Plus standups and kudos in the same app.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Compare", "/compare/"), ("vs Donut", None)],
        define='Morgenruf is a free, open-source (MIT) Donut alternative for Slack coffee chats. It pairs people from a channel, suggests hours both can make, and books the Zoom meeting. Donut has a free plan and paid plans from about $74 a month (checked 2026-09-26); Morgenruf is free at any size, hosted or self-hosted.')


def heytaco():
    rows = [
        ("Peer recognition in Slack", "Yes", "yes", "Yes", "yes"),
        ("Daily allowance that resets", "Yes, midnight in each timezone", "yes", "Yes", "yes"),
        ("Your own emoji as the token", "Yes", "yes", "Tacos", "no"),
        ("Leaderboards for giving", "Yes", "yes", "Yes", "yes"),
        ("Rewards catalogue and gift cards", "No", "no", "Yes", "yes"),
        ("Async standups in the same app", "Yes", "yes", "No", "no"),
        ("Coffee chat introductions", "Yes", "yes", "No", "no"),
        ("Runs on your own servers", "Yes", "yes", "No", "no"),
        ("Source you can read", "MIT", "yes", "Closed", "no"),
        ("Microsoft Teams", "In progress", "no", "Yes", "yes"),
        ("Price", "Free, any team size", "yes", "Per seat, monthly", "no"),
    ]
    body = f'''<section class="section"><div class="wrap">
{table(rows, "HeyTaco")}
<p class="shot-cap" style="margin-top:12px">Checked against HeyTaco's public pages in September 2026.</p>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
<h2 id="the-honest-version">The honest version</h2>
<p>HeyTaco is the best-known recognition bot for a reason: the taco is a genuinely good piece of
product design, the gamification is thought through, and the rewards side is a real programme rather
than a leaderboard.</p>
{HONEST % ("If you want a rewards catalogue, gift cards, or a recognition programme with a budget "
           "attached, HeyTaco does that and Morgenruf does not. Do not switch and then discover it.")}

<h2 id="where-this-is-different">Where this is different</h2>
<h3>Recognition is one of three things it does</h3>
<p>Standups, coffee chats and kudos in one app, one database, one deployment. Teams rarely want only
one of the three, and three subscriptions is how most of them end up.</p>

<h3>The token is yours</h3>
<p>Any emoji in your workspace. A maple leaf, your logo, an in-joke. The Morgenruf icon imports as a
custom emoji and the bot picks it up on its own.</p>

<h3>Recognition data next to something else</h3>
<p>A leaderboard tells you who is thanked. Put it beside standup answers and you can ask who is
contributing and being thanked by nobody, which is the question worth acting on.</p>

<h3>Nothing for HR to install</h3>
<p>Add to Slack puts Morgenruf on the free hosted instance, so whoever runs recognition can switch
kudos on without an engineer. If the data has to stay in-house, the self-hosted route is one
container and a Postgres; <a href="/setup/">the setup page</a> is the link to forward.</p>

<h3>The price, again</h3>
<p>Free for every seat, hosted or self-hosted. Recognition tools are usually priced per person per
month, which means the cost of thanking people grows exactly as you hire them.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq([
        ("Does Morgenruf do rewards or gift cards?",
         "No. Recognition here is a public message and a leaderboard. If you need a catalogue, "
         "HeyTaco or Bonusly is the right tool."),
        ("Can we keep our taco?",
         "You can use any emoji in your workspace as the token, including a taco, though that is "
         "somebody else's brand. A maple leaf is the default joke here."),
        ("Can I import our recognition history?",
         "No importer today. Leaderboards start fresh, which some teams treat as a feature."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="morgenruf-and-heytaco">Morgenruf and HeyTaco</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/heytaco-alternative/",
        title="Free, open-source HeyTaco alternative for Slack kudos",
        description="A free HeyTaco alternative for Slack recognition: any emoji as the token, a "
                    "daily allowance per timezone, plus standups and coffee chats. MIT licensed.",
        h1="A free, open-source HeyTaco alternative for Slack",
        lede="A daily allowance, your own emoji, leaderboards for giving as well as receiving, and "
             "no per-seat bill for thanking your colleagues.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Compare", "/compare/"), ("vs HeyTaco", None)],
        define='Morgenruf is a free, open-source (MIT) HeyTaco alternative for recognition in Slack. Everyone gets a daily allowance of tokens, in any emoji you like, that resets at midnight in their own timezone, with leaderboards for giving and receiving. It has no rewards catalogue, runs hosted free or self-hosted, and includes standups and coffee chats.')


PRICE_ROWS = [
    ("Geekbot", "Async standups, check-ins, polls",
     "Free for up to 10 users. Above that, $3 per user per month, or $2.50 per user per month "
     "billed annually."),
    ("Donut", "Random pairings, onboarding journeys, channel prompts",
     "A free plan, then paid plans from about $74 a month."),
    ("HeyTaco", "Peer recognition, leaderboards, a rewards catalogue",
     "Per person per month, and any gift cards in the catalogue come out of a budget you fund on "
     "top of the subscription."),
    ("Standup &amp; Prosper", "Async standups",
     "Free forever with unlimited standups and team members. Paid plans are $1 or $4 per "
     "standup user a month (checked 2026-09-27)."),
    ("Morgenruf", "Standups, coffee chats and kudos in one app",
     "Free on the hosted instance CloudDrove runs. Self-hosted, no seat component at any size: a "
     "small server and a Postgres, a fixed line whether you are twelve people or three hundred."),
]


def price_table():
    rows = "".join(f'<tr><td><strong>{tool}</strong></td><td>{does}</td><td>{price}</td></tr>'
                   for tool, does, price in PRICE_ROWS)
    return ('<div class="scroll-x"><table><thead><tr><th>Tool</th><th>What you get for it</th>'
            f'<th>How the bill works</th></tr></thead><tbody>{rows}</tbody></table></div>')


def hub():
    body = f'''<section class="section"><div class="wrap">
  <div class="prose" style="margin-bottom:40px">
    <p>Morgenruf does three jobs that most teams buy from three different companies: the async
    standup, the random introduction between people who never talk, and the public thank-you. Each
    of the tools below does one of those jobs, most of them for longer than this has existed, and
    each of them charges by the person by the month. These pages exist so you can work out which
    trade you actually want, including the cases where the answer is to keep paying them.</p>
  </div>

  <span class="eyebrow">The comparisons</span>
  <h2 id="the-comparisons" style="margin-bottom:24px">Start with the one you are paying for</h2>
  <div class="tiles">
    <a class="tile" href="/compare/standup-bots/"><h3>Eleven standup bots</h3>
      <p>Free plan limits and prices side by side, and which bot fits which team.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/geekbot-alternative/"><h3>vs Geekbot</h3>
      <p>Async standups, the closest comparison, and the one most teams arrive from.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/donut-alternative/"><h3>vs Donut</h3>
      <p>Random coffee chats and introductions, plus what Donut does that this does not.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/heytaco-alternative/"><h3>vs HeyTaco</h3>
      <p>Peer recognition, daily allowances, and where a rewards catalogue matters.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/standup-prosper-alternative/"><h3>vs Standup &amp; Prosper</h3>
      <p>Another async standup bot, and the differences that actually show up in use.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/open-source-standup-bot/"><h3>Open source options</h3>
      <p>What else you can self-host, and honestly where each one fits.</p><span class="go">Read →</span></a>
    <a class="tile" href="/self-hosted-standup-bot/"><h3>Why self-host at all</h3>
      <p>Data residency, cost at scale, and the parts that are genuinely harder.</p><span class="go">Read →</span></a>
  </div>

  <div class="prose" style="margin-top:54px">
    <h2 id="where-they-win">Where each of them wins</h2>
    <p>This is the part of the page worth reading. Every one of these tools is better than Morgenruf
    at something, and the something is usually the reason a team bought it.</p>

    <h3>Geekbot</h3>
    <p>It has been running standups since 2015, which means it has met edge cases a younger project
    has not: the workspace that renamed a channel mid-quarter, the person who answers in a thread
    three days late, the enterprise grid. It is listed in the Slack App Directory, so an IT admin
    can approve it through the process they already have, and it comes with support that somebody is
    paid to answer. Nothing to deploy, patch or back up. The longer
    <a href="/geekbot-alternative/">Geekbot and Morgenruf comparison</a> goes through the daily
    shape of both.</p>

    <h3>Donut</h3>
    <p>Donut made this category and still has the widest surface in it: onboarding journeys, channel
    prompts, video facilitation, and a Microsoft Teams version that works today rather than one that
    is in progress. If your pairing programme is really an onboarding programme, Donut is built for
    that and this is not. The
    <a href="/donut-alternative/">Donut alternative page</a> has the feature-by-feature version.</p>

    <h3>HeyTaco</h3>
    <p>The taco is good product design and the gamification is thought through, but the real gap is
    the rewards catalogue: a recognition programme with a budget behind it, where thanks convert
    into something people can spend. Morgenruf gives you a message and a leaderboard and stops
    there. If HR has a recognition budget, read the
    <a href="/heytaco-alternative/">HeyTaco alternative page</a> before you move anything.</p>

    <h3>Standup &amp; Prosper</h3>
    <p>A simple, well made standup bot with a free tier that covers a small team properly. If you
    are eight people and the free tier fits, self-hosting anything is a worse deal than the zero you
    are already paying. It only starts to bite when you outgrow the tier or the answers cannot sit
    in somebody else's cloud, which is what the
    <a href="/standup-prosper-alternative/">Standup &amp; Prosper comparison</a> works through.</p>

    <h2 id="what-it-costs">What the bill actually looks like</h2>
    {price_table()}
    <p style="margin-top:18px">Prices checked 2026-09-26 against
    <a href="https://geekbot.com/pricing/">Geekbot's</a> and
    <a href="https://www.donut.com/pricing/">Donut's</a> pricing pages, and quoted with that date
    attached, because they move. Geekbot is free for up to 10 users. Past that, a team of thirty
    pays $900 a year on annual billing, or $1,080 paying monthly, for the morning questions alone.
    Add pairing and recognition at comparable per-seat rates and the same thirty people cost
    somewhere between two and three thousand a year, rising every time you hire. Morgenruf on the
    hosted instance costs nothing at any size. Self-hosted, the same three rituals are a small VPS
    at roughly $5 to $20 a month plus a Postgres, and that number does not change at three hundred
    people. Counting only money, a standup-only team of ten or fewer pays nothing either way; above
    that, Geekbot's per-user price passes the cost of a small server almost at once.</p>

    <h2 id="what-self-hosting-costs">What self-hosting costs you in effort</h2>
    <p>None of this applies on the free hosted instance. It applies when you self-host, which is
    the route for keeping the data in your own database. The money argument is easy and slightly
    dishonest on its own, because the time is real. Here is the whole of it:</p>
    <ul>
      <li><strong>The install.</strong> One container and a Postgres 13 or newer, about twenty
      minutes, most of which is <a href="/setup/">creating the Slack app</a> rather than deploying
      anything.</li>
      <li><strong>An HTTPS URL Slack can reach.</strong> An ingress if you run Kubernetes, or a
      Cloudflare tunnel, which needs no open port.</li>
      <li><strong>Upgrades.</strong> Pull the image and restart. Migrations run themselves in an
      init container before the app starts.</li>
      <li><strong>Backups.</strong> <code>pg_dump</code>. There is no other state anywhere.</li>
      <li><strong>Somebody owning it.</strong> This is the honest cost. When Slack changes a scope
      or the disk fills, there is no support queue by default, there is you. Budget an hour a
      quarter once it is settled, and accept that the first bad morning is yours.</li>
    </ul>
    <p>The part that catches people is never the container. It is Slack scopes: a workspace that
    installed before a feature existed has not granted that feature's permissions, and the fix is a
    reinstall. <a href="/self-hosted-standup-bot/">What self-hosting involves</a> covers the rest,
    and <a href="/support/">paid setup and hosting</a> exists if you would rather buy the time back.</p>

    <h2 id="who-should-not">Who should not pick Morgenruf</h2>
    <p>Saying this plainly saves everybody an afternoon:</p>
    <ul>
      <li><strong>Anyone on Microsoft Teams.</strong> Support is in progress, which means not today.
      Geekbot, Donut and HeyTaco all ship it now.</li>
      <li><strong>Anyone who needs a rewards catalogue.</strong> Gift cards, budgets, redemption.
      HeyTaco or Bonusly, not this.</li>
      <li><strong>Teams that need their data in-house but have nowhere to run a container</strong>
      and no appetite to find one. The hosted instance is free, but it is CloudDrove's database,
      not yours.</li>
      <li><strong>Anyone who needs an App Directory listing</strong> for procurement or IT
      governance. Morgenruf is not listed there today, hosted or self-hosted.</li>
      <li><strong>Teams that need a contracted response time</strong> and will not buy it
      separately. Community support is one maintainer who also has a job.</li>
      <li><strong>Teams already happy on a free tier.</strong> If Geekbot's free plan covers your
      ten people, or Standup &amp; Prosper's free plan (no user limit) covers your standups, there
      is no argument here worth your time.</li>
    </ul>

    <h2 id="one-app">What the single app is actually for</h2>
    <p>The reason to consolidate is not tidiness, it is that the three signals sit in one database.
    <a href="/standups/">Async standups</a> tell you who is stuck and who quietly stopped answering.
    <a href="/coffee-chats/">Coffee chats</a> tell you who has met whom, which is the map of how work
    actually travels. <a href="/kudos/">Kudos</a> tell you who gets thanked. Separately those are
    three dashboards nobody opens. Together you can ask the question worth acting on: who is
    answering every morning, unblocking other people, and being thanked by nobody. No integration
    between three vendors gives you that, and no vendor is going to build it for you.</p>

    <h2 id="how-these-pages-are-written">How these pages are written</h2>
    <p>Each comparison says where the other tool wins, because they all win somewhere and a page that
    claims otherwise is not worth reading. Prices are quoted with the date they were checked, so you
    can tell at a glance how stale they are rather than trusting a number with no age on it.</p>
    <p>All of them were checked in September 2026. If something is wrong, it is a bug like any other:
    <a href="{REPO}/issues/new/choose">open an issue</a>.</p>
  </div>
</div></section>
'''
    return page(
        path="/compare/",
        title="Standup bot comparison: Morgenruf vs Geekbot and others",
        description="Honest comparisons between Morgenruf and the tools teams usually pay for: "
                    "Geekbot, Donut, HeyTaco and Standup & Prosper, including where each of them "
                    "wins.",
        h1="Compared with the tools you are probably paying for",
        lede="One app does what three subscriptions usually do. Here is where that helps, where it "
             "does not, and what the bill and the effort come to on each side.",
        body=body,
        trail=[("Home", "/"), ("Compare", None)])


# Every figure below was read from the vendor's own pricing page or help centre
# on the date in CHECKED. Research notes with the source for each row are kept
# in the private marketing repo (content/comparisons/). Re-check before editing
# a number; never copy one from somebody else's list.
CHECKED = "2026-09-27"

BOT_ROWS = [
    # tool, url, free plan, paid price, platforms, source
    ("Morgenruf", "/", "Free at any team size on the hosted instance",
     "None", "Slack; Google Chat in beta", "MIT, self-host with Docker or Helm"),
    ("Standup &amp; Prosper", "https://standup-and-prosper.com/",
     "Free forever: unlimited standups and team members",
     "$1 or $4 per standup user a month", "Slack", "Closed"),
    ("Geekbot", "https://geekbot.com/pricing/", "Up to 10 users, unlimited standups",
     "$3 per participant a month, $2.50 billed annually", "Slack, Microsoft Teams", "Closed"),
    ("DailyBot", "https://www.dailybot.com/pricing", "Unlimited members, 50 compiled reports a "
     "month, 14 days of history", "$3 or $6.50 per active user a month ($2.40 or $5 annually)",
     "Slack, Teams, Google Chat, Discord", "Closed"),
    ("Range", "https://www.range.co/pricing", "Up to 12 users, 30 days of check-in history",
     "$8 per team member a month", "Slack, Microsoft Teams", "Closed"),
    ("Troopr", "https://troopr.ai/pricing", "Up to 10 seats and 3 scheduled routines",
     "$8 per seat a month, $6 annually", "Slack, Microsoft Teams", "Closed; self-hosted on Enterprise"),
    ("Team O'clock", "https://www.teamoclock.com/pricing", "Up to 5 active members, 14 days of history",
     "$3 per active member a month, 10 member minimum", "Slack, Microsoft Teams", "Closed"),
    ("Kollabe", "https://kollabe.com/pricing", "Slack standups not included",
     "$29 per space a month, flat", "Slack, Microsoft Teams", "Closed"),
    ("Polly", "https://www.polly.ai/pricing", "Standups not included",
     "From $19 a month billed annually, 500 responses a month", "Slack, Teams, Google Chat and more",
     "Closed"),
    ("Steady (was Status Hero)", "https://runsteady.com/pricing", "None; 100 credits per user added",
     "Credit based, from $25 a month", "Slack, Microsoft Teams", "Closed"),
    ("poddaily", "https://github.com/maggit/poddaily", "Free, self-hosted", "None", "Slack",
     "MIT, self-host (Postgres and Redis)"),
]


# Each vendor's own favicon, copied into /logos/ so the page does not hotlink
# their sites. Shown beside the name to help a reader find a row, not as an
# endorsement; alt is empty because the name follows.
BOT_LOGOS = {'Morgenruf': '/logo-mark-68.png', 'Standup &amp; Prosper': '/logos/standup-prosper.png', 'Geekbot': '/logos/geekbot.png', 'DailyBot': '/logos/dailybot.svg', 'Range': '/logos/range.png', 'Troopr': '/logos/troopr.png', "Team O'clock": '/logos/teamoclock.png', 'Kollabe': '/logos/kollabe.png', 'Polly': '/logos/polly.png', 'Steady (was Status Hero)': '/logos/steady.png', 'poddaily': '/logos/poddaily.svg'}


def bots_table():
    def name(tool, url):
        logo = (f'<img src="{BOT_LOGOS[tool]}" alt="" width="20" height="20" loading="lazy" '
                f'style="flex:none;border-radius:4px">')
        label = tool if url.startswith("/") else f'<a href="{url}">{tool}</a>'
        return f'<span style="display:flex;align-items:center;gap:8px">{logo}<span>{label}</span></span>'
    rows = "".join(
        f'<tr><td><strong>{name(tool, url)}</strong></td><td>{free}</td><td>{paid}</td>'
        f'<td>{where}</td><td>{src}</td></tr>'
        for tool, url, free, paid, where, src in BOT_ROWS)
    return ('<div class="scroll-x"><table><thead><tr><th>Bot</th><th>Free plan</th>'
            '<th>Paid price</th><th>Chat apps</th><th>Source and hosting</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def standup_bots():
    prose = f'''<h2 id="the-table">Free plans and prices, side by side</h2>
<p>Eleven Slack standup bots, including Morgenruf, which is the one this site is about. Each row comes
from that vendor's own pricing page, read on {CHECKED}. Prices are per month unless the row says
otherwise. If a row is wrong, <a href="{REPO}/issues/new/choose">say so</a> and it will be fixed.</p>
{bots_table()}
<p class="shot-cap" style="margin-top:12px">Logos belong to their owners and are shown only
to identify each product. Standuply is left out: its pricing page loads its prices
with JavaScript and the newest figures its help centre publishes are from January 2024, so there is
no current number to quote.</p>

<h2 id="which-one">Which one to pick</h2>
<p>Most teams do not need to compare eleven tools. They need the one that fits how they work.</p>
<ul>
  <li><strong>Standups only, Slack only, and you want it free with nothing to run:</strong>
  Standup &amp; Prosper. Its free plan has no cap on standups or people, which is the largest free
  hosted plan in this table. It is the honest first answer for that team.</li>
  <li><strong>Ten people or fewer, or you need Microsoft Teams, polls and surveys:</strong> Geekbot.
  It is the most established product here, and free up to ten users.</li>
  <li><strong>Your company is on Google Chat or Discord as well as Slack:</strong> DailyBot covers
  the most chat apps.</li>
  <li><strong>Standups are one part of Jira work in Slack:</strong> Troopr.</li>
  <li><strong>You want check-ins tied to goals and meeting agendas:</strong> Range.</li>
  <li><strong>You also run retros and planning poker:</strong> Team O'clock or Kollabe.</li>
  <li><strong>Standup answers must stay on your own servers, or you want coffee chats and peer
  recognition in the same app, at any team size for free:</strong> Morgenruf. It is MIT licensed,
  runs on Docker or Kubernetes, and is also free on a hosted instance if you would rather not run
  it. poddaily is the other active open-source option, smaller and standups only.</li>
</ul>

<h2 id="what-free-means">What "free" means in each case</h2>
<p>A free plan usually runs out in one of four ways. Knowing which one applies tells you when the
bill starts.</p>
<ul>
  <li><strong>A user cap.</strong> Geekbot and Troopr stop at 10, Range at 12, Team O'clock at 5.
  The eleventh person turns the whole team into a paid plan.</li>
  <li><strong>A history limit.</strong> DailyBot keeps 14 days on its free plan, Team O'clock 14,
  Range 30. Fine for the daily habit, not for looking back at a quarter.</li>
  <li><strong>A usage cap.</strong> DailyBot allows 50 compiled check-in reports a month across the
  whole organisation.</li>
  <li><strong>Standups not included.</strong> Polly and Kollabe have free plans, but Slack standups
  are on their paid plans.</li>
</ul>
<p>Standup &amp; Prosper and Morgenruf have no user cap. The difference is that Standup &amp;
Prosper is hosted only and closed source, while Morgenruf can also run on your own infrastructure,
where you keep every answer for as long as you like.</p>

<h2 id="per-seat-maths">What a 30 person team pays in a year</h2>
<p>At list price, paying monthly, for standups only: Geekbot $1,080, DailyBot Essentials $1,080,
Range $2,880, Troopr $2,880, Team O'clock $1,080. Standup &amp; Prosper and Morgenruf: $0 on their
free plans. Where annual billing is offered, it lowers these by 17 to 25 percent.</p>

<h2 id="status-hero">What happened to Status Hero</h2>
<p>Status Hero is now called Steady. statushero.com redirects to runsteady.com, and the product is
sold on credits rather than seats, with no free plan.</p>

<h2 id="about-this-page">About this page</h2>
<p>Morgenruf is built by CloudDrove, so this page is not neutral, and it says so. The rows are
written from each vendor's own pages, and the recommendations above name another tool first
wherever another tool fits better. For a closer look at one of them, see the
<a href="/geekbot-alternative/">Geekbot</a> and
<a href="/standup-prosper-alternative/">Standup &amp; Prosper</a> comparisons.</p>'''
    body = seo_guide(prose, [("The table", "the-table"), ("Which one to pick", "which-one"),
                             ('What "free" means', "what-free-means"),
                             ("A 30 person team", "per-seat-maths"),
                             ("Status Hero", "status-hero"), ("About this page", "about-this-page")])
    faq_html, faq_schema = faq([
        ("What is the best free Slack standup bot?",
         "For standups only on Slack with nothing to run, Standup & Prosper: its free plan has no "
         "limit on standups or people. For ten people or fewer who need Teams or polls, Geekbot. To "
         "keep answers on your own servers, or to add coffee chats and kudos, Morgenruf, which is "
         "free at any size and MIT licensed."),
        ("Is there an open-source Slack standup bot?",
         "Yes. Morgenruf (MIT, Docker or Helm, with a free hosted instance too) and poddaily (MIT, "
         "self-hosted) are both maintained. Older projects such as 18F's standup-slack-bot are "
         "archived."),
        ("Which standup bots have no user limit on the free plan?",
         f"Standup & Prosper and Morgenruf, as of {CHECKED}. DailyBot has no member limit but caps "
         "compiled reports at 50 a month and keeps 14 days of history."),
        ("Is Geekbot free?",
         "For teams of up to 10 users. Above that it costs $3 per participant a month, or $2.50 billed "
         f"annually (checked {CHECKED})."),
        ("What happened to Status Hero?",
         "It was renamed Steady. It now charges for credits rather than seats and has no free plan."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="questions">Slack standup bots</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/compare/standup-bots/",
        title="Slack standup bots compared: free plans and prices, 2026",
        description="Eleven Slack standup bots compared on free plan limits and price, from each "
                    f"vendor's pricing page ({CHECKED}), with honest advice on which fits.",
        h1="Slack standup bots compared",
        lede="Free plan limits and prices for eleven standup bots, read from each vendor's own "
             "pricing page, and which one fits which team.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Compare", "/compare/"), ("Standup bots", None)],
        define=f"Morgenruf is a free, open-source (MIT) Slack standup bot. This page compares it with "
               f"ten other standup bots on free plan limits and paid price, each checked on the "
               f"vendor's own pricing page on {CHECKED}. For standups only, Standup &amp; Prosper has "
               f"the largest free hosted plan; Morgenruf is the option you can also run yourself.")


def seo_guide(prose, toc):
    from seo_pages import guide
    return guide(prose, toc)
