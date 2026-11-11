# Product screenshots

Last refreshed 2026-11-11, all from invented demo data (the Northstar Studio team). No
production workspace, real person or real Slack message appears in any of them.

## How they are made

**Dashboard shots** come from the real frontend running against the app's in-memory browser
fixture, filled with demo data. From `morgenruf/morgenruf`:

    .venv/bin/python frontend/scripts/demo-backend.py &          # 127.0.0.1:3008
    (cd frontend && API_PROXY_TARGET=http://127.0.0.1:3008 ./node_modules/.bin/vite --host 127.0.0.1 --port 5174 --strictPort &)
    cd frontend && VIEWPORT_WIDTH=960 node scripts/capture-screens.mjs <outDir> [page ...]

A 960px window stacks the cards, so text stays readable once the image is shrunk onto a page.
Use 1440 for wide tables.

**Slack shots** are the app's own Block Kit messages, built by calling the message functions in
`app/src/modules/*` with demo data and rendered in Slack's Block Kit Builder. Only the sender name,
icon, time and mention styling are set in the preview, because the demo people do not exist.

Convert to JPEG under 1600px wide and run `scripts/site/build.py`; it writes the WebP copies.

| File | Shows |
|---|---|
| `standup-summary.jpg` | Slack: the channel summary, blocker on top |
| `kudos-slack.jpg` | Slack: a kudos post with the reason quoted |
| `poll-slack.jpg` | Slack: a named poll with results |
| `today.jpg` | Dashboard: Today's responses, mood, blocked badge, still to answer |
| `today-summary.jpg` | Dashboard: answered, waiting, blocked counts and the blocker |
| `coffee-chat-intro.jpg` | Dashboard: the live preview of the coffee chat introduction |
| `kudos-leaderboards.jpg` | Dashboard: most recognised and most encouraging |
| `members.jpg` | Dashboard: member cards with per-feature admin chips |
| `insights.jpg` | Dashboard: recognition gaps and persistent blockers |
| `celebrations.jpg` | Dashboard: coming up birthdays and anniversaries |

## Do not capture from the live production workspace

Every screenshot on this site is public. A live customer workspace contains real
teammates' names, faces, email addresses and standup content, plus links to
private repositories. None of that can ship.

Capture from a dedicated demo Slack workspace with invented people and invented
work. That workspace is also what onboarding should be tested against, so it
pays for itself twice.

## Capture settings

- 2x device pixel ratio. A 1x screenshot looks soft on every modern display.
- Browser at 1440 wide for dashboard shots. Wider leaves dead space, narrower
  trips the 900px drawer breakpoint.
- Slack in light mode, dashboard in whichever theme you lead with on the site.
  Do not mix within one section.
- Crop to the content. No browser chrome, no OS chrome, no bookmarks bar.

## Content rules

- Invented names that do not read as placeholders. "Priya Raman", not "User 1".
- Real-shaped standup answers, two or three lines, with a blocker in at least
  one so shot 3 shows the blocker styling.
- Do not invent metrics that flatter the product. If the demo workspace sits at
  a 47% completion rate, ship 47%.
- No links to private repositories. Point issue links at a public repo.

## Delivery

- WebP with a JPEG fallback via `<picture>`.
- Under 200KB each after compression. The Lighthouse job in CI will catch
  regressions.
- Name by shot: `01-standup-dm.webp`, `03-reports.webp`.
- Alt text describes what the shot shows, never the word "screenshot".
- Add `loading="lazy"` and explicit `width` and `height` so the page does not
  shift as they load.

## Worth doing in the same session

A short screen recording of the install. "Up and running in 30 seconds" is the
central claim on the page and is currently only asserted.
