"""The setup guides.

"How do I self-host a Slack standup bot" is a question with intent behind it
and no good answer on the open web: every result is a hosted product's signup
page. These pages are the answer, and each one carries HowTo schema so the
steps can surface directly in a result.
"""

from __future__ import annotations

import diagrams

import json

from shell import INSTALL, REPO, SITE, SLACK_MARK, breadcrumbs, cta_band, faq, footer, head, nav


def howto(name, description, steps, total_time="PT20M"):
    return json.dumps({
        "@context": "https://schema.org", "@type": "HowTo", "name": name,
        "description": description, "totalTime": total_time,
        "step": [{"@type": "HowToStep", "position": i + 1, "name": s[0], "text": s[1]}
                 for i, s in enumerate(steps)],
    })


def guide(prose_html, toc):
    """Contents beside the text. Built from the same list the headings use."""
    links = "".join(f'<a href="#{slug}">{label}</a>' for label, slug in toc)
    return (f'<section class="section"><div class="wrap"><div class="guide">'
            f'<nav class="toc" aria-label="On this page"><strong>On this page</strong>'
            f'<div class="toc-links">{links}</div></nav>'
            f'<div class="prose">{prose_html}</div></div></div></section>')


def page(*, path, title, description, h1, lede, body, schema=(), trail=(), current=""):
    crumb_html, crumb_schema = breadcrumbs(trail)
    schemas = list(schema) + ([crumb_schema] if crumb_schema else [])
    return (head(title=title, description=description, path=path, schema=schemas)
            + nav(current) + crumb_html
            + f'''<main>
<header class="page-head"><div class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></header>
{body}
</main>''' + cta_band() + footer())


HUB_FAQ = [
    ("How long does it take to set up?",
     "About twenty minutes end to end: ten to create the Slack app from the manifest, five to start "
     "the containers, and five to point it at a channel. Migrations run themselves on first start, "
     "so there is no database step beyond having a Postgres URL."),
    ("What do I actually need?",
     "A machine that can run Docker or a Kubernetes cluster, a Postgres database, and an HTTPS URL "
     "Slack can reach. A Cloudflare tunnel covers the last one without opening a port."),
    ("Can I try it without a server?",
     "Yes. Run it on your laptop with Docker Compose and expose it with a tunnel while you try it. "
     "Nothing about that is different from the production path except where it runs."),
    ("Do I need a paid Slack plan?",
     "No. Morgenruf uses the standard Slack app APIs available on the free plan."),
]


def hub():
    body = '''<section class="section"><div class="wrap">
  <span class="eyebrow">Three ways in</span>
  <h2 id="pick-a-way-to-run-it">Pick a way to run it</h2>
  <div class="tiles" style="margin-top:24px">
    <a class="tile" href="/setup/docker">
      <h3>Docker Compose</h3>
      <p>The shortest path. One file, one command, runs on a laptop, a VPS or a spare Mac mini.</p>
      <span class="go">Set it up with Docker →</span>
    </a>
    <a class="tile" href="/setup/kubernetes">
      <h3>Kubernetes and Helm</h3>
      <p>A published chart, an external Postgres, and an ingress or a tunnel. For clusters you already run.</p>
      <span class="go">Set it up with Helm →</span>
    </a>
    <a class="tile" href="/setup/slack-app">
      <h3>The Slack app</h3>
      <p>Creating the app from the manifest, the scopes it asks for and why, and installing it.</p>
      <span class="go">Create the Slack app →</span>
    </a>
  </div>

  <div class="prose" style="margin-top:54px">
    ''' + diagrams.architecture() + '''
    <h2 id="what-you-need-before-you-start">What you need before you start</h2>
    <ul>
      <li><strong>Somewhere to run it.</strong> Any machine with Docker, or a Kubernetes cluster.
      It is a single Python process and a Postgres database; it is not demanding.</li>
      <li><strong>Postgres.</strong> Anything from 13 up. Migrations apply themselves when the app
      starts, so an empty database is enough.</li>
      <li><strong>An HTTPS URL Slack can reach.</strong> Slack posts events to your app, so it needs
      a public address. A Cloudflare tunnel works and needs no open port.</li>
      <li><strong>A Slack workspace where you can install apps.</strong> Whoever installs it becomes
      the first admin.</li>
    </ul>

    <h2 id="the-shape-of-it">The shape of it</h2>
    <p>Three things talk to each other: Slack, the app, and your database. Slack sends events to
    your URL, the app writes to Postgres, and a scheduler inside the app sends the messages that
    start standups and coffee chats. There is no other service and nothing phones home.</p>

    <div class="note"><p><strong>One value people miss:</strong> <code>FLASK_SECRET_KEY</code> signs
    dashboard sessions. Generate a real one with <code>openssl rand -hex 32</code>. Leaving it blank
    means nobody can stay logged in.</p></div>

    <h2 id="after-it-is-running">After it is running</h2>
    <ol>
      <li>Open your app URL and sign in with Slack. You are the first admin.</li>
      <li>Create <a href="/standups">a standup</a>: pick a channel, the questions, the hour, and
      who takes part.</li>
      <li>Turn on <a href="/coffee-chats">coffee chats</a> and <a href="/kudos">kudos</a> when you
      want them. Both are off until you say so.</li>
      <li>Optional: connect Zoom so coffee chats book a real meeting, and set up a digest email.</li>
    </ol>
  </div>
</div></section>
'''
    faq_html, faq_schema = faq(HUB_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span>
  <h2 id="before-you-begin">Before you begin</h2>
  <div style="margin-top:24px">{faq_html}</div>
</div></section>'''
    return page(
        path="/setup",
        title="Set up a self-hosted Slack standup bot",
        description="Three ways to run Morgenruf yourself: Docker Compose, Kubernetes with Helm, or "
                    "from source. What you need, and the Slack app, in about twenty minutes.",
        h1="Set it up yourself, in about twenty minutes",
        lede="Morgenruf is one process and a Postgres database. Pick whichever of these you already "
             "have, and the Slack side is the same either way.",
        body=body, schema=[faq_schema],
        trail=[("Home", "/"), ("Set up", None)], current="/setup")


DOCKER_STEPS = [
    ("Create the Slack app", "Create an app from the manifest in the repository, add your redirect "
     "URL under OAuth and Permissions, and copy the client id, client secret and signing secret."),
    ("Clone and configure", "Clone the repository, copy .env.example to .env, and fill in the three "
     "Slack values, a Postgres URL, APP_URL and a generated FLASK_SECRET_KEY."),
    ("Start the containers", "Run docker compose up -d. Migrations apply themselves on first start, "
     "so an empty database is enough."),
    ("Give Slack a URL it can reach", "Expose the app over HTTPS, with a reverse proxy or a "
     "Cloudflare tunnel, and set that address as APP_URL."),
    ("Install it into Slack", "Open your app URL, authorise the workspace, and create your first "
     "standup. Whoever installs it becomes the first admin."),
]

DOCKER_FAQ = [
    ("Can I run this on a Mac mini or a Raspberry Pi?",
     "A Mac mini yes, and it is a good home for it. On a Pi you would need an arm64 image; the "
     "published image is amd64, so build it yourself on the Pi or use a small cloud VM instead."),
    ("Does Docker Compose bring its own Postgres?",
     "Yes, the bundled compose file starts one for you. For anything you care about, point "
     "DATABASE_URL at a managed Postgres instead and keep backups out of the container's lifecycle."),
    ("How do I upgrade?",
     "Pull the new image and restart: docker compose pull && docker compose up -d. Migrations run "
     "on start, and they are written to be safe to run against a live database."),
    ("How do I back it up?",
     "It is one Postgres database, so pg_dump is the whole backup story. No state lives in the "
     "container."),
]


def docker():
    prose = '''<h2 id="what-you-need">What you need</h2>
<ul>
  <li>Docker and Docker Compose</li>
  <li>A Slack workspace where you can install an app</li>
  <li>A way to give Slack an HTTPS URL. A Cloudflare tunnel is fine and needs no open port.</li>
</ul>
<p>Nothing on this page costs money beyond the machine it runs on, which is the point of
<a href="/blog/async-standups-slack-free">running async standups in Slack for free</a>.</p>

<h2 id="1-create-the-slack-app">1. Create the Slack app</h2>
<p>Do this first, because the next step wants three values from it. The
<a href="/setup/slack-app">Slack app page</a> covers it properly; the short version is: create an
app from the manifest, add <code>https://your-domain/oauth/callback</code> as a redirect URL, and
copy the client id, client secret and signing secret.</p>

<h2 id="2-clone-and-configure">2. Clone and configure</h2>
<pre><code>git clone https://github.com/morgenruf/morgenruf.git
cd morgenruf/app
cp .env.example .env</code></pre>
<p>Open <code>.env</code> and set at least these:</p>
<pre><code>SLACK_CLIENT_ID=...
SLACK_CLIENT_SECRET=...
SLACK_SIGNING_SECRET=...
DATABASE_URL=postgresql://morgenruf:password@db:5432/morgenruf
APP_URL=https://standups.your-domain.com
FLASK_SECRET_KEY=$(openssl rand -hex 32)</code></pre>

<div class="note"><p><strong>APP_URL has to be the address Slack will call</strong>, not localhost.
If you are using a tunnel, put the tunnel's URL here and restart after it changes.</p></div>

<h2 id="3-start-it">3. Start it</h2>
<pre><code>docker compose up -d
docker compose logs -f app</code></pre>
<p>The log will show migrations applying and then <code>Scheduler started</code>. That is the whole
startup: there is no separate migration step and no seed data to load.</p>

<h2 id="4-let-slack-reach-it">4. Let Slack reach it</h2>
<p>Slack posts events to your app, so it needs a public HTTPS address. If you already run a reverse
proxy, point it at port 3000. If you do not:</p>
<pre><code>cloudflared tunnel --url http://localhost:3000</code></pre>
<p>Copy the <code>https://….trycloudflare.com</code> address it prints, set it as
<code>APP_URL</code>, and restart with <code>docker compose restart app</code>. For anything
permanent, use a named tunnel rather than a quick one, because the quick URL changes each run.</p>

<h2 id="5-install-it">5. Install it</h2>
<p>Open your app URL in a browser and authorise the workspace. You become the first admin, and the
dashboard opens on an empty Standups page. Create one: channel, questions, the hour, and who takes
part. What <a href="/standups">a standup does once it is running</a> is described separately, as are
<a href="/coffee-chats">coffee chats</a>, which stay off until you turn them on.</p>

<h2 id="keeping-it-running">Keeping it running</h2>
<ul>
  <li><strong>Upgrades:</strong> <code>docker compose pull &amp;&amp; docker compose up -d</code>.
  Migrations apply on start.</li>
  <li><strong>Backups:</strong> it is one Postgres database. <code>pg_dump</code> is the whole
  story.</li>
  <li><strong>Logs:</strong> <code>docker compose logs -f app</code>. Standups, coffee chat rounds
  and delivery failures all appear there.</li>
</ul>

<div class="note"><p><strong>Stuck?</strong> The
<a href="https://github.com/morgenruf/morgenruf/issues">issue tracker</a> and
<a href="https://github.com/morgenruf/morgenruf/discussions">discussions</a> are where setup
questions get answered, and <a href="/support">CloudDrove will do the whole thing for you</a> if you
would rather not.</p></div>

<div class="next">
  <a class="tile" href="/setup/slack-app"><h3>The Slack app</h3><p>The manifest, the scopes and why each one is asked for.</p><span class="go">Read it →</span></a>
  <a class="tile" href="/setup/kubernetes"><h3>Kubernetes instead</h3><p>The Helm chart, an external database, and ingress or tunnel.</p><span class="go">Read it →</span></a>
</div>
'''
    body = guide(prose, [("What you need", "what-you-need"), ("1. Create the Slack app", "1-create-the-slack-app"),
                         ("2. Clone and configure", "2-clone-and-configure"), ("3. Start it", "3-start-it"),
                         ("4. Let Slack reach it", "4-let-slack-reach-it"), ("5. Install it", "5-install-it"),
                         ("Keeping it running", "keeping-it-running")])
    faq_html, faq_schema = faq(DOCKER_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="running-it-with-docker">Running it with Docker</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/setup/docker",
        title="Run a Slack standup bot with Docker Compose",
        description="Self-host Morgenruf with Docker Compose: environment variables, starting the "
                    "containers, giving Slack an HTTPS URL with a tunnel, upgrades and backups.",
        h1="Set it up with Docker Compose",
        lede="The shortest path, and the one to use if you are trying it out. One compose file, one "
             "command, and a tunnel if you have nowhere public to put it.",
        body=body,
        schema=[howto("Set up Morgenruf with Docker Compose",
                      "Self-host an open-source Slack standup bot using Docker Compose.",
                      DOCKER_STEPS), faq_schema],
        trail=[("Home", "/"), ("Set up", "/setup"), ("Docker", None)], current="/setup")


K8S_STEPS = [
    ("Add the chart repository", "helm repo add morgenruf https://charts.morgenruf.dev and run helm repo update."),
    ("Prepare a database", "Point externalDatabase.url at a Postgres you control. Migrations run in an init container on every rollout."),
    ("Install the release", "helm upgrade --install with your Slack credentials, app URL and a generated Flask secret key."),
    ("Expose it", "Use an ingress, a Gateway API HTTPRoute, or a Cloudflare tunnel if the cluster has no ingress controller."),
    ("Install into Slack", "Open the app URL, authorise the workspace, and create the first standup."),
]

K8S_FAQ = [
    ("Does the chart ship a database?",
     "It can, but do not use it for anything you care about. Point externalDatabase.url at a managed "
     "Postgres so the data outlives the release."),
    ("How do migrations run?",
     "An init container runs them before the app container starts, so a rollout is also a migration. "
     "When you pin an image tag, set it on both containers or the init container will run the old "
     "migrations against the new code."),
    ("Can it run without an ingress controller?",
     "Yes. A Cloudflare tunnel in the same namespace works, and the chart has values for it. "
     "Nothing needs a public load balancer."),
    ("How many replicas?",
     "One. The scheduler lives in the process, and two replicas would both try to send the morning "
     "standup. Horizontal scaling is on the roadmap behind a shared lock; until then, one."),
]


def kubernetes():
    prose = '''<h2 id="install">Install</h2>
<pre><code>helm repo add morgenruf https://charts.morgenruf.dev
helm repo update

helm upgrade --install morgenruf morgenruf/morgenruf \\
  --namespace morgenruf --create-namespace \\
  --set slack.clientId="YOUR_CLIENT_ID" \\
  --set slack.clientSecret="YOUR_CLIENT_SECRET" \\
  --set slack.signingSecret="YOUR_SIGNING_SECRET" \\
  --set externalDatabase.url="postgresql://user:pass@host:5432/morgenruf" \\
  --set flaskSecretKey="$(openssl rand -hex 32)" \\
  --set app.url="https://standups.your-domain.com"</code></pre>

<div class="note"><p><strong>Use a real database.</strong> The chart can start one for you, which is
fine for a look, but point <code>externalDatabase.url</code> at managed Postgres for anything you
intend to keep. The data outliving the release is the point.</p></div>

<h2 id="exposing-it">Exposing it</h2>
<p>Slack has to reach the app over HTTPS. Three ways, in order of how common they are:</p>
<ul>
  <li><strong>Ingress.</strong> Set <code>ingress.enabled=true</code> and your host. Standard
  annotations for cert-manager work.</li>
  <li><strong>Gateway API.</strong> An HTTPRoute is supported for clusters that have moved on from
  Ingress.</li>
  <li><strong>Cloudflare tunnel.</strong> No ingress controller, no public load balancer, no open
  port. Useful on a homelab cluster or anywhere the cluster is not internet-facing.</li>
</ul>

<h2 id="one-replica-on-purpose">One replica, on purpose</h2>
<p>The scheduler that fires <a href="/standups">standups</a>, <a href="/coffee-chats">coffee chat
rounds</a> and the midnight <a href="/kudos">kudos</a> reset runs inside the app process. Two
replicas would both wake up at nine and both send the morning message. Until that moves behind a
shared lock, run one replica and let Kubernetes restart it; a restart mid-round resumes rather than
repeating, because delivery is recorded per person as it happens.</p>

<h2 id="upgrades">Upgrades</h2>
<pre><code>helm repo update
helm upgrade morgenruf morgenruf/morgenruf --reuse-values</code></pre>
<p>Migrations run in an init container before the new app container starts. If you pin an image tag
rather than using the chart's, set it on <strong>both</strong> the app and the migrate container, or
you will run the previous release's migrations against the new code.</p>

<h2 id="what-to-watch">What to watch</h2>
<ul>
  <li><code>kubectl logs deploy/morgenruf -c migrate</code> after a rollout, to see which migrations
  applied.</li>
  <li><code>Scheduler started with N jobs</code> in the app log. N should grow when you add a
  standup.</li>
  <li>The status page endpoint, if you run your own monitoring.</li>
</ul>

<div class="note"><p><strong>Stuck?</strong> Ask in
<a href="https://github.com/morgenruf/morgenruf/discussions">discussions</a>, or have
<a href="/support">CloudDrove run the cluster for you</a>.</p></div>

<div class="next">
  <a class="tile" href="/setup/slack-app"><h3>The Slack app</h3><p>The manifest, the scopes, and installing it.</p><span class="go">Read it →</span></a>
  <a class="tile" href="https://github.com/morgenruf/helm-charts"><h3>Chart values</h3><p>Every value the chart takes, with defaults.</p><span class="go">Open the chart →</span></a>
</div>
'''
    body = guide(prose, [("Install", "install"), ("Exposing it", "exposing-it"),
                         ("One replica, on purpose", "one-replica-on-purpose"),
                         ("Upgrades", "upgrades"), ("What to watch", "what-to-watch")])
    faq_html, faq_schema = faq(K8S_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="running-it-on-kubernetes">Running it on Kubernetes</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/setup/kubernetes",
        title="Kubernetes and Helm setup for a Slack standup bot",
        description="Install Morgenruf on Kubernetes with the published Helm chart: values, "
                    "external Postgres, ingress or Cloudflare tunnel, migrations, and why one "
                    "replica.",
        h1="Set it up on Kubernetes",
        lede="A published chart, an external Postgres, and whichever way you already expose things. "
             "Migrations run themselves on every rollout.",
        body=body,
        schema=[howto("Install Morgenruf on Kubernetes with Helm",
                      "Self-host an open-source Slack standup bot on Kubernetes using the published "
                      "Helm chart.", K8S_STEPS, "PT15M"), faq_schema],
        trail=[("Home", "/"), ("Set up", "/setup"), ("Kubernetes", None)], current="/setup")


SLACK_STEPS = [
    ("Create the app from the manifest", "At api.slack.com/apps choose Create New App, then From an "
     "app manifest, and paste slack-manifest.yaml from the repository."),
    ("Add the redirect URL", "Under OAuth and Permissions add https://your-domain/oauth/callback."),
    ("Copy the credentials", "From Basic Information, copy the client id, client secret and signing "
     "secret into your environment or Helm values."),
    ("Install it into the workspace", "Open your app URL and authorise. Whoever installs it becomes "
     "the first admin."),
    ("Invite the bot to a channel", "Invite the bot to the channel a standup posts in, and to any "
     "channel coffee chats pair from."),
]

SLACK_FAQ = [
    ("Why does it ask for so many scopes?",
     "It does not ask for all of them at once. Standups need the basics: reading channel membership, "
     "writing messages, and opening DMs. Coffee chats add three more, because a group introduction is "
     "a multi-person DM. Kudos needs emoji read access to use your own token. A workspace that never "
     "turns on coffee chats never grants those scopes."),
    ("What are the three extra coffee chat scopes?",
     "mpim:write and mpim:history, to open and follow the group DM an introduction lives in, and "
     "users.profile:read, to know each person's timezone so a suggested hour is not the middle of "
     "their night."),
    ("Can I restrict it to one channel?",
     "Yes. The bot only acts in channels it has been invited to, and each standup names its own "
     "channel. Nothing happens anywhere it has not been asked."),
    ("Does it read our messages?",
     "No. It reads replies to its own DMs and the membership of channels you point it at. It has no "
     "scope to read channel history."),
    ("Who becomes the admin?",
     "Whoever installs the app. That person can promote others, hand out per-feature grants, and "
     "always counts as an admin even if their member row is removed, so a workspace cannot lock "
     "itself out."),
]


def slack_app():
    prose = '''<h2 id="1-create-the-app-from-the-manifest">1. Create the app from the manifest</h2>
<p>Go to <a href="https://api.slack.com/apps">api.slack.com/apps</a>, choose <strong>Create New
App</strong>, then <strong>From an app manifest</strong>, pick your workspace, and paste the
contents of <a href="https://github.com/morgenruf/morgenruf/blob/main/slack-manifest.yaml">slack-manifest.yaml</a>
from the repository.</p>
<p>The manifest sets the scopes, the slash commands, the event subscriptions and the App Home tab in
one go, which is why it is worth using rather than clicking through the settings.</p>

<h2 id="2-add-your-redirect-url">2. Add your redirect URL</h2>
<p>Under <strong>OAuth &amp; Permissions</strong>, add:</p>
<pre><code>https://your-domain/oauth/callback</code></pre>
<p>This has to match the <code>APP_URL</code> you configured, including https.</p>

<h2 id="3-copy-three-values">3. Copy three values</h2>
<p>From <strong>Basic Information</strong>, copy the <strong>client id</strong>,
<strong>client secret</strong> and <strong>signing secret</strong> into your environment or Helm
values. The signing secret is what lets the app verify a request genuinely came from Slack; without
it every event is rejected.</p>

<h2 id="4-what-it-asks-for-and-why">4. What it asks for, and why</h2>
<p>Scopes are the part people read carefully, so here is each group and what it is for.</p>
<ul>
  <li><code>channels:read</code>, <code>groups:read</code> — to see who is in the channel a standup
  or a coffee chat draws from.</li>
  <li><code>chat:write</code> — to post the summary and the introductions.</li>
  <li><code>im:write</code>, <code>im:history</code> — to ask each person their questions in a DM and
  read their answers to it.</li>
  <li><code>users:read</code>, <code>users:read.email</code> — names and email, for the dashboard and
  the digest.</li>
  <li><code>users.profile:read</code> — timezones, so nobody is asked at midnight.</li>
  <li><code>mpim:write</code>, <code>mpim:history</code> — the group DM a
  <a href="/coffee-chats">coffee chat</a> introduction happens in. Only needed if you turn coffee
  chats on.</li>
  <li><code>emoji:read</code> — so <a href="/kudos">kudos</a> can use a custom token from your
  workspace.</li>
  <li><code>commands</code> — the slash commands.</li>
</ul>
<p>There is no scope for reading channel history, because the app never does.</p>

<div class="note"><p><strong>If you installed before coffee chats existed</strong>, your workspace
will not have granted the three mpim scopes. Coffee chats stay dark until you reinstall, rather than
failing at runtime, and the dashboard tells you which scopes are missing.</p></div>

<h2 id="5-install-and-invite">5. Install and invite</h2>
<p>Open your app URL, authorise, and you are the first admin. Then invite the bot to the channel the
summary posts in, and to any channel you want coffee chats to pair from. The bot has to be in the
channel before <a href="/standups">a standup</a> can post there:</p>
<pre><code>/invite @Morgenruf</code></pre>

<h2 id="slash-commands-you-get">Slash commands you get</h2>
<ul>
  <li><code>/standup</code> — start your standup now</li>
  <li><code>/skip</code> — skip today</li>
  <li><code>/kudos @teammate a reason</code> — give recognition</li>
  <li><code>/help</code> — what the bot can do</li>
</ul>

<div class="next">
  <a class="tile" href="/setup/docker"><h3>Docker Compose</h3><p>Get the app itself running in a few minutes.</p><span class="go">Read it →</span></a>
  <a class="tile" href="/setup/kubernetes"><h3>Kubernetes</h3><p>The Helm chart, values and rollouts.</p><span class="go">Read it →</span></a>
</div>
'''
    body = guide(prose, [("Create from the manifest", "1-create-the-app-from-the-manifest"),
                         ("Add your redirect URL", "2-add-your-redirect-url"),
                         ("Copy three values", "3-copy-three-values"),
                         ("What it asks for, and why", "4-what-it-asks-for-and-why"),
                         ("Install and invite", "5-install-and-invite"),
                         ("Slash commands", "slash-commands-you-get")])
    faq_html, faq_schema = faq(SLACK_FAQ)
    body += f'''<section class="section"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Questions</span><h2 id="about-the-slack-app">About the Slack app</h2>
  <div style="margin-top:24px">{faq_html}</div></div></section>'''
    return page(
        path="/setup/slack-app",
        title="Create the Slack app: manifest, scopes, install",
        description="Create a Slack app from the Morgenruf manifest, add the redirect URL, and see "
                    "every scope it asks for, including the three extra ones coffee chats need.",
        h1="Create the Slack app",
        lede="Ten minutes, and the only part that touches Slack's settings. The manifest does most "
             "of it; the rest is three values and an invite.",
        body=body,
        schema=[howto("Create a Slack app for Morgenruf",
                      "Create and install the Slack app for a self-hosted standup bot.",
                      SLACK_STEPS, "PT10M"), faq_schema],
        trail=[("Home", "/"), ("Set up", "/setup"), ("Slack app", None)], current="/setup")
