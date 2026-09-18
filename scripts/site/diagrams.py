"""Drawn diagrams.

Eight pages had no image at all, which is what makes a page feel like a wall.
A stock photograph would be worse than nothing, so these are drawn in the
brand's own colours and each one carries information the paragraph beside it
would otherwise have to spell out.
"""

INK, AMBER, SUN, ROOSTER, SKY, VIOLET, LEAF = (
    "#12131F", "#FFB23F", "#FFD166", "#E0322E", "#00A3DE", "#4B3BD0", "#0E8A5F")


def _box(x, y, w, h, label, sub, fill="#fff", stroke="#E9E2D6", accent=INK):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-size="15" font-weight="700" fill="{accent}">{label}</text>
<text x="{x + w/2}" y="{y + h/2 + 16}" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#5A5E74">{sub}</text>'''


def _arrow(x1, y1, x2, y2, label="", colour=AMBER):
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    text = (f'<text x="{mid_x}" y="{mid_y - 9}" text-anchor="middle" font-family="Manrope,sans-serif" '
            f'font-size="12" fill="#5A5E74">{label}</text>') if label else ""
    return f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="2.5" marker-end="url(#a)"/>{text}'''


ARROW_DEF = f'''<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
<path d="M0 0 L10 5 L0 10 z" fill="{AMBER}"/></marker></defs>'''


def architecture():
    """What talks to what, for the setup hub."""
    return f'''<figure class="diagram">
<svg viewBox="0 0 760 240" role="img" aria-label="Slack sends events to the Morgenruf app, which reads and writes your own Postgres database. A scheduler inside the app sends standups and coffee chat introductions.">
{ARROW_DEF}
{_box(20, 80, 170, 80, "Slack", "your workspace", "#FFF7EA", "#F0E4CE", INK)}
{_box(295, 80, 170, 80, "Morgenruf", "one process", "#fff", "#E9E2D6", INK)}
{_box(570, 80, 170, 80, "Postgres", "your database", "#FFF7EA", "#F0E4CE", INK)}
{_arrow(190, 105, 290, 105, "events")}
{_arrow(290, 138, 192, 138, "messages")}
{_arrow(465, 120, 566, 120, "reads and writes")}
<rect x="295" y="192" width="170" height="36" rx="10" fill="{INK}"/>
<text x="380" y="215" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#F6F3EC">scheduler, inside the process</text>
<line x1="380" y1="160" x2="380" y2="190" stroke="{AMBER}" stroke-width="2.5" marker-end="url(#a)"/>
<text x="380" y="30" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-size="14" font-weight="700" fill="{INK}">Three things, and nothing else</text>
<text x="380" y="52" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#5A5E74">No queue, no third party, no telemetry</text>
</svg>
<figcaption>Everything runs in one process against one database. Nothing leaves your infrastructure except calls to Slack.</figcaption>
</figure>'''


def standup_flow():
    """A morning, as a timeline."""
    stops = [
        (60, "09:30", "The bot DMs each person", SKY),
        (240, "09:31", "They answer in their own time", VIOLET),
        (420, "10:30", "One summary posts to the channel", LEAF),
        (600, "10:10", "A private nudge to whoever has not", ROOSTER),
    ]
    dots = ""
    for x, time, label, colour in stops:
        words = label.split()
        line1 = " ".join(words[:3])
        line2 = " ".join(words[3:])
        dots += f'''<circle cx="{x}" cy="96" r="9" fill="{colour}"/>
<text x="{x}" y="74" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-size="14" font-weight="700" fill="{INK}">{time}</text>
<text x="{x}" y="128" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#5A5E74">{line1}</text>
<text x="{x}" y="146" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#5A5E74">{line2}</text>'''
    return f'''<figure class="diagram">
<svg viewBox="0 0 700 180" role="img" aria-label="A standup morning: the bot sends a direct message at the scheduled hour, people answer in their own time, whoever has not filed gets a private nudge, and one summary posts to the channel.">
<line x1="60" y1="96" x2="600" y2="96" stroke="#E9E2D6" stroke-width="3"/>
{dots}
</svg>
<figcaption>One morning, in the order it happens. The nudge is private; only the summary is public.</figcaption>
</figure>'''


def pairing_flow():
    """Why a pairing ends in a meeting rather than a promise."""
    steps = [
        ("Pair", "avoiding last round's match", VIOLET),
        ("Introduce", "in a group DM, with an opener", SKY),
        ("Agree an hour", "both press the same button", AMBER),
        ("Meet", "Zoom books it at that hour", LEAF),
    ]
    out, x = "", 18
    for label, sub, colour in steps:
        out += f'''<rect x="{x}" y="40" width="150" height="86" rx="12" fill="#fff" stroke="{colour}" stroke-width="2"/>
<text x="{x + 75}" y="76" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-size="15" font-weight="700" fill="{INK}">{label}</text>
<text x="{x + 75}" y="98" text-anchor="middle" font-family="Manrope,sans-serif" font-size="11.5" fill="#5A5E74">{sub[:26]}</text>'''
        if x < 520:
            out += f'<line x1="{x + 152}" y1="83" x2="{x + 186}" y2="83" stroke="{AMBER}" stroke-width="2.5" marker-end="url(#a)"/>'
        x += 188
    return f'''<figure class="diagram">
<svg viewBox="0 0 760 150" role="img" aria-label="A coffee chat round: people are paired avoiding last round's match, introduced in a group message, they agree an hour by pressing a button, and Zoom books the meeting.">
{ARROW_DEF}{out}
</svg>
<figcaption>The last two steps are the ones most pairing tools leave to the humans, which is where they stall.</figcaption>
</figure>'''


def allowance():
    """Why a budget that resets is the mechanic."""
    return f'''<figure class="diagram">
<svg viewBox="0 0 700 176" role="img" aria-label="Each person gets five tokens a day. Spent ones post publicly with a reason. Unspent ones expire at midnight in that person's own timezone.">
{ARROW_DEF}
<text x="350" y="28" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-size="14" font-weight="700" fill="{INK}">Five a day, each</text>
{''.join(f'<circle cx="{120 + i*34}" cy="70" r="13" fill="{SUN}" stroke="{AMBER}" stroke-width="2"/>' for i in range(5))}
{_arrow(300, 70, 380, 70, "given")}
<rect x="392" y="46" width="180" height="48" rx="10" fill="{LEAF}" opacity=".12"/>
<text x="482" y="70" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#0E8A5F">posted publicly, with a reason</text>
{_arrow(200, 104, 200, 140, "", ROOSTER)}
<text x="330" y="150" text-anchor="middle" font-family="Manrope,sans-serif" font-size="12.5" fill="#5A5E74">whatever is left expires at midnight, in that person's own timezone</text>
</svg>
<figcaption>Scarcity is the design. A budget that resets is what makes people spend it.</figcaption>
</figure>'''
