"""A page per module.

The home page has to sell three things at once, so it says a little about each.
These pages say everything about one, which is also what somebody searching for
"slack coffee chat bot" is looking for.
"""

from __future__ import annotations

import diagrams

from shell import INSTALL, REPO, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav


def page(*, path, title, description, h1, lede, body, hero="", schema=(), trail=(), current=""):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = list(schema) + ([crumb_schema] if crumb_schema else [])
    return (head(title=title, description=description, path=path, schema=schemas)
            + nav(current) + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap"><div class="head-in">
  <div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="head-cta">
      <a class="btn btn-sun" href="{INSTALL}">{SLACK_MARK}Add to Slack</a>
      <a class="btn btn-line" href="/setup">Set it up yourself</a>
    </div>
  </div>
  <div>{hero}</div>
</div></div></header>
{body}
</main>''' + cta_band() + footer())


def shot(src, alt, caption, w=None, h=None):
    """Width and height come from the file, so the space is reserved correctly."""
    if w is None or h is None:
        try:
            from PIL import Image
            import pathlib as _p
            with Image.open(_p.Path(__file__).resolve().parent.parent.parent / src.lstrip("/")) as im:
                w, h = im.size
        except Exception:
            w, h = 1100, 700
    return (f'<div class="shot"><img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}"/></div>'
            f'<p class="shot-cap">{caption}</p>')


STANDUP_FAQ = [
    ("What time does it ask people?",
     "Whatever hour you set, in each person's own timezone. A team across four continents gets asked "
     "at a sensible local hour rather than yours."),
    ("Can we have more than one standup?",
     "As many as you like, each with its own channel, schedule, questions and participants. A morning "
     "engineering call and a Tuesday design sync are two standups, not a compromise."),
    ("What happens when somebody is on leave?",
     "They are skipped, not nagged. Vacation is set from the Slack App Home or the dashboard, and "
     "nobody on leave counts against the completion figure."),
    ("Can people edit an answer after sending it?",
     "Within a window you choose: until the report posts, for four hours, or indefinitely."),
    ("What does the summary look like?",
     "One message in your channel, grouped by person or by question, with blockers pulled out. It can "
     "post in a thread to keep the channel quiet, and can go to a different channel from the one the "
     "questions came from."),
    ("Does it chase people who have not answered?",
     "If you want it to. A nudge goes as a private DM a set number of minutes before the report "
     "posts, to the people who have not filed, and to nobody else."),
]


def standups():
    body = f'''<section class="section"><div class="wrap">
  <div class="mod" style="border-top:0">
    <div class="mod-copy">
      <span class="tag tag-standup">How it works</span>
      <h2 id="a-direct-message-not-a-meeting">A direct message, not a meeting</h2>
      <p class="lede">At the hour you choose, each person gets a DM with your questions. They answer
      in their own time. When the window closes, one formatted summary goes to the channel.</p>
      <ul>
        <li>Your own questions, in your own words</li>
        <li>Answers in a thread or the channel, grouped by person or by question</li>
        <li>Blockers highlighted so they are not buried in paragraph three</li>
        <li>A private nudge for whoever has not filed yet</li>
      </ul>
    </div>
    <div>{shot("/screenshots/standups.jpg", "Two standups in the dashboard, each with a completion sparkline and a health badge", "Each standup carries fourteen days of completion, so one that is slipping says so.")}</div>
  </div>

  <div class="mod">
    <div class="mod-copy">
      <span class="tag tag-standup">Every morning</span>
      <h2 id="the-page-you-check-with-your-coffee">The page you check with your coffee</h2>
      <p class="lede">Who has answered, who is still to file, and who is blocked, on one screen. The
      blocked list is the point: it is the thing a standup exists to surface and the thing a
      transcript buries.</p>
      <ul>
        <li>Counts that reconcile: expected, answered, waiting, blocked</li>
        <li>Recent recognition, so the good news is not only in a channel nobody scrolled</li>
        <li>When the next coffee chat round goes out, and whether it is overdue</li>
      </ul>
    </div>
    <div>{shot("/screenshots/today.jpg", "The Today page showing answered and blocked counts, this morning's answers and recent kudos", "Today, for a team of eight.")}</div>
  </div>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
''' + diagrams.standup_flow() + '''
<h2 id="the-things-that-decide-whether-a-standup-survives">The things that decide whether a standup survives</h2>
<p>Most async standup tools do the same first ten percent. What separates one that a team still uses
in six months is the handling of ordinary human situations. The same list is worked through against
a hosted tool in <a href="/geekbot-alternative">the comparison with Geekbot</a>.</p>
<ul>
  <li><strong>Timezones per person.</strong> Not per workspace. A 9:30 standup in Toronto is 19:00 in
  Kolkata, and a tool that asks at 19:00 gets ignored.</li>
  <li><strong>Leave.</strong> Somebody on holiday should not receive a message, and should not drag
  the completion rate down while they are gone.</li>
  <li><strong>Edits.</strong> People send too early and remember something a minute later.</li>
  <li><strong>Silence.</strong> A private reminder works. A public callout breeds resentment.</li>
  <li><strong>Knowing it is working.</strong> Fourteen days of completion on the card, with a badge
  when it starts slipping, so you find out before the habit dies.</li>
</ul>

<h2 id="what-you-can-do-with-the-answers">What you can do with the answers</h2>
<ul>
  <li><strong>A digest email</strong> per standup, to a lead who does not live in Slack.</li>
  <li><strong>Signed webhooks</strong> on every completed standup, for whatever you build next.</li>
  <li><strong>Automation rules</strong>: if nobody has answered by ten, post in another channel.</li>
  <li><strong>Ask an assistant.</strong> The MCP server lets Claude or Cursor answer questions like
  "who has been blocked on the same thing for days" against your own history.</li>
  <li><strong>CSV export</strong>, because it is your data.</li>
  <li><strong>Read them next to recognition.</strong> <a href="/insights">Insights</a> asks the
  questions that need standup answers and kudos at the same time.</li>
</ul>
<p>If the reason you are here is the per-seat bill, <a href="/blog/async-standups-slack-free">the
write-up on running async standups in Slack for free</a> is the shorter version of this page.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq(STANDUP_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="about-standups">About standups</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/standups",
        title="Async standups in Slack, self-hosted — Morgenruf",
        description="Async daily standups in Slack: your own questions, per-person timezones, "
                    "blockers highlighted, and one summary in the channel. Open source and "
                    "self-hosted.",
        h1="Async standups that survive contact with a real team",
        lede="Each person answers in a DM at a sensible local hour. One summary lands in the channel. "
             "Nobody sits in a call to hear what they could have read.",
        body=body, schema=[faq_schema],
        hero=shot("/screenshots/today.jpg", "The Today page: who has answered, who is blocked, and recent recognition", "Today, for a team of eight."),
        trail=[("Home", "/"), ("Standups", None)], current="/standups")


CONNECT_FAQ = [
    ("How does it pick who meets whom?",
     "It avoids whoever you met last, and keeps avoiding them until everyone in the pool has been "
     "met once. With an odd number, one group of three forms so nobody sits out."),
    ("Can we have groups of three or four?",
     "Group size runs from two to eight. A remainder of two or more forms its own group rather than "
     "being folded into a larger one, so ten people in fours are four, four and two."),
    ("How does the pair agree on a time?",
     "The introduction offers hours that fall inside both people's working days, and each presses a "
     "button. When they both pick the same hour, that is the meeting. Nobody's calendar is read, and "
     "the message says so rather than pretending otherwise."),
    ("Does it create the meeting?",
     "With Zoom connected, yes: the meeting is created at the agreed hour on the account of whoever "
     "in the pair linked theirs. Otherwise the programme's own room link is used, or none at all."),
    ("What if somebody does not want to be matched this round?",
     "They can skip a round or pause entirely from the Slack App Home, and ask for a different match "
     "once per round. None of that needs an admin."),
    ("How do we know if it is working?",
     "The round closes by asking whether the pair met, and the answer is recorded four ways: met, did "
     "not meet, never replied, and never delivered. The last one is our bug, not their behaviour, and "
     "folding it into 'did not meet' would blame the wrong party."),
]


def coffee_chats():
    body = f'''<section class="section"><div class="wrap">
  <div class="mod" style="border-top:0">
    <div class="mod-copy">
      <span class="tag tag-connect">How it works</span>
      <h2 id="pick-a-channel-and-a-cadence">Pick a channel and a cadence</h2>
      <p class="lede">Everyone in the channel goes in the pool. On the day, they are paired and
      introduced in a group message with an opener, and the round closes by asking whether they
      actually met.</p>
      <ul>
        <li>Never repeats a pairing until everyone has met</li>
        <li>Groups of two to eight, with a sensible remainder</li>
        <li>An icebreaker, so the first message is not "hi"</li>
        <li>One quiet nudge on day three if nothing has happened</li>
      </ul>
    </div>
    <div>{shot("/screenshots/coffee-chat-settings.jpg", "Coffee chat settings beside a live preview of the Slack introduction", "Settings on the left, the message they produce on the right.")}</div>
  </div>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
''' + diagrams.pairing_flow() + '''
<h2 id="the-part-most-pairing-tools-leave-out">The part most pairing tools leave out</h2>
<p>Two people get introduced, say "we should find a time", and never do. The introduction has to
carry the meeting or the meeting does not happen. Where a hosted product still wins on this is set
out in <a href="/donut-alternative">the comparison with Donut</a>.</p>
<ul>
  <li><strong>Hours that suit both.</strong> Each person's working day comes from their Slack
  timezone. The suggestions are the overlap, not your convenience.</li>
  <li><strong>A button, not a negotiation.</strong> They both press an hour. Matching presses make
  the meeting.</li>
  <li><strong>Zoom books it</strong> at that hour, on the account of whoever linked theirs. Linking
  is per person, from the message, and revoking affects nobody else.</li>
  <li><strong>Honest wording.</strong> The message says nobody has checked your calendars, because
  nobody has. Implying otherwise would be worse than offering nothing.</li>
</ul>

<h2 id="working-hours-matching-and-when-to-leave-it-off">Working hours matching, and when to leave it off</h2>
<p>There is a switch for requiring an hour of overlap between two people's working days. It is off
by default, and worth leaving off for a team spread very wide: a nine-to-five in Toronto and one in
Kolkata share no hours at all, so turning it on stops them being matched entirely. A tool that
silently matched nobody would look broken, so this one tells you what the setting does before you
turn it on.</p>

<h2 id="where-people-manage-their-own-participation">Where people manage their own participation</h2>
<p>From the Morgenruf tab in Slack, which is where people look. Pause, skip a round, snooze for a
fortnight, ask for a different match, connect or disconnect Zoom. It is the same tab where somebody
sets leave for <a href="/standups">a standup</a> or checks what is left of their
<a href="/kudos">kudos allowance</a>. An admin can see who is in the pool and why somebody is not,
which is the question the attendance table exists to answer.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq(CONNECT_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="about-coffee-chats">About coffee chats</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/coffee-chats",
        title="Random coffee chats for Slack, self-hosted — Morgenruf",
        description="Pair people from a Slack channel on a cadence, avoid repeat matches, suggest "
                    "hours that suit both timezones, and let Zoom book the meeting. Self-hosted.",
        h1="Introduce the people who never talk",
        lede="Random pairings from a channel, on a cadence, that end in an actual meeting rather than "
             "two people agreeing they should find a time.",
        body=body, schema=[faq_schema],
        hero=shot("/screenshots/coffee-chat-settings.jpg", "Coffee chat settings beside a live preview of the Slack introduction", "The settings, and the message they produce."),
        trail=[("Home", "/"), ("Coffee chats", None)], current="/coffee-chats")


KUDOS_FAQ = [
    ("How many can each person give?",
     "You choose. Five a day is a sensible default. Unused ones do not carry over, which is the "
     "entire mechanic: a budget that resets is what makes people spend it."),
    ("When does the allowance reset?",
     "Midnight in each person's own timezone, not yours. Somebody in Sydney should not get a fresh "
     "allowance in the middle of their afternoon."),
    ("Can we use our own emoji?",
     "Yes. Pick any emoji in your workspace as the token. The Morgenruf icon can be imported as a "
     "custom emoji and the bot picks it up on its own, falling back gracefully if it is ever removed."),
    ("Is there a leaderboard?",
     "Two: who is recognised, and who does the recognising. The second is the one worth watching, "
     "because a recognition habit dies when the givers stop."),
    ("Can somebody give themselves kudos?",
     "No."),
]


def kudos():
    body = f'''<section class="section"><div class="wrap">
  <div class="mod" style="border-top:0">
    <div class="mod-copy">
      <span class="tag tag-kudos">How it works</span>
      <h2 id="a-daily-budget-not-a-applause-button">A daily budget, not a applause button</h2>
      <p class="lede">Everyone gets a handful of tokens a day. Give one with a message in a DM or a
      slash command, and it posts publicly with the reason. What is not spent is gone at midnight.</p>
      <ul>
        <li>Your own token: any emoji in your workspace</li>
        <li>Resets at midnight in each person's own timezone</li>
        <li>Leaderboards for giving as well as receiving</li>
        <li>Everything stored in your database, exportable as CSV</li>
      </ul>
    </div>
    <div>{shot("/screenshots/kudos.jpg", "Kudos settings showing the token, the daily allowance, and a preview of the message", "Set the token and the allowance, and see exactly what your team will get.")}</div>
  </div>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
''' + diagrams.allowance() + '''
<h2 id="why-scarcity-is-the-whole-design">Why scarcity is the whole design</h2>
<p>Unlimited praise is worth nothing. If everybody can thank everybody all day, the messages become
noise and people stop reading them. A small daily budget that disappears at midnight does two useful
things: it makes each one mean something, and it creates a mild pressure to spend them, which is
what gets somebody to notice the quiet colleague who fixed the build. Midnight is read per person,
the same way <a href="/standups">a standup</a> works out when to ask.</p>

<h2 id="what-it-is-not">What it is not</h2>
<p>There is no points store, no gift card catalogue, no vendor taking a cut of a reward budget.
Recognition here is a message to a channel and a number in a leaderboard. If your programme needs
prizes, this is the wrong tool and an honest answer now saves you a migration later.
<a href="/heytaco-alternative">The HeyTaco comparison</a> is where that trade is spelled out.</p>

<h2 id="reading-the-room">Reading the room</h2>
<p>Recognition data is only interesting next to something else, which is why it feeds
<a href="/insights">Insights</a>: somebody who answers every standup and has never been thanked is
visible in a way neither dataset shows alone.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq(KUDOS_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="about-kudos">About kudos</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/kudos",
        title="Peer recognition in Slack, self-hosted — Morgenruf kudos",
        description="Peer recognition in Slack with a daily allowance that resets at midnight in "
                    "each person's own timezone, your own emoji as the token, and two "
                    "leaderboards.",
        h1="Praise that means something because it runs out",
        lede="A handful of tokens a day each, given publicly with a reason, gone at midnight if "
             "unspent.",
        body=body, schema=[faq_schema],
        hero=shot("/screenshots/kudos.jpg", "Kudos settings: the token, the daily allowance and a preview of the message", "Your token, your allowance."),
        trail=[("Home", "/"), ("Kudos", None)], current="/kudos")


INSIGHTS_FAQ = [
    ("What does Insights actually look at?",
     "Two datasets at once. Standup answers on their own tell you who is blocked today; kudos on "
     "their own tell you who was thanked. Together they answer questions neither can: who is "
     "contributing and going unrecognised, and which blocker has been in someone's answers for days."),
    ("Is this surveillance?",
     "It is the same information already in your channel, counted. It does not read messages it was "
     "not sent, does not score people, and does not produce a ranking of who is 'productive'. If you "
     "want a tool that tells you who to performance-manage, this is not it."),
    ("Can I turn it off?",
     "Yes. Insights is a module like the others and can be switched off per workspace, at which point "
     "it stops running and leaves the sidebar."),
]


def insights():
    body = '''<section class="section"><div class="wrap"><div class="prose">
''' + diagrams.standup_flow() + '''
<h2 id="two-questions-worth-asking">Two questions worth asking</h2>
<p>Most dashboards count things you already knew. These two need two datasets at once, which is the
only reason to have <a href="/standups">standups</a> and <a href="/kudos">kudos</a> in one app
rather than two subscriptions.</p>

<h3>Who has been blocked on the same thing for days?</h3>
<p>A blocker in today's standup is normal. The same blocker in five consecutive answers is a
different thing, and it is invisible in a channel where each day scrolls away. Insights groups
repeated blockers by person and by how long they have persisted.</p>

<h3>Who answers every standup and is thanked by nobody?</h3>
<p>Recognition data is skewed towards visible work. Somebody who files every morning, unblocks other
people, and never gets a kudo is a retention risk that neither dataset shows on its own.</p>

<h2 id="what-it-deliberately-does-not-do">What it deliberately does not do</h2>
<ul>
  <li>No productivity score, and no ranking of people by output.</li>
  <li>No reading of messages it was not sent.</li>
  <li>No exporting your team's answers anywhere. It reads your database and stops there.</li>
</ul>
<p>It can be switched off per workspace like any other module. Paying two vendors per seat to get one
answer of this kind is most of <a href="/blog/why-i-built-morgenruf">why this was built in the first
place</a>.</p>
</div></div></section>
'''
    faq_html, faq_schema = faq(INSIGHTS_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="about-insights">About insights</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/insights",
        title="Standup and recognition insights, self-hosted — Morgenruf",
        description="Questions that need two datasets at once: blockers nobody has cleared in days, "
                    "and people who answer every standup and are thanked by nobody. No scores.",
        h1="The questions that need two datasets",
        lede="Standups tell you who is blocked. Kudos tell you who was thanked. Together they tell "
             "you something neither can on its own.",
        body=body, schema=[faq_schema],
        hero=shot("/screenshots/members.jpg", "Member cards showing which features each person runs", "Who runs what, at a glance."),
        trail=[("Home", "/"), ("Insights", None)], current="/insights")
