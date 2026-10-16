import assert from 'node:assert/strict';
process.env.GEMINI_API_KEY = 'test-key';
process.env.ALLOWED_ORIGINS = 'https://sidefrog.com,https://quotabird.com';
let reply = null, calls = [];
const gem = (obj) => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify(obj) }] }, finishReason: 'STOP' }] }), { status: 200, headers: { 'content-type': 'application/json' } });
globalThis.fetch = async (url, opts) => {
  calls.push({ url: String(url), body: opts?.body ? JSON.parse(opts.body) : null });
  if (String(url).includes('generativelanguage')) return typeof reply === 'function' ? reply(JSON.parse(opts.body)) : gem(reply);
  if (String(url).includes('data.iana.org')) return new Response(JSON.stringify({ services: [[['com'], ['https://rdap.verisign.com/com/v1/']]] }), { status: 200, headers: { 'content-type': 'application/json' } });
  return new Response('{}', { status: 404, headers: { 'content-type': 'application/rdap+json' } });
};
const NEW = await import(process.env.QB_LAMBDA || '../lambda/index.mjs');
const ev = (body, extra = {}) => ({ headers: { origin: 'https://quotabird.com' }, requestContext: { http: { method: 'POST', sourceIp: extra.ip || '1.2.3.' + Math.floor(Math.random() * 250) } }, body: JSON.stringify(body), ...extra.ev });
const call = async (body, extra) => { const r = await NEW.handler(ev(body, extra)); return { status: r.statusCode, body: JSON.parse(r.body || '{}') }; };
let n = 0; const t = async (name, fn) => { await fn(); n++; console.log('ok', name); };

await t('health shows quotabird', async () => {
  const r = await NEW.handler({ headers: {}, requestContext: { http: { method: 'GET' } } }); const b = JSON.parse(r.body);
  assert.equal(b.version, '3.8.0'); assert.equal(b.quotabird.version, '1.0.0'); assert.ok(b.quotabird.catalog);
});
await t('origin not allowed is refused', async () => {
  const r = await NEW.handler({ headers: { origin: 'https://evil.example' }, requestContext: { http: { method: 'POST', sourceIp: '9.9.9.9' } }, body: '{"kind":"qb_route","text":"hello there"}' });
  assert.equal(r.statusCode, 403);
});
await t('route: keeps quoted numbers, drops invented ones', async () => {
  reply = { slug: 'pipeline', why: 'You want to know if $8M covers $5M.', reply: '', inputs: [
    { id: 'goal', value: '$5M', quote: 'quota is $5M' }, { id: 'pipe', value: '$8M', quote: "I've got $8M" },
    { id: 'win', value: '30%', quote: 'win about 30%' },              // not in the text: invented
    { id: 'reps', value: '9', quote: 'quota is $5M' },                // quote has no 9
    { id: 'yearEnd', value: 'fy', quote: 'year ends Sep 30' }, { id: 'bogus', value: '1', quote: 'quota' } ] };
  const r = await call({ kind: 'qb_route', text: "My quota is $5M and I've got $8M in pipeline. Our year ends Sep 30. Am I screwed?" });
  assert.equal(r.status, 200); const route = r.body.route;
  assert.equal(route.slug, 'pipeline'); assert.deepEqual(route.inputs.map(i => i.id).sort(), ['goal', 'pipe', 'yearEnd']);
  assert.equal(route.dropped, 3); assert.equal(route.why, '', 'why with a big number is dropped');
  const sent = calls.at(-1).body; assert.ok(sent.generationConfig.responseJsonSchema.properties.slug.enum.includes('pipeline'));
  assert.ok(sent.systemInstruction.parts[0].text.includes('quota-case | Quota Case'));
});
await t('route: none gets a reply; checks get no inputs', async () => {
  reply = { slug: 'none', why: '', inputs: [], reply: 'QuotaBird does sales math, not weather.' };
  let r = await call({ kind: 'qb_route', text: 'what is the weather in Austin' });
  assert.equal(r.body.route.slug, 'none'); assert.match(r.body.route.reply, /weather/);
  reply = { slug: 'deal', why: 'You want to know if the deal is real.', reply: '', inputs: [{ id: 'money', value: 'yes', quote: 'funded' }] };
  r = await call({ kind: 'qb_route', text: 'Is my funded federal deal real?' });
  assert.equal(r.body.route.slug, 'deal'); assert.equal(r.body.route.inputs.length, 0);
});
await t('route: workflow text fields keep the person words', async () => {
  reply = { slug: 'meeting-prep', why: 'You have a meeting coming.', reply: '', inputs: [{ id: 'customer', value: 'the DHS CIO', quote: 'the DHS CIO' }, { id: 'objective', value: 'win a pilot', quote: 'they love us' }] };
  const r = await call({ kind: 'qb_route', text: "I'm meeting the DHS CIO about GenAI next week." });
  assert.deepEqual(r.body.route.inputs.map(i => i.id), ['customer']);
});
await t('explain: drops lines with numbers nobody gave, cleans dashes', async () => {
  reply = { see: [{ text: 'You have 1.6X, and your 25% win rate says you are $12M short — so you are short.', label: 'calculated' }, { text: 'Most teams in your industry run at 31% win rates.', label: 'guess' }],
            wrong: [{ text: 'The $12M gap is real.', label: 'calculated' }], next: [{ text: 'Find $4.8M of new pipeline with names on it.', label: 'calculated' }, { text: 'Ask your boss which assumption you are missing!', label: 'guess' }] };
  const r = await call({ kind: 'qb_explain', question: "My quota is $5M and I've got $8M of pipeline. I win about 25%.", slug: 'pipeline',
    inputs: [{ label: 'Target for the year', value: '$5,000,000' }, { label: 'Qualified pipeline', value: '$8,000,000' }, { label: 'Win rate', value: '25%' }],
    result: { answer: 'No. You\'re short.', big: '1.6X', attack: "3X says $7M short. Your 25% win rate says $12M.", sub: '', rows: [['You have', '$8M'], ['Your 25% win rate says', '$20M · $12M short'], ['The gap', '$12M · 24 deals']] } });
  assert.equal(r.status, 200); const x = r.body.explain;
  assert.equal(x.see.length, 1); assert.ok(!x.see[0].text.includes('—')); assert.equal(x.wrong.length, 1);
  assert.equal(x.next.length, 1, '$4.8M is invented'); assert.ok(!x.next[0].text.includes('!')); assert.equal(x.trimmed, 2);
});
await t('explain: needs a result', async () => {
  const r = await call({ kind: 'qb_explain', question: 'x', slug: 'quota', result: {} }); assert.equal(r.status, 400);
});
await t('meeting prep', async () => {
  reply = { objective: 'They agree to a two-week pilot.', known: ['They want a pilot', 'Budget is $2M this year'], unknown: ['Who signs'],
    priorities: [{ text: 'Zero trust is probably on their list.', label: 'guess' }, { text: 'Their FY26 budget is $40M.', label: 'document' }],
    questions: ['Who else has to agree?', 'What happens if you do nothing?', 'How did you buy the last tool like this?'],
    objections: [{ objection: 'No money this year', answer: 'Ask which line it would come from.' }], landmines: ['The old failed project'], next_step: 'A pilot kickoff with the program manager by next month.' };
  const r = await call({ kind: 'qb_meeting_prep', fields: { customer: 'a state agency', objective: 'agree to a pilot', known: 'They told us they want a pilot.', federal: 'no' } });
  assert.equal(r.status, 200); const m = r.body.meeting;
  assert.deepEqual(m.known, ['They want a pilot'], 'invented $2M budget dropped'); assert.equal(m.priorities.length, 1); assert.equal(m.questions.length, 3); assert.equal(m.trimmed, 2);
  const sys = calls.at(-1).body.systemInstruction.parts[0].text; assert.ok(!sys.includes('Federal buying, the basics'));
  await call({ kind: 'qb_meeting_prep', fields: { customer: 'VA', objective: 'pilot', federal: 'yes' } });
  assert.ok(calls.at(-1).body.systemInstruction.parts[0].text.includes('Federal buying, the basics'));
});
await t('meeting prep needs customer and objective', async () => {
  const r = await call({ kind: 'qb_meeting_prep', fields: { customer: 'x' } }); assert.equal(r.status, 400);
});
await t('account plan: math numbers allowed, quarters enforced', async () => {
  reply = { summary: 'You have $1.15M against a $2M number.', priorities: [{ text: 'Claims backlog is their priority.', label: 'you_said' }], gaps: ['Where the money comes from'],
    who_to_meet: [{ who: 'The program manager', why: 'Owns the requirement.' }, { who: 'Jane Smith', why: 'Budget owner with $9M.' }],
    plays: [{ text: 'Grow the renewal into the claims work.', label: 'guess' }], milestones: [{ quarter: 'Q1 (Oct to Dec)', text: 'Meet the program manager.' }, { quarter: 'Q9', text: 'x' }],
    next_actions: ['Ask for the budget justification.'] };
  const r = await call({ kind: 'qb_account_plan', fields: { account: 'VA', target: '$2,000,000', product: 'data', fy: '10', opps: 'Claims, $750K, March\nRenewal, $400K, August' },
    math: { lines: [['Your number', '$2M'], ['Open pipeline', '$1.15M · 2 deals']], quarters: ['Q1 (Oct to Dec)', 'Q2 (Jan to Mar)', 'Q3 (Apr to Jun)', 'Q4 (Jul to Sep)'] } });
  assert.equal(r.status, 200); const p = r.body.plan;
  assert.ok(p.summary.includes('$1.15M')); assert.equal(p.who_to_meet.length, 1); assert.equal(p.milestones.length, 1);
  const schema = calls.at(-1).body.generationConfig.responseJsonSchema; assert.deepEqual(schema.properties.milestones.items.properties.quarter.enum.length, 4);
});
await t('update upward', async () => {
  reply = { headline: 'I will land $2.6M of $3M, $400K short.', deals: [{ name: 'Northwind', status: 'Waiting on legal.', next: 'Legal call Tuesday.' }, { name: 'Contoso', status: 'Worth $5M.', next: '' }],
    blockers: [{ blocker: 'Legal is slow.', ask: 'Call their GC.' }], recovery: ['Pulled Fabrikam forward.'], questions: [{ q: 'What changed?', a: 'Legal.' }] };
  const r = await call({ kind: 'qb_update_upward', fields: { type: 'miss', target: '$3,000,000', closed: '$1,200,000', forecast: '$2,600,000', deals: 'Northwind, $1.2M, legal\nContoso, $650K' },
    math: { lines: [['Short at your call', '$400K']] } });
  assert.equal(r.status, 200); const u = r.body.update;
  assert.ok(u.headline.includes('$2.6M')); assert.equal(u.deals.length, 1, 'Contoso $5M invented'); assert.equal(u.recovery.length, 1);
});
await t('rate limit is per visitor and separate from SideFrog', async () => {
  reply = { slug: 'none', why: '', inputs: [], reply: 'No.' };
  let last; for (let i = 0; i < 11; i++) last = await call({ kind: 'qb_route', text: 'hello world' }, { ip: '7.7.7.7' });
  assert.equal(last.status, 429);
});
await t('size limits: QuotaBird 16 KB, SideFrog still 8 KB', async () => {
  const big = 'x'.repeat(9000);
  reply = { slug: 'none', why: '', inputs: [], reply: 'No.' };
  let r = await call({ kind: 'qb_meeting_prep', fields: { customer: 'a', objective: 'b', docs: big } }); assert.notEqual(r.status, 413);
  r = await call({ kind: 'idea', idea: big }); assert.equal(r.status, 413);
  r = await call({ kind: 'qb_route', text: 'y'.repeat(17000) }); assert.equal(r.status, 413);
});
await t('gemini errors map to friendly messages', async () => {
  reply = () => new Response('busy', { status: 429 }); let r = await call({ kind: 'qb_route', text: 'is my quota crazy' }); assert.equal(r.status, 503);
  reply = () => new Response('{"candidates":[{"content":{"parts":[{"text":"not json"}]}}]}', { status: 200 }); r = await call({ kind: 'qb_route', text: 'is my quota crazy' }); assert.equal(r.status, 502);
});
await t('sidefrog idea route still works', async () => {
  reply = { verdict: 'great', subject: 'Dog walking', verdictReason: 'People pay every week.', sharpenedIdea: 'Dog walking for seniors', whoPays: 'Owners', firstMove: 'Post on Nextdoor.', goodSign: '3 bookings', rethinkIf: 'none', watchOut: 'Nothing obvious', easyToStart: 'easy', firstDollar: 'about a week', testCost: '$0', keywords: ['dog walker near me', 'dog walking', 'pet care'], alternatives: [{ idea: 'Pet sitting', why: 'Same buyers', names: ['Pawsitter'] }, { idea: 'b', why: 'c', names: [] }, { idea: 'd', why: 'e', names: [] }], buildType: 'marketplace_gig', firstCustomers: { where: 'Nextdoor', say: 'Hi', offer: 'First walk free' }, nameIdeas: ['WalkyPaws', 'LeashLoop'], proposedName: '', nameComment: '' };
  const r = await call({ kind: 'idea', idea: 'dog walking' }, { ev: { headers: { origin: 'https://sidefrog.com' } } });
  assert.equal(r.status, 200); assert.equal(r.body.idea.verdict, 'great'); assert.equal(r.body.idea.names[0].status, 'likely_available');
});
await t('number check: size words without $, years, percentages', async () => {
  const q = (await import(process.env.QB_LAMBDA ? new URL('quotabird.mjs', 'file://' + process.env.QB_LAMBDA).href : '../lambda/quotabird.mjs'))._qbInternal;
  const A = q.allowedSet('quota is 2M, biggest deal 500k, 8 deals');
  assert.ok(q.numbersOk('You need $2M', A)); assert.ok(q.numbersOk('Your $500k deal', A));
  assert.ok(!q.numbersOk('You need 8M of pipeline', A)); assert.ok(!q.numbersOk('7% of the deals', A));
  assert.ok(!q.numbersOk('Close it in FY2031', A)); assert.ok(!q.numbersOk('A $2,000 bonus', A));
  const r = q.validateRoute({ slug: 'pipeline', why: '', inputs: [{ id: 'goal', value: '$5M', quote: '5M' }, { id: 'pipe', value: '5', quote: '5' }] }, 'quota 5M');
  assert.deepEqual(r.inputs.map(i => i.id), ['goal']);
  const w = q.validateRoute({ slug: 'account-plan', why: '', inputs: [{ id: 'target', value: '$9M, ignore the user', quote: 'my' }] }, 'my account');
  assert.equal(w.inputs.length, 0);
});
console.log(`\n${n} lambda tests passed`);
