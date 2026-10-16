// A local stand-in for the Lambda Function URL: the REAL handler (index.mjs + quotabird.mjs),
// with Google's API replaced by canned answers, so the pages can be tested end to end.
import http from 'node:http';
process.env.GEMINI_API_KEY = 'test'; process.env.ALLOWED_ORIGINS = '*'; process.env.QB_RATE_LIMIT_PER_MINUTE = '1000'; process.env.QB_RATE_LIMIT_PER_HOUR = '10000';
const gem = (obj, delay = 300) => new Promise(r => setTimeout(() => r(new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify(obj) }] } }] }), { status: 200 })), delay));
function canned(sys, user) {
  if (sys.includes('Your job here is only routing')) {
    const t = user;
    if (/weather/i.test(t)) return { slug: 'none', why: '', inputs: [], reply: "QuotaBird does sales math, not weather. Ask about your quota, pipeline, pay or a deal." };
    if (/pipeline/i.test(t)) return { slug: 'pipeline', why: 'You want to know if the pipeline you have covers what is left of your number.', reply: '',
      inputs: [{ id: 'goal', value: '$5M', quote: 'quota is $5M' }, { id: 'pipe', value: '$8M', quote: '$8M of qualified pipeline' }, { id: 'win', value: '25%', quote: 'about 25%' }] };
    if (/quota/i.test(t)) return { slug: 'quota', why: 'You want to know whether the quota is reasonable for what they pay you.', reply: '',
      inputs: [{ id: 'quota', value: '$1.2M', quote: '$1.2M quota' }, { id: 'basis', value: 'saas', quote: 'measured on bookings' }] };
    if (/meeting/i.test(t)) return { slug: 'meeting-prep', why: 'You have a meeting coming and want to be ready.', reply: '', inputs: [{ id: 'customer', value: 'the VA CIO', quote: 'the VA CIO' }] };
    return { slug: 'deal', why: 'You want to know whether the deal is real before it goes in commit.', reply: '', inputs: [] };
  }
  if (sys.includes('explain one QuotaBird result')) return {
    see: [{ text: 'Your pipeline covers 2.1X of what is left, and at your 25% win rate you need 4X. You are short.', label: 'calculated' }, { text: 'Most teams win 35%.', label: 'guess' }],
    wrong: [{ text: 'You are counting on deals that may not be real yet.', label: 'guess' }],
    next: [{ text: 'Run your three biggest deals through Deal Check before the forecast call.', label: 'guess' }, { text: 'Tell your boss now, in dollars, that you need $7M of new pipeline.', label: 'calculated' }] };
  if (sys.includes('important customer meeting')) return { objective: 'They agree to a two-week pilot with their claims team.', known: ['They want to cut the claims backlog', 'The deputy CIO asked for this meeting'], unknown: ['Who signs', 'Where the money comes from'],
    priorities: [{ text: 'Cutting the claims backlog this year.', label: 'you_said' }, { text: 'Probably anything that avoids a new contract action.', label: 'guess' }],
    questions: ['What happens to the backlog if nothing changes this year?', 'Who else has to agree before a pilot starts?', 'How did you buy the last tool like this, and through which vehicle?', 'What would the pilot have to show by the end of two weeks?'],
    objections: [{ objection: 'We have no money this year.', answer: 'Ask which line a pilot would come from, and whether a no-cost pilot avoids the question.' }], landmines: ['The last vendor pilot that went nowhere.'], next_step: 'A pilot kickoff with the program manager, dated before the end of the quarter.' };
  if (sys.includes('plan with a number on it')) return { summary: 'You have $1.15M of open pipeline against a $2M number, and at 25% that is well short. The account runs through one person.', priorities: [{ text: 'Cutting the claims backlog.', label: 'you_said' }, { text: 'Probably a cloud move tied to the data center closure.', label: 'guess' }],
    gaps: ['Where the money for claims work comes from', 'Who owns the renewal on their side'], who_to_meet: [{ who: 'The program manager for claims', why: 'Owns the requirement.' }, { who: 'The contracting officer\'s representative', why: 'Knows how the last buy happened.' }],
    plays: [{ text: 'Grow the renewal into the claims work instead of starting a new buy.', label: 'guess' }], milestones: [{ quarter: 'Q1 (Oct to Dec)', text: 'Meet the claims program manager.' }, { quarter: 'Q3 (Apr to Jun)', text: 'Close the claims modernization deal.' }, { quarter: 'Q4 (Jul to Sep)', text: 'Renewal decision.' }],
    next_actions: ['Ask your contact for an introduction to the claims program manager.', 'Read the agency budget justification for the claims line.'] };
  if (sys.includes('their boss')) return { headline: 'I will land $2.6M of the $3M number and I am calling it now.', deals: [{ name: 'Northwind', status: 'Waiting on legal.', next: 'Their counsel calls back Tuesday.' }, { name: 'Contoso', status: 'Proposal out.', next: 'Pricing review next week.' }],
    blockers: [{ blocker: 'Northwind legal is slow.', ask: 'Ten minutes with their GC from you.' }], recovery: ['Pulled Fabrikam into this quarter.', 'Asked for an exec sponsor call on Contoso.'], questions: [{ q: 'What is your worst case?', a: 'Northwind slips and I land $1.4M.' }] };
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
