// Streaming the chat through the streaming handler: sentences arrive as they're ready, the final answer matches
// the plain route, the no-sugarcoating guard holds, errors before the first word are plain JSON, errors after
// are an error line, and the buffered handler still answers plain JSON when the page asks for a stream.
import assert from 'node:assert/strict';
// Like the real runtime (aws-lambda-nodejs-runtime-interface-client): the status and headers go out with the first
// write(), even an empty one; a stream ended without a write loses them.
globalThis.awslambda = { streamifyResponse: (f) => f, HttpResponseStream: { from: (s, m) => { const w = s.write.bind(s); let first = true; s.write = (t) => { if (first) { first = false; s.meta = m; } return w(t); }; return s; } } };
process.env.GEMINI_API_KEY = 'k'; process.env.ALLOWED_ORIGINS = '*'; process.env.QB_RATE_LIMIT_PER_MINUTE = '1000'; process.env.QB_RATE_LIMIT_PER_HOUR = '10000';

let mode = 'ok', answer = null, calls = [];
const sse = (json, size = 9) => { const enc = new TextEncoder(); const parts = []; for (let i = 0; i < json.length; i += size) parts.push(json.slice(i, i + size));
  return new ReadableStream({ async pull(c) { const p = parts.shift(); if (p === undefined) return c.close(); c.enqueue(enc.encode('data: ' + JSON.stringify({ candidates: [{ content: { parts: [{ text: p }] } }] }) + '\r\n\r\n')); } }); };
globalThis.fetch = async (url, opts) => {
  url = String(url); calls.push({ url, body: JSON.parse(opts.body) });
  const j = JSON.stringify(answer);
  if (url.includes(':streamGenerateContent')) {
    if (mode === '429') return new Response('quota', { status: 429 });
    if (mode === 'schema') return new Response('bad schema', { status: 400 });
    if (mode === 'midway') { const enc = new TextEncoder(); let n = 0; return new Response(new ReadableStream({ pull(c) { if (n++ === 0) c.enqueue(enc.encode('data: ' + JSON.stringify({ candidates: [{ content: { parts: [{ text: j.slice(0, 80) }] } }] }) + '\n\n')); else c.error(new Error('reset')); } }), { status: 200 }); }
    return new Response(sse(j), { status: 200, headers: { 'content-type': 'text/event-stream' } });
  }
  return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: j }] } }] }), { status: 200 });
};
const L = await import('../lambda/index.mjs');
const ev = (body, method = 'POST') => ({ headers: { origin: 'https://quotabird.com' }, requestContext: { http: { method, sourceIp: '9.9.9.' + Math.random() } }, body: body == null ? '' : JSON.stringify(body) });
const viaStream = async (body) => { const s = { chunks: [], write(t) { this.chunks.push(String(t)); }, end() { this.ended = true; } }; await L.handler(ev(body), s); return { status: s.meta.statusCode, headers: s.meta.headers, chunks: s.chunks, text: s.chunks.join(''), ended: s.ended }; };
const lines = (t) => t.trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));
let n = 0; const t = async (name, fn) => { await fn(); n++; console.log('ok', name); };

const ASK = { kind: 'qb_mark', stream: true, messages: [{ role: 'user', text: "I'm at 40% with two months left. I can still make it, right?" }] };
answer = { reply: "I hear you, that's a tough spot. Probably not, and I wouldn't plan like you will.\n\nOne deal that could come in is a hope, not a plan. Ask what the customer has actually done.\n\nCall the miss now. You've got this!", tool: 'pipeline', followups: ['What do I tell my boss?', 'Which deals close faster?'] };

await t('streams sentence by sentence, and the done line is the plain answer', async () => {
  const r = await viaStream(ASK);
  assert.equal(r.status, 200); assert.match(r.headers['Content-Type'], /ndjson/); assert.ok(r.ended);
  const ls = lines(r.text); const deltas = ls.filter((l) => l.t === 'd'); const done = ls.at(-1);
  assert.ok(deltas.length >= 4, 'several pieces, not one: ' + deltas.length); assert.equal(done.t, 'done');
  assert.ok(calls.at(-1).url.includes(':streamGenerateContent?alt=sse'));
  assert.equal(deltas.map((d) => d.x).join('').trim(), done.reply.join('\n\n'), 'what streamed is what the answer is');
  const plain = await L.bufferedHandler(ev({ ...ASK, stream: false })); const pb = JSON.parse(plain.body);
  assert.deepEqual(done.reply, pb.reply); assert.deepEqual(done.followups, pb.followups); assert.deepEqual(done.tool, pb.tool);
  assert.ok(!r.text.includes('I hear you') && !r.text.includes("got this"), 'cushion and pep talk never go out');
});
await t("streamed and plain answers get the same plain voice", async () => {
  answer = { reply: "No. At a 20% win rate, 3X is not enough pipeline.\n\nLet us look at the arithmetic. You need 5X, and I would take that to your manager now.", tool: 'pipeline', followups: [] };
  const ls = lines((await viaStream(ASK)).text); const streamed = ls.filter((l) => l.t === 'd').map((l) => l.x).join('').trim();
  assert.equal(streamed, ls.at(-1).reply.join('\n\n')); assert.ok(!/Let us|is not|I would/.test(streamed), streamed);
});
await t('a closer mid-answer still goes out once something follows it', async () => {
  answer = { reply: 'No. Good luck. Then call the CO before Friday.', tool: 'none', followups: [] };
  const d = lines((await viaStream(ASK)).text);
  assert.equal(d.filter((l) => l.t === 'd').map((l) => l.x).join('').trim(), 'No. Good luck. Then call the CO before Friday.');
});
await t('an error before the first word is a plain JSON error with its status', async () => {
  mode = '429'; const r = await viaStream(ASK); mode = 'ok';
  assert.equal(r.status, 503); assert.match(r.headers['Content-Type'], /json/); assert.match(JSON.parse(r.text).error, /busy/);
});
await t('an error after words went out is an error line', async () => {
  answer = { reply: 'Probably not. One deal that could come in is a hope, not a plan. Ask what the customer has actually done on it this week.', tool: 'none', followups: [] };
  mode = 'midway'; const r = await viaStream(ASK); mode = 'ok';
  const ls = lines(r.text); assert.equal(r.status, 200); assert.equal(ls.at(-1).t, 'error'); assert.ok(ls.some((l) => l.t === 'd'));
});
await t('a schema refusal falls back to the plain call, delivered as one done line', async () => {
  mode = 'schema'; const r = await viaStream(ASK); mode = 'ok';
  const ls = lines(r.text); assert.equal(ls.length, 1); assert.equal(ls[0].t, 'done'); assert.ok(ls[0].reply.length);
});
await t('bad input is a plain 400, nothing streamed', async () => {
  const r = await viaStream({ kind: 'qb_mark', stream: true, messages: [{ role: 'mark', text: 'hi' }] });
  assert.equal(r.status, 400); assert.match(r.headers['Content-Type'], /json/);
});
await t('the plain-JSON handler ignores stream:true and answers JSON', async () => {
  const r = await L.bufferedHandler(ev(ASK)); assert.equal(r.statusCode, 200); assert.ok(JSON.parse(r.body).reply.length);
});
await t('workflow pages stream too, with their frame', async () => {
  answer = { reply: "I'd want one thing out of Thursday: the pilot with a date on it. Walk in with the two things the demo didn't answer.", tool: 'none', followups: [] };
  const r = await viaStream({ kind: 'qb_mark', page: 'meeting-prep', stream: true, messages: [{ role: 'user', text: 'Thursday I meet the HHS deputy CIO about a pilot.' }] });
  assert.equal(lines(r.text).at(-1).t, 'done'); assert.ok(calls.at(-1).body.systemInstruction.parts[0].text.includes('Meeting Prep page'));
});
await t('Partner Check and Federal Readiness are chat pages with their own frame; Meeting Prep plays the room for a brief', async () => {
  answer = { reply: 'Probably mostly talk. Give them one account and one date.', tool: 'none', followups: [] };
  for (const [page, words] of [['partner', 'Partner Check page'], ['federal-readiness', 'Federal Readiness Check page'], ['meeting-prep', 'play the room']]) {
    const r = await viaStream({ kind: 'qb_mark', page, stream: true, messages: [{ role: 'user', text: 'Our SI partner has had eight months and brought us nothing.' }] });
    assert.equal(lines(r.text).at(-1).t, 'done', page); assert.ok(calls.at(-1).body.systemInstruction.parts[0].text.includes(words), page);
  }
  const before = calls.length; await viaStream({ kind: 'qb_mark', page: 'risk', stream: true, messages: [{ role: 'user', text: 'Is my pipeline fragile?' }] });
  assert.ok(!calls.at(-1).body.systemInstruction.parts[0].text.includes("Why they're here"), 'a retired page gets the plain chat'); assert.ok(calls.length > before);
});
await t('health check says which handler is serving', async () => {
  const s = { chunks: [], write(t) { this.chunks.push(t); }, end() {} }; await L.handler(ev(null, 'GET'), s);
  assert.equal(JSON.parse(s.chunks.join('')).stream, true);
  assert.equal(JSON.parse((await L.bufferedHandler(ev(null, 'GET'))).body).stream, false);
});
await t('a response with no body (OPTIONS) keeps its status and headers', async () => {
  const s = { chunks: [], write(t) { this.chunks.push(String(t)); }, end() { this.ended = true; } };
  await L.handler(ev(null, 'OPTIONS'), s);
  assert.equal(s.meta && s.meta.statusCode, 204, 'status went out'); assert.ok(s.ended);
});
await t('index.handler is the streaming entry point; streamingHandler is the same function', async () => {
  assert.equal(L.streamingHandler, L.handler); assert.equal(typeof L.bufferedHandler, 'function');
});
console.log(`\n${n} stream tests passed`);
