# QuotaBird — handoff

**Current build: 2026-10-28.1900.** This file describes the site as it is today. Work from it. Everything here is current; there is no archive. Where a decision was tried and dropped, it's listed under "Already decided" so nobody proposes it again.

## What QuotaBird is

quotabird.com, by Mark Flournoy (retired; six years leading federal partner sales teams at AWS, after plenty of years carrying a number; before that F5, Red Hat, storage companies, and 20 years as a Marine).

**Primary focus: helping reps and managers plan, push back on, and accept quota**, armed with data. Mark's words: "All my years of selling, 'Dude, my quota is crazy!' has been a recurring conversation starter between sales reps, managers, and teams. Reps usually have no idea how their quota and comp plans are created. Managers may find their boss isn't even goaled on their number, it may be growth rate or new business. Managers don't know how to fight comp plans and also don't know how to help reps accept a tough quota and still crush it. Everyone in sales loves a bluebird, but usually, it's just the Quota Bird dropping off more quota."

**The guardrail:** know the math well enough to tell whether they're screwing you. Not a grievance site. Sometimes the quota is crazy, sometimes it's hard but fair, sometimes the rep just doesn't like the number.

Free tools, no login, no AI, nothing stored. The consulting offer (a free 20-minute call, then Manager Wingman or a team session) is the business. Not affiliated with the U.S. government or Amazon.

## Voice

- Mark: older, dry, mildly grumpy, anti-bullshit (not anti-company, anti-management or anti-AI). The tone reference is the Stuff I Like page. Humor comes as an aside; don't explain the joke.
- **The coffee test:** would Mark say it to one person over coffee? If it reads like website copy, a LinkedIn bio, a keynote or a founder statement, rewrite it.
- **Stop at the point.** No trailing tag lines ("Free. Nothing stored.", "No email."), no closing sentence that restates or sells, no résumé triplets, no neat X-not-Y lines, no "the key takeaway." The privacy promise lives in each page's FAQ.
- Contractions always. No em or en dashes anywhere. "Territory," never "patch." Bio wording is exactly "six years leading federal partner sales teams at AWS."
- Numbers are sourced (see Data). Self-reported data is labelled as self-reported.

## UX rules (apply to every page)

1. **Show value before any ask.** The home page answers a question in the first screen (the live mini Quota Check) before anyone taps anything.
2. **Answer first.** Tools show the verdict above the inputs; results and Quota Shorts lead with the number, big.
3. **One filled button per screen.** Everything else is tonal, text or a link.
4. **Put proof where people decide.** Mark's photo and bio sit next to the booking button; the booking card comes right after a verdict, before links to other tools.
5. **Pre-fill with example numbers, shown grey, and say so** ("Example numbers. Type yours over them."). Tapping a field selects it, so typing replaces the value.
6. **Never pass off an example as the user's number.** Links carry only fields the person actually typed; anything else stays a grey example (`calc.js` tracks which fields came from the link).
7. **Mobile first, from 320px.** No sideways scrolling at any width. The main answer and its button fit the first screen of an iPhone SE.
8. **Touch targets at least 44px.** Every button has hover, pressed and focus states; motion respects reduced-motion.
9. **Readable everywhere:** all text passes WCAG AA in light and dark mode. Coloured fills carry dark text; the only blue that can be text on white is #0A71B1.
10. **Receipt-style rows** for numbers: label left, value right, one edge each.
11. **Emphasis is difference.** One tinted container per screen at most; colour only where it means something.
12. **Snack-size content** (Quota Shorts): one idea per card, the number big, one line under it, a source, and the tool that does the math.
13. **Keep forms short.** The fewer fields between someone and an answer (or a booking), the better. Calendly asks name, email and one line.
14. **No decoration that isn't doing work:** no highlighter, gradients, gloss or shadows.

## Design system (Material 3 roles, seeded from the bird)

- **The bird:** Mark's drawing, body #9DD2FF, outline and eye in #1B1F23. Dark versions get a light rim; the 404 bird has an X eye. PNGs are rendered from the SVGs (make sure the local server is running first, or they come out as broken-image icons).
- **Page:** pure white. Text #1B1F23; muted #5B6670 (only on white and light neutrals). Font: Inter, self-hosted.
- **Blue scale (Mark's monochromatic):** #4FAEFF, #6AB8FF, #86C5FF, #9FD1FF, #B8DDFF, #D3E7FF, #EAF4FF (tokens `--blue-1` to `--blue-7`).
- **Roles:** filled button `--blue-1` #4FAEFF with #00182B text (hover `--blue-2`); filled tonal button `--blue-6` #D3E7FF; selected chip = the bird #9DD2FF; emphasis container (booking card, headline stat) `--blue-7` #EAF4FF; text links #0A71B1 only. Dark mode: the filled button is the bird.
- **Shapes (M3 scale):** buttons and answer choices full; chips 8px; cards 16px; text fields 4px. Circles stay circles.
- **Cards:** flat, 1px #D6DCE2 border, no shadow, no gradient. Plain cards #F7F8F9.
- **Verdict tints:** green #C6EBC9, yellow #FFF982, orange #FFCF8A, red #F5B3AD.
- **The shelf keeps Mark's original book colours**, each with its own title colour (`--on-k`): Quota coral #E07A5F (featured), Pipeline #F2C14E, Deal #1C3D5A, Rep #388073, Territory #F4E1C1, Account #6C5B7B, Competition #C35037, Risk #2E2E3A (gold type), Discount #9DD2FF, Commission #567E55, Partner #F28482, Talent Review #264653 (gold type), Brief #E9C46A, Field Kits #EDEDE9, Sales Math #1D3557. Quota Shorts use the same colours.
- **Big numbers:** the hero answer and the Quota Shorts use 48px, weight 800. Stats on /quota-by-the-numbers/ are plain cards (`stat()` / `stat_grid()`): value, label, a source line per section. No donuts or bar charts.
- The system lives in the blocks at the end of `site.css` ("One system", "M3 roles and shapes", the Shorts numbers), which win over older rules above them.

## Pages

**Home:** "The quota landed / Is your quota crazy? / Maybe. Let's do the math." then the live mini Quota Check (basis chips; quota, base, variable pre-filled grey; multiple and verdict update as you type; "See the whole plan" hands typed numbers to /quota/). Then "Push back or build a plan." over three paths (Understand it → /how-quotas-get-built/, Push back → /quota-case/, Accept it and plan → the note), the Quota Shorts strip, and the shelf under "The quota isn't the only problem." The hero's thresholds must match Quota Check's.

**The 14 tools:**

| URL | Tool | Kind | Headline |
|---|---|---|---|
| /quota/ | Quota Check | calculator | Is my quota crazy? |
| /quota-case/ | Quota Case | calculator | What has to be true for this quota to work? |
| /pipeline/ | Pipeline Check | calculator (pipeline.src.html) | You sure that's enough pipeline? |
| /discount/ | Discount Check | calculator | How much discount is too much? |
| /commission/ | Commission Check | calculator | It closed. What do I actually keep? |
| /deal/ | Deal Check | questions (hand-written page) | Is it real, or is it hopium? |
| /rep/ | Rep Check | questions | Is it the rep, or the territory? |
| /territory/ | Territory Check | questions | Does this territory suck? |
| /account/ | Account Check | questions | Do you know your customer? |
| /competition/ | Competition Check | questions | Why you and not them? |
| /risk/ | Risk Check | questions | Are two deals carrying your year? |
| /partner/ | Partner Check | questions | Is this partner doing anything? |
| /olr/ | Talent Review Check | questions | Can you defend your people? |
| /brief/ | Brief Check | questions, with Pressure test | Will your brief survive the room? |

Question tools run on `check.js`, calculators on `calc.js`. Five questions per tool in a fixed order (scoring and shared links depend on it).

**Quota pages:** /how-quotas-get-built/ (how a big company builds the number: company target → capacity → territories → quotas → comp plan; over-assignment; consumption quotas; fiscal calendars; "your boss may not be goaled on your number"), /quota-by-the-numbers/ (sourced stat cards), /shorts/ (all Quota Shorts).

**Field Notes (11):** Your quota is crazy. Now prove it (managers pushing back) · You're the rep and the number is crazy · You have to hand down a number you don't love · The number isn't changing. Now what? · Before you decide the comp plan sucks, figure out how it pays · 3X is a win rate in disguise · Why I don't start with BANT or MEDDIC · If three people failed in the same territory · Your quota went up 30%. Did your territory? · They asked for 15% off · Your best rep hates meetings.

**Field Kits:** Seller's (4 pages), Manager's (8), Leadership (3), printed from their pages to Letter and A4. Re-check page counts after any kit copy change. The Manager's kit index has a Quota problem row (chapter 5).

**Also:** Sales Math (4 pages), About (opens on Mark's photo and "Hi, I'm Mark."), Ask Mark ("Got a quota problem?"), Stuff I Like, 404 (shows the shelf).

## Funnel and analytics

Every result: verdict → what to fix → (Pressure test, tonal) → Mark's card (filled "Grab 20 minutes" to Calendly with the verdict pre-filled; tonal "DM me on LinkedIn" copies a note) → next-step card → fedhoo line (federal-relevant weak answers only) → Share · Start over.

GA4 `G-BG9NR9GXQZ` via `analytics.js` (`window.qbTrack`). Events: `hero_calc_edit`, `hero_calc_go`, `front_pick`, `<slug>_start`, `verdict`, `<slug>_book` (Deal: `book`), `<slug>_book_after_grill`, `<slug>_dm_copy`, `<slug>_share`, `<slug>_edit`, `ask_book`, `kit_download` / `seller_download` / `leader_download`, `<slug>_fedhoo`, `related_tool_click`.

Calendly: calendly.com/markflournoy/chat-with-mark (utm_source=quotabird, utm_medium=<page>). Email mark@quotabird.com. LinkedIn linkedin.com/in/markflournoy/.

## Navigation

Header: Tools ▾ · Field Kits · Field Notes · About · Ask Mark. Don't add to it. The Tools menu leads with Your number (Quota Check, Quota Case, Territory, Commission, Discount), then Your team, Your deal, Any meeting. Footer: "QuotaBird is a pile of free sales tools. I built them because they helped me, and maybe they'll help you." and "Not affiliated with the U.S. government or Amazon."

## Build and deploy

- **Edit:** `make-tools.py` (every generated page), `home.src.html`, `pipeline.src.html`, `deal/index.html`, `check.js`, `calc.js`, `analytics.js`, `site.css`, `partials/*.html`, `404.html`, `make-card.py`, `make-social.py`.
- **Never edit by hand:** built `index.html` files, `sitemap.xml`, `llms.txt`, `ai-catalog.json`, the fingerprinted `site.<hash>.css` / `check.<hash>.js` / `calc.<hash>.js` / `analytics.<hash>.js`, `card*.jpg`.
- **Build:** `python3 make-tools.py` (pages, sitemap, llms.txt, ai-catalog, fingerprints). Cards: `python3 make-card.py <slug|home|banner>`, then rebuild. Social images: `python3 make-social.py`. Copy workbook: `python3 extract-copy.py`.
- **Deploy:** AWS Amplify from GitHub. `customHttp.yml` caches css/js for a year (safe: names change with content) and html not at all. Rewrites in `amplify-rewrites.json` (45 rules, 404 catch-all last); every new page needs a `/<slug>` → `/<slug>/` rule. Never edit the live site directly.

## Data (researched Sept 27, 2026; refresh yearly)

Bridge Group 2026 (158 B2B companies): 48% of AEs at 100%+ (51% in 2024, 66% in 2022); median quota $960K on $200K OTE, 4.6× (4.2× in 2024); quotas +2.4%/yr vs OTE +4.9%/yr; ramp 6.2 months. Bridge 2024: 53:47 mix. RepVue (self-reported, Sept 2026): 42% of AEs reach quota, enterprise 41%, federal 46%, SLED 45%; Cloud Sales Index Q2 2025 average attainment 42.7% (246 companies); AWS Account Manager $150K base / $280K OTE / 54:46 / 64% hit; Microsoft Enterprise AE 56%, SLED AE 67%. Mostly Metrics: over-assignment 20-30%. Accelerators 1.5-2× (comp surveys). Microsoft fiscal year July-June; Microsoft field incentives tied to Azure consumed revenue (Microsoft Learn). Keep "share of reps at 100%" and "average attainment" separate.

## Already decided (don't re-propose)

- **Bird colours:** raven/charcoal, yellow canary, dusty blue #88B1CB and an X-eyed main logo were all tried; the bird is #9DD2FF. No bluebird-versus-blackbird imagery.
- **Palettes:** warm-ink monochrome, "raven" bone-and-slate, Mark's mustard/Material palette, the six-colour card system and a colourless one-family shelf were all tried and dropped. The shelf keeps its original colours; the UI is the M3 blue roles above.
- **Type:** Google Sans Flex was tried and dropped. Inter stays.
- **Visual treatments:** no highlighter on the hero (or anywhere), no editorial "By the Numbers" panels with donuts and bars, no field-guide/kraft look, no gradients or gloss.
- **Hero:** leads with the live mini Quota Check, not just a headline and a button.
- **Copy:** the "kill" language is gone except one line of Mark's on About; don't add more.

## Pending (Mark)

Replace `mark.jpg` (background-removal artifacts; it sits beside the booking button). Set prices for Wingman and Team session. Calendly: 20-minute event, one intake question, no marketing emails. Submit the sitemap in Search Console. Post the Field Notes; write new notes before new tools (queue: The best quota fight happens before January · Show me the bridge · If only 20% of the team hits quota, maybe the reps aren't the problem · Your boss may not be goaled on your quota · When a tough quota is still a fair quota · One giant deal made last year's number · New reps don't produce twelve months of revenue in six months · A vacant territory still has quota · Stop using 3X pipeline if your win rate is 18%).
