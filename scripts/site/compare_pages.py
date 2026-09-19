"""Comparison pages.

Written to be useful to somebody weighing the choice, including the cases where
the answer is "keep paying them". A comparison page that says the competitor is
bad at everything convinces nobody and ranks badly, because people bounce.
"""

from __future__ import annotations

from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav


def page(*, path, title, description, h1, lede, body, schema=(), trail=(), current="/compare"):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = list(schema) + ([crumb_schema] if crumb_schema else [])
    return (head(title=title, description=description, path=path, schema=schemas)
            + nav(current) + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="head-cta">
    <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
    <a class="btn btn-line" href="/setup">Set it up yourself</a>
  </div>
</div></header>
{body}
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
        ("Runs on your own servers", "Yes", "yes", "No", "no"),
        ("Source you can read", "MIT", "yes", "Closed", "no"),
        ("Your pairing data lives in", "your database", "yes", "their cloud", "no"),
        ("Microsoft Teams", "In progress", "no", "Yes", "yes"),
        ("Price", "Free, any team size", "yes", "Per seat, monthly", "no"),
    ]
    body = f'''<section class="section"><div class="wrap">
{table(rows, "Donut")}
<p class="shot-cap" style="margin-top:12px">Checked against Donut's public pages in September 2026.
Their plans change; if something here is out of date, please
<a href="{REPO}/issues/new/choose">tell me and I will fix it</a>.</p>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
<h2 id="the-honest-version">The honest version</h2>
<p>Donut is a good product and the one that made this category. It has years of polish, a Teams
version that works today, and a wider surface than this: journeys for onboarding, channel prompts,
video facilitation.</p>
{HONEST % ("If you need Microsoft Teams today, or onboarding journeys, or you simply do not want to run "
           "software, Donut is the better answer and you should use it.")}

<h2 id="where-this-is-different">Where this is different</h2>
<h3>It is one app, not three subscriptions</h3>
<p>Most teams that pay for pairing also pay for standups and recognition. Morgenruf runs all three
against one database, which is also what makes the cross-signal questions possible: who answers
every standup and is thanked by nobody.</p>

<h3>The introduction carries a meeting</h3>
<p>Two people being told to meet is the easy part. This proposes hours that fall inside both working
days, each of them presses one, and a matching pair becomes a Zoom meeting at that hour, hosted on
the account of whoever connected theirs.</p>

<h3>Your data stays yours</h3>
<p>Who met whom, and who quietly opted out, lives in Postgres you control. Nothing is sent anywhere
else, and leaving is not a migration because it is already yours.</p>

<h3>The price</h3>
<p>Free for every seat, at any size, because you run it. A thirty person team pays for a small server
and a database instead of a per-seat subscription that grows with hiring.</p>

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
        ("Does it need Zoom?",
         "No. Without it a pairing uses whatever room link you set on the programme, or none. Zoom "
         "only adds a real meeting at the agreed hour."),
        ("What does it cost for 200 people?",
         "Nothing per seat. The server and database you run it on, which for 200 people is a small "
         "instance."),
    ])
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="morgenruf-and-donut">Morgenruf and Donut</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/donut-alternative",
        title="Open-source Donut alternative for Slack coffee chats",
        description="A self-hosted Donut alternative for random coffee chats in Slack, plus "
                    "standups and kudos in the same app. MIT licensed, no per-seat fee, your data "
                    "stays put.",
        h1="An open-source Donut alternative you host yourself",
        lede="Random introductions from a channel, a time both people actually pick, and the meeting "
             "booked at that hour. Plus standups and kudos in the same app.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Compare", "/compare"), ("vs Donut", None)])


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

<h3>The price, again</h3>
<p>Free for every seat. Recognition tools are usually priced per person per month, which means the
cost of thanking people grows exactly as you hire them.</p>
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
        path="/heytaco-alternative",
        title="Open-source HeyTaco alternative for Slack recognition",
        description="A self-hosted HeyTaco alternative for Slack recognition: any emoji as the "
                    "token, a daily allowance per timezone, plus standups and coffee chats. MIT "
                    "licensed.",
        h1="An open-source HeyTaco alternative you host yourself",
        lede="A daily allowance, your own emoji, leaderboards for giving as well as receiving, and "
             "no per-seat bill for thanking your colleagues.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Compare", "/compare"), ("vs HeyTaco", None)])


PRICE_ROWS = [
    ("Geekbot", "Async standups, check-ins, polls",
     "Per person per month, published at $2.50 on the standard plan, less on an annual term, "
     "billed on the people who take part."),
    ("Donut", "Random pairings, onboarding journeys, channel prompts",
     "A free tier that covers a single small programme, then per person per month once you want "
     "more than that."),
    ("HeyTaco", "Peer recognition, leaderboards, a rewards catalogue",
     "Per person per month, and any gift cards in the catalogue come out of a budget you fund on "
     "top of the subscription."),
    ("Standup &amp; Prosper", "Async standups",
     "A free tier that genuinely fits a small team, then per person per month above it."),
    ("Morgenruf", "Standups, coffee chats and kudos in one app",
     "No seat component at any size. You pay for a small server and a Postgres, which is a fixed "
     "line whether you are twelve people or three hundred."),
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
    <a class="tile" href="/geekbot-alternative"><h3>vs Geekbot</h3>
      <p>Async standups, the closest comparison, and the one most teams arrive from.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/donut-alternative"><h3>vs Donut</h3>
      <p>Random coffee chats and introductions, plus what Donut does that this does not.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/heytaco-alternative"><h3>vs HeyTaco</h3>
      <p>Peer recognition, daily allowances, and where a rewards catalogue matters.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/standup-prosper-alternative"><h3>vs Standup &amp; Prosper</h3>
      <p>Another async standup bot, and the differences that actually show up in use.</p><span class="go">Compare →</span></a>
    <a class="tile" href="/open-source-standup-bot"><h3>Open source options</h3>
      <p>What else you can self-host, and honestly where each one fits.</p><span class="go">Read →</span></a>
    <a class="tile" href="/self-hosted-standup-bot"><h3>Why self-host at all</h3>
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
    <a href="/geekbot-alternative">Geekbot and Morgenruf comparison</a> goes through the daily
    shape of both.</p>

    <h3>Donut</h3>
    <p>Donut made this category and still has the widest surface in it: onboarding journeys, channel
    prompts, video facilitation, and a Microsoft Teams version that works today rather than one that
    is in progress. If your pairing programme is really an onboarding programme, Donut is built for
    that and this is not. The
    <a href="/donut-alternative">Donut alternative page</a> has the feature-by-feature version.</p>

    <h3>HeyTaco</h3>
    <p>The taco is good product design and the gamification is thought through, but the real gap is
    the rewards catalogue: a recognition programme with a budget behind it, where thanks convert
    into something people can spend. Morgenruf gives you a message and a leaderboard and stops
    there. If HR has a recognition budget, read the
    <a href="/heytaco-alternative">HeyTaco alternative page</a> before you move anything.</p>

    <h3>Standup &amp; Prosper</h3>
    <p>A simple, well made standup bot with a free tier that covers a small team properly. If you
    are eight people and the free tier fits, self-hosting anything is a worse deal than the zero you
    are already paying. It only starts to bite when you outgrow the tier or the answers cannot sit
    in somebody else's cloud, which is what the
    <a href="/standup-prosper-alternative">Standup &amp; Prosper comparison</a> works through.</p>

    <h2 id="what-it-costs">What the bill actually looks like</h2>
    {price_table()}
    <p style="margin-top:18px">Prices checked against public pricing pages in September 2026 and
    quoted with that date attached, because they move. At the $2.50 per person per month Geekbot
    publishes, a team of thirty pays $900 a year for the morning questions alone. Add pairing and
    recognition at comparable per-seat rates and the same thirty people cost somewhere between two
    and three thousand a year, rising every time you hire. Self-hosted, the same three rituals are a
    small VPS at roughly $5 to $20 a month plus a Postgres, and that number does not change at three
    hundred people. Counting only money, a standup-only team crosses over at around a dozen people.
    Counting somebody's attention as well, later than that.</p>

    <h2 id="what-self-hosting-costs">What self-hosting costs you in effort</h2>
    <p>The money argument is easy and slightly dishonest on its own, because the time is real. Here
    is the whole of it:</p>
    <ul>
      <li><strong>The install.</strong> One container and a Postgres 13 or newer, about twenty
      minutes, most of which is <a href="/setup">creating the Slack app</a> rather than deploying
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
    reinstall. <a href="/self-hosted-standup-bot">What self-hosting involves</a> covers the rest,
    and <a href="/support">paid setup and hosting</a> exists if you would rather buy the time back.</p>

    <h2 id="who-should-not">Who should not pick Morgenruf</h2>
    <p>Saying this plainly saves everybody an afternoon:</p>
    <ul>
      <li><strong>Anyone on Microsoft Teams.</strong> Support is in progress, which means not today.
      Donut and HeyTaco both ship it now.</li>
      <li><strong>Anyone who needs a rewards catalogue.</strong> Gift cards, budgets, redemption.
      HeyTaco or Bonusly, not this.</li>
      <li><strong>Teams with nowhere to run a container</strong> and no appetite to find one. A
      per-seat bill is cheaper than an afternoon of somebody's attention every month.</li>
      <li><strong>Anyone who needs an App Directory listing</strong> for procurement or IT
      governance. A self-hosted app you installed yourself does not have one.</li>
      <li><strong>Teams that need a contracted response time</strong> and will not buy it
      separately. Community support is one maintainer who also has a job.</li>
      <li><strong>Teams already happy on a free tier.</strong> If Standup &amp; Prosper covers your
      ten people for nothing, there is no argument here worth your time.</li>
    </ul>

    <h2 id="one-app">What the single app is actually for</h2>
    <p>The reason to consolidate is not tidiness, it is that the three signals sit in one database.
    <a href="/standups">Async standups</a> tell you who is stuck and who quietly stopped answering.
    <a href="/coffee-chats">Coffee chats</a> tell you who has met whom, which is the map of how work
    actually travels. <a href="/kudos">Kudos</a> tell you who gets thanked. Separately those are
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
        path="/compare",
        title="Morgenruf vs Geekbot, Donut, HeyTaco and Standup & Prosper",
        description="Honest comparisons between Morgenruf and the tools teams usually pay for: "
                    "Geekbot, Donut, HeyTaco and Standup & Prosper, including where each of them "
                    "wins.",
        h1="Compared with the tools you are probably paying for",
        lede="One app does what three subscriptions usually do. Here is where that helps, where it "
             "does not, and what the bill and the effort come to on each side.",
        body=body,
        trail=[("Home", "/"), ("Compare", None)])
