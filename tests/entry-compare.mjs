// The old shared entry point vs the QuotaBird-only one, same QuotaBird files: every QuotaBird request answered the same.
globalThis.awslambda = { streamifyResponse: (f) => f, HttpResponseStream: { from: (s, m) => { s.meta = m; return s; } } };
process.env.GEMINI_API_KEY = 'k'; process.env.ALLOWED_ORIGINS = 'https://quotabird.com';
let reply, mode = 'ok';
const sse = (j) => { const enc = new TextEncoder(), parts = []; for (let i = 0; i < j.length; i += 11) parts.push(j.slice(i, i + 11)); return new ReadableStream({ pull(c) { const p = parts.shift(); if (p === undefined) return c.close(); c.enqueue(enc.encode('data: ' + JSON.stringify({ candidates: [{ content: { parts: [{ text: p }] } }] }) + '\n\n')); } }); };
globalThis.fetch = async (url) => { url = String(url);
  if (mode === '429') return new Response('busy', { status: 429 });
  if (mode === 'garbled') return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: 'not json' }] } }] }), { status: 200 });
  const j = JSON.stringify(reply);
  if (url.includes(':streamGenerateContent')) return new Response(sse(j), { status: 200 });
  return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: j }] }, finishReason: 'STOP' }] }), { status: 200 }); };
const A = await import('./old/index.mjs'), B = await import('./new/index.mjs');
const MARK = { reply: "I hear you. Probably not, and I wouldn't plan like you will.\n\nCall the miss now. Good luck!", tool: 'pipeline', followups: ['What do I tell my boss?'] };
const cases = [
  ['chat', MARK, { kind: 'qb_mark', messages: [{ role: 'user', text: 'I am at 40% with two months left. Can I make it?' }] }],
  ['chat, page', MARK, { kind: 'qb_mark', page: 'meeting-prep', messages: [{ role: 'user', text: 'Thursday I meet the HHS deputy CIO.' }] }],
  ['chat, streamed', MARK, { kind: 'qb_mark', stream: true, messages: [{ role: 'user', text: 'I am at 40% with two months left. Can I make it?' }] }],
  ['chat, bad input', MARK, { kind: 'qb_mark', messages: [{ role: 'mark', text: 'hi' }] }],
  ['coach', { read: 'A fan.', hole: 'No vehicle.', move: 'Find the path.', people: [], next_72_hours: ['Call.'], what_would_change_my_mind: 'An order.', tool: 'deal' }, { kind: 'qb_coach', situation: 'My champion at DHS loves us but no vehicle.' }],
  ['meeting prep', { known: ['x'], missing: ['who signs'], sections: [{ heading: 'Read', body: 'Short.' }, { heading: 'Ask', body: '- one' }] }, { kind: 'qb_meeting_prep', situation: 'Thursday with the deputy CIO at HHS about a pilot.' }],
  ['update upward', { known: [], missing: [], sections: [{ heading: 'The update', body: 'Closed $1.2M of $3M.' }, { heading: 'Your boss will ask', body: '- worst case' }] }, { kind: 'qb_update_upward', type: 'miss', situation: '$3M number, $1.2M closed.' }],
  ['route', { slug: 'pipeline', why: 'Coverage.', inputs: [{ id: 'goal', value: '$5M', quote: 'quota is $5M' }], reply: '' }, { kind: 'qb_route', text: 'quota is $5M and I have $8M' }],
  ['explain', { see: [{ text: 'You need 3X.', label: 'calculated' }], wrong: [], next: [{ text: 'Ask your manager.', label: 'guess' }] }, { kind: 'qb_explain', slug: 'pipeline', question: 'ok?', inputs: [{ label: 'Quota', value: '$3M' }], result: { answer: 'Short', rows: [['Coverage needed', '3X']] } }],
  ['gemini busy', '429', { kind: 'qb_mark', messages: [{ role: 'user', text: 'Am I fine on pipeline?' }] }],
  ['gemini garbled', 'garbled', { kind: 'qb_route', text: 'is my quota crazy' }],
  ['too large', MARK, { kind: 'qb_route', text: 'y'.repeat(17000) }],
  ['not json', MARK, 'not json'],
];
const ev = (b, origin = 'https://quotabird.com', ip = '5.5.5.' + Math.random(), method = 'POST') => ({ headers: { origin }, requestContext: { http: { method, sourceIp: ip } }, body: typeof b === 'string' ? b : JSON.stringify(b) });
const viaStream = async (h, e) => { const s = { chunks: [], write(t) { this.chunks.push(String(t)); }, end() {} }; await h(e, s); return { statusCode: s.meta.statusCode, headers: s.meta.headers, body: s.chunks.join('') }; };
let same = 0, diff = 0;
const cmp = (name, x, y, note = '') => { const ok = x.statusCode === y.statusCode && x.body === y.body && JSON.stringify(x.headers) === JSON.stringify(y.headers); ok ? same++ : diff++; if (!ok) console.log('DIFF', name, note, x.statusCode, y.statusCode, String(x.body).slice(0, 120), '|', String(y.body).slice(0, 120)); };
for (const [name, r, body] of cases) {
  if (r === '429' || r === 'garbled') mode = r; else { mode = 'ok'; reply = r; }
  cmp(name, await A.handler(ev(body)), await B.bufferedHandler(ev(body)), '(plain JSON)');
  cmp(name, await viaStream(A.streamingHandler, ev(body)), await viaStream(B.handler, ev(body)), '(streaming: index.handler now)');
}
mode = 'ok'; reply = MARK;
cmp('refused origin', await A.handler(ev(cases[0][2], 'https://evil.example')), await B.bufferedHandler(ev(cases[0][2], 'https://evil.example')));
cmp('options', await A.handler(ev('', 'https://quotabird.com', '1.1.1.1', 'OPTIONS')), await B.bufferedHandler(ev('', 'https://quotabird.com', '1.1.1.1', 'OPTIONS')));
let la, lb; for (let i = 0; i < 11; i++) { la = await A.handler(ev(cases[7][2], undefined, '8.8.8.8')); lb = await B.bufferedHandler(ev(cases[7][2], undefined, '8.8.8.8')); }
cmp('11th request from one visitor', la, lb);
console.log(`QuotaBird, old shared entry point vs QuotaBird-only: ${same} same, ${diff} different`);
