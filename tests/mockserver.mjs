// A local stand-in for the Lambda Function URL: the REAL handler (index.mjs + quotabird.mjs),
// with Google's API replaced by canned answers, so the pages can be tested end to end.
import http from 'node:http';
process.env.GEMINI_API_KEY = 'test'; process.env.ALLOWED_ORIGINS = '*'; process.env.QB_RATE_LIMIT_PER_MINUTE = '1000'; process.env.QB_RATE_LIMIT_PER_HOUR = '10000';
const gem = (obj, delay = 300) => new Promise(r => setTimeout(() => r(new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify(obj) }] } }] }), { status: 200 })), delay));
function canned(sys, user) {
  if (sys.startsWith('You are the AI version of Mark') || sys.startsWith('You are QuotaBird, speaking')) {
    if (!user.includes('Give your read') && !user.includes('ready for the meeting') && !user.includes('account plan') && !user.includes('sends their boss')) return { reply: "You don't have a deal yet, you have a fan. A champion who can't name the vehicle is a fan.\n\nFind out which vehicle the CIO's office used for its last security buy. Then line up a reseller or prime who holds it and walk in with the path, not a request for one. The CO isn't against you. The CO has no way to buy you.\n\nIf it's August, you're probably looking at next year's money unless the office already has an existing order you can ride. Ask your champion that question today.", tool: 'deal' };
    if (user.includes('Give your read, the hole, the move')) return { read: 'A fan, not a deal.', hole: 'No vehicle.', move: 'Find the path.', people: [{ role: 'CO', why_they_matter: 'The path.', move: 'Bring one.' }], next_72_hours: ['Call the champion.'], what_would_change_my_mind: 'An existing order.', tool: 'deal' };
    if (false) return { high_level_recommendation: (user.includes('NEW SCENARIO') ? 'With the RFP slipping, ' : '') + "Ok, let's think about this. Your champion at DHS is real, but a champion without a vehicle is a fan. In the next 72 hours, find out which contract vehicle the CIO's office used for its last security buy, get your champion to forward a one-page mission brief to the CIO, and line up a prime or reseller who holds that vehicle. Handle the 'no vehicle' objection by bringing the path with you instead of asking them to find one.",
      coaching_plan: [['Decision Maker', 'Get 20 minutes with the CIO within two weeks, framed around the zero trust mandate and the deadline it carries, with your champion making the introduction.', ['Zero trust deadline', 'Mission risk', 'No new contract action']],
        ['Economic Buyer', 'Confirm by Friday which budget line funds this and whether it is one-year money that expires September 30.', ['Use-or-lose money', 'Cost avoidance', 'Fast time to value']],
        ['Technical Buyer', 'Send the FedRAMP package and an architecture one-pager to the security lead within 72 hours.', ['FedRAMP authorized', 'Fits existing stack', 'Low integration risk']],
        ['Blocker', 'The contracting officer is not against you, they just have no path. Bring the path: a prime on SEWP or the GSA schedule with a quote ready.', ['Compliant path', 'Less work for the CO', 'Competition already done']],
        ['Champion', 'Give your champion a forwardable one-pager this week that makes them look like the person who solved the mandate.', ['Your win, not ours', 'Ready to forward', 'Mission impact in one page']],
        ['Your Boss (Sales Director/VP)', 'Tell your VP by Wednesday that the deal is real but pathless, and ask for one exec call to the prime partner.', ['Real demand, no vehicle', 'One specific ask', 'Date for a decision']],
        ['Your Internal Stakeholders', 'Get partner management to confirm which primes hold the vehicle and price the quote through them by Friday.', ['Partner pricing', 'Quote turnaround', 'Who owns the prime relationship']]].map(([persona, smart_goal, talking_points]) => ({ persona, smart_goal, talking_points })), tool: 'deal' };
    if (user.includes('ready for the meeting')) return { known: ['Deputy CIO is coming'], missing: ['Who signs', 'Where the money is'], sections: [
      { heading: "What's really going on", body: "That director gets measured on partner-influenced revenue in their own cloud. They meet ISVs every week who want co-sell and bring nothing, so you're competing for an hour of attention." },
      { heading: 'Walk in with', body: "- Two or three real federal deals: agency, program, rough size, where it stands\n- What you need from them on each one, usually an intro to the account manager who covers that agency" },
      { heading: 'What to ask', body: "- Which of your account teams cover these agencies?\n- What do we have to show before your sellers get credit for working with us?" },
      { heading: 'The one ask', body: 'An intro to the account manager on your biggest deal, with a date. Send a forwardable note the same day.' } ] };
    if (user.includes('account plan')) return { known: ['$2M number'], missing: ['Who owns the renewal'], sections: [{ heading: 'Where it stands', body: 'VA is a good account with one thread. Everything runs through the program manager.' }, { heading: 'This week', body: '- Ask her for one introduction upward\n- Ask Carahsoft when the renewal quote has to go out' }] };
    return { known: [], missing: [], sections: [{ heading: 'The update', body: "Quick read on Q4. Closed $1.2M against $3M, and my call is $2.6M.\n\nNorthwind ($1.2M) is stuck in their legal. I need ten minutes from you with their GC this week." }, { heading: 'Your boss will ask', body: "- What's your worst case? Northwind slips and I land $1.4M." }] };
  }
  return {};
}
globalThis.fetch = async (url, opts) => { const b = JSON.parse(opts.body); return gem(canned(b.systemInstruction.parts[0].text, b.contents[0].parts[0].text)); };
const { handler } = await import(process.env.QB_LAMBDA || '../lambda/index.mjs');
http.createServer(async (req, res) => {
  const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'content-type' };
  if (req.method === 'OPTIONS') { res.writeHead(204, cors); return res.end(); }
  let body = ''; for await (const c of req) body += c;
  const r = await handler({ headers: { origin: req.headers.origin || '' }, requestContext: { http: { method: req.method, sourceIp: '127.0.0.1' } }, body });
  res.writeHead(r.statusCode, { ...r.headers, ...cors }); res.end(r.body);
}).listen(8803, () => console.log('mock lambda on 8803'));
