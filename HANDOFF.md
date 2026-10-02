# QuotaBird — handoff

**Current build: 2026-11-07.0900** This file describes the site as it is today. Work from it. Everything here is current; there is no archive. Where a decision was tried and dropped, it's listed under "Already decided" so nobody proposes it again.

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

## Plain talk, no machine patterns (Nov 1)

Everything reads the way Mark talks across the table: literal, plainspoken, dry. Say what you mean in the order you'd say it out loud. Before shipping copy, look for these and rewrite them:
- The reversal: "X isn't Y. It's Z." ("Asking isn't pushing back. It's doing your job.") Just say the point.
- Paired punchlines: "A rep with a path works the plan. A rep without one works on their resume." One plain sentence does it.
- Counted setups and bold triads: "They do three things differently" followed by three bold, parallel lead-ins. Write normal paragraphs.
- Flipped lines ("every week, and ... never") and literary metaphors ("good news with a deadline").
- The same device repeated: "in disguise" had crept into four places. A line that works once is a tic the second time.
- Buzzwords: leverage (as a verb), navigate, robust, seamless, crucial, ensure, unlock, empower, landscape, journey, delve.
Mark's own lines stay, even when they're punchy ("3X is a 33% win rate wearing a nicer shirt", "Maybe. Let's do the math."). The test: would Mark say it to a rep at a bar? If it sounds like it was written to be quoted, rewrite it.

## Voice in results (Oct 30)

1. **Tools speak to "you".** Your quota, your territory, your deal, your number. No "I", "my" or "this number" in any result, next step, row or share text. Tool questions are in second person too ("Is your quota crazy?", "What do you actually keep?"). Buttons say "Check your quota", not "Check my quota".
2. **Mark's "I" lives only where he is clearly the speaker:** his card after each result, About, Ask Mark, Field Notes, and his DM and booking templates. Quoted lines stay in their speaker's voice: "Your VP will ask" questions are the VP talking; Quota Case's push-back script is what the rep says out loud.
3. **Every verdict answers its tool's question**, starting with the answer: "Does this territory suck?" gets "Yes. Nobody could hit this." Each tool keeps a short internal tag (At risk, HOPIUM) for the sticky bar, booking notes and lookups, and an `answers` map (in each tool's config; `ANSWER` in the Pipeline and Deal pages) that turns the tag into the answer shown on the card and in share text. **Add an answer for every new tag.**
4. **No unsourced authority.** Keep published fact and QuotaBird interpretation visibly separate:
   - The quota-multiple ranges are **QuotaBird's working ranges** (say that), not industry benchmarks. Bookings 4 to 6× is a working range built around published data (Bridge Group 2026 median 4.6×, 158 B2B companies). Cloud 15 to 30× and whole book 40 to 80× come from cloud-provider plans Mark has seen, not a survey.
   - Bridge Group's sample is B2B, not "SaaS": "$960K median AE quota", never "median SaaS quota".
   - Over-assignment (20 to 30%) and accelerators (1.5 to 2×) are practitioner rules of thumb: "a common rule of thumb", "a common range", never "most" or a market fact.
   - Consumption claims apply to consumption plans, not all cloud quotas ("On a consumption plan, a commit nobody uses…").
   - Live self-reported figures (RepVue) carry their snapshot date next to the number, and no "the most of any" superlatives that can go stale.
   - Don't write "CSP" alone: it means Microsoft's Cloud Solution Provider program to many readers. Say "cloud provider".
5. **Federal-only content is labeled.** Deal Check is federal (appropriations, contract vehicles) and says so on the home card, its page and its share card. The Tools menu just says "Deal Check" (Mark's call: the label is unnecessary for most of the audience). Federal specifics elsewhere are marked as a "Federal wrinkle" or "Selling government:" aside rather than stated as the general rule. A commercial Deal Check (same five questions: customer, money, power, path, now; "path" becomes security, legal, procurement and vendor onboarding) is a good next build.

| Tool | Answers (green → red) |
|---|---|
| Quota Check | No. It's favorable. / No. It's standard. / It's unusually low. / Not crazy. A stretch. / Close. It's aggressive. / Yes. It's crazy. |
| Quota Case | Yes. It already adds up. / You're a little short. / You've got a gap. / You've got a big gap. |
| Pipeline | Yes. You're covered. / Close. Not quite. / Not really. You're at risk. / No. You're short. |
| Discount | This much is normal. / This much needs a trade. / This much is expensive. / This much is too much. |
| Commission | That's your take-home. |
| Deal | It's real. / Real, but at risk. / Hopium. / Not a deal yet. |
| Rep | Neither. They're fine. / The territory. / The rep: a skill gap. / The rep: an effort gap. / The rep. Wrong fit. / Not clear yet. |
| Territory | No. It's workable. / A little. It's thin. / Mostly, yes. / Yes. Nobody could hit this. |
| Account | Yes. You know the account. / Partly. / Barely. One thread. / No. You know one person. |
| Competition | They prefer you. / You're in the mix. / You're behind. / Doing nothing is winning. |
| Risk | No. It's spread out. / Almost. It's lopsided. / Yes. It's fragile. / Yes. It won't hold. |
| Partner | Yes. Real work. / Mostly talk. / Not much. / No. Just promises. |
| Talent Review | Yes. You're ready. / Not yet. / Not really. It's a story. / No. No receipts. |
| Pay | Yes, it pays for beating the number. / A little extra above 100%. / It pays in a straight line. / Not much above 100%. / The cap takes the upside. |
| Comp Plan | Yes. It's clear. / Mostly. Get a few answers in writing. / Not yet. Too much is unwritten. / No. Get answers before you count on it. |
| Offer | About the same money. / Offer A pays more in a normal year. / Offer B pays more in a normal year. |
| Commit | Yes, and then some. / Yes. They're on pace. / Not at this pace. / No. They'll fall short. / No. Not even close. |
| Brief | Yes. It's room-ready. / Maybe. It'll be a fight. / No. Shark food. / No. There's no point yet. |

## Share cards

- **Every share card follows one structure: problem, tool, inputs, output.** Someone scrolling gets about a second. The left side says what it's for in plain words (Quota Case: "Build the case against a crazy quota." / "Last year. Run rate. Pipeline. Win rate."); the right side shows a real output (the gap, and the pipeline it takes to close it). Keep abstract, in-product questions off the cards.
- **Share cards for Quota Check and home use a warm result on purpose.** A green "Standard" gives nobody a reason to click; a believable warm result makes people check their own. Home: red **68×, Yes. It's crazy.** Quota Check: yellow **47×, Close. It's aggressive.** Both sit inside the real bands for cloud run rate, so a visitor who enters them gets the same verdict. Keep numbers specific and plausible (never absurd like 571×), and keep "Maybe. Let's do the math." under the question.

**Quota Case model (fixed Oct 31):** first question is what the quota is measured on (Bookings / Run rate / Whole book).
- *Run rate or whole book:* evidence = current run rate as entered (it already reflects today's team) + new pipeline × win rate. Without a run rate, last year (minus one-time revenue, scaled by ramped headcount) is the baseline. Headcount is shown as context and **never** adjusts a run rate the user entered (the old code did, which counted headcount twice).
- *Bookings:* evidence = the stronger of last year's bookings (minus one-time deals) × ramped reps now ÷ reps last year, and this year's pipeline × win rate. Run rate is ignored.
- Gap = quota − evidence; new pipeline to close it = gap ÷ win rate. Example numbers give a $1.8M gap and $7.2M of new pipeline, matching the kits.

## Next steps after a result (Nov 1)

Every result hands off to the most useful next thing for that verdict, usually a Field Note with the talk track:
- Quota Check: Standard or better → Pipeline Check; Aggressive or Crazy → "Your quota is crazy. Now prove it."
- Quota Case: a gap → the prove-it playbook; supported → Pipeline Check.
- Discount Check → "They asked for 15% off" (what to ask for in return). Not Deal Check, which is federal.
- Commission Check → "Before you decide the comp plan sucks" (accelerators, caps, clawbacks, crediting).
- Commit Check: behind → Account Check (burning a commit takes more than one team); on pace or over → Quota Case.

**Considered and deliberately not built (Nov 1):** marketplace fee and co-sell quota-retirement calculators, multi-year crediting and side-by-side deal comparisons. The rules differ by company and change often, so a generic tool would be wrong for many users. Worth building later as their own projects: a manager team roll-up ("team health"), and churn / NRR ("how much new just to stand still"). Danger-zone colours and shareable scenario links already exist.

**Mark's operating rules (Nov 7), stated on Work with Mark and Federal GTM; keep every page consistent with them:**
- Payment: a payment link for the small fixed-price sessions ($200 Sales Reality Check, $600 Federal GTM Pressure Test); an invoice for recurring, team and company work (Manager Wingman, Team Reality Check, the Federal GTM Sprint, the Federal Revenue Reality Check). The site says "a link I'll send you"; there's no public payment link yet.
- Manager Wingman: month to month, invoiced monthly, cancel anytime before the next billing date, no long-term contract.
- Response: "I usually reply within one business day." Never "24 hours."
- Written recap: within two business days of the session.
- "Starting at" prices: a bigger team, more sessions or offsite travel cost more; the price is quoted before work starts.
- Confidentiality (exact text on both pages): treated as confidential, nothing company-, deal-, personnel- or customer-specific shared without permission, a reasonable NDA for company engagements, and no classified, export-controlled, unauthorized government-sensitive or employer-prohibited material. Never promise privilege, classified handling, a secure data room, or "100% confidential."
Also this round: calculators say exactly what's missing or wrong instead of "Fill in the numbers below" (a tool's compute can return { msg }); the LinkedIn option under results is a text link under the one "Grab 20 minutes" button; Pipeline Check's average deal size, sellers on quota and already closed live under More details (opens when a link or export fills them).

## Math audit (Nov 6)

Every calculator was checked against formulas written independently from the methodology page and this handoff: 230 browser cases across Quota Check, Quota Case, Pipeline, Discount, Commission, Pay, Offer and Commit (random values, edge cases, and values just either side of each verdict cutoff). All match. All ten question tools' weights sum to 100 and match their five questions; cutoffs are 75 / 55 / 35; one "no" never reaches the top verdict; Deal Check's caps (Customer 45, Money 55, Power 60, any no 74) behave as documented.
Two bugs found and fixed:
- **Shared links mixed in example numbers.** A field the sender left blank was missing from the link, and the receiving calculator filled it with the example (a blank accelerator became 150%, a blank monthly spend became $70K, a blank commission rate became 8%). A shared link now describes the whole form: anything it leaves out arrives blank. The home calculator always passes all three numbers it shows.
- **Commit Check showed "$3.00M" and "$2.50M"** because its trailing-zero cleanup was mis-escaped; it now uses the same formatter as Discount Check ("$3M", "$2.5M").
The audit scripts (reference formulas, browser runner, comparison) are in math-audit.zip. Rerun them after any change to a formula, a cutoff, or how links are read.

## Work with Mark and Federal GTM (Nov 6)

QuotaBird is not becoming a consulting-company site. The free tools stay the center and stay ungated; consulting is the paid version of the same idea. One Mark, one front door (FedHoo is a federal data/tools property, cross-linked from /federal/, never a second consulting brand).
- **/work-with-mark/**: "Bring me the ugly one." Sales Reality Check ($200: one problem, 60-minute working session plus a short written recap), Manager Wingman (from $750 a month: two working sessions a month), Team Reality Check (from $1,500: a virtual session or offsite working session), a Federal teaser, the free 20 minutes, and a short proof paragraph.
- **/federal/**: "You think you have a federal business. Let's find out." Federal GTM Pressure Test ($600: 90 minutes plus written observations), Federal GTM Sprint (from $2,500: a pressure test and working plan, not a 75-slide deck), Federal Revenue Reality Check (from $3,500, for investors and acquirers, positioned quietly; no implied prior M&A work), free resources, the free 20 minutes.
- **One front door (Nov 6):** the header button is "Work with Mark" (shows "Ask Mark" at 430px and narrower, same page; hidden under 380px as before, where the Tools menu's bottom links carry Work with Mark). /ask/ redirects to /work-with-mark/#ask (Amplify: /ask and /ask/ go to /work-with-mark/; a stub page backs it up). The footer has one Work with Mark link. The page opens with "Hi, I'm Mark." and the photo, then "What people usually bring me" (from the old Ask page), the offers, the free twenty minutes (with a LinkedIn alternative), and "The specifics" at the bottom.
- **Voice of the two pages (rewritten Nov 6 from Mark's own draft):** Work with Mark opens "Need a second opinion?" with Mark's four paragraphs nearly verbatim, ending "send it over. I'll tell you what I think." The main button is "Send it over" (an email), with the free 20 minutes as the alternative; offers follow under "What it costs" as two plain sentences each; "A few specifics" closes the page. The Federal page uses the same voice and the same buttons. Keep this voice: plain first-person sentences in normal paragraphs, no slogans, no "X, not Y" or "isn't X. It's Y", no strings of short fragments.
- **Starting a paid engagement:** each offer's button is a pre-addressed email to mark@quotabird.com with the offer as the subject. Swap in paid booking links later if Mark wants.
- **Federal Readiness Check** (/federal-readiness/): Customer, Money, Path, Partners, Team (weights 24/24/20/14/18, any-no cap 74). Answers: "Yes. There's a business here." / "Maybe. Prove the weak part." / "Not yet. It's mostly hope." / "No. Not yet." Left out of the Tools menu (MENU_SKIP); reached from /federal/ and the home list.
- **Quiet next steps** (`offer` in a tool config; one line at the bottom of the Mark card, after the useful result; never a banner, modal or gate): Quota Case with a gap, Sales Reality Check; Deal Check when not healthy, Sales Reality Check; Pipeline Check with more than one seller, Team Reality Check; Rep, Talent Review and Risk, Manager Wingman; Federal Readiness, Federal GTM Pressure Test. No line on other tools.
- **Proof** is only what Mark can substantiate: 20 years in the Marine Corps (COTR, government technology and acquisition work), about 15 years in enterprise technology sales at Red Hat, F5 and Amazon, a Senior Sales Manager at Amazon leading federal partner sales teams across four markets, about 25 partner sales managers with a shared goal above $1B, a $54M four-year committed cloud agreement with a major DoD systems integrator, President's Circle at F5. Add testimonials or anonymized examples only when Mark provides them.
- **Not built, on purpose:** a newsletter platform, email capture, a training catalog, a page per offer. A LinkedIn follow is enough for now.
- Voice on these pages is the site's voice: plain, dry, skeptical, never guru. Banned there too: transformation, unlock, optimize, excellence, world-class, fractional CRO.

## After the Sales plugin review (Nov 5)

- **Pipeline Check, biggest deal:** an optional "Biggest single deal" field adds "If your biggest deal slips": the same target and coverage needed, with that deal out of the year. Shared links carry it (`b`).
- **Pipeline Check, export (rebuilt Nov 5 after Mark's test):** never rejects a file. Reads comma, semicolon or tab files, with or without a heading row; amounts like $12K, 12,000 or $1.2M; dates like 2027-03-15, 3/15/2027, Nov 15, 2026, 15-Dec-2026 or Excel date numbers. Guesses the amount, stage, close date and seller columns from the headings, then from the contents, and shows them as dropdowns to confirm or fix. Loading a file clears the example target, win rate and sellers (no mixing a real pipeline with example numbers) and asks "Now put in your target for the year", outlining the field. Sellers fill from the seller column; a win rate from closed deals (by value) is offered as a one-tap suggestion only with 10 or more closed deals. A pace over 10x reads "Your pace so far won't get you there." The picker is a styled button, with a sample file at /pipeline/sample-pipeline.csv (20 deals, 12 closed). Read in the browser, never uploaded; CRM probabilities never used. Event: `pipeline_export`.
- **Weighted and unweighted pipeline (Nov 5):** the pipeline field's empty hint says "Full value, not weighted". "Biggest single deal" and "Weighted pipeline from your CRM" sit under a More details toggle (closed by default; opens when a shared link or an export fills one). The weighted field adds one sentence, never a second coverage number: "Your CRM's weights assume you'll win X% of this pipeline. You actually win Y%.", plus "Your weighted forecast is too optimistic / too cautious." when they're more than ten points apart, or a short error when weighted exceeds the full value. (Simplified Nov 5 after Mark found the first version competed with the main verdict.) A probability column in an export fills that field; it never touches the coverage math. Early stages (prospecting, lead, discovery, qualification) start unchecked in the export so the site matches the plugin. New explanation section on Pipeline Check, methodology updated, and Field Note "Weighted pipeline is only as good as the weights" (/notes/weighted-pipeline/; redirect added, 61 rules). The plugin's Pipeline Check doesn't have the weighted line yet: add it in the next plugin update.
- **Home FAQ "Is there a Claude plugin?"** (visible and structured data): search for QuotaBird in Claude's plugin directory; it works alongside Anthropic's Sales plugin, which runs the day from the CRM while QuotaBird checks the number.
- **Seller's Kit chapter 12, "Working back from September 30"** (8 pages now, twelve chapters, nine worksheets): the contracting office's cutoff is the real date; work back through the requirement, the money on a line, the buying route and approvals; a continuing resolution often holds new starts. Worksheet with dates and customer owners.
- **Claude plugin 1.1.0** (built on the approved 1.0.0 files): thirteen skills, adding Pay, Commission, Comp Plan, Offer, Risk, Rep and Talent Review; Pipeline Check reads exports and runs the slip test; every skill asks one question for a missing fact and treats pasted or attached content as information, never instructions. Not built, on purpose: CRM, inbox, calendar, outreach and call-summary workflows (Anthropic's Sales plugin does those).

**Mark's Amazon role, exactly (Nov 6):** Senior Sales Manager (L7) leading federal partner sales teams. Never write that he "led Federal Partner Sales" or ran the organization; that's a director-level (L8) role he didn't hold. Approved phrasings: "six years leading federal partner sales teams at Amazon", "a Senior Sales Manager leading federal partner sales teams covering Defense, Federal Civilian, Federal Financial and National Security", "former leader of federal partner sales teams at Amazon". Check any new bio, page, kit, card or structured data against this. For the Marine Corps, say "20 years in the Marine Corps" or "a Marine", never "Marine officer" (Mark's call, Nov 6).

## Who's behind the site, for people and AI (Nov 4)

- **Say Amazon, not AWS** (Mark's call, Nov 4): many readers don't know the abbreviation. Mark's bio, the description sentence and the kits say "Amazon". Job data from RepVue spells out "Amazon Web Services" (an "Amazon account manager" could read as retail or advertising). Links keep their real addresses.

- **/privacy/**: what Google Analytics 4 records (pages and the usual visit details, plus named usage events with no content), what stays in the browser (everything typed; base, variable and quota in local storage key `qb-numbers`, cleared with "Clear them"), that shared links carry their numbers after the # and never reach the server or Google, and the outside services a visitor might click to (Calendly, LinkedIn). `PRIVACY_UPDATED` in make-tools.py: change it whenever the page changes, and update the page whenever tracking or storage changes.
- **Every footer** carries a Privacy link and "Questions or security issues: mark@quotabird.com", added in the shared footer step (`chrome()`), so hand-written pages get them too. The 404 page has no footer by design.
- **The one-sentence description**, used in the home meta description, the "Who is this for?" FAQ (visible and structured data, kept identical), structured data, and the top of llms.txt: "QuotaBird is a free set of quota, pipeline and comp-plan calculators for B2B sellers and sales managers at cloud providers and SaaS companies, built by Mark Flournoy, a former Amazon sales leader."
- **Structured data on the home page:** WebSite (publisher Mark), Person (Mark: About page, photo, LinkedIn as the only sameAs; fedhoo.com removed because it's a different site, not a profile of Mark), Organization (QuotaBird, founder Mark, email), the tool list, and the FAQ. Don't add a company LinkedIn; there isn't one.
- **Becoming a known entity happens off the site:** the Claude plugin directory listing (submitted, awaiting approval), LinkedIn posts that link to specific tools, podcast and guest appearances, and other people citing the methodology page. Don't create a Wikidata entry.

## Website design skill v2.1 pass (Nov 3)

- **Home page, one route to each tool.** The two jobs are lists of rows, side by side: "The number they gave you." (the guide, Quota Case, Territory, Pipeline, Discount, and "The number isn't changing" note) and "What they'll pay you for it." (Pay, Commission, Comp Plan, Offer). Below the Shorts, "Also useful." holds Your deal, Your team, and Print and learn. Brief Check is off the home page and the menu; its page and the plugin skill stay. The home block uses class `jobs` (not `pillars`, which is the uppercase label strip on tool pages).
- **The home calculator shares the remembered numbers too (fixed Nov 6):** it reads `qb-numbers` on load, shows the same "remembered in this browser only. Clear them" note, saves what's typed there, and passes the shown values to Quota Check, so the home page and Quota Check always show the same multiple. Before this, a visitor who had used another tool saw 21× on the home page and 24× after "See the whole plan".
- **Numbers carry between tools.** Base, variable and quota are remembered in the visitor's browser (localStorage key `qb-numbers`) and prefill Quota Check, Quota Case, Pay Check and Offer Check (Offer A). The page says so and offers "Clear them". Nothing is sent anywhere. Fields map through `share` in a tool's config.
- **Optional fields fold away** under "More details" (`more=True` on a field; `head='…'` adds a small section heading). The panel opens itself when a shared link or remembered number fills one of its fields.
- **Shape scale:** small 12px (buttons, fields, answers), medium 16px (cards, panels), large 24px (the verdict card), full (pills and chips).
- **One state system:** hover is a 5% ink layer and press 10% on rows, notes, answers and menu links; solid blue only on real buttons.
- **Focus:** one 2px ink ring on every interactive element, keyboard only; a field row shows the ring around the whole row.
- **Touch targets:** 48px on the controls people tap constantly (answers, chips, segmented switches); 44px minimum elsewhere.
- **Motion:** the verdict "pop" plays only when the verdict changes, and never when the device asks for reduced motion.
- **Type roles:** display 120/96/76/60, headline 44/36/28, title 22/18, body 17, secondary 15, label 13, overline 12. Eleven sizes on a phone, twelve on desktop (was 17). Don't add sizes; map new text to a role.
- **Not done:** trimming tools by usage. It needs the Google Analytics numbers; once known, move the least-used tools out of the menu and home list (`MENU_SKIP`) and keep their pages live.
- **A bug this pass fixed:** the reading-column rule from the redesign had also narrowed the home page's main block to 680px; `.wrap.wide` pages now keep their full width.

## Layout rules (redesign, Nov 3)

Applied from a website-design review: audit first, remove before adding, one edge, rows over boxes.
- **One left edge on every page.** The header, headings and body all start on the same edge (the header container is 920px everywhere; reading text keeps a 680px measure inside it). Check new pages against the logo's edge.
- **Rows, not a box per item.** Tool lists and note lists are rows with a hairline between them: the question on the left, the tool name and an arrow on the right. Keep cards for things that really are separate objects: the verdict card, the pillar steps, the Shorts, the kit card.
- **The home page shows six Field Notes** (`HOME_NOTES` in make-tools.py) and links to the rest with a live count. Don't list every note on the home page again.
- **No reassurance line under the hero button** (Mark removed "Free. No login. What you type stays in your browser." on Nov 3). The FAQ answers what stays in the browser. The old "How these work" section stays cut.
- Result: the home page went from about 6,700px to 4,300px on desktop and from 9,400px to 6,600px on a phone, with nothing a visitor needs removed.

## Two pillars: your number and your pay (Nov 2)

QuotaBird's core is two jobs: **the number they gave you** (Quota Check, Quota Case, Territory, Discount) and **what they'll pay you for it** (the Your pay group). Your pay, first pass:
- **Pay Check** (/pay/): "What does this plan actually pay?" Base, variable, accelerator rate and where it starts, optional cap and threshold. Shows total pay at 50 / 75 / 100 / 125 / 150 / 200% of quota and the extra from 100% to 150%. Uses the `pctx` field type (percentages that can pass 100%: "150%", "150" and "1.5" all mean 1.5); regular `pct` fields still reject 100% and up, which is right for win rates.
- **Commission Check** now takes your share of the credit and a product multiplier (credit = deal × share × multiplier).
- **Comp Plan Check** (/comp-plan/): five questions (credit, payout, upside, clawback, changes). Its "Ask your manager" lines are questions the rep asks, not questions a boss asks the rep.
- Field Notes: **"How to review an offer, and push back on it"** and **"You think the company is shorting you"**.
- **Equity and advice:** stock, RSUs and ESPPs are mentioned, never valued. Every comp page steers clear of financial and legal advice and says so: talk to HR, an employment attorney or a financial professional where it matters.
- Big result numbers stay on one line and shrink to fit their card (`fitBig` in calc.js).
- **Second pass (built Nov 2):** **Offer Check** (/offer/): two offers side by side, year one with the ramp (guarantee if any, otherwise half your normal attainment, an assumption the page states) and a normal year at a realistic attainment; neutral verdicts ("About the same money." / "Offer A pays more in a normal year."); guarantee and attainment fields use `pctx` so 100% works. Field Notes: "How to explain a bad comp plan without losing the room", "How to fight a comp plan before it ships", "OTE is what you make if everything goes right", "Your accelerator only matters if somebody reaches it", "A cap tells you how much upside they're willing to share", "How a $1M deal turns into a small paycheck", "The plan says uncapped. Read the footnotes." The home page now shows both pillars under the hero: "The number they gave you." and "What they'll pay you for it.", three steps each.

## Methodology (/methodology/, Nov 1)

"How QuotaBird's numbers work" is the citable reference for every number on the site. It labels each one as **published data**, a **common rule of thumb**, or a **QuotaBird working range**; shows the quota-to-OTE ranges by basis; derives the run-rate and whole-book ranges from one identity (quota ÷ OTE = variable share ÷ commission rate: with a 46% variable share, about 8 to 12% gives 4 to 6×, 1.5 to 3% gives 15 to 30×, 0.6 to 1.2% gives 40 to 80×); lists every other number's source; gives each tool's formula; says what the site doesn't model; and carries a last-reviewed date (`METHOD_REVIEWED` / `METHOD_DATE` in `make-tools.py`) and Dataset structured data. It is listed first under "Methodology and benchmarks" in llms.txt.
- **When any range, benchmark or formula changes, update the methodology page in the same edit**, and bump the review date.
- **Review schedule:** RepVue Cloud Sales Index each quarter (quote only figures confirmed on RepVue's own page; the index covers software sellers, not cloud-provider consumption sellers); Bridge Group when a new report ships.
- Sources considered and usable: Bridge Group (2026, 2024 with percentiles 3.2 / 4.2 / 4.8×), RepVue (Cloud Sales Index, Sales Salary Guide), QuotaPath (5× observed SaaS standard; 1.5 to 2× accelerators), Gong (attainment from CRM data), Pavilion (leader comp). No public benchmark exists for cloud-provider consumption quotas; Mark chose not to run a survey.
- Fixed Nov 1: three places said consumption is "paid at a fraction of a percent", which contradicts 15 to 30× (it implies about 100×). Consumption is about 1.5 to 3%; whole book about 0.6 to 1.2%.

## Language reps actually use

- **"The gap", never "the bridge."** Reps don't say bridge. The sequence the site follows everywhere: know your quota against your pipeline and ARR, see the gap, then either push back with it (the conversation) or close it with new pipeline from growth in existing accounts and net-new accounts (the plan). Quota Case shows both: the gap, the new pipeline it takes at your win rate, and the words for each conversation.
- Say "run rate or ARR", not just "run rate". *Bridge Group* (the research firm) is the only "bridge" on the site.

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

## Design system (Option A structure + the BOLD colour system, Oct 30, final)

Built from the 2026 palettes Mark supplied (@346eur): flat, confident colour on clean cool whites and blue-blacks.

| Role | Meaning | Light | Dark |
|---|---|---|---|
| **Standard** | defensible, ordinary, okay | Yellow Green `#AAD576` | same `#AAD576` |
| **Caution** | you've got a gap, the situation, a stretch | Corn Yellow `#FCEC60` | same `#FCEC60` |
| **Problem** | unrealistic, crazy | Coral Orange `#FF7F50` | same `#FF7F50` |
| **Action** | only things you tap | Bird blue `#7CC0F5`, black text | the same `#7CC0F5`, black text |
| **Structure** | page / cards / lines | `#FFFFFF` / `#EEF2F8` / `#E2E8F0` | Midnight Abyss `#0B1215` / `#16202A` / `#222E3A` |
| **Text** | everything | `#0B1215`, muted `#4F5B66` | `#F2F6FC`, muted `#A3AFBB` |
| **Brand** | the bird | `#7CC0F5`, ink outline | `#7CC0F5`, outline `#3F77A8` |

**One blue (Nov 2):** the bird, the light-mode button and the dark-mode button are all `#7CC0F5` with black text (9.6:1). The grammar: **black = interface** (selected segment, Tools menu, links), **blue = do something** (buttons and pressed states) **and the bird**, **green / yellow / coral = QuotaBird's answer**. Blue is used nowhere else. The dark-mode bird outline is `#3F77A8` (4.0:1 against the page so the beak stays crisp, 2.4:1 against the body so it reads as a line).

**Rules:**
1. **Verdict cards are bold stickers: the same colour in light and dark, always with black text** (7.6 to 15.6:1). They never darken, so dark mode never turns yellow into brown.
2. **Colour appears on the answer card only.** Everything else is structure; blue is only for things you tap.
3. **Verdict words are always black**, large and heavy; the card colour carries the meaning.
4. Three bands, not four (`--v-orange` = Caution).

**Verdict wording:** see *Voice in results* below; every verdict is an answer to its tool's question. Quota Case's middle verdict is **"You've got a gap."** (the sticky bar shortens it to "$2.6M gap"); the explanation and next steps go in the text below it, never in the label. Avoid homework phrasing like "Gap to explain" or "Needs a bridge".

**Type: chunky.** Inter. Headings weight 900, tight tracking (-.045em). Home headline 44px on phones, 76px on desktop. The answer number 96px on phones (scales down to 58px on 320px screens so "$2.6M" never overflows), 120px on the desktop home. Verdict words in sentence case, never capitals ("The situation", "At risk").

**Components (standard, modern):**
- Buttons: 14px corners, 54px tall for the main action. Secondary actions are grey, or an underlined text link on the booking card.
- Segmented control (iOS style): grey track, black selected segment, no check. Used for *Bookings / Run rate / Whole book* (the label is "Run rate", not "Cloud growth"). Pipeline Check's preset rows (win rate, year end) use it too, sized to their text. Win-rate presets are 20% / 25% / 33% (33% is the 3X assumption, which the result line explains); the year-end row is only Dec 31 / Sep 30 (the old "Just me" button was removed Nov 5: it duplicated typing 1 in Sellers and looked like a third year-end option).
- Inputs are grouped rows: label left, number right, in one grey panel with hairline dividers. Number fields keep at least 128px; long labels wrap. Where preset buttons interrupt a list, each panel keeps rounded corners.
- Cards: grey, 16px corners. The checks are plain cards: the question in bold, the tool name and an arrow underneath. Pressing a card turns it blue.
- Links: underlined only inside sentences. Buttons and whole-card links are never underlined.
- Focus: a 2px ink ring for keyboard focus only; headings and verdicts moved into view for screen readers show no ring.

**The bird:** Mark's fainter bluebird, `#9DD2FF` with an ink outline and eye. In dark mode the outline is medium blue `#4F86B5` (4.9:1 against the page, so the beak and wing line stay crisp); a light rim looked like a sticker, a deep blue lost the beak, a soft blue blurred into the body. The 404 bird has an X eye.

**The system lives in the "OPTION A" block at the end of `site.css`** and the small fix-ups after it, which win over everything above. Older palette blocks above it are dead weight and can be pruned once this has been live for a while.

## Pages

**Home:** "The quota landed / Is your quota crazy? / Maybe. Let's do the math." then the live mini Quota Check: the answer card (big number on its verdict tint), the segmented control, the grouped input rows (pre-filled grey examples), and "See the whole plan" (blue), which hands typed numbers to /quota/. On desktop the inputs sit left and the answer right. Then "Push back or build a plan." over three paths, the Quota Shorts strip (grey cards, big numbers), and under "The quota isn't the only problem." the checks as plain grey cards grouped like the Tools menu: Your number, Your team, Your deal, Any meeting, and Print and learn (Field Kits, Sales Math). Quota Check itself isn't listed on the home page (the hero is Quota Check); the 404 page copies the same block and adds it. The hero's thresholds must match Quota Check's.

**The 18 tools:**

| URL | Tool | Kind | Headline |
|---|---|---|---|
| /quota/ | Quota Check | calculator | Is my quota crazy? |
| /commit/ | Commit Check | calculator | Will they burn the commit? (committed spend vs consumption: pace, monthly spend needed, shortfall or overage) |
| /quota-case/ | Quota Case | calculator | Is your quota actually possible? (the gap, and the pipeline that closes it) |
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

**Field Kits (rebuilt Oct 30): every kit leads with the number**, because that's why people come to QuotaBird. Printed from their pages to Letter and A4 with `node kitpdf.js` (local server running); re-check page counts after any kit copy change and set `SELLER_PAGES`, `KIT_PAGES`, `LEADER_PAGES` in `make-tools.py` and the `pages` map in `make-card.py`.
- **Seller's Kit (8 pages, 12 chapters, 9 worksheets).** Opens with *Your number*: 1. Where your quota came from (prior year revenue plus a growth rate, set above the geo VP at AWS; over-assignment; bookings vs ARR/MRR vs consumption vs whole book; reading the comp plan: OTE, split, rate, accelerators, caps, crediting; what to ask for this week). 2. Is your quota crazy? Check it, then decide (quota ÷ OTE; the gap from PYR minus one-time revenue, run rate, committed contracts, pipeline × win rate; what can move and what can't; one ask; the script; when to accept). 3. It's a tough number. Crush it anyway (gap ÷ win rate = new pipeline; existing-account growth vs net-new with names; front-load, since a March workload runs ten months and an October one three). Then the eight deal chapters (4 to 11).
- **Manager's Kit (11 pages, 13 chapters, 9 worksheets).** Opens with 1. How your team's number got built (and what your boss is actually paid on: growth rate, new business, new logos, consumption, margin). 2. Fighting the plan without losing (early, one page, one ask for what can move; escalate once; commit publicly; know when to stop). 3. Handing down a tough number, and still crushing it. Then the original ten chapters (4 to 13). The *Having a bad week?* index points Where the number came from, Quota or comp plan problem, and Handing down a tough number at 1 to 3.
- **Leadership Kit (3 pages, 7 chapters, 2 worksheets and a checklist).** Opens with 1. Shape the number before it shapes your team (plan from a clean baseline and capacity, choose over-assignment on purpose, get into the planning room, know what the people above you are paid on).
- **The through-line in all three:** "The best time to shape your quota was last year. The next best time is now." Push back with data (PYR, run rate, committed contracts, pipeline × win rate), know when to accept, then fill the gap from existing accounts and net-new. Kits stay in Mark's first person; they're signed.

**About photo:** the text wraps around the round photo itself (`shape-outside: circle()` on `.who img`), not its square box.

**Also:** Sales Math (4 pages), About (opens on Mark's photo and "Hi, I'm Mark."), Ask Mark ("Got a quota problem?"), Stuff I Like (Mark edits this page's wording himself; carry his changes into the `_stuff` article in make-tools.py, never paste a built page over the site), 404 (shows the shelf).

## Funnel and analytics

Every result: verdict → what to fix → (Pressure test, tonal) → Mark's card (filled "Grab 20 minutes" to Calendly with the verdict pre-filled; tonal "DM me on LinkedIn" copies a note) → next-step card → fedhoo line (federal-relevant weak answers only) → Share · Start over.

GA4 `G-BG9NR9GXQZ` via `analytics.js` (`window.qbTrack`). Events: `hero_calc_edit`, `hero_calc_go`, `front_pick`, `<slug>_start`, `verdict`, `<slug>_book` (Deal: `book`), `<slug>_book_after_grill`, `<slug>_dm_copy`, `<slug>_share`, `<slug>_edit`, `ask_book`, `kit_download` / `seller_download` / `leader_download`, `<slug>_fedhoo`, `related_tool_click`.

Calendly: calendly.com/markflournoy/chat-with-mark (utm_source=quotabird, utm_medium=<page>). Email mark@quotabird.com. LinkedIn linkedin.com/in/markflournoy/.

## Navigation

Header: Tools ▾ · Field Kits · Field Notes · About · Ask Mark. Don't add to it. In the Tools menu, four groups sit two by two: Your number over Your pay on the left, Your deal over Your team on the right (about 590px open on a phone, 44px tap targets). Brief Check is deliberately left out of the menu (Mark's call, Nov 3: not important enough for the menu); it stays on the home page tool list, at /brief/, and in the plugin. To leave another tool out of the menu, add its path to `MENU_SKIP` in `menu()`. The Tools menu leads with Your number (Quota Check, Quota Case, Territory, Commission, Discount), then Your team, Your deal, Any meeting. Footer: "QuotaBird is a pile of free sales tools. I built them because they helped me, and maybe they'll help you." and "Not affiliated with the U.S. government or Amazon."

## Build and deploy

- **Edit:** `make-tools.py` (every generated page), `home.src.html`, `pipeline.src.html`, `deal/index.html`, `check.js`, `calc.js`, `analytics.js`, `site.css`, `partials/*.html`, `404.html`, `make-card.py`, `make-social.py`.
- **Never edit by hand:** built `index.html` files, `sitemap.xml`, `llms.txt`, `ai-catalog.json`, the fingerprinted `site.<hash>.css` / `check.<hash>.js` / `calc.<hash>.js` / `analytics.<hash>.js`, `card*.jpg`.
- **Build:** `python3 make-tools.py` (pages, sitemap, llms.txt, ai-catalog, fingerprints). Share cards: `python3 make-card.py <slug|home|banner|seller|kit|leader>`, then rebuild. Each card is the tool's question as a chunky headline beside a result card in its verdict tint, using the page's real default answer (calculators) or a real verdict word (question tools); the list is `RESULTS` in `make-card.py`, so update it if a default changes. The banner keeps its text clear of the lower-left, where LinkedIn places the profile photo. Kit PDFs: start the local server, then `node kitpdf.js` (saved with the build tools); re-check 4 / 8 / 3 pages afterwards. Social images: `python3 make-social.py`. Copy workbook: `python3 extract-copy.py`.
- **Deploy:** AWS Amplify from GitHub. `customHttp.yml` caches css/js for a year (safe: names change with content) and html not at all. Rewrites in `amplify-rewrites.json` (45 rules, 404 catch-all last); every new page needs a `/<slug>` → `/<slug>/` rule. Never edit the live site directly.

## Data (researched Sept 27, 2026; refresh yearly)

Bridge Group 2026 (158 B2B companies): 48% of AEs at 100%+ (51% in 2024, 66% in 2022); median quota $960K on $200K OTE, 4.6× (4.2× in 2024); quotas +2.4%/yr vs OTE +4.9%/yr; ramp 6.2 months. Bridge 2024: 53:47 mix. RepVue (self-reported, Sept 2026): 42% of AEs reach quota, enterprise 41%, federal 46%, SLED 45%; Cloud Sales Index Q2 2025 average attainment 42.7% (246 companies); AWS Account Manager $150K base / $280K OTE / 54:46 / 64% hit; Microsoft Enterprise AE 56%, SLED AE 67%. Mostly Metrics: over-assignment 20-30%. Accelerators 1.5-2× (comp surveys). Microsoft fiscal year July-June; Microsoft field incentives tied to Azure consumed revenue (Microsoft Learn). Keep "share of reps at 100%" and "average attainment" separate.

## Already decided (don't re-propose)

- **The look is Option A with the BOLD colour system** (above, Oct 30). Tried and dropped along the way: pale kiwi/sunshine/tomato tints, dusty coral, brick, ochre, sage caution, deep dark-mode verdict cards (always drifted brown), and coloured verdict words. Tried and dropped before it: raven, yellow canary, dusty blue and purple birds; warm-ink, bone-and-slate, mustard/Material, six-colour, rainbow-shelf, colourless-shelf, M3 purple and teal, retro-sunset, palette B, oat milk, the Swiss "mood and trope" cover palette, colour-coded groups (dots, switches, shapes and badges), Monocle-style rules, the iPhone-primary palette, Google Sans Flex, the highlighter, editorial charts, the bookshelf. Mark's words at the end: "I just want a modern site with modern UI elements and chunky hero text and numbers." Keep it that simple.
- **No decorative systems:** no badges, switches, filter chips or colour codes on the checks. Grouping is done with quiet grey labels.
- **Switches mean on/off only.** Never use one as decoration.
- **Copy:** the "kill" language is gone except one line of Mark's on About; don't add more.

## Pending (Mark)

Redo the social collateral (post images, carousel, email signature) in Option A; `make-social.py` still draws the old bookshelf covers, so those files are not in the latest package. Replace `mark.jpg` (background-removal artifacts; it sits beside the booking button). Set prices for Wingman and Team session. Calendly: 20-minute event, one intake question, no marketing emails. Submit the sitemap in Search Console. Post the Field Notes; write new notes before new tools (queue: The best quota fight happens before January · Show me where the gap closes · If only 20% of the team hits quota, maybe the reps aren't the problem · Your boss may not be goaled on your quota · When a tough quota is still a fair quota · One giant deal made last year's number · New reps don't produce twelve months of revenue in six months · A vacant territory still has quota · Stop using 3X pipeline if your win rate is 18%).
