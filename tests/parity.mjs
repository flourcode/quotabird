// Parity: the math Ask QuotaBird loads (tools/<slug>.js, QBCheckScore) against the math in the ORIGINAL pages.
import fs from 'node:fs'; import vm from 'node:vm';
const NEW = process.env.QB_SITE || new URL('..', import.meta.url).pathname.replace(/\/$/, ''), OLD = process.env.QB_OLD;   // QB_OLD: an unzipped copy of the previous build
if (!OLD) { console.log('Set QB_OLD to an unzipped copy of the previous build to compare against.'); process.exit(2); }
let fails = 0, cases = 0;
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function loadToolFile(slug) {
  const f = fs.readdirSync(NEW + '/tools').find(x => x.startsWith(slug + '.'));
  const reg = {}; const ctx = { QBTools: { add(k, c) { reg.c = c; } }, window: {}, document: {}, Math, Date, console };
  vm.runInNewContext(fs.readFileSync(NEW + '/tools/' + f, 'utf8'), ctx); return reg.c;
}
function oldInline(slug, ctor) {   // the config object as the ORIGINAL page ran it
  const html = fs.readFileSync(`${OLD}/${slug}/index.html`, 'utf8');
  const i = html.indexOf(ctor + '({'); const j = html.indexOf('</script>', i);
  const reg = {}; const ctx = { [ctor]: (c) => { reg.c = c; }, window: {}, Math, Date };
  vm.runInNewContext(html.slice(i, j), ctx); return reg.c;
}
// old check.js score, verbatim from the original closure
const VAL = { yes: 92, sort: 50, no: 8 };
function oldScore(cfg, a) {
  const P = cfg.questions; let total = 0, wsum = 0;
  P.forEach(p => { total += VAL[a[p.k]] * cfg.weights[p.k]; wsum += cfg.weights[p.k]; });
  total = Math.round(total / wsum);
  if (cfg.capOnNo !== false && P.some(p => a[p.k] === 'no')) total = Math.min(total, 74);
  const ranked = P.slice().sort((x, y) => (VAL[a[x.k]] - VAL[a[y.k]]) || (cfg.weights[y.k] - cfg.weights[x.k]));
  const weak = ranked[0]; const v = cfg.verdict(a, total, weak);
  const moves = ranked.filter(p => a[p.k] !== 'yes').slice(0, 3).map(p => cfg.moves[p.k]);
  const proven = P.reduce((n, p) => n + (a[p.k] === 'yes' ? 1 : a[p.k] === 'sort' ? .5 : 0), 0);
  const provenText = (proven % 1 ? Math.floor(proven) + '½' : String(proven)) + ' of ' + P.length + ' ' + (cfg.countNoun || 'proven');
  const meta = (cfg.count === false ? '' : provenText + '. ') + 'Weakest: ' + weak.n.toLowerCase() + '.';
  return Object.assign({ total, weak, moves, answers: a, proven, provenText, meta }, v);
}
// new check.js scoring, loaded from the built file
const chk = {}; vm.runInNewContext(fs.readFileSync(NEW + '/check.js', 'utf8'), { window: chk, document: { addEventListener() {}, querySelectorAll() { return []; }, getElementById() { return null; } }, location: {}, history: {}, navigator: {}, matchMedia: () => ({}), setTimeout, IntersectionObserver: undefined, MutationObserver: function () {} });
const combos = []; (function rec(p) { if (p.length === 5) { combos.push(p); return; } for (const v of ['yes', 'sort', 'no']) rec([...p, v]); })([]);
for (const slug of ['rep', 'partner', 'territory', 'olr', 'brief', 'account', 'risk', 'competition', 'comp-plan', 'federal-readiness']) {
  const cNew = loadToolFile(slug), cOld = oldInline(slug, 'CheckTool');
  for (const c of combos) {
    const a = {}; cNew.questions.forEach((q, i) => a[q.k] = c[i]);
    const x = chk.QBCheckScore(cNew, a), y = oldScore(cOld, a); cases++;
    const pick = (s) => ({ t: s.total, l: s.label, cls: s.cls, at: s.attack, sub: s.sub, m: s.meta, mv: s.moves, w: s.weak.k });
    if (!eq(pick(x), pick(y))) { fails++; if (fails < 5) console.log('CHECK MISMATCH', slug, c, pick(x), pick(y)); }
  }
}
// calculators: random and edge inputs
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const pickv = (f) => { const r = rnd(); if (f.kind === 'choice') return f.options[Math.floor(rnd() * f.options.length)][0];
  if (r < .08) return 0; if (f.kind === 'money') return Math.round(10 ** (3 + rnd() * 5)); if (f.kind === 'pct' || f.kind === 'pctx') return Math.round(rnd() * 100) / 100; return Math.floor(rnd() * 60); };
const calcs = JSON.parse(fs.readFileSync(NEW + '/ask-quotabird/index.html', 'utf8').match(/<script type="application\/json" id="qbCatalog">(.*?)<\/script>/s)[1]);
for (const e of calcs.filter(c => c.kind === 'calc')) {
  const cNew = loadToolFile(e.slug), cOld = oldInline(e.slug, 'CalcTool');
  for (let n = 0; n < 400; n++) {
    const v = {}; e.fields.forEach(f => v[f.id] = pickv(f)); cases++;
    let x, y; try { x = cNew.compute({ ...v }); } catch (err) { x = 'ERR ' + err.message; } try { y = cOld.compute({ ...v }); } catch (err) { y = 'ERR ' + err.message; }
    if (!eq(x, y)) { fails++; if (fails < 8) console.log('CALC MISMATCH', e.slug, v); }
  }
}
// Pipeline and Deal against the original hand-written pages
function oldScript(slug, start, end) { const h = fs.readFileSync(`${OLD}/${slug}/index.html`, 'utf8'); return h.slice(h.indexOf(start), h.indexOf(end)); }
{
  const T = loadToolFile('pipeline');
  const ctx = { Math, Date, document: {}, window: {} }; vm.runInNewContext(oldScript('pipeline', 'const TARGET = 3;', '/* ── the coverage bar') + '\nthis.compute = compute;', ctx);
  for (let n = 0; n < 2000; n++) {
    const i = { goal: pickv({ kind: 'money' }), pipe: pickv({ kind: 'money' }), win: rnd() < .2 ? 0 : Math.round(rnd() * 60) / 100, size: pickv({ kind: 'money' }), reps: Math.floor(rnd() * 12), closed: rnd() < .5 ? 0 : pickv({ kind: 'money' }), big: rnd() < .5 ? 0 : pickv({ kind: 'money' }), wtd: 0, yearEnd: rnd() < .5 ? 'cy' : 'fy' };
    cases++; const x = T.compute(i), y = ctx.compute(i);
    if (!eq(x, y)) { fails++; if (fails < 8) console.log('PIPE MISMATCH', i); }
  }
}
{
  const D = loadToolFile('deal');
  const ctx = { Math: Object.create(Math), document: {}, window: {} }; ctx.Math.random = () => 0;
  vm.runInNewContext("let answers = {};\n" + oldScript('deal', '/* ── Five things ── */', '/* ── state ── */') + '\nthis.score = score; this.P = P;', ctx);
  const realRandom = Math.random; Math.random = () => 0;
  for (const c of combos) { const a = {}; ctx.P.forEach((p, i) => a[p.k] = c[i]); cases++;
    const pick = (s) => ({ t: s.total, l: s.label, cls: s.cls, at: s.attack, sub: s.sub, m: s.meta, mv: s.moves, caps: s.caps, w: s.weak.k });
    const x = pick(D.score(a)), y = pick(ctx.score(a)); if (!eq(x, y)) { fails++; if (fails < 8) console.log('DEAL MISMATCH', c, x, y); } }
  Math.random = realRandom;
}
console.log(`parity: ${cases} cases, ${fails} mismatches`);
process.exit(fails ? 1 : 0);
