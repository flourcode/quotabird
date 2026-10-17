// QuotaBird playbooks: how Mark thinks through a problem. Plain text, sent to the model only when the
// question needs them (see pickPlaybooks in quotabird.mjs). Distilled from the QuotaBird tools, the
// Field Kits, the Field Notes and the useful parts of AskArti. Not a textbook: judgment, in the order
// Mark would actually run it. Ten playbooks. Don't add more until these are good.

export const PLAYBOOKS = {
  deal: `DEAL

A real deal needs five things: customer, money, power, path, now.

Customer: have they actually said they want to solve this, in their words? Not "they liked the demo". Said it.
Money: do we know where the money comes from? Which pot, which year, is it on a line. "They have budget" from a champion is a rumor until somebody who owns the money says it.
Power: are we talking to somebody who can move the decision, and do we know who signs? Your champion liking you is not power.
Path: do we know how the customer can buy it? Vehicle, reseller, prime, marketplace, existing order. If nobody can name the path, there isn't one yet.
Now: what forces action in this period? A date, a mandate, an expiring contract, an end of life, a budget year. No forcing event, no close date.

Money and power are where a manager attacks first. If either is a flat no, the deal is capped at hopium no matter how good the rest looks.

The seller's activity is not customer progress. Meetings aren't progress. Emails aren't progress. A nice champion isn't progress. A proposal isn't progress unless the customer did something that required it. Ask what the customer has done, not what the seller has done.

When a deal stalls: work out what changed before doing anything. Does it still map to the buyer's current priority? Where does it sit in their decision path, and who owns the next step? Don't send another checking-in email. Bring something new. Escalate only with a stated purpose. Ask for the smallest useful next commitment, with an owner on their side and a date.

Champion versus coach: a champion spends their own credibility for you; a coach just tells you things. Arm a champion with a short, forwardable summary and the answers to the objections they'll hear inside.

Doing nothing is always a competitor, and it wins more deals than anyone.

Commit means you'd bet your own money on it. Real and committed are different words.`,

  meeting: `MEETING PREP

Start with the outcome. What does the seller need the customer to do next, not what the seller wants to say. A meeting objective that isn't a customer action ("build the relationship", "share our roadmap") is a visit.

Separate what the seller knows (they told you, or the customer said it) from what they're assuming. Say which is which.

Check: who in the room can move the outcome; what the customer is trying to get done this year; what happens if they do nothing; who else has to agree; how they would buy; what could kill the meeting; what objection the seller hopes nobody raises; whether the ask fits this stage.

A first meeting earns one small, specific commitment: an introduction, a scoped follow-up, a date. Not a signed plan, not a budget.

Don't waste meeting time on things the seller should have looked up: the strategic plan, the budget justification, who holds the contracts, the last buy.

Questions worth asking are the ones only the customer can answer: what happens if nothing changes, who else has to say yes, how they bought the last thing like this, what has to be true by when.

Landmines: the thing not to say, the person in the room who loses if you win, the incumbent's friend, the old project that failed.

An executive meeting needs: who they're meeting, what that person probably cares about, the opportunity, the one ask, and what not to say. Senior people give you minutes, not an hour.

A good meeting ends with one next move owned by someone on the customer side, with a date. Same day, send a short note they could forward without editing.

For federal meetings, keep separate: mission owner, program office, contracting path, money, incumbent, vehicle. Never invent any of those.`,

  account: `ACCOUNT

An account plan is worth having when it has a number on it and names attached. Everything else is a brochure about the customer.

Pressure-test these, in order: mission (what they're trying to get done this year, in their words); money (where it comes from, when it moves, on their fiscal year not yours); power (who matters beyond the seller's one contact); incumbent (who owns the relationships, the contracts and the workloads today, and what they'd lose); buying path (how this account actually buys, and who runs it); current business (what they buy now and whether it's growing); whitespace (what else they buy that you could be selling); relationships (how many threads, really); pipeline (named deals, values, stages, dates); next people to meet (and who introduces you).

Single-threaded is the most common way a good account goes quiet. One promotion or one reorg and the seller starts over. Every plan names the next two people to meet.

Coverage for an account follows the pipeline rule: what's left of the number divided by the win rate is the pipeline it takes. The gap closes from growth in what they already buy and from new places in the account, with names.

If the seller supplied half the information, say what's missing instead of writing around it. "You don't know where the money comes from yet. That's the first hole." A plan with holes named is more useful than a plan that looks complete.

Research the seller should do, not the model: for a company, the annual report or 10-K; for an agency, the strategic plan, the budget justification, award history on USAspending, the AI use case inventory. Use it to ask better questions, not to pretend you know what's inside.`,

  pipeline: `PIPELINE

The pipeline you need is what's left of the target divided by your real win rate. 3X is a 33 percent win rate in disguise. At 20 percent you need 5X. At 18 percent, 3X is a quarter you'll spend explaining.

Qualified pipeline only, at full value. Weighted pipeline is only as good as the weights, and most CRM stage probabilities were typed in once and never checked.

Concentration: when one or two deals carry the period, ask what happens if the biggest one slips. If the answer is "then I miss", that's the forecast, not the deal.

Pipeline theater: lots of stages moving, nothing closing. Ask what the customer did this week on each deal in commit. If the answer is what the seller did, the stage is wrong.

Short on pipeline late in the period usually can't be closed in one period. Say it early, in dollars, and ask whether the number or the plan has to change. "Prospect harder" is not a plan; a named list of where the next pipeline comes from is.

On a consumption commit: the number that matters is the monthly spend it takes from here versus today's pace. New workloads with dates close a shortfall. A more hopeful forecast doesn't. Running over the commit is the time to start the next commit conversation, not the renewal.

The model never does this arithmetic. Pipeline Check and Commit Check do. Point there.`,

  federal: `FEDERAL

The year: October 1 to September 30. Heavy buying July through September, but the contracting office's own cutoff, often weeks before September 30, is the real date. Work back from it. Early in the year a continuing resolution usually holds funding at last year's level and blocks new starts.

Money: Congress appropriates to programs. In defense the type of money (O&M, procurement, RDT&E) decides what it can buy, and one-year money expires. "They like it" is not "there's money on a line for it". Ask which line, which year, who owns it.

People: the requirement comes from the mission or program owner. Only a contracting officer can obligate funds. Don't pitch the CO. Make the buy easy and compliant for the CO. The CO isn't against you; the CO may have no way to buy you.

Path: an existing vehicle the customer already uses (GSA MAS, NASA SEWP, an agency IDIQ or BPA), a prime or reseller who holds one (Carahsoft is the big distributor in federal), a cloud marketplace private offer (useful when the customer has a committed cloud agreement it can draw down). Not being on a vehicle the customer uses is a real hole. A partner who is on one fixes it faster than you can.

Authorization gates for cloud and SaaS: FedRAMP (Moderate for most civilian work, High for the sensitive stuff) and DoD impact levels (IL2, IL4, IL5, IL6) decide what a product is even allowed to hold. No authorization, no deal, only a timeline. The rules keep changing; tell people to check the current ones.

Primes and integrators: the executive cares about winning the next contract and delivering the current one on cost, schedule and performance. Pitch the division, not the parent company. Workshare promises mean nothing until they're in writing.

Small business and startups: the whole game is getting on paper somebody can buy from. Set-asides (8(a), SDVOSB, HUBZone) are a door, not a deal.

Senior leaders (SES, general and flag officers) give you minutes. Lead with mission in one minute, then be ready for their three questions.

Rules worth naming as things to check, not to explain: CMMC for defense contractors handling CUI, Section 889, TAA on GSA.

Public sources, for the seller to read: SAM.gov, USAspending.gov, the agency strategic plan and budget justification, a command's posture statement, the agency AI use case inventory. Use them to ask better questions. Never present what's in them as what's inside the agency today.`,

  partner: `PARTNER

A real partner has named deals, named people and a pipeline you can both see. Everything else is a logo swap.

Where the deal flows and who gets paid: agency to prime to reseller to cloud provider to ISV. Everyone in the chain needs a reason. The cloud provider's partner team is measured on partner-sourced and partner-influenced consumption on their cloud. The reseller wants margin and a clean transaction. The prime wants to win and deliver its contract. An ISV that shows up with real deals gets help. One that shows up with a pitch gets a nice meeting.

Co-sell with a cloud provider works when there's a named account, a named account manager on their side, a registered opportunity, and something in it for their number. Without those four, co-sell is a slide.

Testing a partner: give them one account and one ask with a date. "Can you introduce me to the AM covering VA by Friday? We have an active opportunity around X." If that doesn't move after two tries, spend the time somewhere else.

Partner managers: inspect the joint pipeline by deal, not by partner. Which deals did the partner source, which did they touch, which did they just register. Output-based incentives beat activity-based ones. Monthly inspection, not quarterly surprises.

A prime that won't commit workshare in writing isn't teaming with you, it's keeping you warm.`,

  update: `UPDATE UPWARD

An update your boss can use leads with the number and your call in one line, then the top three deals with what's next on each, then what's in the way with the exact thing you need from them. One page. No adjectives standing in for numbers.

Calling a miss: early, in dollars, before your boss's own forecast call. A miss called in week six is a problem you solve together. A miss they find out about in week twelve is a problem with you. Separate what you controlled from what you didn't. Say what you've already tried. Give the recovery plan and what next period looks like. Make one specific ask.

Forecast call: say what's real and what's hope. Commit means you'd bet your own money on it. Don't put a deal in commit to make the call go better.

Monthly review: results against the number, what went right and wrong, pipeline risk with the deals named, and no more than three asks, each tied to revenue.

Your boss will ask: what changed since last time, what's your worst case, what would it take to close the gap, what's in commit that shouldn't be. Have the answers before the call.

Managing up is clarity before they ask, and a clean specific ask when you need something. Not more updates. Better ones.

Numbers in an update come from the seller or from the calculators. The model never computes them.`,

  manager: `MANAGER

Rep or territory: look at the territory before the person. If three people failed in the same territory, it's the territory. Separate a skill gap from an effort gap from a territory that can't produce the number. Then act on the one it actually is.

A struggling rep: if they haven't asked for help, don't swoop. Ask what the customer has done on each of their top deals. Activity reports tell you about the rep. Customer actions tell you about the deals.

Talent review: the case for a rating survives the room when it has receipts (numbers, examples, scope) and the manager can say what the person owns. Adjectives don't survive calibration.

Handing down a tough number: you can say you pushed back. Say what you got. Then the number is the number, and you stop relitigating it in team meetings. Help the team build the plan: the gap, the pipeline it takes at the real win rate, where it comes from, with names.

When the manager is probably right: say so to the seller. Managers are wrong about plenty, but "my manager wants it in commit" is not evidence the deal is real, and "my manager says the number is the number" is usually just true.

High performers who hate meetings are usually telling you the meetings are bad.

A commit review is an inspection, not a performance. The question is "what did the customer do this week", asked the same way every week.`,

  territory: `TERRITORY

A territory can support a number when there's enough spend in your category, enough accounts you can actually reach, an installed base to grow, access to the people who buy, and history that says it has produced before. Missing two of those and the number is a hope.

A quota went up and the territory didn't change: ask what else changed. New product, new partner help, a big renewal nobody mentioned. If nothing, the growth is coming from a spreadsheet, and the seller should say so with the math, once, early, in writing.

Vacant territories still carry quota, and a rep hired in March doesn't sell much until summer. Count ramped reps, not hired ones.

A seller blaming the territory is sometimes right. Check: did the last two people in it make the number? Is the installed base growing or shrinking? Are the accounts reachable? If the territory produced for the last person and not this one, it's not the territory.

The first month in a new territory: find the installed base, find who already owns the relationships, find the one or two accounts where the money moves this year, and ignore the rest until those are worked.`,

  competition: `COMPETITION

Doing nothing beats more deals than any competitor. Before worrying about the other vendor, ask what forces the customer to act at all.

The incumbent owns the relationships, the contracts and the workloads today, and has a friend in the room. Know who the friend is and what the incumbent loses if you win.

"They prefer us" from a champion is not a position. A position is: the customer has said what the incumbent isn't doing, you can do that thing, and somebody with power agrees it matters this year.

Why you and not them is a question the customer answers, not the seller. If the seller can't repeat what the customer said about why, the seller doesn't know.

Being behind: find out what the decision is really about and whether it's already made. If the evaluation criteria were written for the incumbent, the deal is a reference, not an opportunity. Don't spend a quarter on it.

Competing on price alone is a sign the customer never heard a reason to choose you. A discount is a purchase; the question is what you got for it.`,

  boss: `YOUR BOSS (managing up)

Your boss usually isn't the enemy. Most of the time they're getting grilled by their own boss on a number they don't control either. Work out what they're being asked for, and hand them that before they ask.

A boss who tears into your deals on the forecast call usually doesn't trust the forecast. Bring the ugly deals yourself, before the call, with what the customer has and hasn't done on each. Surprises are what make managers mean.

One-on-ones that are all about what you haven't done: change the agenda. Walk in with your top deals, the customer's next action on each, and one ask. Ten minutes of that beats an hour of being inspected.

A boss who wants a deal in commit you don't believe: don't fight about the label, fight about the evidence. Say what you'd need to see to call it commit and the date you'll know. Put that in writing.

When your boss is wrong: say it once, privately, with numbers, and ask what you're missing. If they've got something you don't, fine. If not, you've made the case. Don't relitigate it in team meetings.

When it's personal or political (favorites, taking credit, a territory moved out from under you): keep your numbers clean and in writing, and be honest about the options: talk it out, a skip-level, a different team, a different company. Say the trade-off of each plainly. No legal or HR advice; say who to talk to.

Asking for help: one specific ask, tied to a deal, with a date. "Can you call their CIO before the 15th" gets done. "I need exec support" doesn't.

Sometimes the boss is right. If the seller is describing a fair point delivered badly, say so.`,

  quota: `QUOTA

Start with what the number is actually measured on. Bookings, consumption growth and a whole book are different animals, and the right argument depends on which one it is.

A quota is defensible when the territory, installed base, pipeline, headcount and growth assumptions can plausibly produce it. When they can't, somebody made it in a spreadsheet.

When a seller wants to push back, don't argue fairness. Bring last year's clean number with the one-time deals taken out, the current run rate, qualified pipeline at the real win rate, what changed in the territory, and ramped headcount if there's a team. Then ask one question: what assumption am I missing?

If management has a legitimate assumption you didn't have, fine. If not, you've made the case.

Make the argument once, early and with numbers, in writing. Then either escalate it or build the plan. Spending six months being right about a bad quota doesn't help you make it.

A quota that went up and a territory that didn't change: ask what else changed. New product, new partner help, a renewal nobody mentioned. If nothing, say so with the math.

The arithmetic belongs to Quota Check and Quota Case, not to you. Point there.`,

  pay: `COMPENSATION

Start with what the plan actually pays at realistic attainment, not the OTE printed on the offer. OTE is a story about 100 percent; most sellers don't live there.

Read the crediting rules first: who gets credit for a renewal, an expansion, a partner-sourced deal, a multi-year. Then thresholds, accelerators, caps, splits, clawbacks, payout timing, and whether the company can change the plan after the year starts.

An accelerator only matters if you can realistically reach it. A cap tells you exactly how much upside the company is willing to share. Credit moved to somebody else is a pay cut with a new name.

An offer against the job they have: compare a normal year at a realistic attainment for each (they know what they hit now; the new number is a guess, so guess low), then year one with the ramp, any guarantee or sign-on, and what they'd leave behind (unpaid commission, a bonus, stock vesting soon). Then the month they'd catch up. The bigger OTE loses more often than people expect, and the money rarely decides a good move alone: the territory, the manager and the quota do. Offer Check runs it.

A discount isn't free. It usually costs company margin and seller commission. The question is what you got in return, and whether you'd have won without it.

No tax or legal advice. Tell them what to verify with payroll, HR or a tax professional, and to get the plan document in writing before they sign anything.

The arithmetic belongs to Pay Check, Offer Check, Commission Check and Discount Check. Point there.`,
};

// Which playbooks a question probably needs, by words in it. Cheap on purpose; the chat gets the matches
// plus deal, because almost everything is a deal underneath. Nothing is sent that doesn't match.
const CUES = {
  deal: /\b(deal|commit|close|closing|champion|stalled|stuck|propos|poc|pilot|evaluation|decision|sign)/i,
  meeting: /\b(meeting|meet|call with|qbr|brief|deck|presentation|demo|room|agenda|exec)/i,
  account: /\b(account|customer|single.?thread|incumbent|whitespace|renewal|relationship)/i,
  pipeline: /\b(pipeline|coverage|forecast|3x|win rate|number|burn|consumption|commit|gap|quarter|target)/i,
  federal: /\b(federal|agency|government|gov\b|dod|army|navy|air force|marine|dha|va\b|dhs|hhs|faa|dot\b|treasury|irs|nasa|disa|contracting|co\b|cor\b|vehicle|sewp|gsa|idiq|bpa|fedramp|il[2456]\b|appropriat|continuing resolution|sept(ember)? 30|fiscal|prime|integrator|8\(a\)|set.?aside|sam\.gov|usaspending|rfp|rfi|recompete)/i,
  partner: /\b(partner|prime|reseller|distributor|carahsoft|var\b|isv|co.?sell|marketplace|teaming|sub\b|subcontract|workshare|channel|alliance|aws|amazon|azure|google cloud|gcp)/i,
  update: /\b(boss|manager wants|vp wants|my vp|update|forecast call|miss|missing the number|monthly review|mbr|tell my|report)/i,
  manager: /\b(my reps?\b|my team|my sellers|i manage|as a (sales )?manager|new (sales )?manager|first.line|managing (a|my|the) team|my (direct|report)s?\b|coach(ing)? (my|a|the) (rep|team|seller)|talent review|calibration|olr|performance (review|plan|improvement)|pip\b|one.on.one|hand(ing)? (it |the number |quota )?down|underperform|low performer|top performer)/i,
  territory: /\b(territory|patch|accounts? list|installed base|new rep|ramp)/i,
  competition: /\b(compet|incumbent|rival|versus|vs\.?|instead of us|they prefer|evaluation criteria|price war|discount)/i,
  boss: /\b(boss|my manager|my vp|my director|my svp|skip.level|micromanag|hates me|one.on.ones?|in front of (everybody|everyone|the team)|takes? credit|favou?rites?|managing up|manage up|performance plan|fire me|let me go)/i,
  quota: /\b(quota|my number|number went up|number is|attainment|plan is|assigned|unreasonable|fair number|make the number|against plan|% of plan|percent of plan)/i,
  pay: /\b(comp\b|comp plan|compensation|commission|ote\b|on.target|accelerator|decelerator|clawback|payout|crediting|credit (for|on) (the )?(renewals?|expansions?|partner|multi.?year)|cap(ped)? at|base salary|salary|offer|offers|draw\b|guarantee|spiff|discount|margin|paid on|get paid|pay me|my pay)/i,
};

// Hits are ranked by how many cue words matched, so the subject the person said the most about
// survives the cap. The cap is five; the playbooks are short enough that the extra one is cheap.
export function pickPlaybooks(text, { always = [], federal = null, max = 5 } = {}) {
  const t = String(text || "");
  const count = (re) => (t.match(new RegExp(re.source, "gi")) || []).length;
  const hits = Object.keys(PLAYBOOKS).map((k) => [k, CUES[k] ? count(CUES[k]) : 0]).filter(([, n]) => n > 0)
    .sort((a, b) => b[1] - a[1]).map(([k]) => k);
  let keys = [...new Set([...always, ...hits])];
  if (federal === false) keys = keys.filter((k) => k !== "federal");
  if (federal === true) keys = [...new Set([...always, "federal", ...keys])];
  return keys.slice(0, max);
}

export const playbookText = (keys) => keys.map((k) => PLAYBOOKS[k]).filter(Boolean).join("\n\n");
