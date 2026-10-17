// The QuotaBird evaluation set: eighteen realistic situations run through the real Lambda code against the
// real Gemini API, so a before/after or a model comparison uses the same questions every time.
//
//   GEMINI_API_KEY=... node tests/eval-set.mjs                          # the model in GEMINI_MODEL
//   GEMINI_API_KEY=... QB_GEMINI_MODEL=gemini-3.5-flash node tests/eval-set.mjs   # QuotaBird on a stronger model
//   ... --out eval-flash.md                                             # write the answers to a file
//
// Score each answer 1 to 5 on: sounds like Mark; doesn't sugarcoat (bad news first, no cushion, no pep talk); identifies the real issue; specific next action; avoids
// invented facts; avoids consultant language; avoids generic coaching; willing to disagree with the seller;
// concise enough to feel conversational. Don't reward length. The scoring sheet is printed at the end.
//
// Nothing here is stored by the Lambda; this script writes only what you ask it to with --out.

import fs from "node:fs";
if (!process.env.GEMINI_API_KEY) { console.error("Set GEMINI_API_KEY (and optionally QB_GEMINI_MODEL)."); process.exit(2); }
process.env.ALLOWED_ORIGINS = process.env.ALLOWED_ORIGINS || "*";
process.env.QB_RATE_LIMIT_PER_MINUTE = "1000"; process.env.QB_RATE_LIMIT_PER_HOUR = "10000";
const { handler } = await import(process.env.QB_LAMBDA || "../lambda/index.mjs");

export const CASES = [
  ["quota pushback", "qb_mark", { messages: [{ role: "user", text: "My VP says I need 3X pipeline but my win rate is 18%. Am I being unreasonable pushing back?" }] }],
  ["thin pipeline", "qb_mark", { messages: [{ role: "user", text: "It's April. My number is $4M, I've closed $600K, and I've got about $3M of qualified pipeline. I win maybe one in four. My manager says I'm fine because I'm over 2X on what's left. Am I fine?" }] }],
  ["one huge deal carrying the quarter", "qb_mark", { messages: [{ role: "user", text: "One deal is 70% of my Q4 commit. It's a $1.8M Army cloud migration through a prime. The PM loves it, the prime says it's in their plan, and the money is supposedly FY27. Should I keep it in commit?" }] }],
  ["fake partner activity", "qb_mark", { messages: [{ role: "user", text: "My partner keeps saying they'll introduce me to the account team but nothing happens. We've been 'partners' for eight months." }] }],
  ["stalled federal procurement", "qb_mark", { messages: [{ role: "user", text: "The program office at DHS picked us in June. The RFQ was supposed to go out in August. It's October and the CO says it's 'in review'. My champion says be patient. What do I actually do?" }] }],
  ["weak champion", "qb_mark", { messages: [{ role: "user", text: "My champion says this is going to close but procurement hasn't engaged. She's a branch chief. Is that enough?" }] }],
  ["executive meeting prep", "qb_meeting_prep", { situation: "Thursday I have 30 minutes with the deputy CIO at HHS and her program manager about our analytics platform. They liked the demo last month. I want them to agree to a pilot with the claims team. The incumbent has been in there six years and I think their rep is friends with the PM." }],
  ["single-threaded account", "qb_account_plan", { situation: "VA is my biggest account, $2M number this year. We sell a data platform to the claims office through Carahsoft. I know the program manager really well and nobody above her. The renewal is in August and there's a $750K claims modernization deal I think closes in March." }],
  ["seller blaming territory", "qb_mark", { messages: [{ role: "user", text: "I got handed a territory in January that two people failed in before me. Mostly small civilian agencies, no installed base. My manager says it's a fair number. I think the territory can't make it. How do I make that case without sounding like I'm making excuses?" }] }],
  ["manager probably right", "qb_mark", { messages: [{ role: "user", text: "My manager pulled my biggest deal out of commit because 'the customer hasn't done anything'. But I've had six meetings with them and they love us. He's wrong, right?" }] }],
  ["comp plan problem", "qb_mark", { messages: [{ role: "user", text: "New comp plan has a 2x accelerator above 100% but a cap at 150%, and they moved credit for renewals to the account manager. My OTE is $240K. Is this a bad plan or am I just annoyed?" }] }],
  ["calling a miss", "qb_update_upward", { type: "miss", situation: "$3M number for the half, $1.2M closed, and it's six weeks out. Northwind ($1.2M) is stuck in their legal for three weeks, Contoso ($650K) has a proposal out with a pricing review next week. I'll probably land around $2.6M. I need my VP to get on a call with Northwind's general counsel." }],
  ["federal startup without a vehicle", "qb_mark", { messages: [{ role: "user", text: "We're a Series A SaaS company. A CISO at a civilian agency wants our tool and says he has money this year. We're not on any contract vehicle and we don't have FedRAMP. It's July. Is there a way to get this done before September 30?" }] }],
  ["prime promising workshare", "qb_mark", { messages: [{ role: "user", text: "We're an 8(a). A big prime wants us as a sub on an Air Force recompete. They keep saying 'meaningful workshare' but won't put a number on it, and the incumbent has been there eight years. Worth our time?" }] }],
  ["boss wants it in commit", "qb_mark", { messages: [{ role: "user", text: "My boss wants me to put a $900K deal in commit for the quarter. The customer hasn't started procurement and I don't believe it closes. What do I do?" }] }],
  ["boss takes credit", "qb_mark", { messages: [{ role: "user", text: "My VP takes credit for my deals in the QBR and my one-on-ones keep getting cancelled. I'm at 110% of plan. Do I say something or just leave?" }] }],
  ["fishing for reassurance", "qb_mark", { messages: [{ role: "user", text: "I'm at 40% of my number with two months left, but I've got one big deal that could come in. I can still make it, right?" }] }],
  ["customer taking meetings but not advancing", "qb_mark", { messages: [{ role: "user", text: "I've had four meetings with this customer and they're still interested." }] }],
];

const ev = (body) => ({ headers: { origin: "https://quotabird.com" }, requestContext: { http: { method: "POST", sourceIp: "127.0.0.1" } }, body: JSON.stringify(body) });
function render(kind, p) {
  if (p.reply) return p.reply.join("\n\n") + (p.tool ? `\n[tool: ${p.tool.name}]` : "");
  if (p.sections) return (p.missing?.length ? `[missing: ${p.missing.join("; ")}]\n\n` : "") + p.sections.map((s) => `${s.heading.toUpperCase()}\n${s.body}`).join("\n\n");
  if (p.coach) return JSON.stringify(p.coach, null, 1);
  return JSON.stringify(p);
}
const outIdx = process.argv.indexOf("--out");
const outFile = outIdx > 0 ? process.argv[outIdx + 1] : null;
const health = JSON.parse((await handler({ headers: {}, requestContext: { http: { method: "GET" } } })).body);
const lines = [`# QuotaBird eval, ${new Date().toISOString().slice(0, 16)}, model ${health.model}, quotabird ${health.version}`, ""];
for (const [name, kind, body] of CASES) {
  const t0 = Date.now();
  const r = await handler(ev({ kind, ...body }));
  const p = JSON.parse(r.body || "{}");
  const text = r.statusCode === 200 ? render(kind, p) : `ERROR ${r.statusCode}: ${p.error}`;
  lines.push(`## ${name} (${kind}, ${Date.now() - t0} ms, ${text.split(/\s+/).length} words)`, "", "> " + (body.messages ? body.messages.at(-1).text : body.situation), "", text, "");
  console.log(`\n=== ${name} (${kind}, ${Date.now() - t0} ms) ===\n${text}`);
}
lines.push("## Scoring (1 to 5 each)", "", "| case | sounds like Mark | no sugarcoating | real issue | specific next action | no invented facts | no consultant language | no generic coaching | disagrees when needed | concise | notes |", "|---|---|---|---|---|---|---|---|---|---|---|",
  ...CASES.map(([n]) => `| ${n} | | | | | | | | | | |`), "");
if (outFile) { fs.writeFileSync(outFile, lines.join("\n")); console.log(`\nwritten to ${outFile}`); }
