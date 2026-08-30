# Product screenshots

The landing page currently shows a Slack conversation rebuilt in HTML and CSS
(`.slack-mock` in `index.html`) rather than the product. See website#2 for why
that costs credibility against Geekbot and the other named competitors.

Replacing it needs real captures. This file is the spec so the capture session
is short and the results are consistent.

## Do not capture from the live CloudDrove workspace

Every screenshot on this site is public. The production workspace contains real
teammates' names, faces, email addresses and standup content, plus links to
private repositories. None of that can ship.

## Dogfood instead of inventing

Create a `Morgenruf Dev` Slack workspace (free tier is enough) and install the
bot into it. Then run real standups about work on Morgenruf itself.

Every repository in the morgenruf GitHub org is public, so standup answers can
link to genuine issues and pull requests with nothing to redact. That removes
the hardest part of a demo capture, which is inventing engineering work that
does not read as invented. A Reports shot showing actual work on the product
being demonstrated is more convincing than any mock, and it is honest.

The same workspace pays for itself twice more: it is what onboarding should be
tested against, and it is what reproduces issue morgenruf/morgenruf#53, since
that needs a channel containing the bot plus a second app.

## Blocked on

morgenruf/morgenruf#61. Reports currently renders raw Slack markup: links show
as `<https://...|label>`, bold as `*text*`, mentions as `<@U071G30EEKV>`.
Photograph it today and the bug ships as marketing. Capture after that lands.

## Shot list

| # | Shot | Where | Why it earns its place |
|---|------|-------|------------------------|
| 1 | Standup DM, question and answer | Slack DM with the bot | The core interaction. Replaces the CSS mock in the hero. |
| 2 | Posted summary in a channel | Slack channel | What the team actually sees each morning. |
| 3 | Reports, a few days of responses | Dashboard, Reports | The manager view, and the strongest proof the product is finished. |
| 4 | Standups list | Dashboard, Standups | Shows multi-schedule support, which competitors charge for. |
| 5 | Analytics | Dashboard, Analytics | Backs the "every feature from paid tools" claim. |
| 6 | New Standup modal | Dashboard, Standups | Shows questions, days and timezone control in one frame. |
| 7 | App Home | Slack App Home tab | Backs the "no dashboard needed" line in the features grid. |

## Capture settings

- 2x device pixel ratio. A 1x screenshot looks soft on every modern display.
- Browser at 1440 wide for dashboard shots. Wider leaves dead space, narrower
  trips the 900px drawer breakpoint.
- Slack in light mode, dashboard in whichever theme you lead with on the site.
  Do not mix within one section.
- Crop to the content. No browser chrome, no OS chrome, no bookmarks bar.

## Content rules

- Use real work on Morgenruf, linked to public issues in the morgenruf org.
  Anything invented should still avoid placeholder names: "Priya Raman", not
  "User 1".
- Two or three lines per answer, with a blocker in at least one so shot 3 shows
  the blocker styling.
- Do not invent metrics that flatter the product. If the demo workspace sits at
  a 47% completion rate, ship 47%.
- Nothing from the CloudDrove workspace, and no links to private repositories.

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
