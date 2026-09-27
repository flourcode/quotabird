# QuotaBird — handoff

**Current build: 2026-10-28.0900** This file has two parts. Part one is the site as it is today; work from it. Part two is an archive of how it got here; read it for the reasoning, never as instructions.

## North star (Mark's words, Oct 27)

"All my years of selling, 'Dude, my quota is crazy!' has been a recurring conversation starter between sales reps, managers, and teams. Reps usually have no idea how their quota and comp plans are created. Managers may find their boss isn't even goaled on their number, it may be growth rate or new business. Managers don't know how to fight comp plans and also don't know how to help reps accept a tough quota and still crush it. Everyone in sales loves a bluebird, but usually, it's just the Quota Bird dropping off more quota."

The site's primary focus: helping people **plan, push back, and accept** quota, armed with data. It should be the go-to resource for a rep questioning their quota.

**Stop at the point.** Mark's rule (Oct 27): when the point is made, stop. Home is "Is your quota crazy? / Maybe. Let's do the math. / Push back or build a plan." and then the button, nothing more. No trailing tag lines after the point ("Free. Nothing stored.", "No email.", "One minute, nothing stored.", card feet like "No login. No names."). The privacy promise lives in each page's FAQ ("Does anything I enter leave my device?"), not tacked onto the end of other copy. No closing sentence that restates or sells.

## North star (Oct 26 pivot)

QuotaBird is primarily about helping sales reps and managers **understand quota, push back on a bad quota with evidence, and accept a tough but legitimate quota by building a plan to hit it.** The conversation at the center of the site: *"Dude, my quota is crazy."* The site answers: is it actually crazy? If so, prove it. If not, what does it take to hit it?

**The constraint that runs everything: know the math well enough to tell whether they're screwing you.** Not a grievance site. Sometimes the quota is crazy, sometimes it's hard but defensible, sometimes the rep just doesn't like the number; the site helps tell those apart. Mark is retired, not looking for another job; he enjoys helping people figure things out.

**Three paths, on the home page and everywhere quota comes up:** (1) Understand it: `/how-quotas-get-built/` (where quotas come from; "your boss may not be goaled on your number"). (2) Push back: `/quota-case/` (the bridge) and the note "Your quota is crazy. Now prove it." (3) Accept it and plan: the note "The number isn't changing. Now what?" and Pipeline Check (works backward from the quota). Comp: the note "Before you decide the comp plan sucks, figure out how it pays", Quota Check, Commission Check.

**The bird (Oct 27, decided by users): Mark's bluebird.** Users preferred the bluebird, and the joke works better that way: everybody wants a bluebird; instead, the Quota Bird shows up. A cheerful little bird carrying terrible news. Mark's drawing, `better_blue.svg`: body #88B1CB, round eye, outline and eye in the site's ink (#121A22, never pure black). `logo.svg`, `favicon.svg`; dark versions (`logo-dark.svg`, favicon dark style) give the outline a light rim (#E9EFF4) so the beak and wing line don't vanish; the 404 (`logo-x.svg`) is the same bluebird with an X eye. `logo.png`, `favicon.png`, `apple-touch-icon.png` are rendered from the SVG (check the local server is running first). Yellow, raven and blackbird versions were all tried and dropped; don't bring them back.

**The palette (restored Oct 27, final): the original bluebird palette.** Mark tried raven, yellow, a warm-ink monochrome and a mustard/Material palette, and came back to this. Don't re-propose any of them.

- Page: pure white #FFFFFF. Text: inky black #131619; greys #556270 / #667380; lines #DDE4EA; panels #EDF2F7 / #E0E6EC.
- The bird: #9DD2FF body, ink outline and eye (#131619), Mark's drawing. Dark versions get a light rim so the beak doesn't vanish; the 404 bird has an X eye.
- One blue family for the interface (Mark's monochromatic scale): #4FAEFF, #6AB8FF, #86C5FF, #9FD1FF, #B8DDFF, #D3E7FF, #EAF4FF. These are fills with ink text on them (7.6:1 or better); none of them can be text on white.
- The one blue that can be text or a button on white: #0A71B1 (5.2:1). Buttons and links use it. Dark mode: the button is the bird (#9DD2FF with #00182B text).
- The highlighter under "crazy?" is #9DD2FF. Selected answers and pills: #D3E7FF. By the Numbers panels: #9DD2FF with ink text, ink bars and white bars with an ink outline (dark mode: #184B71 panel, bird-blue and white bars).
- Verdict pastels: green #C6EBC9, yellow #FFF982, orange #FFCF8A, red #F5B3AD.
- Colour lives on the book covers; the interface stays blue and ink.

**One system (Oct 28). The site used to look like three design systems sharing a page (app UI, editorial data graphics, poster-like books). Now everything follows one set of M3-style rules:**
- **Type:** Google Sans Flex (SIL OFL 1.1, `gsf-OFL.txt`), self-hosted as `gsf.woff2`, subset to the site's characters with the weight (300-900) and optical-size (12-72) axes kept; 63 KB. The share cards and social images use the same file. Inter is retired.
- **Shape:** 16px for cards (question cards, verdicts, lists, paths, offers, Quota Shorts, stat cards, the featured book); 12px for controls (buttons, answer choices, inputs, chips, menu items, small books). Circles stay circles (avatars, step numbers, progress dots).
- **One container:** light cool fill #F6F9FC with a thin cool outline #DDE4EA, no shadows. **One emphasis container:** light bird blue #EAF4FF with #C9E1F7 outline, used only for the featured Quota book, the booking card, and the headline stat. Otherwise colour only where it means something: the primary button (#0A71B1) and the verdict tints.
- **The shelf is one family of books:** every cover the same container, the bird mark in brand blue, only the Quota book tinted. No per-tool colours (Mark decided against semantic colours per tool: they made the shelf lively but weakened the identity).
- **Stats are plain cards** (`stat()` / `stat_grid()` in `make-tools.py`): value, label, a source line per section. No editorial giant numbers, donuts or bar charts. Quota Shorts are plain cards with the number inside the sentence.
- The rules live in one block at the end of `site.css` ("One system"), which wins over older rules above it.

**The shelf** uses Mark's original multicoloured covers in their original order, led by the Quota book (Oct 27): Quota coral #E07A5F (featured), Pipeline #F2C14E, Deal navy #1C3D5A, Rep teal #388073, Territory #F4E1C1, Account #6C5B7B, Competition #C35037, Risk #2E2E3A with gold type, Discount #9DD2FF, Commission #567E55, Partner #F28482, Talent Review #264653 with gold type, Brief #E9C46A, Field Kits #EDEDE9, Sales Math #1D3557. Quota Shorts use the same colours. Share card, banner and social images match.

## What QuotaBird is

quotabird.com: quota help first, and a shelf of other free sales tools by Mark Flournoy for sellers and managers (mostly cloud, AI, cyber and data, many selling to government). Nine question tools, five calculators (Quota Check, Quota Case, Pipeline, Discount, Commission), three printable Field Kits, nine Field Notes, four Sales Math pages, How quotas get built, About, Stuff I Like, and Ask Mark, which is the consulting funnel ("Got a quota problem?"). No login, no AI, nothing stored, nothing typed into a system a boss can see. Not affiliated with the U.S. government or Amazon.

## QuotaBird voice

**Tone reference: the Stuff I Like page.** Mark is older, mildly grumpy, somewhat jaded, dry, concise, and occasionally funny. Seen a lot, skeptical by default, mildly amused by how sales organizations behave. He does not perform wisdom, optimism, warmth, toughness, or expertise. He assumes the reader is an adult who has been in sales a while. He can call something stupid, corny, flaky, ugly, or a bad idea when that's the simplest description. Humor comes as an aside, not a punchline ("Twenty-some minutes and you know enough about the economy to sound less surprised."). Advice sounds earned, not packaged. Understatement is fine ("Pretty much what it says."), and some sentences can be dismissive ("Your library or podcast app can find them."). Not every page needs to reveal a philosophy; sometimes the answer is "this pipeline is thin."

**Mark knows bullshit when he sees it.** Low patience for fake pipeline, fake urgency, fake partner activity, fake coaching and management theater. Especially skeptical of sales programs that ask more from reps while making comp plans worse, quotas less attainable and territories less coherent. He does not treat AI as magic: if it helps a rep research, write or prepare faster, fine; if a company thinks it can replace trust, judgment, customer context, negotiation or an experienced seller with a bot, he's skeptical. He sides with evidence over management fashion. He is not anti-company, anti-management, or anti-AI. He is anti-bullshit.

Short is good, but don't manufacture punchiness. Avoid tidy three-sentence conclusions, résumé triplets, "That matters," "the useful part," "here's why," "the point is," and neat X-not-Y constructions. Don't explain the joke. Don't make every paragraph land. Mild words like "suck," "crazy," "ugly," "stupid," and "hopium" are fine when they sound natural. No weapons/death/kill language (one deliberate exception on About, Mark's own line; don't add more). Prefer the thing a seller would actually say: "Does this territory suck?" over "Assess territory viability." Keep "QuotaBird is mostly stuff I wish we'd had back then."

**The coffee test:** would Mark say it to one person over coffee? If it reads like website copy, a LinkedIn bio, a keynote intro or a founder statement, rewrite it. Remove performative summary sentences: if a passage compresses credentials, motivation and an offer into a neat run of short declaratives, rewrite it as something a person would say out loud. One plain thought at a time, uneven rhythm, specific words, mild informality. If a sentence sounds designed to prove credibility, simplify it until the facts carry it. Model line (Made by Mark): "I spent six years leading federal partner sales teams at AWS, after plenty of years carrying a number myself. QuotaBird is mostly stuff I wish we'd had back then. Most of it's free. If the problem's messier than a little tool can handle, we can talk it through."

Mechanics: contractions always; "territory" not "patch"; "customer" not "account" when it means the buyer; no em or en dashes anywhere; American spelling; buttons 18 characters or fewer; Mark's bio wording is exactly "six years leading federal partner sales teams at AWS"; company list is Amazon, Microsoft, Google, Oracle (his).

## The 14 tools

| URL | Tool | Kind | Headline on the page |
|---|---|---|---|
| /deal/ | Deal Check | questions (hand-written page) | Is it real, or is it hopium? |
| /pipeline/ | Pipeline Check | calculator (pipeline.src.html) | You sure that's enough pipeline? |
| /quota/ | Quota Check | calculator | Is my quota crazy? |
| /quota-case/ | Quota Case | calculator | What has to be true for this quota to work? |
| /rep/ | Rep Check | questions | Is it the rep, or the territory? |
| /territory/ | Territory Check | questions | Does this territory suck? |
| /account/ | Account Check | questions | Do you know your customer? |
| /competition/ | Competition Check | questions | Why you and not them? |
| /risk/ | Risk Check | questions | Are two deals carrying your year? |
| /discount/ | Discount Check | calculator | How much discount is too much? |
| /commission/ | Commission Check | calculator | It closed. What do I actually keep? |
| /partner/ | Partner Check | questions | Is this partner doing anything? |
| /olr/ | Talent Review Check | questions (nav says "Talent Review") | Can you defend your people? |
| /brief/ | Brief Check | questions, with Pressure test | Will your brief survive the room? |

Question tools run on `check.js`; calculators on `calc.js`; Deal and Pipeline carry their own scripts. Five questions per tool, in a fixed order (scoring and shared links depend on it); every question answerable with yes, sort of, or no. Deal, Talent Review and Brief have a Pressure test (three hard questions from the room).

## The home page and the shelf

Home, top to bottom: THE QUOTA LANDED / **Is your quota crazy?** / "Maybe. Let's do the math." / one line on what to look at / *Check my quota* (the one blue button) and "or see how quotas get built" / the three paths / "Know the math well enough to tell whether they're screwing you. Sometimes they are, and sometimes the number is just hard." / **The quota isn't the only problem.** / the shelf.

Shelf, 15 covers in order: Start here (featured): Is my quota crazy? · Pipeline: Enough pipeline? · Territory: Does this territory suck? · Commission: What do I actually keep? · Deal: Is this even a deal? · Rep: Rep or territory? · Risk: Too much riding on two deals? · Partner: Is this partner doing anything? · Discount: They want a discount. · Account: Do you know them? · Competition: Why you? · Talent Review: Can you defend them? · Brief: Will this survive? · Field Kits: Worth printing. · Sales Math: Why 3X?

Covers are the short version; each opens on the fuller question (the tool's h1). Covers live in `home.src.html`; the share card, banner and social images carry their own copies in `make-card.py` and `make-social.py`. Fifteen fills the grid exactly: replace covers, don't add. The 404 shows the same shelf.

## The consulting funnel

Every result screen, in order: verdict → what to fix → (Pressure test, tonal button) → **Mark's card** ("Stuck on …?", one blue button *Grab 20 minutes* to Calendly with the verdict pre-filled, a secondary *DM me on LinkedIn* that copies a short note, fine print "It's free, and if I can't help, I'll say so.") → next-step card to another tool → fedhoo line (federal-relevant weak answers only) → Share · Start over. Same card after a finished Pressure test. One blue button per result.

Ask Mark (`/ask/`): "Want to talk it through?" → one sentence → *Grab 20 minutes* + "or DM me on LinkedIn" → three steps (Pick a time / I read it before we talk / Twenty minutes, free; if I can't help, I'll say so in the first five) → Mark's photo and one line of background plus the company names → "What people usually bring me" (four problems) → Manager Wingman and Team session side by side (no prices yet; "If we keep going, I'll tell you what it costs before we do anything.") → a line for people not ready.

Kits end with the same offer and a bridge line ("Used this with your team and found something ugly? That's most of the stuff I help managers with."). Every page carries the Made by Mark card. Calendly: calendly.com/markflournoy/chat-with-mark with utm_source=quotabird and utm_medium=<page>. Email mark@quotabird.com. LinkedIn linkedin.com/in/markflournoy/.

Analytics (GA4 `G-BG9NR9GXQZ`, `analytics.js`): `front_pick`, `<slug>_start`, `verdict`, `<slug>_book` (Deal: `book`), `<slug>_book_after_grill`, `<slug>_dm_copy`, `<slug>_share`, `ask_book`, `kit_download`/`seller_download`/`leader_download`, `<slug>_fedhoo`. The "Useful?" row and its events are gone.

## Data pages (Oct 27)

- **Quota Shorts**: snack-size cards (Headway-style), one fact + one line + source + the tool that does the math. One list, `SHORTS` in `make-tools.py`, feeds the swipeable strip on the home page (after the three paths, before the shelf) and the full page at `/shorts/`. Card colours are the shelf's.
- **Quota by the numbers** (`/quota-by-the-numbers/`): the sourced benchmarks in receipt rows, with a sources list. Every number on a Short must be on this page with its source.
- **How quotas get built** now opens with how a big company builds the number (company target → capacity → territories → quotas → comp plan), over-assignment, consumption quotas, and fiscal calendars.
- **Numbers used (research Sept 27, 2026; refresh each year):** Bridge Group 2026: 48% of AEs at 100%+ (51% in 2024, 66% in 2022), median quota $960K, OTE $200K, 4.6× (4.2× in 2024), quotas +2.4%/yr vs OTE +4.9%/yr, ramp 6.2 months; Bridge 2024: 53:47 mix. RepVue (self-reported, Sept 2026): AEs 42% reach quota, enterprise 41%, federal 46%, SLED 45%; Cloud Sales Index Q2 2025 average attainment 42.69% across 246 companies; AWS Account Manager $150K base / $280K OTE / 54:46 / 64% hit; Microsoft Enterprise AE 56%, SLED AE 67%. Mostly Metrics: over-assignment 20–30%. Accelerators 1.5–2× (comp surveys). Microsoft fiscal year July–June; Microsoft field incentives tied to Azure consumed revenue (Microsoft Learn). Keep "share of reps at 100%" and "average attainment" separate; never swap them.

## Navigation

Header: Tools ▾ · Field Kits · Field Notes · About · Ask Mark (chip). Do not add to it. The Tools menu leads with Your number (Quota Check, Quota Case, Territory, Commission, Discount), then Your team, Your deal, Any meeting. Footer: Tools · Field Kits · Sales Math · Field Notes · Stuff I Like · About · Ask Mark, then "QuotaBird is a pile of free sales tools. I built them because they helped me, and maybe they'll help you." and "Not affiliated with the U.S. government or Amazon." The Tools menu lists the tools by audience; on desktop it drops the rows the header already shows.

## Design rules that hold

One font (Google Sans Flex, self-hosted). One type scale: 11, 13, 15, 17, 22, 28, 36 (h1 36; section h2 22; intro line 22 in `--ink-2`; body 17). Monochrome plus the bird's yellow (see the north star); one ink button per screen. Every tap target 44px; every button has hover, pressed and focus states. Receipt-style rows: labels left, values right; centering only for fine print. Mark's photo: round, floated left, text wraps with a straight edge (same on About and Ask Mark). Example values in calculators are grey until edited. Covers are 3:4. Kits print to 4, 8 and 3 pages (Seller / Manager / Leadership); re-check after any kit copy change.

## Build and deploy: which files to edit

- **Edit:** `make-tools.py` (every generated page's copy and structure), `home.src.html`, `pipeline.src.html`, `deal/index.html`, `check.js`, `calc.js`, `analytics.js`, `site.css`, `partials/*.html`, `404.html`, `make-card.py`, `make-social.py`.
- **Never edit by hand:** `index.html`, every other `*/index.html`, `sitemap.xml`, `llms.txt`, `ai-catalog.json`, the hashed `site.<hash>.css` / `check.<hash>.js` / `calc.<hash>.js` / `analytics.<hash>.js` (the build writes them and links every page to them; stale ones are removed), `card*.jpg`.
- **Build:** `python3 make-tools.py` (regenerates all pages, sitemap, llms.txt, ai-catalog, fingerprints, share-tag hygiene). Cards: `python3 make-card.py <slug|home|banner>` then rebuild so fingerprints match. Collateral: `python3 make-social.py`. Copy workbook: `python3 extract-copy.py`.
- **Deploy:** AWS Amplify from GitHub; `amplify.yml` strips the build tools and sources; `customHttp.yml` caches css/js for a year (safe: names change) and html not at all; rewrites in `amplify-rewrites.json` (43 rules, 404 catch-all last). New pages need a `/<slug>` → `/<slug>/` rule.
- **Never edit the live site directly;** the next deploy overwrites it. Send copy changes through the build (or the workbook).

## What not to change

The shelf (15 covers, one Start here). The five questions per tool and their order. The "nothing stored / no AI / no login" promises (the fedhoo line is a plain link; nothing is sent). The header. Mark's bio wording and company list. `/olr/` as Talent Review's URL and `/kit/` as the Manager's kit's. The voice rules above.

## Pending (Mark)

New notes from the brief, not yet written: The best quota fight happens before January · Show me the bridge · If only 20% of the team hits quota, maybe the reps aren't the problem · Your boss may not be goaled on your quota · When a tough quota is still a fair quota · A bluebird is not a territory plan · One giant deal made last year's number · New reps don't produce twelve months of revenue in six months · A vacant territory still has quota · Stop using 3X pipeline if your win rate is 18%.


Replace `mark.jpg` (background-removal artifacts; it now sits beside the booking button). Prices for Wingman and Team session. Calendly: 20-minute event, one intake question, no automated marketing emails. Submit the sitemap in Search Console. Then: post the Field Notes; write new notes before new tools (candidates: the deal that's been "closing this month" for three months; ask the partner to name three relationships; is no pipeline really a prospecting problem; everybody likes your champion, can they buy anything).

---

## Archive: history and decisions already made (do not rebuild from this)

Everything below is the record of how the site got here, kept for the reasoning behind decisions. It is not a description of the current site; the section above is. Where the two disagree, the section above wins.

### Original handoff (KillMyDeal → SellClouds → QuotaBird)

Everything needed to maintain, extend or rebuild this. One directory, two
pages, one shared stylesheet and font, no build step, no server, no dependencies.

**Current build: 2026-10-25.1100**

## Naming: checks, not kills

The tools were called *Kill My Deal*, *Kill My Pipeline* and so on until
October 2026. The sales-humor didn't land with a lot of readers, and "kill"
unsettled some, so the family became **checks**: Deal Check, Pipeline Check,
Brief Check, Territory Check, Partner Check, Rep Check, OLR Check, under the
umbrella line *Quick reality checks for complicated deals*. Buttons read
*Check my deal*, *Check a deal*, *Check my case* (OLR). The punch lives in
the headlines instead of the names: *Before you commit it, prove it.*,
*Before you renew the partnership, test it.*, *Before you walk into OLR,
test your case.* Verdicts lost the same edge: Deal Check is **Healthy /
Hopium / At risk / Not a deal yet**, Pipeline Check is **Covered / Hopium /
At risk / Short**, and the 404 says *Wrong turn.* *Hopium* stays: it's the
most-quoted word on the site and funny without being dark. Do not bring
"kill", "dead" or weapons language back into names, headlines, verdicts or
buttons. The dead bluebird mascot is retired; the only mark is Mark's
S-cloud. The engine is `check.js` (`CheckTool({...})`); URLs and analytics
event names were already neutral and did not change.

## QuotaBird

As of October 2026 the site is **QuotaBird** (quotabird.com). It was Kill My
Deal, then briefly SellClouds; the SellClouds name never landed, and the
bird was the best asset all along. Positioning: *quick reality checks for
people who carry a number.* Same Rick Steves voice, same rules (no "kill",
no weapons language, no hype, no dark patterns).

**The bird is back, with a round eye.** `logo.svg` is a vector rebuild of
the original bluebird PNG (body and outline traced separately at 8× after a
heavy Gaussian blur, radius 22, which removes the pixel stair-steps of the
256px source; 41 curve segments, not 259; the
eye is a true circle at (156.3, 84.8), radius 16.5, where the X used to
be). Body `#9DD2FF`, outline `#122F4D`; `logo-dark.svg` swaps the outline
for the accent blue (`#1DA1F2`, the button colour; white read as a hard rim
on dark); `favicon.svg` switches by colour scheme; the PNG icons and every
share card are rendered from it. The S-cloud mark is retired. The 404 page alone uses `logo-x.svg` /
`logo-x-dark.svg`, the same bird with the original X eye: that is the one
place the bird is meant to be dead.

**Thirteen tools, and that's the shelf for a while.** A second round of
suggestions (Forecast, Champion, Close Plan, Discovery, Business Case,
Exec Meeting Prep, Value, Expansion) was declined as overlap with Deal
Check's five questions; three real gaps were built as question tools:
- **Account Check** (`/account/`): *Do you know the account, or just your
  contact?* MISSION, MONEY, POWER (beyond the deal), INCUMBENT, PATH.
  Verdicts *Mapped / Half mapped / One thread / A contact*. Hands off to
  Deal Check when the account is known, Territory Check when it isn't.
- **Risk Check** (`/risk/`): *4X coverage can still be a house of cards.*
  The shape of the pipeline, not the size: SPREAD, MOTION, NEXT, TIMING,
  FRESH, all phrased so Yes is the safe answer. *Sturdy / Lopsided /
  Fragile / House of cards*. Hands off to Pipeline Check for the size.
- **Competition Check** (`/competition/`): *Why you, instead of nothing?*
  NOTHING (cost of inaction), SWITCH, PREFERENCE, PROOF, ACCESS.
  *Preferred / In the mix / Behind / Nothing wins*. Hands off to Deal Check
  or, when behind, Account Check.
The menu and the home doorways now use four groups: *Your deal* (Deal,
Account, Competition), *Your number* (Quota, Territory, Discount,
Commission), *Your team* (Pipeline, Risk, Rep, Partner, OLR), *Any
meeting* (Brief); the menu balances them into two columns (`menu()`).

**Ten tools, in two kinds.** Seven question tools (Deal, Territory, Brief,
Rep, Partner, OLR, plus the Pipeline calculator) and three new calculators
rebuilt from the old Fedmo tools page:
- **Quota Check** (`/quota/`, *Is my quota crazy?*): first asks what the
  number is measured in, because the OTE multiple is a commission rate in
  disguise (10% on bookings at 50/50 ≈ 5× OTE; 1–2% on consumption growth ≈
  25–50×). Three ladders, quota ÷ OTE, Low / Favorable / Standard / A stretch
  / Aggressive / Crazy at these cut points: **new bookings** 3, 4, 6, 8, 12
  (the published consensus: Bridge Group, RepVue, Pavilion all say 4–6×);
  **cloud consumption growth** 8, 15, 30, 45, 60; **whole book** 20, 40, 80,
  120, 160. The cloud and whole-book cuts are Mark's ranges from CSP and
  partner plans, derived from the rates those plans pay; there is no public
  dataset for them (the sites that "estimate" AWS quotas at 5× are applying
  the SaaS formula, not reporting). They live in one line (`B` in the quota
  config) and the page says they are ranges, not rules. Also shown: implied
  rate (variable ÷ quota), variable share of OTE, growth over last year's
  close. The example is a cloud AM: $150K base, $130K variable, $6M growth
  target → 21×, Standard. Hands off to Pipeline Check with the quota
  prefilled as the target (`/#t=…`).
- **Discount Check** (`/discount/`, *They want a discount.*): revenue given
  away, commission lost, margin after (cost of goods held constant, so the
  margin falls faster than the discount). Normal (≤5%) / Meaningful (≤15%) /
  Expensive (≤25%) / Giveaway. Hands off to Deal Check ("is it the price, or
  the deal?").
- **Commission Check** (`/commission/`, *It closed. What do I take home?*):
  gross, withheld, net at ~30% (W-2), ~40% (high bracket) or ~20% (1099).
  Planning estimate, labelled not tax advice. Hands off to Quota Check.
All three open verdict-first, like the home page: the example result and
its one-line reading sit under the hero, the fields come after, and the
summary strip carries the answer while you're down in the fields. Every
tool's intro is one sentence that says what to do ("Plug in your own numbers
to find out.", "Answer five questions and find out whether…"); keep it to
one. All three run on `calc.js` (`CalcTool({...})`), a sibling of `check.js`:
fields with example values, live update on input, share links that carry the
inputs, DMs and booking notes in percentages and multiples only. Configs
live in `CALCS` in `make-tools.py`; the page template is `calc_page()`.
Menu group *Your number*; home doorways *I just got my quota*, *They want a
discount*, *It closed*.

**The front door is a shelf.** *The sales problems shelf / Pick the problem
you've got.* Fifteen covers styled as a matched paperback series: the
thirteen tools plus Field Kits and Sales Math. Each cover is the problem in
the user's words (*Is my quota crazy?*), the small label above it is the tool
("Territory", no "Check", so labels fit a phone), and a faint Quota Bird in
the corner of each cover is the publisher's mark. Deal Check is the big
*Start here* cover so nobody has to choose. Fifteen fills a 3-column phone
grid and a 6-column desktop grid with no orphans; adding or removing a
cover breaks that, so replace rather than add. Covers keep their own colors
in dark mode. Question tools open on question 1 via `#start`.

**Context survives the tap.** Covers open question 1 directly (`#start`), so
every question screen carries a context line built from the page's own
tool name and headline: on question 1 a small hero (tool, the question in
the user's words, "Five questions, about a minute, nothing stored."), on
questions 2 to 5 one quiet line. Both engines (`check.js`, the Deal page)
read it from the intro at load, so a new tool gets it for free. Back
twice reaches the full intro. The 404 page shows the same shelf, pulled
from `home.src.html` at build time between `<!--shelf-->` markers; the
shelf is deliberately not on About or elsewhere (the Tools menu is the
shelf in list form, and each tool's hand-off names the specific next step).

**The front door asks the question (superseded by the shelf).** The home page opens with *What's
giving you trouble this week?* and six first-person answers, styled like the
tools' own answer buttons: a deal, pipeline, quota, a rep, a partner, a deck
or brief. Six is the cap (more is a menu). Each is one tap into the right
tool, and the question tools open on question 1 via a `#start` link
(`/deal/#start`, `/rep/#start`…; `check.js` and the Deal page both honor
it). The pipeline answer scrolls to the calculator, which sits right below
the front door with its own heading. Recognition is the instant value here:
a jaded seller sees their week named before they see a number. All six fit
above the fold on a 375×667 phone; the tool names beside each answer show
only from 420px up. Taps count as `front_pick`.

**Home is Pipeline Check, second.** The site is named for the number, so the front
door is the tool that checks it. On a phone the order is hero, verdict card
and coverage bar (`#out`), the fields, then the rows, clock, hand-off, share
and Mark card (`#out2`); on desktop the fields sit left and the two output
blocks stack on the right. The example (3.2X, At risk, 3X says covered and
20% says $18M short) is the light bulb and must be on the first screen of a
375×667 phone; it is. The summary strip shows only while the fields are on
screen and the verdict has scrolled off the top. A hash with a target but no
pipeline (Quota Check's hand-off) fills every field: the target, pipeline at the
3X ballpark Quota Check just quoted, the conservative Federal 20% win rate,
$500K deals and *just me*, and says exactly that in a banner, so the page
opens on a real verdict (*3X says you're covered, your 20% win rate says
you're $12M short*) and nobody has to know which fields to touch. The
page's own example uses the same 20% default. The first edit clears the
banner. It is not treated as a shared verdict. The earlier home hero (a
live Deal Check question, then a photo byline) was replaced by this; Deal
Check still accepts a 1-to-4 letter hash as a check in progress.

| Path | What |
| --- | --- |
| `/` | **Home = Pipeline Check.** Hero (*You sure that's enough pipeline?*), the calculator with the verdict above the fields, then *Nine more checks* doorways, the 3X essay, how the tools work, Field Notes, About, FAQ. `/pipeline/` redirects here. |
| `/deal/` | **Deal Check**, formerly the home page |
| `/quota/`, `/discount/`, `/commission/` | the calculators (Quota, Discount, Commission Check) |
| `/account/`, `/risk/`, `/competition/` | the October 2026 additions: Account Check, Risk Check, Competition Check |
| `/brief/`, `/territory/`, `/partner/`, `/rep/`, `/olr/` | the generated five-question tools |
| `/about/` | **About Mark**: the full story and the booking steps; every other page carries only the short *Made by Mark* card |
| `/notes/` | **Field Notes**: short reads, each ending with the tool that does the math |
| `partials/mark.html` | the About section every page carries (bio, situations, *Need another set of eyes?*) |
| `home.src.html` | source for the home page; the script fills in the notes list |
| `site.css`, `inter.woff2` | shared design system and typeface |
| `check.js`, `calc.js`, `make-tools.py` | the question engine, the calculator engine; the generator for everything (tools, calculators, notes, home, header, About, sitemap) |

**One command builds everything.** `python3 make-tools.py` regenerates the five
question tools, the Field Notes, the home page, then stamps the same header
and the same About section onto every page (including the hand-written Deal
and Pipeline pages and the 404), then rebuilds every FAQ's structured data.
Edit the header in `header()`, the About in `partials/mark.html`, a note in
`NOTES`; never edit those parts inside a page.

**Who it's for, in the copy.** Jaded, overworked sellers and sales managers:
making the number, managing up to a boss who wants the forecast by noon,
keeping cranky customers happy. The home dek says exactly that. Doorways
and the Tools menu use the same three groups: *For sellers* (Deal, Quota,
Territory, Discount, Commission), *For managers* (Pipeline, Rep, Partner,
OLR), *Any meeting* (Brief). The About's situations open with the one every
seller recognises: the forecast call has become the job.

**Mark's AWS role, in his own words:** *six years leading federal partner
sales teams at AWS* (or "led federal partner sales teams at AWS" where the
six years is already stated). Never "led partner sales at AWS" or "ran
partner sales"; the difference matters to him and to anyone who was there.

**Nav.** Header: bird + *QuotaBird* (home), *Field Notes* and *About* as
text links on screens 700px and wider, an *Ask Mark* chip that jumps to the
*Need another set of eyes?* heading on the current page, and the *Tools*
menu: a compact two-column list of the ten tools in three groups, no
subtitles, with Home / Field Notes / About in a small row underneath
(307px tall on a phone; it was over 550). Because Tools is the first
item in the nav, the panel is not anchored to the chip's right edge: on
phones it spans the screen under the header (`.menu { position:static }`,
`left:16px; right:16px`), on wider screens it centres under the chip. Every footer also carries
Tools · Field Notes · About · Ask Mark. No Services, no
Solutions, no Consulting.

**Every screen asks one easy question.** From the October 2026 UX review
(three videos, consolidated): the tools already ask easy questions, so the
work went into the questions the site asks about Mark. Six changes, keep them:
- *The hero is the tool.* The home page is Pipeline Check with its example
  verdict on the first screen (see *Home is Pipeline Check*).
- *Trust at the top, as a clause, not a face.* The photo byline was tried and
  removed: on a small phone it pushed the value below the fold. Credibility
  is one clause in the dek ("back when I carried a number and led partner
  sales teams at AWS"); the photo lives in the About.
- *Specific cost under every start button*: "5 taps · about a minute ·
  nothing stored" (home: "Free · no login · nothing stored"). No "one
  minute" in the deks; the note says it once, precisely.
- *Sticky start.* On tool pages, once the start button scrolls away a copy
  rides at the bottom (`stickyStart()` in `check.js` and the Deal page); it
  hides over the About/booking section and while a check is running.
- *A booking that feels safe, not sold.* The About ends with a three-step
  "how it works" (pick a time; I read your line first; twenty minutes, then
  you decide, no pitch, no sales follow-ups), the line "If I don't think I
  can help, I'll tell you.", and a short button: *Chat with Mark*. "Twenty minutes, free" lives in step 3,
  not on the button. Result-card links read *Or book a call*.
  Those are promises; keep them true.
- *One left edge on desktop.* `#screen` is left-aligned so the tool column,
  the prose and the logo share an edge; the Pipeline page uses `.wide-page`
  so its prose aligns with the wider calculator.
Deliberately not adopted: crossed-out prices, countdowns, "most popular"
badges, sensory hype. This audience runs those plays on its own customers.

**Button labels: 18 characters or fewer, always one line.** Details (time,
cost, what happens next) go in the text around a button, never in its label.
The longest labels today are *Check my territory* (18), *Check my pipeline*,
*Copy this & DM me* and *I can answer that* (17). Every button, chip and
answer choice was measured in every screen state at 320px, 360px and
desktop: none wraps or clips. Re-run that check (`btns.js` in the test
scripts) after adding any button.

**Review of 2026-10-08, what was taken and what wasn't.** Taken: Tools
first in the nav (use the tools first, call if they're not enough); the long
About block cut from every page and replaced by the short *Made by Mark*
card (`partials/made-by.html`), with the full story and booking steps on
`/about/`; *Grill me* renamed **Pressure test** on Deal, OLR and Brief (the
analytics event stays `grill`); rules of thumb reworded as ranges Mark has
seen, not the usual range; Commission Check's presets became an editable
*Set aside for taxes* field (the IRS supplemental rate is a flat 22% federal
plus payroll and state, so the old "withheld ~30%" was wrong as stated; the
percentages are planning buffers now, and the copy says so); three more
Field Notes (quota vs territory, 15% off, the rep who hates meetings), each
ending at its tool; site-wide `related_tool_click` and `ask_mark_click`
events plus a one-tap *Useful? Yes / Not really* after every verdict
(`<slug>_useful_yes|no`); home metadata about QuotaBird, not pipeline, with
a *One of ten quick checks ↓* link under the hero. Not taken: moving
Pipeline Check off the home page (instant value on load was a deliberate
choice, and the phone screenshot backs it); renaming OLR Check to Talent
Review (the users are at Amazon); more bird decoration.

**Analytics is the standard Google tag, on purpose.** On 2026-09-25 Windows
Defender flagged a zip of the site (`Trojan:Win32/MalUri.A!cl`, a cloud/ML
heuristic) on `analytics.js` and `about/index.html`. Inspection found nothing
but the site's own files; the likely triggers were two benign-but-suspicious
patterns in `analytics.js`: a `<script>` element created at runtime with a
URL built from a variable, and a page-wide click listener reading every
link's href. Both are gone: the gtag script is a plain `<script async src>`
tag in every head (Google's documented install), `analytics.js` only
configures it and counts named events, and the two extra counts attach to
the specific elements. The photo's inline `onerror` handler was removed too.
Keep it that way: no runtime script injection, no global link listeners, no
inline event handlers. The site has no executables and references only its
own domain, LinkedIn, Calendly, fedhoo, Google Tag Manager, schema.org and
sitemaps.org.

**The Manager's Field Kit (`/kit/`).** A free printable, no email gate:
ten short chapters (first 30 days, the weekly rhythm, the forecast call,
pipeline, your boss, a struggling rep, review season, mistakes, lines that
work) and five worksheets, in Mark's plain voice: a retired sales guy who
has signed on to a few dumpster fires, first person, no methodology, no
travel metaphors. One filled button at the top (*Print or save PDF*, which
calls `window.print()`), chapter chips for jumping around on a phone, and a
*Chat with Mark* card at the end. The print stylesheet drops the site
chrome, lets chapters flow with headings kept attached, puts each worksheet
on its own page, and prints the CTA as a short card with the URL: 12 pages
on Letter and A4. If you change the content, re-check the page count and
the "About 12 pages" note. Events: `kit_print`, `kit_book`. Linked from the
menu, the footer, the home page and `llms.txt`.

**The kit is a real PDF, promoted by one card.** `kit/managers-field-kit.pdf`
(8 pages, Letter or A4) is rendered from `/kit/` with the print
stylesheet; `kit/preview-1.jpg` and `preview-2.jpg` are its page 1 and page 4
(the deal-inspection worksheet) at 480px. **When the kit's words change,
re-render all three**: open `/kit/` in Chrome, Print, Save as PDF, Letter,
default margins, background graphics on; then export pages 1 and 4 as
images. The promo card (`partials/kit-card.html`: stacked page preview,
*Free printable* pill, one sentence, filled *Download the PDF* with the
`download` attribute, *What's inside*) is injected above *Made by Mark* on
the home page and the manager pages (`KITCARD_PAGES`: home, Rep, Partner,
OLR, Risk, Field Notes, Sales Math, About). The kit page uses the same card
as its hero, with *Print this page* as the quiet second action; on phones
the button comes before the preview so it stays above the fold. Nav: *Free
kit* in the header on desktop, and a highlighted *Free: The Manager's Field
Kit (PDF)* row at the top of the Tools menu on every screen. Downloads count
as `kit_download`. PDFs are cached for a day.

**Sales Math Library (`/math/`).** Citation pages for the arithmetic behind
the tools, each with a one-paragraph short answer at the top (the sentence
people and AI answers will quote), the formula, a table, a worked example, a
*Run your own* card to the matching tool, a Sources list and a *Cite this
page* line. Four pages: pipeline coverage by win rate, quota-to-OTE as pay
mix ÷ rate, discount math (commission and margin), commission take-home
(withholding). The rule, and it is not optional: **the math needs no
source; every benchmark has one; Mark's experience is labelled as
experience.** Sourced today: IRS Publication 15 (2026) for the 22% / 37%
supplemental rate; Bridge Group's 2024 SaaS AE report for median OTE
($190K, 53:47), with the 11.5% rate and 4.2× multiple attributed to the
secondary summaries that report them (the full report is gated). The two
check each other (0.47 ÷ 0.115 = 4.1×), which is the page's argument.
Federal sales-cycle benchmarks are listed as *coming when I find data I
trust*; don't publish a number without a source. Pages are generated from
`MATH` in `make-tools.py` (tables computed, not typed); each calculator and
the home 3X essay link to their page, and `llms.txt` lists them.

**Agent discovery files.** `llms.txt` (llmstxt.org format) and
`ai-catalog.json` (ARD / ai-catalog schema 1.0, served at
`/.well-known/ai-catalog.json` and at the root) are generated by
`make-tools.py` from the same `TOOLS` list as the site, with a
representative-queries list per tool (`QUERIES`); add a tool there and both
files update. The catalog validates against the ARD schema; every entry is a
`text/html` page with a `urn:air:quotabird.com:tools:<slug>-check` URN. They
exist because Google's page audit checks for them; they cost nothing and
describe the site accurately.

**Voice rules (from the October 2026 read-through of all 30 pages).** The
site should sound like one veteran seller talking, not a manual:
- **Contractions, always**: don't, isn't, can't, it's, you're. The oldest tool
  pages were written "do not / is not" (Territory and Partner were 100%
  formal); that is the single biggest tell of machine-written or corporate
  copy, and it's gone. Every page now sits between 0 and 12% formal, the same
  as the kits.
- **Rarely "X isn't Y. It's Z."** One or two on the site is speech; more is a
  template. Say the thing directly.
- **No lecturing**: no "make sure", "you should", "you must", "always", "never"
  (the privacy promise "never sends your answers" is a promise, not a lecture).
  First person ("I'd", "what I do") in the kits; plain second person on the
  tools is fine.
- **Headings are specific and plain**, never the same template on five pages.
- **No AI vocabulary** (leverage, robust, navigate, journey, unlock...) and no
  dashes. A quick check: search the built pages for those words and for "do not",
  "is not", "make sure" and "you should".
- **The site's one idea: every tool is the question you're hoping nobody asks.**
  Tool headlines are that question (*Is it a deal, or is it hopium? Is it the
  rep, or the patch? Can this patch make the number? Will your case survive
  the room?*), not instructions ("Before you X, test Y"). Intros are one
  sentence starting "Five questions…" with different endings; never the same
  sentence on seven pages.
- **Warm about the person, unsentimental about the deal.** The edge lives in
  the verdicts (*Doing nothing is beating you, and it isn't even trying*;
  *Pick one account and one date, or stop pretending this is a partnership*)
  and is aimed at the deal, the pipeline or the case, never at the reader.
  The explanations around the tools stay plain and even-tempered.
- **"Actually" only when it's the point** (what the customer *actually* said
  versus what's in the CRM). Not as padding ("when they're actually in the
  room"). Fifteen padding uses came out in October.
- **The coffee test (Oct 24, the rule every line now follows):** remove
  performative summary sentences. If a passage compresses credentials,
  motivation and an offer into a neat run of short declarative sentences,
  rewrite it as something a person would say out loud. No résumé triplets
  ("I carried a number, managed people who did, and…"), no symmetrical pairs,
  no "I did X, then Y, therefore Z", no tidy closers ("If you need more, I do
  that too", "good enough", "That's what X is for"). One plain thought at a
  time, uneven rhythm, specific words, mild informality; not every paragraph
  has to land cleanly. If a sentence sounds designed to prove credibility,
  simplify it until the facts carry it. Test: would Mark say it to one person
  over coffee? If it sounds like website copy, a LinkedIn bio, a keynote intro
  or a founder statement, rewrite it. Model line (Made by Mark): "I spent six
  years leading federal partner sales teams at AWS, after plenty of years
  carrying a number myself. QuotaBird is mostly stuff I wish we'd had back
  then. Most of it's free. If the problem's messier than a little tool can
  handle, we can talk it through."
- **Mark's rules, in his words (Oct 23):** plainspoken, literal, jaded
  salesperson. No "it's not this, it's that". No third sentence that states
  the obvious. Short sentences and fragments are fine ("No login. No AI.").
- **Mark's own voice (from his first round of edits, Oct 22).** Plain seller
  words, not insider ones: *territory* not *patch*, *customer* not *account*
  when it means the buyer. Literal over clever: he replaced every metaphor he
  touched (*a logo on a slide* became *just promises*). Blunt with some edge
  (*Does my territory suck? Is your pipeline just a pipe dream?*). Fewer
  disclaimers: cut "no deck", "no methodology", "no names"; result cards end
  "Send me your problem." except where money is involved (Commission, Quota,
  Discount, Pipeline, Risk keep "no dollar figures"). Warm and personal
  (*I'll do my homework before we talk. Can you defend your people?*).
  Amazon-specific where it fits (*an Amazon doc read*).
- **Write like a 58-year-old sales manager who's seen this movie before, not a
  28-year-old copywriter describing what sales managers experience.** In
  practice: assume the reader has been in sales a while; prefer the sentence
  you'd say out loud; mild annoyance is good and cleverness is optional; don't
  wrap up every thought; and if a sentence sounds quotable, be suspicious.
- **Never tell the reader a point matters. Make the point matter.** No "That
  matters.", "The useful part is", "The point is", "The important thing",
  "Here's why", "The reality is", "At the end of the day". No sentence that
  explains the joke after the joke.
- **Rooms don't respect things; people do.** Say "nobody cares about your
  deck", not "the room isn't attacking the document."
- Lines to keep because they're unmistakably Mark: *hopium with a spreadsheet*,
  *pick the day you're having*, *a couple of storage companies you've probably
  forgotten*, *no new sales religion*, *like Santa, but with quota*.
- **Careful contracting "it is / that is / there is":** only when the word is
  the subject ("whether it's moving", "and that's the point"). Never when it's
  the object of the word before it: "behind it is sane", "short of that is
  hope", "after that is an answer", "underneath it is real". The October
  contraction pass got nine of these wrong; all are fixed.
- Editing copy that lives inside the tool configs (JavaScript inside Python
  strings) needs an escaped apostrophe: `\\'` in the source. Run a syntax
  check on every page after copy edits.

**Example numbers look like examples.** Every calculator opens on example
values in quiet grey (`.is-example`, `--ink-2`, 5.5:1 on the field); a
field turns full ink the moment the user types in it or taps a chip that
fills it, so at a glance you can tell your numbers from the assumptions.
After the Quota Check hand-off the quota is black and the assumed fields are
grey; a shared link shows someone's real numbers, all black.

**Contrast meets WCAG AA everywhere (measured Oct 19, light and dark).** Two
blues: `--accent` (#0A71B1) for text, links and buttons, which passes 5.2:1
with white text and 5.1:1 as a link; `--accent-bright` (#1DA1F2, the brand
blue) only for decoration (progress bar, kit-preview edge). Never put text in
the bright blue. Cover colours were checked the same way: white titles need
4.5:1, so teal, rust and green were darkened a hair and Quota's coral carries
dark text; the share card and banner use the same colours.

**One type scale: 11, 13, 15, 17, 22, 28, 36** (plus 76 for the big verdict
number). Every page renders six to eight sizes; before October 18 the home
page used sixteen (13, 14, 15, 16, 17, 18 and 19 all appeared). Inputs are
17px, so iOS never zooms. Tiny-phone overrides (under 360px) and print
sizes (in pt) sit outside the scale on purpose. Use a size from the scale;
don't add one.

**Every tap gets a response.** Buttons, answer choices, chips, doorways,
menu rows, kit links and footer links have a pressed state (a slight
shrink, off for reduced-motion users). Keyboard focus is a site-wide 2px
accent ring. In dark mode the book covers are dimmed 10% so the pale ones
don't glare.

**Phone tap targets: 44px.** Every button, menu row, footer link, chip and
text link outside running prose is at least 44px tall on a phone (chips are
40px, which Material allows). Measured October 2026 across the home page,
Deal, Quota, the kit pages and About, open menu included. Prose links inside
sentences are the exception, as everywhere on the web. Page weight is 115 to
240 KB in 6 to 8 requests; every input is 16px so iOS doesn't zoom; every
image has width and height so nothing jumps. The footer nav is regenerated
on every page each build (it had drifted on Deal). The sticky start button
hides over the About/Made-by section and over the footer.

**The ask is soft on purpose.** The three-tier rate card is gone. The About
section ends *Need another set of eyes? 20 minutes. Free. No deck required.*
and one quiet line: *If it's something that takes more than a conversation,
we can figure that out too.* That is the whole consulting pitch.

**Not built yet, deliberately.** *Field Kits* (paid PDF guidebooks) go into
the nav when the first one exists and not before; a store with prices for
things that don't exist is the one un-Rick-Steves move available. The line
*"They're free. I'm retired. I have time."* was proposed for the home page
and left out; it's Mark's to say, and it sits oddly next to a booking link.


**The mark** is Mark's own design: an S drawn as one flowing stroke through a
six-lobed cloud. The shipped version is "option 6" from the October 2026
weight study: stroke 96, lobes 6% larger than the original drawing, and every
corner (the outer notches and the inner points) rounded to a radius of 24.
It's built from exact geometry (six identical circles on a regular hexagon
plus one symmetric curve for the S, see `logo-src/geometry.py`), then the
corners are rounded and the result stored as a single filled path.
`logo.svg` is ink `#131619`, `logo-dark.svg` is `#E8EDF2`, and `favicon.svg`
switches with the browser's colour scheme. `favicon.png`, `apple-touch-icon.png`
and `logo.png` (600px tall, for the share cards) are rendered from the SVG;
if the mark changes, change the SVG and re-render those. `logo-src/` stays
out of the web root.

**Footers** all end *Not affiliated with the U.S. government or Amazon.*
The OLR tool and the AWS credentials make the Amazon half worth saying.

The third part of the family — can the team defend what they're carrying — is
the consulting, not software. Do not brand it "Kill My Review"; two products
and a person is a system, three "Kill My" things is a bit.

---

## 1. What it is

A federal seller answers five questions about a deal and gets a verdict, the
question their manager is most likely to ask, and the one thing to go do before
the review. About a minute on a phone.

It is not a CRM, a forecast model, or a system of record. It is a **rehearsal**:
the sixty seconds before somebody senior says *"okay, tell me about this deal."*

**Hero:** *Before you commit it, try to kill it.*
**Promise:** *Five questions to separate proof from hopium before your manager does.*
**Philosophy (not on the page):** *Hope is not evidence.*

### The vocabulary

One system, four words. Everything on the site should fit inside it:

| Word | Role |
| --- | --- |
| **Kill** | the action — try to disprove your own forecast first |
| **Hopium** | the problem — what you believe but haven't proved |
| **Proof** | the cure — the artifact or the person that settles it |
| **Commit** | the moment that matters — the decision the seller and manager make, not the tool |

**The intellectual claim, and its limit.** The site does not claim a new
methodology. It claims a narrower job: *MEDDIC helps you work the deal; Kill My
Deal helps you decide whether you've earned the right to call it one.* The "Why
these five" section makes that argument — each question disproves a different
failure mode (inventing the requirement, no real money, access without
influence, no way to transact, no reason to act) and PATH is the one BANT and
MEDDIC underweight, which is the federal-specific reason this exists. Keep that
framing: a gate before those frameworks matter, never a replacement for them.

Three phrases carry it: **TRY TO KILL IT** (product), **HOPE IS NOT EVIDENCE**
(philosophy), **BRING THE PROOF** (standard). The middle one belongs in talks,
posts and the way the offer is described — it was tried as a line under the five
questions on the homepage and read as preaching. The site should demonstrate the
idea, not announce it. The four verdicts are written in
that language — *it survived, bring the proof / you believe it, you haven't
proved it / something important is still an assumption / this is a conversation,
not a deal* — as is the managers section ("get the hopium out of the pipeline
before the review") and the free call ("bring me a deal and we'll try to kill it
together").

Hopium is the recurring joke **inside** the system, never the brand itself.
Do not make "get off the hopium" the tagline: it tips into sales-guru bit, which
the voice rules below rule out. It works as occasional copy and would work as a
content series.

The dead bluebird is the **mascot, not the message**. The user never has to
understand the metaphor: the bird carries the brand in the logo and the share
card while the words carry the instruction. Copy explaining what a bluebird is
was removed from the hero and the lede. It lives in exactly one place: the FAQ
entry "What is a bluebird in sales?", which is a real search and the only spot
a curious reader can learn what the logo is.

A bluebird, in sales, is the deal nobody worked for — an inbound call, a warm
introduction, a requirement that appears out of nowhere. They feel like luck,
which is why they get forecast on feelings instead of facts. The whole brand
sits on that joke: the logo is a dead bluebird, and the tool tells you which
kind you are holding.

---

## 2. Who uses it

**The seller.** Ten minutes before a pipeline review, on a phone, often carrying
a deal they already suspect is soft. Ages run Gen X to Gen Z, so the design can
skew neither corporate-beige nor startup-toy — it has to be something nobody is
embarrassed to be caught using at work.

**The manager.** Asks the five questions out loud during a review and taps the
answers as the rep gives them. Gets a neutral instrument, so the disagreement is
with the rubric rather than with them.

**The skeptic.** A federal seller who has been pitched a lot of sales software
and assumes anything free is harvesting something. This person is why the
privacy design is absolute and why the scoring math is printed on the page.

---

## 3. The end goal

1. **Be genuinely useful in one minute.** Nothing else works if that fails. The
   measure is whether a seller walks into a review already knowing where they
   will get hit.
2. **Earn a conversation with Mark.** The result writes the DM for them — a
   sanitized one-liner naming their weakest pillar — and one tap copies it and
   opens LinkedIn. Calendly is the secondary path for people who already know
   they need help.

Not goals: accounts, retention, a SaaS product, traffic for its own sake. If a
change requires a database or a login, it is the wrong change.

**Sharing is not the growth mechanic.** A bad verdict is self-incriminating and
a good one is boring, so almost nobody pastes it in a team channel. The share
block exists, but the DM is the conversion path; do not re-prioritise them.

---

## 4. How the scoring works

Five pillars, chosen to be memorable without opening the site:
**CUSTOMER · MONEY · POWER · PATH · NOW.**

Each is answered YES / SORT OF / NO, worth **92 / 50 / 8**, weighted:

| Pillar | Weight | Question |
| --- | --- | --- |
| MONEY | 26 | Do you know where the money comes from? |
| POWER | 22 | Are you talking to someone who can make this happen? |
| CUSTOMER | 20 | Has the customer actually said they want to solve this? |
| PATH | 16 | Do you know how they will buy it? |
| NOW | 16 | Is there a real reason this happens now? |

Three caps, each printing its reason on screen:

| Condition | Cap | Reason shown |
| --- | --- | --- |
| MONEY = NO | 55 | you can't say where the money comes from |
| POWER = NO | 60 | you haven't reached anyone who can act |
| CUSTOMER = NO | 45 | the customer hasn't confirmed they intend to act |
| **any pillar = NO** | **74** | **you answered no on {pillar}** |

That last row is an invariant, not a tuning choice: **no deal with a flat NO can
be HEALTHY.** Before it existed, YES on everything but PATH scored 79 and printed
HEALTHY with "nothing obvious to attack" while the same screen showed PATH = NO.
The prose elsewhere says a missing acquisition path makes the timeline guesswork
and that the weakest link sets the forecast; the score has to agree.

Verdicts:

| Score | Verdict |
| --- | --- |
| 75+ | **HEALTHY** |
| 55–74 | **HOPIUM** |
| 35–54 | **ON LIFE SUPPORT** |
| under 35 | **DEAD ON ARRIVAL** |

The ladder is medical and the mascot is a bird; they meet at "dead," which is
the only place they need to agree. An earlier draft used GRILL IT for the second
tier, which collided with the GRILL ME button two inches below it. Do not
reintroduce that.

Everything else is a lookup keyed to the **weakest pillar**, ties broken toward
MONEY because money is what gets attacked: the attack line (`ATTACK`, with
`POWER_ATTACKS` randomising the power variant), the BE READY FOR question, the
three Boss Mode questions (`GRILL`), and the ordered actions (`FIX`) — every
pillar not answered YES, weakest first, capped at three.

**Honest limits, stated in the FAQ and worth keeping:** the weights are not
calibrated against thousands of closed deals and the tool has never seen the
pipeline. What it offers is consistency. *Use it to find the hole, not to set
the number.*

**The tool never makes the commit decision.** HEALTHY reads "no obvious fatal
hole — bring the proof and defend the deal," not "commit it." The other three
tiers may warn against committing, which is a different thing from authorising
it. The promise is: the tool pressure-tests, the seller and the manager decide
the forecast. Copy that crosses that line undermines the rigor FAQ two sections
below it.

---

## 5. There is no AI, on purpose

An earlier build sent the five answers to a language model for coaching. It
produced confident, specific, wrong advice — task orders, recompetes and bridge
contracts nobody had mentioned — because five words is not enough context to
reason from. Confident wrong advice is worse than none when the whole promise is
that every line is defensible.

That is the bar for anyone revisiting it: the model must not be able to invent
procurement context. The deterministic list cannot.

---

## 6. Privacy is a feature, not a footnote

Nothing the user enters is stored or transmitted. No localStorage, no cookies,
no analytics on answers, no server, no account. The tool never asks for the
customer, agency, contract number, partner or dollar value.

**If you add analytics, a save feature, a CRM integration or an AI call, the
copy on the page stops being true.** Update it in the same commit or don't make
the change. The claim lives in two places per page and no more: one clause in
the dek (*No deal data* / *Nothing stored*) and the FAQ entry "Does anything I
enter leave my device?". It used to be in five, and repeating a privacy promise
reads as protesting too much.

**Analytics, and what the promise now says.** `analytics.js` loads Google
Analytics 4 when `GA_ID` is set. That changed the FAQ wording from "no
analytics" to "counts page views and never sends your answers", which is
exactly true and must stay true. Two guarantees are built in: `page_location`
is sent without the URL fragment, so a shared verdict (`#ysnys`) or the
pipeline numbers never reach Google; and the events the pages fire (`start`,
`verdict`, `verdict_shared`, `grill`, `share`, `dm_copy`, `pipeline_edit`,
`pipeline_share`, `pipeline_dm_copy`) carry no parameters. Never add an event
parameter that contains an answer, a score, a number or DM text. Events
fired before the deferred script loads are queued and flushed.

---

## 7. The ask, and how it spreads

**The DM (primary).** The result block names the weakest pillar in its heading
("Stuck on money?") and shows the message already written in a dashed preview:

> Mark — just ran a deal through Deal Check. Scored 47, on life support.
> Weakest pillar is money: who exactly has told you the money is available?
> I don't have a good answer yet. Worth 20 minutes?

**COPY THIS & DM ME** copies it and opens LinkedIn. A second, hotter version
appears at the end of Boss Mode when the seller fails questions — that is the
peak-discomfort moment and converts better than the calm one. See `dmText()`,
`dmGrillText()`, `copyDM()`.

**The squares (secondary).** Copy/share emit a block that reads in any channel:

```
Deal Check 47 · ON LIFE SUPPORT
● ○ ◐ ● ○
CUSTOMER · MONEY · POWER · PATH · NOW

Your boss is going to come after the money.
killmydeal.com/#ynsyn
```

Filled / half / empty circles rather than coloured squares: emoji colours belong
to whatever platform renders them so they never match the palette, and red vs
green is invisible to a colourblind reader. These inherit the message's own text
colour anywhere they land.

**The link.** A result is five letters — y/s/n in pillar order — in the URL hash.
`killmydeal.com/#ynsyn` restores that verdict, shows a "someone sent you this"
banner, and offers to run the reader's own. No storage, no server: the deal *is*
the five answers, so the five answers *are* the URL.

**The hash is written only when the user asks for it.** Finishing a deal does not
touch the address bar; Copy link does. Hash fragments never reach a server, but
they do land in browser history, and "nothing is saved" is easier to defend when
the tool doesn't quietly write someone's answers into a URL they never chose to
share. Incoming shared hashes still restore normally.

**The three actions are deliberately distinct:** *Copy for review* gives the
formatted block, *Copy link* gives the bare URL, the DM button copies the
message. `copyDM()` calls `window.open` synchronously inside the click — a
deferred open after an await or a timeout gets eaten by popup blockers.

**Every copy path goes through `copyText()`**, which returns the promise so
failures are caught. `writeText` is async: a synchronous `try/catch` around it
misses permission denials and the button then lies about having copied. On
failure the labels say what to do instead ("Copy failed — use the address bar",
"Press and hold the text above to copy"). Verified with clipboard access
denied.

---

## 8. Style guide

### The one thing

The tool must do one thing perfectly: tell a seller, in a minute, whether the
deal is real. Every design decision is measured against that. If an element
doesn't serve it, it is there because it could be, and it goes.

### Two colors, seeded from the bird

**Ink and blue.** Every neutral — surfaces, inks, hairlines — is the bird's
hue (207) at very low chroma, so the page and the mark belong to each other:
`#F9FCFF` surface, `#EDF2F7` cards, `#131619` ink. Blue is the old Twitter
blue, `#1DA1F2`, and it means *go*: it is on exactly one element per screen
(the primary button) plus links and the filled progress segments. The verdict
card is the one place colour means something else: a traffic light in
pastels. Green `#C6EBC9`, yellow `#FFF982`, orange `#FFCF8A`, washed red
`#F5B3AD` for the four tiers, ink text on all of them (`--v-*` tokens; dark
mode dims each a step). The red must read as red, not pink: keep the blue out
of it. Nowhere else on the site uses these colours.

**The verdict word is the hero, and the number is literal.** The 0 to 100
score still runs underneath to pick the tier, but nobody sees it. The card
shows the verdict word (HOPIUM, KILL IT, THE PATCH), then one line: *2½ of 5
proven. Weakest: money.* A yes is one, a sort of is a half. That is a number
someone who has never seen the tool understands at a glance, and it is what
the DM and the share block now carry instead of "scored 56". Pipeline Check
keeps its number because 1.1X is a real quantity.

**Labels are 15 characters or fewer.** `.verdict-word` is sized with `clamp`
to fit two lines at a 360px phone and never breaks mid-word; every label on
every tool has been rendered at 360 and 390 and checked. Hyphenated labels
break at the hyphen and look wrong, which is why *Co-marketing* became *All
talk*. If you add a verdict, keep it short and run `shot/fit.js` or eyeball
it at 360.

**Deal Check's bottom tier is KILL IT**, not *Dead on arrival*. The
medical ladder stays for the middle two; the bottom one is the instruction.

**In the dark, the button is the bird.** Dark-mode primary is `#9DD2FF` with
`#00182B` text, so the logo and the action share a colour. Surfaces are the
same hue near black (`#101418`). It is the same design inverted, not a
second one.

The light blue is 2.8:1 against white, which fails WCAG AA. That was a
deliberate call: the brand colour wins here. Don't "fix" it by darkening.

**Components never contain a literal hex.** They consume `--bg`, `--ink`,
`--accent` and the rest. If you find yourself typing a `#` inside a component
rule, you are adding a colour to the system; add a token and name what it
means.

### Type and spacing

Inter set the way Apple sets SF: tight negative tracking on headlines
(−.025em at 36px), generous line height on body (17px / 1.47), and whitespace
doing the work borders used to. Headline → dek → one button. Section headings
at 28px. Overlines at 12px uppercase +.06em in `--ink-2` label every card.

### Components

Buttons (pill, 44 / 54dp, grey by default, blue for primary, text for
utilities, `scale(.97)` on press); choices (60dp grey pills, all identical);
the segmented five-pill progress; cards (`--bg-2`, 20px radius); lists inside
cards with hairline dividers; text fields (label above, grey fill, blue ring
on focus); the app bar with one chip pointing at the other tool. Nothing else.

### Motion

Every screen change fades up 10px over 420ms (`--ease-out`). The verdict
number and label pop in on a spring; the attack line and subtitle fade after.
Buttons compress on press. That is all the motion there is, and it is enough.

### What was cut, and why

The home screen used to carry a five-question list, a doorway card and five
navigation chips under the button. The list restated the tool, the doorway
duplicated the header chip, and the chips navigated to headings a scroll
finds anyway. The result screen merged "be ready for" and "do this" into one
card, moved the arithmetic into the FAQ, and collapsed three text actions to
*Share* and *Start over*. The three-ways cards became three paragraphs. If
you add something back, ask which of the eight questions it answers.

### The Mark section

It is the mentorship pitch, and it is written to the manager, who is the
buyer. Credentials in two sentences, then *A few things I see a lot*: four
situations carried over from the old consulting site (the pipeline looks
better than it is; the partner likes you but nothing happens; busy team, no
rhythm; the number from above disagrees with the number below), then the
thesis: figure out which problem you have before you fix the wrong one, which
is also what the tools do. The tools are how a mentor introduces himself at
scale; this section is where the mentor shows up. Do not reframe it around
the tool. The free tier is *Talk it through*, 20 minutes, and it accepts a
deal, a pipeline or a rep. The old consulting site is retired; nothing else
from it comes over. Same markup on both pages; edit both.

### Voice

Plain, specific, unsparing. One verb: commit. Never label the tone.

**Case, one rule per kind of thing.** Buttons, chips and links are sentence
case, because they are instructions (*Kill my deal*, *Grill me*, *Start
over*). The two product names are proper nouns in title case wherever they are
named rather than clicked (*Deal Check*, *Pipeline Check*, in the wordmark,
the footer, prose and the pipeline overline). The five pillars are identifiers
and are always capitals (*CUSTOMER*, in the answer list, the share block, the
section headings and the five-word line under the hero); after the colon in a
heading the question starts with a capital, as any sentence does. The four
verdicts are capitals in the verdict card only, as display, and sentence case
in prose and the FAQ. Overlines are sentence case in the source and uppercased
by CSS. Nothing else on the site is in capitals. No stat bar. No faces in chrome. **No em or en dashes anywhere
in site copy**, and go easy on the "not X, it is Y" construction. Both are
machine tells. Use a colon, a comma, parentheses, or a new sentence.

## 9. Where to change things

| Change | Where |
| --- | --- |
| Question wording or options | `const P = [...]` at the top of the script |
| Weights, caps, thresholds | `function score()` |
| Attack lines | `ATTACK`, `POWER_ATTACKS` |
| Boss Mode questions, BE READY FOR | `const GRILL` |
| DO THIS actions | `const FIX` |
| The DM copy | `dmText()`, `dmGrillText()` |
| Share block format | `shareBlock()`, `DIAL` |
| Mark's block after a result | `mountMark()` |
| SEO copy, FAQ, bio, offer | the `<section class="band">` blocks |
| Structured data | the `application/ld+json` block in `<head>` |
| Google Analytics ID, events | `analytics.js` |
| Colour, type, shape, motion | `:root` tokens at the top of `site.css` |
| Pipeline Check model, tiers, copy | `compute()` in `pipeline/index.html` |
| Pipeline Check share / DM | `shareBlock()`, `dmText()` there — the DM carries multiples, never dollars |

---

## 10. SEO and social

- One `<h1>`, rendered as **static HTML**, not by JavaScript. The script captures
  it into `INTRO_HTML` at load and restores it on return home, so crawlers and
  no-JS visitors get real content and there is never a second `<h1>`.
- Canonical URL, description, OpenGraph and Twitter tags, `card.jpg` at 1200×630
  with width, height and alt declared.
- The `<title>` carries the search terms ("Federal Sales Pipeline Review Tool |
  Deal Check"); the bluebird line stays the `<h1>` and the OpenGraph title,
  where it actually does its work.
- JSON-LD: `WebApplication`, `Person`, `FAQPage`. Treat it as semantic
  housekeeping rather than an SEO lever — Google no longer shows standalone FAQ
  rich results in normal search, and `HowTo` was dropped because Google retired
  it in 2023 and it was the five pillars stated a fourth time. **The JSON-LD FAQ
  text must match the on-page FAQ word for word**; it drifted once and carried a
  privacy claim the page had already retired.
- ~1,300 words across five sections: the five questions and what each disproves,
  why not BANT/MEDDIC, the pipeline review (sellers first, then managers), the
  bio, and the FAQ. Each pillar is explained **once**. An earlier build explained
  them three times — as signals, as bullets, and as failure-pattern cards — and
  the repetition read as filler. Written for sellers, not for a keyword. Thin SEO
  filler would undercut the only thing the tool is selling, which is credibility.
- The dek names the audience: *Built for federal sellers.* Everything above the
  fold was otherwise generic sales-speak, and federal is the reason PATH exists.

To regenerate the cards: `python3 make-card.py deal` and `python3 make-card.py
pipeline` from the web root (they use `inter.woff2` and `bluebird.png`, so the
cards cannot drift from the pages' typeface or palette). Change the copy in the
script's `CARDS` table, not the JPEG. A card must carry its page's current hero
and dek; it fell out of sync once.

---

## 11. Traps that have already bitten

- **Leftover grid columns.** `.markblk` kept `grid-template-columns:64px 1fr`
  after its avatar was removed, squeezing the DM preview into a 64px lane, one
  word per line. It is `display:block` now.
- **Class-name collisions.** `.mark` was the pillar checkmark style before the
  bio block reused it and got forced to 40px wide. The bio block is `.markblk`.
- **Logo with a white background.** The first bird PNG was not transparent and
  showed as a white box on the tinted surface. The shipped `bluebird.png` has
  the field knocked out and is trimmed to the art.
- **Long button labels.** Two CTAs have overflowed on a phone. Buttons are
  `white-space:nowrap` with ellipsis; short labels are the real fix.
- **Duplicate script tags.** Assembling this page from the tool-only version
  once included the script twice and every `const` collided. There should be
  exactly two `<script>` elements: JSON-LD and the app.
- **Share text duplicating the URL.** `shareBlock()` already ends with the link.
- **Regex that eats the rest of a tag.** A `<link rel="icon">` replacement
  stopped at the first `>` inside a data URI and left `😵">` visible on the page.
- **Opening a tab before copying.** `window.open` moves focus; Chrome then
  rejects `navigator.clipboard.writeText` with "document is not focused", so
  the DM copied nothing and the catch stuffed a sentence into a 44px pill.
  Copy now runs synchronously inside the click through a hidden textarea and
  LinkedIn opens after it succeeds. Button feedback is two words, always.
- **Passing a handler the event.** `back2.onclick = result` handed the click
  event to `result(shared)`, so *Back to the verdict* showed "Someone sent you
  this verdict" on the user's own deal. Wrap it: `() => result(false)`.
- **Focus ring changing the shape.** `:focus-visible { border-radius:8px }`
  reset every pill button to 8px corners on keyboard focus. The ring is
  `outline` only now, in `--primary-ink` so it clears AA on the light surface.
- **Favicon inlined as base64.** A 256px PNG as a data URI put 69 KB in `<head>`,
  more than the font. It is `favicon.png` (64px) and `apple-touch-icon.png` now.
- **`theme-color` from a template.** It was M3's default lavender `#FEF7FF`,
  not the surface. Light and dark values are declared with media queries.

---

## 12. Deploy (AWS Amplify Hosting, from GitHub)

The repo is the site. `amplify.yml` has no build step; its build phase only
deletes files that belong in the repo but not on the web (`preview/`,
`HANDOFF.md`, `make-card.py`). `customHttp.yml` sets security headers and
caching: HTML is `no-cache`, CSS and JS one hour, the font a year, images a
week. There is no asset versioning, so a CSS change is live within an hour.

Set these in the Amplify console; they cannot live in the repo.

1. **Domain.** Attach **quotabird.com** under *Hosting → Custom domains*,
   with www redirecting to the apex. killmydeal.com was retired at launch
   and is not used anywhere.
2. **Rewrites and redirects** (*Hosting → Rewrites and redirects → Manage
   redirects → text editor*), in this order; the 404 catch-all must be last:

```json
[
  { "source": "https://www.quotabird.com/<*>", "status": "301", "target": "https://quotabird.com/<*>" },
  { "source": "/deal", "status": "301", "target": "/deal/" },
  { "source": "/pipeline", "status": "301", "target": "/pipeline/" },
  { "source": "/brief", "status": "301", "target": "/brief/" },
  { "source": "/territory", "status": "301", "target": "/territory/" },
  { "source": "/partner", "status": "301", "target": "/partner/" },
  { "source": "/rep", "status": "301", "target": "/rep/" },
  { "source": "/olr", "status": "301", "target": "/olr/" },
  { "source": "/notes", "status": "301", "target": "/notes/" },
  { "source": "/kit", "status": "301", "target": "/kit/" },
  { "source": "/leader", "status": "301", "target": "/leader/" },
  { "source": "/seller", "status": "301", "target": "/seller/" },
  { "source": "/kits", "status": "301", "target": "/kits/" },
  { "source": "/math", "status": "301", "target": "/math/" },
  { "source": "/pipeline", "status": "301", "target": "/" },
  { "source": "/pipeline/<*>", "status": "301", "target": "/" },
  { "source": "/quota", "status": "301", "target": "/quota/" },
  { "source": "/discount", "status": "301", "target": "/discount/" },
  { "source": "/commission", "status": "301", "target": "/commission/" },
  { "source": "/<*>", "status": "404", "target": "/404.html" }
]
```

3. **Search Console.** Verify quotabird.com and submit its sitemap.
4. **Analytics**: the GA4 measurement ID (`G-BG9NR9GXQZ`) is in `GA_ID` in `analytics.js`.
5. **Calendly**: the free call is described as 20 minutes everywhere; make
   sure the `chat-with-mark` event is 20 minutes, or change the copy.

After deploy: open the site, type `QB_BUILD` in the console and check it
matches this file; share a link in Slack or LinkedIn and confirm `card.jpg`
renders; submit `sitemap.xml` in Google Search Console.

**`mark.jpg` still needs replacing.** The current headshot has background
artifacts. A clean 640×640 on a plain background.

## 13. Testing before you ship

1. Answer all five questions; the verdict block appears in the right colour.
2. GRILL ME asks three questions and reaches a closing verdict; failing any
   shows the DM block underneath.
3. COPY THIS & DM ME copies the written message and opens LinkedIn.
4. *Copy for review* emits the circles block, *Copy link* emits only the URL,
   and the address bar stays clean until one of them is pressed.
5. Opening that link in a fresh tab restores the verdict with the "someone sent
   you this" banner.
6. The logo returns home with answers cleared and exactly one `<h1>`.
7. DevTools → Network shows only the page's own files (`index.html`, the
   images, `favicon.png`) and nothing to any other host.
8. At 390px nothing overflows horizontally and no button clips its label.
9. Dark mode: the button is bird-blue with navy text; links stay legible.
10. No combination of answers containing a NO returns HEALTHY.
11. GRILL ME → *Back to the verdict* does **not** show the "someone sent you
    this" banner.
12. Tab through the answer buttons: they stay pills while focused.

---

## 14. Related properties

- **fedhoo.com** — Mark's federal market research tool, built on USASpending and
  SAM data. Cross-linked from the bio note and the footer.
- **Calendly** — `calendly.com/markflournoy/chat-with-mark`, free 20 minutes,
  UTM-tagged `utm_source=killmydeal`.
- **LinkedIn** — `linkedin.com/in/markflournoy`. The DM is the primary ask;
  a stressed rep sends one line long before booking a meeting.

---

## 15. Pipeline Check

The manager's half. Inputs: revenue target, qualified pipeline due in the
period, qualified win rate; behind *Go deeper*: average deal size, sellers,
closed so far, months in / months left. Sales-cycle days were cut — nine
fields is not a one-minute tool.

**It is a calculator, not a question set, and must stay one.** Managers and
sellers want to change a field and watch the gap move. A two-step stepper was
tried in September 2026 and reverted: it made the one numeric tool behave
like the question tools and hid the numbers people came for. Every field is
visible (target, pipeline, win rate with Federal / SaaS / A third chips, deal
size, sellers, closed so far, a Dec 31 / Sep 30 year-end chip, *Just me*),
prefilled with an example, and everything updates on input. Money fields
tidy themselves on blur ("10m" becomes "$10M"); focusing a field selects it
so typing over the example is one step.

**The light bulb is the example and the bar.** The page opens on $10M
target, $32M pipeline, 25% win rate: 3.2X, which 3X calls covered and the win
rate calls *Hopium, $8M short*. The verdict's attack line is that sentence
(`flip` in `compute()`), and under the verdict a coverage bar puts your
pipeline, the 3X line and your own line on one scale, with the gap shaded in
the verdict colour. Seeing your line sit past the 3X line is the insight; do
not replace the example with one where the two agree.

**Layout.** Phone: fields, then verdict. While the fields are on screen and
the verdict is below the fold, a summary strip rides at the bottom (*3.2X
hopium · $8M short at 25%*) so the answer is visible while typing; it hides
once the verdict is in view or scrolled past. Desktop (≥ 880px): fields
left, verdict sticky right, no strip. The page widens via `.wrap.wide`.

**Rows.** You have; 3X says you need (and short or covered); your win rate
says (and short or covered); the gap with deal count; per seller (or *For
you* when sellers is 1) with deals each. The clock line fills itself from the
date and year-end chip, with pace when closed-so-far is known.

**Lead with the win rate, show 3X as the thing being killed.** Required pipeline
is `still-to-find ÷ win rate` (× 3 if no win rate given). 3X is a 33% win rate
in disguise; the page says so. The old consulting site had this backwards —
3X was the benchmark and win rate was "go deeper" — and in this voice that
makes the name a costume.

Verdict is `pipeline ÷ required`, on the same ladder as Deal Check:
COVERED ≥ 1.0 · HOPIUM ≥ .75 · ON LIFE SUPPORT ≥ .5 · DEAD ON ARRIVAL below.
The tier that justifies the product is HOPIUM at ≥ 3X: *"3X says you're fine.
Your win rate says you need 3.3X."* DEAD ON ARRIVAL at the start of a period
is a creation problem, not a closing problem, and the copy says that; the
"period is already written" line lives in the pace block, which only appears
when closed-so-far and months are given.

**The hand-off runs both ways.** Every pipeline verdict ends with *how much of
the pipeline you already have would survive Deal Check?* and a KILL A DEAL
button. The homepage's review section carries the doorway the other way
(*Managing the whole pipeline?* → PIPELINE CHECK). Neither tool's result
screen links to the other above the DM; the DM stays the conversion path.

**Dollars.** This tool necessarily asks for them, which Deal Check never does.
So: the DM contains multiples only (*I'm at 1.1X; my win rate says I need
3.3X*). *Copy for review* does contain dollars because the person chose to
copy it. Copy link writes the inputs to the hash only when pressed, same rule
as the other page.

**Not brought over from the old consulting site:** the gtag/plausible hooks,
the stat bar, the rep-archetype section (content topics, not homepage), the
partner-strategy material, the generic GTM positioning. The federal specialty
pitch is already the dek. The old site should be retired; this is the front
door now.

## 16. Rep, Partner, Territory, and the engine

The three newer tools share one script, `check.js`. Each page is a shell
plus a config passed to `CheckTool({...})`: five questions, weights, a
`verdict(answers, total, weak)` function, the question the boss will ask per
pillar (`grill`), the first move per pillar (`moves`), a hand-off card, the
Mark card copy and the DM template. The engine does the rest: intro, the
five screens with segmented progress, the result, share (five-letter hash,
same as Deal Check), the DM, analytics events named `<slug>_start`,
`<slug>_verdict`, `<slug>_share`, `<slug>_dm_copy`.

**The pages are generated.** Edit copy in `make-tools.py`, run it from the web
root, commit the three `index.html` files it writes. Do not hand-edit those
files; the next run overwrites them. The generator also builds the header
menu from its `TOOLS` list, and copies the Mark section out of `index.html`,
so the bio is edited once.

**Deal Check and Pipeline Check keep their own scripts.** Deal has Boss
Mode and the score caps; Pipeline is arithmetic, not questions. Porting Deal
onto the engine is possible and was not worth the regression risk.

**Two verdict shapes.** Partner and Territory score 0 to 100 on the Deal
ladder (green ≥ 75, yellow ≥ 55, orange ≥ 35, red below) with a NO capping the
score at 74; the card shows the word and the literal count, never the score.
**Rep is a diagnosis, not a score**: `capOnNo: false`, `count: false`, and
`verdict()` returns one of six labels by rule.

**Rep Check asks about the situation before the person.** The five, in
order: PATCH (could a good rep make this number here, on this plan), CUSTOMERS
(do customers choose them; pull, not meeting count), PIPELINE (what exists
because they're here), CRAFT (can they actually sell), WILL (are they still
trying). CRAFT is the question that separates *can't* from *isn't*, which are
different management problems, and it was missing from the first version.
The verdicts are the four managerial buckets plus two: *The situation* (patch
no; good rep, bad situation), *Coach them* (craft no, will yes), *Manage them*
(craft yes, effort or activity no), *Wrong rep* (craft no and will no), *They're
fine* (all yes; leave them alone) and *Not sure*. Order of evaluation matters:
the situation is checked before anything about the person, so a rep in a dead
patch is never called a performance problem. The hand-off depends on the
verdict (`handoff` may be a function): *The situation* sends them to Kill My
Territory; everything else says sit with the rep and run five real deals
through Deal Check, which is the best advice on the page. Comp is part of
PATCH ("on this plan"); do not add it back as a sixth question. Five is the
family.

**Hand-offs follow the verdict, and they form a loop.** Deal is the front
door and has no outbound hand-off; the other four all point somewhere that
makes sense for the verdict they just gave: Pipeline → Risk Check when covered ("now the shape of it"), → Deal Check
for Hopium and At risk ("how much of this survives?"), → Territory when
the gap is a creation problem (ratio under .5); Partner → Deal for *Real* and *All talk*, → Pipeline ("how much of
your number is leaning on them?") for *Neighbors* and *Logo swap*; Territory →
Pipeline for *Workable* and *Thin*, → Rep ("their version of this question,
and its first question is the patch") for *A stretch* and *Nobody could*;
Rep → Territory for *The situation*, → Deal ("sit with them and run five real
deals") for everything else. Every page also listens for `hashchange`, so a
shared link opened in an already-open tab renders.

**The booking link arrives already knowing the verdict.** Every *Or book 20
minutes* link on every result screen carries Calendly's `a1=` parameter,
which prefills the first question on the event type (the default "anything
to help prepare" question counts). The note is the verdict, the count and
the weakest pillar, or for Pipeline the coverage multiples and pace: *Kill My
Pipeline: 1.9X coverage, dead on arrival, needs 5.0X at 20%, 4.1x current
pace.* Never a name, never a dollar figure; the old site's version sent
dollars and this one must not. If the Calendly event type's first question
is ever removed, the prefill silently does nothing, which is fine.

**Talent Review Check (at `/olr/`) grades the case, never the rep.** It was built as *Kill My
Case* at `/case/` and renamed because most users are at Amazon and OLR is the
word they use; *case* stays in body copy where it is the precise word (the
room tests your case), but not in the name, URL, card, menu or DMs. The FAQ
defines OLR for anyone who isn't Amazon, and says the tool works the same in
any calibration room. `/case/` 301s to `/olr/` (Amplify console rule). Built for the AWS talent
review (evaluate, calibrate, communicate) but true of any calibration room:
the manager proposes, the room probes, and all the room can test is the case.
Five questions about the case: RECEIPTS (three things with numbers, the
Forte framing), OWNERSHIP (what wouldn't have happened without them), SCOPE
(their level, not strong execution a level down), HOW (an example per
principle cited), NEXT (the harder thing you'd hand them). Verdicts are
brief-quality only: *Ready*, *Thin*, *A story*, *No receipts*. It never asks
a name, never predicts, suggests or mentions a rating, and the FAQ says so.
The engine's **Grill mode** was added for it (`grillSet`: three questions per
pillar, `fix`, `grillLines`, `dmGrill`); it works the same as Deal Check's
Boss Mode and is available to any tool that provides a `grillSet`. The bias
checklist (recency, visibility, halo, horns, style, context) is a band, not a
screen: it is the thing to read, not a form to fill. The research that led
here proposed evidence-entry screens, a team table and local storage; all of
that is typing, and the tools don't ask for typing.

**Brief Check is the first tool whose audience is wider than sales**, and
its copy is written for someone presenting a six-pager to a VP as much as
for a QBR. The premise, from the research that led to it: the room is not
attacking the document, it is attacking the assumptions underneath it. Five
questions about the argument: POINT (one sentence, and why now), RECEIPTS
(evidence for the three load-bearing claims, at least one from outside your
team), ALTERNATIVE (including doing nothing), HOLE (your own weakest
assumption and who will find it), ASK (what you need today and who owns
what). Verdicts: *Room ready*, *A fight*, *Shark food*, *No point*. The hero
is the signature question, *What's the question you're hoping nobody asks?*
The research proposed eight questions; the three extra (why, so what,
audience) live inside POINT, RECEIPTS and HOLE.

**The sharks.** Grill mode on this tool opens with *Who's across the table?*
and five choices (Finance, the executive, the technical leader, the sales
leader, the skeptic); each shark has three questions for every pillar, so the
grill is always that chair's questions about your weakest answer. This is the
engine's `sharks` option (`{ id: { name, qs: { pillar: [3] } } }` plus
`sharkPrompt`); a tool without `sharks` grills from `grillSet` as before. The
chooser lives after the verdict, never on the intro: personalization comes
after value. Nothing is ever uploaded; the tool never sees a word of the
document.

**Names.** None of the five ever asks for one, and the DM templates carry the
verdict and the weakest pillar only. A tool that stores judgments about named
people is a different product.

**The bird always goes home.** Every page's header is the same: bird plus
*Deal Check*, linking to `/`. The tool's own name is the small label above
its headline (`.tool-name`). An earlier version put the tool name in the
header and made it restart the tool, which meant tapping the logo never
reached the front door. Restarting a tool is *Start over* and the back
gesture; the logo is navigation. On the home page itself the logo returns to
the intro.

**Header and the kit's frame.** The *Tools* menu is a `<details>` with no JS,
grouped by audience: *For sellers* (Deal, Territory), *For managers*
(Pipeline, Rep, Partner, Case), *For anyone* (Brief), each with the moment
it's for under the name. The home page carries *Seven places hope gets in*
directly under the tool, before the essay: one line per tool, organized by
**moment, not funnel stage** (before commit, month one in a patch, before a
meeting, Monday with a worrying rep, quarterly, review season). That is the
kit's honest shape, seven inspection points rather than prospecting-to-close,
and it is the Rick Steves frame: which line to skip, where the back door is.
The `TOOLS` list in `make-tools.py` is the single source for the menu; add a
tool there with its group and its moment. That list and the menu are the only
cross-navigation; do not add a tools portal page.

**Shared behaviors, in all three runtimes** (the flagship's inline script,
the pipeline page's, and `check.js`), kept identical on purpose:
- *History.* Every screen is a history entry (`nav()`), so the phone's back
  gesture steps back one screen, including back through Grill to the shark
  chooser, instead of leaving the site. In-page *← Back* buttons call
  `history.back()` so the two stacks never disagree. Re-renders of the same
  screen (a win-rate chip) replace rather than push.
- *Focus.* Every screen change moves focus to the new question, verdict or
  heading (`focusScreen()`), with no visible ring for programmatic focus.
- *Share.* On a touch device *Share* opens the native share sheet with the
  verdict as text and the link as URL; elsewhere, or if the sheet fails, it
  copies. Cancelling the sheet does nothing.
- *Menu.* The Tools menu closes on an outside tap and on Escape.
- *Shared links.* Every page, the flagship included, renders a shared link
  opened in a tab that already has the site (`hashchange`).

**Structured data follows the page.** The last step of `make-tools.py`
rebuilds every page's FAQPage JSON-LD from its visible FAQ, including the
two hand-written pages. Edit the visible FAQ, run the script, done. It drifted
three times by hand; it cannot now.

**The header bird is `bird-sm.png`** (90px, 2 KB, and `bird-sm-dark.png`).
`bluebird.png` is only for the 404 and the share cards.

**One vocabulary.** Pipeline's bottom tier is *Kill it*, same as Deal. No two
tools share a verdict word (OLR's middle tier is *Not yet*, Territory keeps
*Thin*). Nobody outside the source says "pillar"; copy says "answer".

## 17. Changelog

**2026-09-18.1400** — review pass.
- `card.jpg` regenerated to match the current hero and dek (it still carried
  the retired bluebird line); `make-card.py` added so it cannot drift again.
- Content: the five pillars explained once instead of three times; the review
  section and the managers section merged; FAQ entries that restated sections
  above cut; the bluebird FAQ entry added; the third consulting tier reshaped
  for teams; "Built for federal sellers" added to the dek.
- Bugs: *Back to the verdict* showing the shared-link banner; focus ring
  reshaping buttons; `theme-color` mismatch; stale privacy claim in JSON-LD;
  shared hash surviving *Kill another deal* from the Boss Mode screen.
- Housekeeping: dead CSS and JS state removed (`mode`, `nick`, `step`,
  `setHome`, `MARK`, `strongOnes`, input/ghost/avatar rules); `HowTo` schema
  dropped; favicon moved out of the head; `color-scheme` and dark
  `theme-color` declared; answer buttons are plain buttons in a `group` rather
  than radios that never get checked. Page 192 KB → 118 KB.

**2026-09-18.1500** — cohesion pass.
- One button component with three emphasis levels replaces `.big`, `.act`,
  `.act-p`, `.cta-a`, `.cta-b`, `.linkbtn`, `.back`; shape morphing now applies
  to every button including the primary. Label case made consistent.
- Shape tokens replace nine ad-hoc radii; signals list uses the same grouped
  idiom as the answer set.
- Header aligned with the prose column; *Work with Mark* text link added.
- Boss Mode close: navigation buttons outlined so the DM is the only filled one.
- `h1` weight 400 → 700 to match the card, the question type and the verdicts.

**2026-09-18.1700** — Pipeline Check.
- `/pipeline/` added: coverage against target and win rate, same ladder, same
  share/DM pattern, cross-linked both ways. `card-pipeline.jpg` and a
  `pipeline` mode in `make-card.py`.
- Shared `site.css` and `inter.woff2` extracted; `index.html` 118 KB → 37 KB.
- Homepage: doorway block in the review section, footer link, `knowsAbout`
  on the Person schema (the one useful thing in the old site's structured data).
- `sitemap.xml` lists both pages.

**2026-09-18.1900** — UX pass.
- Header: single assist chip that swaps between the two tools; *Work with Mark*
  header link removed. Doorway moved onto the home screen under the peek.
- `/pipeline/` opens on example numbers with a live verdict and an EXAMPLE chip;
  bio section added; KILL A DEAL is tonal under the filled DM.
- Buttons no longer shape-morph or scale on press; state layer only.
- Bio text wraps the photo instead of a second column.
- `bluebird-dark.png`: light outline for dark mode, via `<picture>`.
- Privacy copy cut to dek + FAQ per page; footer is one line; build stamp
  removed from the footer (still in `window.QB_BUILD`).

**2026-09-18.2100** — Material Design 3 rebuild.
- `site.css` rewritten from tokens up: full M3 color roles (light primary is now
  tone 40 with white text; the bird blue is primary-container / dark primary),
  the M3 shape scale, the M3 type scale, standard easings.
- Every element is now an M3 component: app bar + assist chip, buttons in
  four emphases and two sizes, list items, cards, filled text fields, linear
  progress, expansion. The answer "bun" is gone: three size-M tonal buttons.
- Button labels in sentence case throughout.
- Dark-mode bird outline is pure white.
- Pipeline page: bio photo path fixed, go-deeper labels shortened to fit the
  two-column grid.
- `preview/` folder in the package: headless-Chromium screenshots of every
  screen in both schemes, taken from this build.

**2026-09-19.0900** — palette.
- Primary a step lighter (`#0B5A9A` → `#0F73BC`), toward Twitter blue, at the
  lightest value that still passes AA with white text. Pastel Twitter blue in
  `primary-container`.
- Dark mode rebuilt as muted charcoal neutrals with pastel containers; all
  pairs ≥ 7:1.
- Neutrals quieter on both sides (lighter dividers, softer secondary text).
- Cards regenerated in the new palette; `theme-color` updated.

**2026-09-19.1200** — one thing.
- Monochrome: ink plus Twitter blue. All semantic colours removed; verdict is
  ink, HEALTHY / COVERED is blue.
- Home screen reduced to headline, dek, button, the five words. Result screen
  reduced to verdict, answers, one next-step card, Grill me, Share / Start over.
- Segmented progress restored. Screen transitions, verdict spring, press
  compression added.
- Apple-style type scale and spacing. Three-ways cards → paragraphs. Score
  arithmetic → FAQ. Field labels above inputs.

**2026-09-19.1400** — seeded neutrals.
- Neutrals re-derived from the bird's hue on both sides; dark-mode primary is
  the bird itself (`#9DD2FF`); highlight container from the same ramp.
  Semantic colours and the dark primary button were considered and declined
  (see §8).

**2026-09-19.1600** — copy and clutter.
- Copy fixed: synchronous `execCommand` copy inside the click, iOS range
  selection, LinkedIn opened after success; feedback is "Copied ✓" or
  "Couldn't copy" and nothing longer. Tapping a DM preview selects it.
- Boss Mode close screen: one Mark card (with the Boss Mode DM text) instead
  of an inline DM block plus a second Mark card; one text link back to the
  verdict instead of two buttons.
- Mark card: primary button full width, Calendly as a text link below.

**2026-09-19.1700** — hero line: *Before you commit it, try to kill it.* Updated in the h1, og/twitter titles and alts, and `card.jpg`.

**2026-09-20.0900** — launch prep.
- `analytics.js` (GA4, hash stripped, parameter-free events, early-event
  queue) on both pages; FAQ and JSON-LD privacy wording updated to match.
- Pipeline dek rewritten. Bio: "Marine" for "Marine officer".
- All em and en dashes removed from site copy; two "not X, it is Y" lines
  tightened.
- `amplify.yml`, `customHttp.yml`, `404.html` added; §12 rewritten for Amplify.

**2026-09-20.1100** — case audit: pillar headings capitalise after the colon; FAQ referenced the old *GRILL ME* label; case rules written into §8.

**2026-09-20.1300** — verdict pastels (green / yellow / peach / pink) in light and dark, from user feedback; blue back to meaning the button only.

**2026-09-21.0900** — Mark section rewritten on both pages as the mentorship pitch: credentials, four situations, the thesis, three ways to work together; free tier is *Talk it through*, 20 minutes; CTA *Talk with Mark*.

**2026-09-21.1300** — Rep Check, Partner Check, Territory Check.
- `check.js` shared engine; `make-tools.py` generates the three pages from one
  template and the copy in the script.
- Header *Tools* menu on every page; *Other things worth killing* list on the
  home page; sitemap and share cards for all five tools.
- Rep is a rule-based diagnosis with six verdicts; Partner and Territory
  score on the Deal ladder.

**2026-09-22.0900** — verdict card rework.
- Traffic-light pastels: orange and washed red replace peach and pink.
- Verdict word is the hero on every question tool; the literal count (*2½ of
  5 proven*) and the weakest pillar replace the 0 to 100 score on the card,
  in the DM and in the share block.
- *Dead on arrival* is now *Kill it* on Deal Check. Rep verdicts shortened
  to fit (*They're fine*, *The patch*, *The plan*, *Checked out*, *The rep*,
  *Not sure*); Partner verdicts renamed *Real*, *All talk*, *Neighbors*, *Logo
  swap*. All labels fit-tested at 360 and 390px.

**2026-09-24.0900** — Rep Check rebuilt on the situation-first five (PATCH,
CUSTOMERS, PIPELINE, CRAFT, WILL) with the four-bucket verdicts; hand-off now
follows the verdict; engine supports `handoff` as a function. Card and home
list updated.

**2026-09-24.1100** — hand-offs on Pipeline, Partner and Territory now depend on the verdict (see §16); pipeline page handles `hashchange`.

**2026-09-25.0900** — Pipeline Check restructured: two-step entry, verdict
at 3X, win-rate chips that flip the verdict in place with the flip recorded
on the card, calendar-filled months with a Dec 31 / Sep 30 chip and a clock
line, three result rows with the arithmetic behind a button, "Just me".

**2026-09-25.1100** — Calendly `a1=` prefill on every tool, multiples and verdict words only.

**2026-09-26.0900** — Kill My Case at `/case/`: five questions on the
manager's case for a rep, verdicts on the case only, Grill mode ("the room"
asks three), bias-check band. Grill mode added to `check.js`. Menu, home list,
footer, sitemap, share card updated.

**2026-09-26.1200** — Brief Check at `/brief/`: five questions on the
argument, four verdicts, Grill mode with a shark chooser (five chairs, three
questions each per pillar). Engine gained `sharks`. Menu, home list, footer,
sitemap, share card updated.

**2026-09-27.0900** — kit review: Tools menu grouped by audience with the
moment under each name; home page list rewritten by moment and moved under
the tool; Pipeline bottom tier *Kill it*; Case middle tier *Not yet*; bio
free tier accepts "a territory you've been handed".

**2026-09-28.0900** — audit fixes: back gesture steps through screens on
every tool; focus moves to each new screen; native share sheet on phones;
Tools menu closes on outside tap and Escape; the flagship handles shared
links in an open tab; `--ink-3` darkened to pass AA in both schemes (4.7:1
light, 6.2:1 dark); FAQ JSON-LD generated from the visible FAQ on every
build; header bird 56 KB → 2 KB.

**2026-09-29.0900** — Kill My Case renamed **OLR Check** at `/olr/`: name, title, hero, CTA, DMs, card (`card-olr.jpg`), menu, home list, footer, sitemap; FAQ adds *What is OLR?*; `/case/` redirects.

**2026-09-30.0900** — Pipeline Check back to a live calculator: every field
visible and prefilled, updates on input, coverage bar with the 3X line and
your win-rate line, the flip sentence as the verdict line, a summary strip on
phones, two columns on desktop. The stepper from 2026-09-25 is gone.

**2026-09-30.1100** — logo links home on every page with one wordmark, *Deal Check*; each tool's name moved to a label above its headline.

**2026-10-01.0900** — **QuotaBird.** New home page at `/` (doorways, how the
tools work, Field Notes, About, FAQ); Deal Check moved to `/deal/`; three
Field Notes at `/notes/`; one header and one About section generated onto
every page (QuotaBird wordmark, Field Notes, About, Ask Mark, Tools menu);
three-tier offer replaced by *Need another set of eyes?*; every URL, card,
sitemap and structured-data reference moved to quotabird.com; killmydeal.com
redirects path by path. Field Kits deliberately not built.

**2026-10-01.1100** — original cloud mark for QuotaBird in the header, favicon, home-screen icon and home share card; the bird remains the Deal Check mascot on tool cards and the 404.

**2026-10-01.1300** — Mark's S-cloud mark traced to SVG and installed: header (light/dark), SVG favicon that follows the colour scheme, PNG fallbacks, home share card. The interim cloud marks are removed.

**2026-10-01.1500** — logo rebuilt from true geometry (six circles and one curve) in place of the trace; PNGs re-rendered from it.

**2026-10-02.0900** — **Checks.** Kill My X renamed X Check across every
page, card, button, DM, share text and the structured data, under *Quick
reality checks for complicated deals*; headlines reworded (*prove it*, *test
it*); verdicts *At risk*, *Not a deal yet*, *Short*; the bluebird mascot and
its FAQ removed, the logo on every card and the 404 (*Wrong turn.*); `kill.js`
renamed `check.js`. Logo stroke 59 → 70 and header mark 30 → 34px.

**2026-10-02.1100** — launch prep. Every reference to killmydeal.com and
the old name removed from the site, including the home FAQ entry; internal
names renamed (`kmd.css` → `site.css`, `KMD_BUILD` → `QB_BUILD`, the
analytics helper `kmd()` → `track()`, the history key). Titles cut to 60
characters or fewer and descriptions to 160 or fewer so search results
don't truncate them. Font preloaded on every page; SVGs cached. A verdict
restored by the back gesture no longer counts as a second analytics event.

**2026-10-03.0900** — logo weight study; option 6 shipped (stroke 96, lobes +6%, corner radius 24). Icons and all share cards re-rendered; home card subtitle shortened to fit.

**2026-10-03.1100** — UX pass: real sample verdict and byline in the home
hero; "5 taps · about a minute · nothing stored" under every start button;
sticky start bar on tool pages; booking section rebuilt as a three-step
"how it works" with "If I don't think I can help, I'll tell you." and *Pick
a time · 20 min, free*; left edges aligned on desktop. The generator's
build stamp had gone stale and is synced again.

**2026-10-03.1300** — button labels: 18 characters max, one line always.
*Chat with Mark*, *Or book a call*, *All tools*, *← The verdict*, *Check
my deal* / *Check my pipeline* on the home page, *Share*, *Try it* on Field
Notes, *The tech leader*. "Twenty minutes, free." moved into the booking
steps. 680 button instances audited at 320, 360 and 1280px: no wraps, no
clipping.

**2026-10-06.0900** — **QuotaBird.** Site renamed from SellClouds; the
bluebird returns as a vector mark with a round eye (header, favicons, every
share card, the 404); home copy re-centered on the number; three
calculators added (Quota, Discount, Commission Check) on a new `calc.js`
engine with a *Your number* menu group and three home doorways; sitemap now
generated from the page list.

**2026-10-06.1000** — 404 bird keeps the X eye (`logo-x.svg`).

**2026-10-06.1100** — bird re-traced with heavier smoothing: smooth curves at any size, all versions (round eye, X eye, dark) and every icon and card re-rendered.

**2026-10-07.0900** — mobile-first pass for the target reader: home dek
rewritten (the number, the boss, the customer), doorways grouped by role,
Tools menu compacted to two columns in three groups with no subtitles,
footer nav on every page, a fifth situation in the About (the forecast
call has become the job), AWS role worded as "led partner sales teams".

**2026-10-07.1100** — home hero rebuilt around instant value: Deal Check's
first question live in the hero (answers land on /deal/ at question 2),
the byline photo removed and credibility folded into the dek, the two
buttons removed (the doorways and menu cover the rest), hero spacing
tightened so all three answers show above the fold on a 375×667 phone.

**2026-10-08.0900** — home page is now Pipeline Check: hero *You sure
that's enough pipeline? Put in your win rate and find out.*, verdict and
bar above the fields on phones, the rest of the home page below;
`/pipeline/` retired (redirect to `/`), every link and hand-off repointed,
Quota Check's target hand-off lands on the home calculator; home share card
redrawn.

**2026-10-09.0900** — see *Review of 2026-10-08* above: nav order, About
page + short Made-by card, Pressure test, softer ranges, Commission buffer,
three notes, behaviour analytics and Useful?, home metadata.

**2026-10-09.1100** — every calculator opens verdict-first (example result
above the fields, rows and hand-off below); every tool intro cut to one
sentence that says what to do; GA4 ID updated to G-BG9NR9GXQZ.

**2026-10-09.1300** — Tools menu panel no longer clipped on phones (it spans the screen under the header; centred under the chip on desktop).


**Money fields format as you type** (`liveMoney()` in `calc.js` and the home page): $10,000,000 with the caret held in place; shorthand like 10m left alone until blur; full comma form on blur. Compact forms ($10M) are for results only.

**2026-10-10.0900** — Quota Check rebuilt around what the number is measured
in (new bookings / cloud consumption growth / whole book), three ladders,
implied rate shown, cloud AM example; money fields format with commas as you
type across all calculators and the home page.

**2026-10-11.0900** — Account Check, Risk Check and Competition Check added;
menu and doorways regrouped into Your deal / Your number / Your team / Any
meeting with balanced two-column menu.

**2026-10-11.1100** — analytics rebuilt on the standard Google tag after a Defender false positive; runtime script injection, the global click listener and the inline onerror removed.

**2026-10-11.1300** — Quota Check hand-off pre-fills the pipeline at 3X with a banner, so the home calculator opens on a verdict instead of empty fields.

**2026-10-11.1500** — a covered pipeline now hands off to Risk Check (the shape), Hopium/At risk to Deal Check, Short to Territory Check. Audit of all hand-offs: no other carries numbers; Quota → Pipeline is the only calculator-to-calculator path.

**2026-10-11.1700** — Quota → Pipeline hand-off fills every field (3X pipeline, Federal 20%, $500K deals, just me) with a banner saying so; Federal 20% is the win-rate default on the home example too.

**2026-10-12.0900** — llms.txt and ai-catalog.json (ARD 1.0, schema-validated) generated from the tool list.

**2026-10-12.1100** — Sales Math Library: four sourced citation pages and an index at /math/, linked from the menu, footer, calculators, home and llms.txt.

**2026-10-13.0900** — The Manager's Field Kit at /kit/: free printable, plain voice, 12-page print layout, Chat with Mark CTA.

**2026-10-13.1100** — kit as a real PDF with page previews; promo card on home and manager pages; kit in the header and at the top of the Tools menu.

**2026-10-13.1300** — kit rewritten from review: retitled *The Sales Manager's
Field Kit*; each worksheet now follows its chapter (rep diagnostic, 1:1, deal
inspection, team pipeline, a new five-minute boss update, talent review prep);
new chapter 10 *When to leave the rep alone*; two new expensive lessons;
"start the process" softened to a performance conversation; the "a third of
the number" rule softened; closing card rewritten (*Sometimes another set of
eyes helps*). The review suggested "led AWS's Federal Partner Vertical team"
and "I'm retired now" for the closing card; Mark's approved wording ("led
partner sales teams at AWS") was kept pending his confirmation. 14 pages.

**2026-10-13.1500** — kit print layout tightened from 14 pages to 8. Worksheets
no longer force a page break before and after; they flow right after their
chapter and only move to a new page when they won't fit (`break-inside:avoid`),
so a sheet never splits. Print type 11pt at 1.36 line height, compact table
and worksheet padding, 12mm page margins, and a three-line closing card in
print. Every page is at least half full on Letter and A4. **If you add text,
re-render and check for a near-empty last page**: the kit is right at 8
pages, and one extra paragraph can spill a line onto a ninth.

**2026-10-13.1700** — kit finished; stop adding chapters, eight pages is the
point. A *Having a bad week? Start here.* box on page 1 maps problems to
chapters (links on screen, a two-column index in print; it replaced the
chapter chips). Every worksheet names its exact online tool; the talent
review sheet prints `quotabird.com/talent-review`, a small forwarding page
(`talent-review/index.html`, noindex, canonical to `/olr/`) so the kit reads
universal while the tool keeps the OLR name Mark chose. Closing line added:
*If one of these pages saves you one bad meeting, it did its job.* Still 8
pages on Letter and A4.

**2026-10-13.1900** — renamed back to *The Manager's Field Kit*, subtitle
*Useful things for the weeks when the number, the team, or both are giving
you trouble.* on the kit page, the promo card, the menu row, the page title,
structured data, llms.txt and the PDF. Still 8 pages; previews regenerated.

**2026-10-13.2100** — chapter 10 is now *Managing high performers*: leave them
alone when the system is working, don't punish them for being good (bigger
number, extra accounts, unpaid coaching), and three questions once a quarter.
Start-here row shortened to *High performers → Chapter 10*. The print closing
card puts the terms and URL on one line, and print paragraph spacing is 5.5pt,
to keep the kit at 8 pages on Letter and A4.

**2026-10-13.2300** — the kit has its own share card, `card-kit.jpg`
(`python3 make-card.py kit`): QuotaBird mark, *Free printable* pill, title
and subtitle on the left, the two page previews stacked on the right. It is
drawn from `kit/preview-1.jpg` and `preview-2.jpg`, so **re-run it after
regenerating the previews**. The kit page's og:image, twitter:image and
structured data point to it.

**2026-10-14.0900** — a small easter egg at the bottom of the About page only:
*Why the bird?* / *If you carry a number, sooner or later the Quota Bird lands
in your territory. Like Santa, but with quota.* with the bird (white outline in dark mode). Keep it there and
nowhere else; the rest of the site stays plain and useful.

**2026-10-14.1300** — from a review of Amazon and Google management ideas
(borrow the behavior, not the vocabulary): three lines added to the kit (the
good-news reporting system, chapter 2; "what changed?", chapter 3; what good
looks like by next Tuesday, chapter 6), still 8 pages. Pipeline Check has a
*Try 5 points lower* button under the result ("Before you defend it, try to
break it."), shown when the win rate is above 10%; each tap drops it five
points (`pipeline_stress` event). Not taken: a sixth "what changed?" question
on every tool (breaks the one-minute promise; Deal Check's *Pressure test*
already does the disconfirming), and any Amazon or Google vocabulary.

**2026-10-14.1500** — Mark's email, `mark@quotabird.com`, added: the About
page's booking section (*Or email me*, after Chat with Mark and LinkedIn),
the kit's closing card (on screen and in print, on the same line as the
terms), and the Person structured data. Not added to every page's footer or
the result cards, which keep "I answer LinkedIn faster than email."

**2026-10-15.0900** — **The Leader's Field Kit** at `/leader/`: the sibling of
the Manager's kit, for managers who want to become the person other managers
call (the thesis: *become useful enough that your name comes up when you're
not in the room*). Six chapters (known for, point of view, receipts, build
something others can borrow, the right rooms, people behind you) and two
worksheets (*My point of view*, *A year from now*), 3 pages on Letter and A4.
Written from general observations; **no invented stories about Mark's
career** (add real ones by editing `LEADER_BODY`). Its own PDF
(`leader/leader-field-kit.pdf`), previews (pages 1 and 3), share card
(`card-leader.jpg`, `python3 make-card.py leader`) and download card
(`partials/leader-card.html`, on About and Field Notes, next to the
Manager's card). Both kits are rows at the top of the Tools menu; the
Manager's kit ends with a pointer to the Leader's. Downloads count as
`leader_download`; the Manager's stay `kit_download`. `LEADER_PAGES` in
`make-tools.py` holds the page count shown on the page; update it after any
re-render. The paid monthly-session idea from the same review is not on the
site; it goes on the About page only once Mark decides format and price.

**2026-10-15.1100** — **Three Field Kits, one ladder.** A manager is already a
leader, so the kits climb by reach, not title: *The Seller's Field Kit*
(`/seller/`, carry the number, 4 pages: is it a real deal, pipeline math, one
deal carrying the quarter, single-threaded, discounts, a quiet deal, behind
the number, don't make your manager guess; five worksheets that map to Deal,
Pipeline and Account Check), *The Manager's Field Kit* (`/kit/`, run the
team, 8 pages), and *The Leadership Field Kit* (`/leader/`, influence beyond
your team, 3 pages; renamed from *Leader's*, new opening, "Recognition
usually follows usefulness", a closing note on reputation lag, and chapters
2 and 3 swapped so the point-of-view worksheet starts cleanly on page 2).
`/kits/` shows all three as a ladder; the header, footer and Tools menu link
there instead of to one kit. Download cards: the Seller's on the seller
tools, the Manager's on home and the manager tools, Manager's + Leadership
on About and Field Notes. Each kit points to the next rung. Downloads count
as `seller_download`, `kit_download`, `leader_download`. The printed closing
card is a little more compact for all three. **Page counts on the kit pages
come from `SELLER_PAGES` / `LEADER_PAGES` and the Manager's hero text; update
them after any re-render.**

**2026-10-16.0900** — full-site voice pass: every negative contracted (57
strings in the generator plus the Deal and home pages), escaped correctly for
the JavaScript they live in and syntax-checked page by page; the five
identical *The five questions, and what each one disproves* headings each got
their own words; the stiff "isn't X. It's Y." lines rewritten; *honestly*,
*make sure* and *you should* tics removed. All thirteen tools run end to end;
kits unchanged at 4, 8 and 3 pages; previews and share cards refreshed.

**2026-10-16.1500** — de-polish pass from a second read: About ("Usually
you've got more than one problem. That's what makes it fun."; the number from
above now ends "Somehow those two numbers are supposed to meet."), Pipeline
("Being short on pipeline doesn't automatically mean everybody needs to
prospect harder."), Deal ("which part of the deal you can't actually prove";
"Deal Check tells you whether you've actually got one yet"), Rep ("six more
months won't fix it"), Brief ("Nobody cares about your deck", "say it before
somebody else does"), and the last two "That matters." lines. A sweep of the
built site finds none of the filler phrases left.

**2026-10-16.1700** — kits read against the de-polish rules. Found and fixed
nine grammar errors introduced by the contraction pass ("it" or "that" as the
object of the word before it, e.g. "after that's an answer too"): Seller's kit,
Manager's kit, Commission, Rep and OLR FAQ, Risk, Territory, a Field Note, and
the home page's share/search description. Two kit lines rewritten (the
calibration room as a person; a wrap-up in the Leadership kit). Lines Mark or
his reviewers kept were left alone. Kits still 4, 8 and 3 pages; previews and
share cards refreshed.

**2026-10-16.1900** — About page order fixed: Mark's story and the booking
section come first, then one quiet line to the Field Kits, then *Why the
bird?*. No kit cards on About (they were landing above the story because the
cards are injected above the About section on every listed page). Decided
against: the easter egg in every footer (it's an easter egg; repeated on 30
pages it's a slogan) and a kit call to action in the footer (every footer
already links to Field Kits, and the right kit card already sits on the pages
where it fits).

**2026-10-17.0900** — third read-through, for cohesion and edge. Five "Before
you…" tool headlines became the question the tool answers; seven identical
"Answer five questions and find out…" intros rewritten to differ; Deal
Check's leftover "Federal Sales Pipeline Review Tool" title and the OLR title
brought into the "X Check: question" pattern; five share cards redrawn with
the new headlines; fifteen padding "actually"s removed. Verdict lines left
alone: they already carry the edge, aimed at the deal.

**2026-10-17.1100** — dark-mode bird outline changed from white to the accent blue (`logo-dark.svg`, `logo-x-dark.svg`, `favicon.svg`): two-tone blue, no harsh rim, wing line kept.

**2026-10-17.1300** — mobile pass against the UX notes: tap targets raised
to 44px (header chips 40px, menu rows, text buttons, footer links, the
start-here links in the kits, the Made-by About link); footer nav regenerated
every build; sticky start button no longer covers the footer.

**2026-10-17.1500** — **Bug fixed:** on the hand-written Deal page, the kit
card was being added again on every build instead of replaced, and had
reached 24 copies (22 phone screens). `chrome()` now strips any existing kit
card before inserting one. Deal Check trimmed from 30.8 to 7.9 phone
screens: *Why not BANT or MEDDIC?* cut to the verdict plus a link to the
Field Note; the pipeline-review essay cut to *If you run the review*; FAQ
from 8 to 5 (customer/dollar and rigor folded into the privacy and scoring
answers). Bio wording updated everywhere to Mark's: *six years leading
federal partner sales teams at AWS*. Kits re-rendered (4, 8, 3 pages).

**2026-10-17.1700** — *OLR Check* renamed **Talent Review Check**. The URL
stays `/olr/` (no redirect needed) and `/talent-review/` still forwards to
it. The copy keeps "OLR" where it explains that it's Amazon's name for the
talent review, which is what people search for; the page title carries
"(OLR Prep)" for the same reason. Renamed in the menu, the home doorway,
the page, the DM text, the share card wordmark, llms.txt and ai-catalog.json.
Also fixed a leftover "then the room grills you" in two descriptions
(Talent Review and Brief), from before *Grill me* became *Pressure test*.

**2026-10-17.1900** — Talent Review Check's share card and share title read *Will your recommendations survive the room?* (the page headline stays *Will your case survive the room?*; a tool can set `ogh1` to give its share card its own line). Three share-card subtitles still said "the room grills you" (Talent Review, Account, Brief); now "pressure-tests you".

**2026-10-18.0900** — Talent Review Check: the thing you bring into the room
is your **assessment** everywhere (page, verdicts, DM, share card; 27
"case"s replaced). Headline and share line are the same again: *Will your
assessment survive the room?* Start button *Test my assessment* (18
characters, at the limit). Nav and home doorway say *Talent Review* (the
page keeps the full name). "The room respects…" line replaced with "A soft
spot you name first stops being a weakness."

**2026-10-18.1100** — new front door on the home page: *What's giving you
trouble this week?* with six one-tap answers; tools accept `#start` to open
on question 1; Pipeline Check moves to second position with an h2. Easy to
revert: the calculator block is unchanged underneath.

**2026-10-18.1300** — full Amplify rewrite list regenerated from the page list (`amplify-rewrites.json`): trailing-slash 301s for every page, including the Field Notes and Sales Math articles; `/talent-review` now a real 301 to `/olr/` (the forwarding page stays as a fallback); `/pipeline` to `/`; the 404 catch-all last. When a page is added, add its `/{slug}` → `/{slug}/` line above the catch-all.

**2026-10-18.1500** — home front door is now *The sales problems shelf*
(15 book covers, featured *Start here* Deal Check), replacing the six
buttons. Taps still count as `front_pick`. Every label fits from 320px up.

**2026-10-18.1700** — final polish against a UI/UX fundamentals review:
type consolidated to one scale (6 to 8 sizes a page, from up to 16);
pressed states on everything tappable; dark-mode covers dimmed slightly;
Tools menu kit row shortened to *The Field Kits (PDF)*. **Bug fixed:** the
Oct 17 guard against duplicate kit cards was stripping the cards from every
page, including `/kits/`, which is made of them; it now runs only on pages
that get a card injected. Full audit clean: 807 buttons at 320, 360 and
1280px, the shelf, the menu, all thirteen tools, kits at 4, 8 and 3 pages.

**2026-10-18.1900** — context line above every question (mini-hero on Q1,
one line after); 404 page shows the shelf instead of a single button.
All nine question tools checked from the shelf on a 375×667 phone: the
context matches the cover, and all three answers stay above the fold.

**2026-10-18.2100** — the default share card (`card.jpg`, `python3 make-card.py
home`) is now the shelf: *The sales problems shelf / Pick the problem you've
got.* with eight real covers in the site's colors, words and bird marks. It
is the card for the home page and for every page without its own (About,
Field Notes, Sales Math and their articles, Field Kits). Home share title
*QuotaBird: Pick the problem you've got.*; description and alt text describe
the shelf; structured data adds the shelf as an ItemList of fifteen. **If a
cover's words or colors change, re-run `make-card.py home` so the card keeps
matching the shelf.**

**2026-10-18.2300** — share-tag hygiene, run at the end of every build:
share images carry a content fingerprint (`card.jpg?v=adec3d8f`) because
LinkedIn caches images by URL and ignored the new home card; a changed card
now gets a new URL, an unchanged one keeps its URL. **Order matters: run
`make-card.py` first, then `make-tools.py`,** so the fingerprints match the
images. Share descriptions under 100 characters (LinkedIn's warning) fall
back to the page's search description; Field Notes' descriptions now say
which tool each ends with. Partner and Rep no longer share with their old
"Before you…" lines.

**2026-10-19.0900** — sharper share cards. LinkedIn's Post Inspector shows its
own 480px copy, so it will always look softer than the feed, but two things on
our side made it worse: every card was saved with 4:2:0 chroma subsampling
(which smears coloured text on coloured backgrounds), and the shelf card's
eight covers had titles too small to survive the shrink. All sixteen cards now
save with `subsampling=0`; the shelf card is drawn at 2x (2400×1260, declared
in og:image:width/height) with six larger covers. Fingerprints changed, so
LinkedIn refetches.

**LinkedIn profile banner** — `python3 make-card.py banner` writes
`linkedin-banner.jpg` (1584×396, LinkedIn's size) and `linkedin-banner@2x.jpg`
(3168×792). The shelf pitch and four covers sit in the right two-thirds; the
left 574px stays clear for the headshot, which overlaps the bottom-left on
desktop and is larger in the mobile app, and nothing sits near the top or
bottom edge, which the app trims. These are for Mark's profile, not the site;
they aren't in the deploy package.

**2026-10-19.1100** — **Ask Mark is a page** (`/ask/`): *Got a problem that
doesn't fit in five questions?* The free twenty-minute call first (button above
the fold on a phone, then how the call works), then *If it needs more than
twenty minutes*: **Manager Wingman** (monthly calls) and **Team session** (a
pipeline or deal review, account planning or manager workshop, one session, not
a rollout), each with an email link, no prices yet ("Paid work is priced by
scope. We agree on it before anything starts."). The header chip, footer, and
Made-by card link there; About's booking section is now a short pointer to it.
Every result card ends "Free either way. For bigger things, here's how I work
with teams."; every kit's closing card adds "Used this with your team and found
something ugly? I do this with sales managers and teams too." (screen only, so
kit page counts hold). Amplify: add `/ask` → `/ask/`. Also fixed: the numbered
steps only rendered inside section bands. Next is distribution, not more site.

**2026-10-19.1300** — **Stuff I Like** (`/stuff/`): eight books and ten
podcasts, each with one line in Mark's voice. No affiliate links and no links
at all ("Your library and your podcast app will find them."); keep it curated,
don't grow it. Linked from the About story and the footer. **Who I've helped**
on About, and one line near the paid offers on Ask Mark: names in plain text
("people I've helped have worked at…"), never a logo wall and never "trusted
by", which implies the companies engaged Mark. No "used by" claim on the home
page: the tools store nothing, so usage can't be backed up. The company list is Mark's: Amazon, Microsoft, Google, Oracle. Amplify: add `/stuff` → `/stuff/`.

**2026-10-19.1500** — from a web-design principles review: contrast audit
(29 failing text styles, all real ones fixed: the brand blue failed as button
and link text at 2.5 to 2.8:1, now a deeper blue of the same hue; four
covers fixed); a proof line in the home hero (*Built by Mark Flournoy, who
spent six years leading federal partner sales teams at AWS*), so the first
screen has headline, context, proof and action. Share card, banner and kit
cards regenerated with the new colours.

**2026-10-19.1700** — from a "why some UI feels perfect" review: example
values in the calculators render grey until edited, so the user's own
numbers stand out (emphasis is the difference from the neighbours; defaults
should look like defaults). The rest of that review was already true of the
site: receipt-style rows (labels left, values right), centring only for
fine print, grouping over white space, colour that carries meaning. Icons
were deliberately not added; the plain-text voice is the brand.

**2026-10-20.0900** — from a homepage roast, what was taken:
- **One name:** *free, private sales checks* (tab title, home eyebrow, share
  card, banner). "The sales problems shelf" is no longer a visible name.
- **Pipeline Check moved back to `/pipeline/`** (source `pipeline.src.html`),
  with its 3X essay and its four FAQ answers. Home is now the shelf, *How these
  work*, Field Notes, the kit card, Made by Mark and a general FAQ; the
  duplicate "Twelve more checks" list is gone. Every link, hand-off (Quota
  Check lands on `/pipeline/#t=…`), llms.txt and ai-catalog entry repointed;
  1,403 internal links checked, none broken. **Amplify: the old `/pipeline` →
  `/` rules must go** (new list in `amplify-rewrites.json`: `/pipeline` →
  `/pipeline/`). Browsers that visited `/pipeline` after Oct 8 may have cached
  the old redirect; it clears with their cache.
- **Pipeline verdict ladder:** Covered / Close / At risk / Short. *Hopium* stays
  in Deal Check, the Deal cover and the 3X essay only.
- Home hero: *Five questions or a few numbers each. Nothing typed into a system
  your boss can see.* (the "five taps" stretch is gone).
- Desktop header no longer repeats Field Kits / Field Notes / About inside the
  Tools menu (phones still need them there).
- Cover stamps are `aria-hidden` (screen readers heard "QuotaBird" 15 times).
- American spelling throughout (three British spellings fixed).
- Made by Mark now says plainly that paid help exists.
Not taken: three tools instead of fifteen (the shelf is Mark's choice and has
one *Start here*), leading the whole site with "federal" (the audience is
cloud and SaaS sellers too; the credential line carries it), renaming `/kit/`
(the PDF is already shared at that address).

**2026-10-20.1100** — the site's one name is now *Help for your sales problems* (tab title, home label, search and share text, share card, banner), replacing *free, private sales checks*; "private" answered a question Mark's users weren't asking.

**2026-10-20.1300** — home hero, Mark's wording: *A little help with sales* /
*Pick the problem you've got.* / *A few questions. A few numbers. A useful
answer.* / *Built by Mark Flournoy, after six years leading federal partner
sales teams at AWS.* Carried through the tab title, search and share text,
share card and banner. The privacy line ("nothing typed into a system your
boss can see") now lives in *How these work* rather than the hero.

**2026-10-20.1500** — home hero trimmed to the label and headline (*A little help with sales / Pick the problem you've got.*) so more of the shelf shows above the fold. The credential still appears on About, Ask Mark and in the Made-by card; the share card and banner keep their three short lines.

**Tried and dropped (Oct 20):** a "worn" shelf (duller covers, a coffee ring, a dog-ear, a sticky-note "start here", a blunter line on the Deal cover). Mocked up side by side; Mark passed. The shelf stays clean.

**2026-10-20.1700** — Mark's live edits folded into the build (he had edited
About and Stuff on the live site; deploying without this would have overwritten
them): About's lede is just "Usually you've got more than one problem."; Stuff
I Like has his order, two new books (*Meditations*, *Tao Te Ching*), his
headings (*Books that made me think*, *Podcasts I fall asleep to*), and each
podcast's host. The list lives only on `/stuff/`; About keeps the one-line
pointer so its story runs straight into the ask. Marketplace is credited to
American Public Media (not NPR). Fixed: About's footer read "QuotaBird is
QuotaBird, a shelf…"; Ask Mark and Stuff I Like were missing from llms.txt
(earlier edits had silently matched nothing). **Edit copy in the build, not on
the live site**, or the next deploy undoes it. The live site was a mix of
builds; deploy this whole package, with `amplify-rewrites.json`, to make every
page consistent.

**2026-10-21.0900** — **fedhoo hand-offs** (Mark's federal market-data site, a
separate product). One quiet line under the result, after the tool's own
next-step card, shown only when a federal-relevant answer is weak ("sort of"
or "no"): Territory (Spend, Access), Competition (Switch, Access), Account
(Incumbent, Money), Partner (Accounts, Pull). Each starts "Selling federal?"
so commercial sellers skip it, links to fedhoo.com with
`utm_source=quotabird&utm_medium=<tool>`, and counts as `<tool>_fedhoo`.
Engine hook: a tool config can set `aside: (s, answers) => ({text, href,
label}) | null`. QuotaBird's promises are unchanged: nothing from the check
is sent to fedhoo.

**2026-10-21.1100** — Territory Check's next-step card now agrees with its
verdict. It used to say "The territory can produce" whenever the score cleared
55% (the *Thin* line), even when Spend was "no". Now: Workable with Spend yes,
"The territory can produce."; Workable with Spend sort of, "…can probably
produce, if the spend is really there."; Thin, "It's thin, but it might
produce."; Spend "no" or below Thin, the manager route (Rep Check). Hand-offs
now receive the answers too: `handoff: (s, answers) => …`.

**2026-10-21.1300** — shelf covers are 3:4 (trade paperback) instead of 2:3,
on the home page, the 404, the share card and the banner. Books were kept over
squircles (distinctive, and already the brand across card and banner); the
shorter shape recovers most of the space: the shelf is about 12% shorter, an
iPhone SE reads six problems before scrolling instead of three, and desktop
shows all fifteen on the first screen. Every title fits from 320px up.

**2026-10-21.1500** — **social and email collateral**, `python3 make-social.py`
(writes `social/`, which the deploy strips): six 1080×1350 LinkedIn post images
(the shelf, Deal, 3X is a win rate, Quota, Rep, the Manager's kit), a 7-slide
*Where deals break* carousel PDF for a LinkedIn document post, a 600×150 email
signature, and `QuotaBird-posts-and-emails.md` with eight posts, four emails and
the signature. Same fonts, colours and 3:4 covers as the site. Every link is
UTM-tagged (`utm_source` linkedin or email; `utm_campaign` per post), so GA4's
Traffic acquisition report shows which post or email sent each visitor. Re-run
after cover or wording changes.

**Wordsmithing workbook (Oct 21).** `extract-copy.py` (repo only; the deploy
strips it) pulls every visible string on the site into rows, 1,361 of them:
page, where it appears, current text, limit. `QuotaBird-your-words.xlsx` is
built from that for Mark to fill in "Your version" in Google Sheets. When it
comes back, import by matching each row's *current text* in the sources
(make-tools.py, home.src.html, pipeline.src.html, deal/index.html, check.js,
calc.js, partials/), escaping apostrophes for the context they sit in (the
contraction pass has the logic), then rebuild, run every tool, re-render the
kits and check their page counts. Rows' IDs (QB-0001…) are stable only for
this export; re-run the extractor for a fresh sheet after big changes.

**2026-10-22.0900** — Mark's first round of copy edits (23 rows: the home
shelf, Ask Mark, four result cards, the Made-by card) applied, and extrapolated:
every tool headline now matches its new cover (and so do the context line,
tab titles, share cards, the home card, the banner and the social collateral);
"patch" became "territory" in all visible text (53 places plus Rep Check's
first question label; scoring keys, share links and the Field Note's URL are
unchanged); the "no names" caveats on the other result cards became "Send me
your problem."; About's company list matches Ask Mark's. Verdict lines were
left for his next round. Card headlines now shrink to fit. Fixed a bug in the
copy-import helper (an apostrophe written unescaped into code); it now
re-parses the generators after every replacement.

**2026-10-22.1300** — voice pass across the site in Mark's style. Account's
cover is "Do you know your customer?". Plain lines replaced ornament: Risk is
"Does your forecast ride on two deals?" with the verdict *Won't hold* (was
*House of cards*); Partner's worst verdict is *Just promises* ("Lots of
meetings. No deals."); Deal's "tour guide" and "fan club" lines became "Your
champion likes you. They can't sign." and "The people who like you aren't the
people who can spend."; "another set of eyes" became "talk it through"
(About, kits, FAQ); home's how-it-works lost its disclaimer list and the
napkin line; Ask Mark's "One session, not a rollout" is "One session with
your team"; the Seller's kit opens "No sales methodology here." Colourful lines
that earn their place stayed ("The room wants receipts", "parked" deals).
The copy helper now picks the right apostrophe escape from the quote that
opens the string (it had written "Won't" unescaped into Risk's code).
`QuotaBird-your-words-round2.xlsx` is the fresh workbook for Mark's next round.

**2026-10-23.0900** — Mark's round 2: 128 edits (kits, tool explanations,
result cards, Ask Mark, About, Stuff, Field Notes, Sales Math). Covers changed
again, so headlines, tab titles and share cards follow: *You sure that's
enough pipeline? Why you and not them? Are two deals carrying your year? Is
this partner doing anything? Will your brief survive the room?* Home label *A
little help with your quota* (title, share text, card, banner). New footer on
every page: "QuotaBird is a pile of free sales tools I built because I wanted
them myself." Tweaks to his edits, by his own rules: three "not this, that"
lines rewritten; "patch" back to "territory" in one Field Note. The copy
helper now also handles text with inline tags (bold lead-ins, links) and
escapes apostrophes correctly for code inside HTML pages (it broke Deal Check
once this round; fixed before packaging). `QuotaBird-your-words-round3.xlsx` is
current for any next round.

**2026-10-23.1100** — About page rewritten from Mark's own draft, made plainer
and more literal by his rules: "I'm retired." up top; the career in one
paragraph; "These days I help people figure out what's stuck"; five things he
sees a lot, each with a bold lead-in, plus "I love ugly deals." Metaphors made
literal ("the quota that came from somebody who's never seen your territory"),
no "X is not Y" lines, triplets cut to two. The Stuff I Like pointer was
dropped from the story (his draft left it out; the footer still links there).
Who I've helped and the ask are unchanged.

**2026-10-23.1300** — About: "The deal everybody thinks should close but really needs to be killed." (Mark's line; "kill" is a deliberate exception to the old no-kill-language rule from the Kill My Deal days.)

**2026-10-23.1700** — the Manager's and Seller's kits, the posts and emails,
and the carousel rewritten to Mark's rules (the Leadership kit was already in
his voice from round 2). 27 kit lines: "X, not Y" contrasts rewritten, metaphors
made literal ("some flavor of hope" → "a guess"; the "archaeological dig"),
clever chapter titles made plain (3. What commit means; 6. Before you write up
a rep), obvious third sentences cut, closing cards end "good enough." Kept on
purpose, as lines earlier reviews singled out: "a couple I made worse before I
made them better", "terrible close rate", "explaining that sentence",
"improving them to death", "I'd like those months back. So would the rep".
Kits still 4, 8 and 3 pages. Workbook for round 3 regenerated.

**2026-10-24.0900** — the coffee-test pass across the whole site: all 471
prose passages read; about 150 rewritten (every result card, Made by Mark,
home, About, Ask Mark, every tool page's explanation and FAQ, all three kits,
Field Notes, Sales Math, the posts). The résumé line is gone everywhere
(kit closing cards now "I spent six years leading federal partner sales teams
at AWS, after plenty of years carrying a number myself."); the repeated
privacy answer is one conversational version everywhere; quotable closers
removed ("you need both to sleep", "columns don't win", "favors do not scale",
"Everything else is adjectives"). Kept: Mark's own stories and fragments, the
reference tables, and short jaded lines that sound spoken. The Leadership
kit's "good enough" is Mark's own and stayed. Kits still 4, 8 and 3 pages
(four wrapped lines were tightened to hold the Manager's kit at 8 on Letter).

**2026-10-24.1100** — shelf covers are Mark's short titles (Real deal or
hopium? / Enough pipeline? / Crazy quota? / Rep or territory? / Does this
territory suck? / Do you know them? / Why you? / Winging it this quarter? / How
much is too much? / What do I actually keep? / Doing anything? / Can you defend
them? / Will this survive? / Worth printing. / Why 3X?). **Covers and tool
headlines are now deliberately different:** the cover is the short version,
the tool page opens on the fuller question (its h1, which the question screens
repeat). Four headlines changed to match their new covers: Territory "Does this
territory suck?", Risk "Are you winging it this quarter?", Discount "How much
discount is too much?", Commission "It closed. What do I actually keep?" (tab
titles and share cards follow). The cover titles live in home.src.html; the
share card, banner and social images carry their own copies in make-card.py
and make-social.py.

**2026-10-24.1300** — Ask Mark rebuilt for conversion. Order: headline "Want to
talk it through?", one plain sentence, the button ("Book 20 minutes", full
width on phones, above the fold on an iPhone SE) with "or DM me on LinkedIn"
beside it and one line of fine print; then proof at the point of decision
(Mark's photo, one sentence of background, the company names); then "What
people usually bring me" (four specific problems, ruled list); then Wingman
and Team session side by side, same structure; then a last line for people
not ready to talk. Removed: the "Start here" card, the repeated "Twenty
minutes, free", and the "How the call works" steps (two of the three had lost
their list markup in the round-2 import, which is why the page looked broken).
The booking click still counts as `ask_book`. The headshot still has the old
background-removal artifacts; now that it sits beside the button, replacing it
matters more.

**2026-10-24.1500** — About opens straight on Mark: the generic header block
("QuotaBird / About Mark / A bit about me…") and the gap under it are gone.
"Hi, I'm Mark." is now the page's only h1, beside the photo (flex row, 104px
photo, 80px on phones), and the story runs full width underneath instead of
wrapping around the photo. The tab title is still "About Mark | QuotaBird".

**2026-10-24.1700** — friction pass on every result screen (all four engines:
check.js, calc.js, Deal Check, Pipeline Check):
- **"Useful? Yes / Not really" removed** everywhere (it sat between the verdict
  and Mark's card). The `<slug>_useful_*` events no longer fire.
- **Mark's card moved up:** verdict → fixes → (Pressure test) → **Mark's card** →
  next-step card to another tool → fedhoo line → Share · Start over. It used to
  come last, after three other actions.
- **One blue button per result:** "Book 20 minutes" (Calendly, with the verdict
  pre-filled). "DM me on LinkedIn" is a secondary button that still copies the
  note; the monospace draft box is gone. Pressure test is now a tonal button.
  Fine print: "It's free, and if I can't help, I'll say so. The DM button copies
  a short note you can paste." (no link away to /ask/).
- Same card after a finished Pressure test (Deal, Talent Review, Brief).
- New events: `<slug>_book` (Deal: `book`), `<slug>_book_after_grill`; `*_dm_copy`
  unchanged.
Earlier today: Ask Mark rebuilt; About opens straight on Mark.

**2026-10-24.1900** — deploy fix and consistency pass. Root cause of the
"hack job" screenshots: stale cached CSS with new HTML (see Architecture).
Then: Mark's photo floats left with a straight text edge on About and Ask
Mark (same size, round, no shape-outside); one intro style (22px, ink-2) on
every page (article pages had a `.note p` rule overriding it to 17px black);
one section-heading size (22px, was 28 on tool pages); the QuotaBird label
above Field Notes like every other page. Ask Mark's button still on the
first screen of an iPhone SE. Kits still 4/8/3.

**2026-10-24.2100** — UX/UI sources read in full (Web Design Principles, perfect
UI, A complete breakdown, ux2 (A/B tests), ux_ui (psychology)). Applied where
they fit: Ask Mark has "how the call works" back as a three-step row (the
paywall test: a plain timeline plus a safety-net line converts; ours ends "If
I can't help, I'll say so in the first five"). Already in place and confirmed
against the sources: value before any ask (no gates), smart defaults (grey
examples), progress never at zero, one number per verdict, the visitor's own
verdict pre-filled into Calendly, no fake urgency or scarcity. Not applied:
price anchoring (no prices yet; don't fake a reference price later).

**2026-10-25.0900** — About lead: "Hi, I'm Mark. / I'm retired, but I still love ugly sales problems." (Mark's line, as a 22px lede under the headline). The later "I love ugly deals" item became "Ugly deals especially." so it doesn't repeat the lead.

**2026-10-25.1100** — About's first paragraph is one flowing paragraph in Mark's voice, opening "I'm retired, but I still love ugly sales problems. Probably because…" (no tagline styling).
