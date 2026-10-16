/* ask.js: Ask QuotaBird and the three workflow pages (Meeting Prep, Account Plan, Update Upward).
   The AI lives on the server (the shared Lambda, quotabird.mjs) and only does two jobs: pick the
   tool and pull the numbers out of what someone typed, then put a result into plain words.
   Every number is calculated here, by the tool's own code (tools/<slug>.js, generated from the
   same source as the tool page), and the person can see and change every input first. */
'use strict';
(function () {
  const CFG = window.QB_ASK || {};
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const track = (n) => { if (typeof window.qbTrack === 'function') window.qbTrack(n); else (window.qbTrackQ = window.qbTrackQ || []).push(n); };
  const LABEL = { you_said: 'You said', document: 'Your document', calculated: 'QuotaBird math', guess: 'A guess' };
  const reduced = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── talking to the server ── */
  async function post(body, timeoutMs = 32000) {
    const ctrl = new AbortController(); const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      // text/plain keeps this a "simple" CORS request (no preflight), the same as SideFrog. The Lambda parses it as JSON.
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(body), signal: ctrl.signal });
      let data = null; try { data = await res.json(); } catch {}
      if (!res.ok || !data || data.error) return { error: (data && typeof data.error === 'string' && data.error.length < 200) ? data.error : 'Something went wrong. Try again.' };
      return { data };
    } catch (e) {
      return { error: e && e.name === 'AbortError' ? 'That took too long. Try again.' : "Couldn't connect. Check your connection and try again." };
    } finally { clearTimeout(timer); }
  }

  /* ── small shared pieces ── */
  const money = (n) => { if (!isFinite(n)) return '$0'; const a = Math.abs(n), s = n < 0 ? '-' : ''; return s + (a >= 1e9 ? '$' + (a / 1e9).toFixed(2).replace(/\.?0+$/, '') + 'B' : a >= 999500 ? '$' + (a / 1e6).toFixed(a >= 1e7 ? 1 : 2).replace(/\.?0+$/, '') + 'M' : a >= 1e4 ? '$' + Math.round(a / 1e3) + 'K' : a >= 1e3 ? '$' + (a / 1e3).toFixed(1).replace(/\.0$/, '') + 'K' : '$' + Math.round(a)); };
  const pct = (r) => Math.round(r * 100) + '%';
  const P = () => window.QBParse || {};
  const src = (label) => label && LABEL[label] ? ` <span class="src">${LABEL[label]}</span>` : '';
  function busy(btn, on, text) { if (!btn) return; if (!btn.dataset.label) btn.dataset.label = btn.textContent; btn.disabled = on; btn.textContent = on ? text : btn.dataset.label; }
  function errorBox(where, msg) { where.innerHTML = `<div class="banner ask-error" role="alert">${esc(msg)}</div>`; }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    try { const ta = document.createElement('textarea'); ta.value = text; ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0'; document.body.appendChild(ta); ta.select(); const ok = document.execCommand('copy'); ta.remove(); return ok ? Promise.resolve() : Promise.reject(); } catch { return Promise.reject(); }
  }
  function actions(where, textFn, slug) {
    const row = document.createElement('div'); row.className = 'btn-row center ask-actions';
    row.innerHTML = '<button class="btn btn-text" type="button" data-act="copy">Copy</button><button class="btn btn-text" type="button" data-act="print">Print</button>';
    row.querySelector('[data-act="copy"]').onclick = (e) => { const b = e.currentTarget; track(slug + '_copy'); copyText(textFn()).then(() => { b.textContent = 'Copied ✓'; }, () => { b.textContent = "Couldn't copy"; }); };
    row.querySelector('[data-act="print"]').onclick = () => { track(slug + '_print'); window.print(); };
    where.appendChild(row);
  }
  const scrollTo = (el) => { if (!el) return; const top = el.getBoundingClientRect().top; if (top < 0 || top > window.innerHeight * .6) el.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'start' }); };
  function chipGroup(root) {
    root.querySelectorAll('[data-choice]').forEach(b => b.addEventListener('click', () => {
      root.querySelectorAll(`[data-choice="${b.dataset.choice}"]`).forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      b.dispatchEvent(new Event('qbchoice', { bubbles: true }));
    }));
  }
  const choiceOf = (root, id) => { const on = root.querySelector(`[data-choice="${id}"].on`); return on ? on.dataset.v : ''; };
  const b64 = { enc: (o) => btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''),
                dec: (s) => { try { return JSON.parse(decodeURIComponent(escape(atob(s.replace(/-/g, '+').replace(/_/g, '/'))))); } catch { return null; } } };

  /* ── loading a tool's own math ── */
  const loaded = {};
  window.QBTools = { add(kind, cfg) { const slug = cfg.slug; (loaded[slug] = loaded[slug] || {}).cfg = Object.assign({ _kind: kind }, cfg); const w = loaded[slug].wait; if (w) w(loaded[slug].cfg); } };
  function loadTool(entry) {
    const L = loaded[entry.slug] = loaded[entry.slug] || {};
    if (L.cfg) return Promise.resolve(L.cfg);
    if (!L.p) L.p = new Promise((ok, fail) => { L.wait = ok; const s = document.createElement('script'); s.src = entry.file; s.onerror = () => { L.p = null; fail(new Error('load')); }; document.head.appendChild(s); });
    return L.p;
  }

  /* ═════════════════════════ Ask QuotaBird ═════════════════════════ */
  function askPage() {
    const CAT = JSON.parse(($('qbCatalog') || {}).textContent || '[]');
    const bySlug = Object.fromEntries(CAT.map(c => [c.slug, c]));
    const form = $('askForm'), text = $('askText'), btn = $('askBtn'), out = $('askOut');
    let run = 0, question = '';
    const autosize = () => { text.style.height = 'auto'; text.style.height = Math.max(96, text.scrollHeight) + 'px'; };
    text.addEventListener('input', autosize); autosize();
    text.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
    document.querySelectorAll('[data-example]').forEach(b => b.onclick = () => { text.value = b.dataset.example; autosize(); track('ask_example'); form.requestSubmit(); });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const q = text.value.replace(/\s+/g, ' ').trim();
      if (q.length < 3) { errorBox(out, 'Tell it what\'s going on first. A sentence is plenty.'); text.focus(); return; }
      const id = ++run; question = q;
      busy(btn, true, 'Thinking…');
      out.innerHTML = '<div class="ask-wait"><span class="dot"></span> Working out which check you need…</div>';
      track('ask_route');
      const { data, error } = await post({ kind: 'qb_route', text: q });
      if (id !== run) return;
      busy(btn, false);
      if (error) { track('ask_route_error'); return errorBox(out, error); }
      const r = data.route || {};
      track('ask_routed_' + (r.slug || 'none').replace(/-/g, '_'));
      if (!r.slug || r.slug === 'none' || !bySlug[r.slug]) {
        out.innerHTML = `<div class="card ask-none"><p class="lede">${esc(r.reply || "That's not one QuotaBird can help with.")}</p><a class="btn btn-full" href="/" style="margin-top:14px;">See all the tools</a></div>`;
        return;
      }
      const entry = bySlug[r.slug];
      if (entry.kind === 'workflow') return showWorkflow(entry, r, q);
      try { await loadTool(entry); } catch { return errorBox(out, "Couldn't load the tool. Refresh and try again."); }
      if (id !== run) return;
      const cfg = loaded[entry.slug].cfg;
      if (entry.kind === 'calc' || entry.kind === 'pipeline') showCalc(entry, cfg, r);
      else showCheck(entry, cfg, r);
    });

    function head(entry, r, extra) {
      return `<div class="ask-head">
        <span class="overline">Sounds like</span>
        <h2>${esc(entry.name)}: ${esc(entry.question)}</h2>
        ${r.why ? `<p class="ask-why">${esc(r.why)}</p>` : ''}${extra || ''}
      </div>`;
    }

    function showWorkflow(entry, r, q) {
      const pre = {}; (r.inputs || []).forEach(i => { pre[i.id] = i.value; });
      if (entry.slug === 'meeting-prep' && !pre.known) pre.known = q;
      if (entry.slug === 'account-plan' && !pre.priorities) pre.priorities = q;
      if (entry.slug === 'update-upward' && !pre.blockers) pre.blockers = q;
      out.innerHTML = head(entry, r) + `<a class="btn btn-primary btn-lg btn-full" href="${entry.url}#p=${b64.enc(pre)}">Open ${esc(entry.name)} with this filled in</a>`;
      scrollTo(out);
    }

    /* calculators and Pipeline: the fields, filled from what they said, the tool's own compute() on every keystroke */
    function showCalc(entry, cfg, r) {
      const given = Object.fromEntries((r.inputs || []).map(i => [i.id, i]));
      const parse = entry.kind === 'pipeline' ? Object.assign({ choice: (v) => v }, cfg.parse) : P();
      const fmtIn = (f, raw) => { const v = parse[f.kind] ? parse[f.kind](raw) : raw; if (!v) return ''; return f.kind === 'money' ? '$' + Math.round(v).toLocaleString('en-US') : f.kind === 'pct' || f.kind === 'pctx' ? (Math.round(v * 1000) / 10) + '%' : String(v); };
      const field = (f) => {
        const g = given[f.id];
        if (f.kind === 'choice') {
          const sel = g ? g.value : f.example;
          return `<div class="tf ask-choice"><span class="tf-label" id="al-${f.id}">${esc(f.label)}</span><div class="chips" role="group" aria-labelledby="al-${f.id}">${f.options.map(([v, l]) => `<button class="chip${v === sel ? ' on' : ''}" type="button" data-choice="${f.id}" data-v="${esc(v)}" aria-pressed="${v === sel}">${esc(l)}</button>`).join('')}</div></div>`;
        }
        const val = g ? fmtIn(f, g.value) : '';
        return `<label class="tf${g ? ' said' : ''}"><span class="tf-label">${esc(f.label)}${g ? `<small class="said-note" title="${esc(g.quote)}">you said</small>` : f.optional ? ' <small>optional</small>' : ''}</span><input id="af-${f.id}" type="text" inputmode="${f.kind === 'count' ? 'numeric' : 'decimal'}" autocomplete="off" value="${esc(val)}" placeholder="${esc(f.example || '')}"></label>`;
      };
      const main = entry.fields.filter(f => !f.optional || given[f.id]), more = entry.fields.filter(f => f.optional && !given[f.id]);
      const filled = (r.inputs || []).length;
      out.innerHTML = head(entry, r, `<p class="fine">${filled ? `${filled === 1 ? 'One number' : filled + ' numbers'} came from what you wrote, marked "you said". Check them, fill in the rest, and the answer updates as you type.` : "Fill in your numbers and the answer updates as you type."}</p>`)
        + `<div class="calc ask-calc"><div class="calc-out" id="aOut" aria-live="polite"></div><form class="calc-in" id="aForm" autocomplete="off" novalidate>${main.map(field).join('')}${more.length ? `<details class="more-fields"><summary>More details <span>optional</span></summary>${more.map(field).join('')}</details>` : ''}</form><div class="calc-out2" id="aOut2"></div></div><div id="aExplain"></div>`;
      const fm = $('aForm'); chipGroup(fm);
      const read = () => {
        const v = {};
        entry.fields.forEach(f => { v[f.id] = f.kind === 'choice' ? (choiceOf(fm, f.id) || f.example) : (parse[f.kind] || String)(($('af-' + f.id) || {}).value || ''); });
        if (entry.kind === 'pipeline') { v.yearEnd = v.yearEnd || 'cy'; v.wtd = 0; }
        return v;
      };
      const inputsShown = () => entry.fields.map(f => ({ label: f.label, value: f.kind === 'choice' ? ((f.options.find(o => o[0] === (choiceOf(fm, f.id) || f.example)) || [])[1] || '') : (($('af-' + f.id) || {}).value || '').trim() })).filter(x => x.value);
      let last = null;
      const render = () => {
        const v = read();
        last = entry.kind === 'pipeline' ? pipelineResult(cfg, v) : calcResult(cfg, v);
        const o = $('aOut'), o2 = $('aOut2');
        if (!last || last.msg) { o.innerHTML = `<div class="empty">${esc((last && last.msg) || 'Fill in the numbers below.')}</div>`; o2.innerHTML = ''; $('aExplain').innerHTML = ''; return; }
        o.innerHTML = `<div class="verdict verdict-${last.cls}" id="aVerdict">${last.big ? `<div class="verdict-number">${esc(last.big)}</div><div class="verdict-label">${esc(last.answer)}</div>` : `<div class="verdict-word">${esc(last.answer)}</div>`}<div class="verdict-attack">${esc(last.attack)}</div>${last.sub ? `<div class="verdict-sub">${esc(last.sub)}</div>` : ''}</div>`;
        o2.innerHTML = `<div class="list" aria-label="The numbers">${last.rows.map(rw => `<div class="list-item"><span class="headline">${esc(rw[0])}</span><span class="trailing strong">${esc(rw[1])}</span></div>`).join('')}</div>${last.note ? `<p class="clock">${esc(last.note)}</p>` : ''}
          <button class="btn btn-primary btn-lg btn-full" id="aExplainBtn" type="button">Explain it</button>
          <p class="startnote"><a href="${esc(fullLink(entry, cfg, v))}">Open the full ${esc(entry.name)} →</a></p>`;
        $('aExplainBtn').onclick = () => explain(entry, last, inputsShown());
        if (window.innerWidth >= 960) {} // desktop layout comes from CSS
      };
      fm.addEventListener('input', () => { $('aExplain').innerHTML = ''; render(); });
      fm.addEventListener('qbchoice', () => { $('aExplain').innerHTML = ''; render(); });
      fm.addEventListener('submit', (e) => e.preventDefault());
      render(); scrollTo(out);
    }
    function calcResult(cfg, v) {
      let s; try { s = cfg.compute(v); } catch { return { msg: 'Check the numbers.' }; }
      if (!s || s.msg) return s || null;
      const answer = (cfg.answers && cfg.answers[s.label]) || s.label;
      return { cls: s.cls, big: s.big || '', answer, attack: s.attack || '', sub: s.sub || '', note: s.note || '', rows: (s.rows || []).map(r => [String(r[0]), String(r[1])]) };
    }
    function pipelineResult(T, i) {
      const s = T.compute(i); if (!s) return { msg: 'Put in your target and the pipeline you expect to close against it.' };
      if (s.done) return { cls: 'ready', big: '', answer: 'Made it', attack: `You've closed ${T.money(s.closed)} against ${T.money(s.goal)}.`, sub: 'Go protect next year.', rows: [['Closed', T.money(s.closed)], ['Target', T.money(s.goal)]] };
      const rows = [['You have', T.money(s.pipe)], ['3X says you need', T.money(s.req3) + (s.gap3 ? ' · ' + T.money(s.gap3) + ' short' : ' · covered')]];
      if (s.win) rows.push([`Your ${T.pct(s.win)} win rate says`, T.money(s.need) + (s.gap ? ' · ' + T.money(s.gap) + ' short' : ' · covered')]);
      rows.push(['The gap', s.gap ? T.money(s.gap) + (s.deals ? ' · ' + s.deals + ' deals' : '') : 'None']);
      if (s.closed) rows.push(['Already closed', T.money(s.closed)]);
      if (s.slip) rows.push(['If your biggest deal slips', T.X(s.slip.cov) + ' · ' + (s.slip.gap ? T.money(s.slip.gap) + ' short' : 'still covered')]);
      if (s.perRep) rows.push([s.reps === 1 ? 'For you' : 'Per seller', T.money(s.perRep) + (s.deals && s.reps > 1 ? ' · ' + Math.ceil(s.deals / s.reps) + ' deals' : '')]);
      const cal = s.cal;
      return { cls: s.cls, big: T.X(s.cov), answer: (T.answers && T.answers[s.label]) || s.label, attack: s.flip, sub: s.sub, rows,
               note: i.yearEnd === 'fy' ? `Your year ends in ${cal.daysLeft} days.` : `Your year has ${cal.daysLeft} days left.` };
    }
    function fullLink(entry, cfg, v) {
      if (entry.kind === 'pipeline') {
        const p = new URLSearchParams();
        if (v.goal) p.set('t', Math.round(v.goal)); if (v.pipe) p.set('p', Math.round(v.pipe)); if (v.win) p.set('w', Math.round(v.win * 100));
        if (v.size) p.set('s', Math.round(v.size)); if (v.reps) p.set('n', v.reps); if (v.closed) p.set('c', Math.round(v.closed)); if (v.big) p.set('b', Math.round(v.big)); p.set('y', v.yearEnd || 'cy');
        return entry.url + '#' + p.toString();
      }
      const p = new URLSearchParams();
      entry.fields.forEach(f => { const x = v[f.id]; if (x !== 0 && x !== '' && x != null) p.set(f.id, (f.kind === 'pct' || f.kind === 'pctx') ? Math.round(x * 1000) / 10 : f.kind === 'money' ? Math.round(x) : x); });
      return entry.url + '#' + p.toString();
    }

    /* question tools and Deal Check: five questions, answered by the person, scored by the tool's own code */
    function showCheck(entry, cfg, r) {
      const Q = entry.questions, ans = {};
      out.innerHTML = head(entry, r, '<p class="fine">Five questions. You answer them, not the AI. Tap one answer for each.</p>')
        + `<div class="ask-qs">${Q.map((q, i) => `<div class="ask-q"><span class="overline">${esc(q.n)} · ${i + 1} of ${Q.length}</span><p class="ask-qt">${esc(q.q)}</p><div class="chips" role="group" aria-label="${esc(q.q)}">${['yes', 'sort', 'no'].map(v => `<button class="chip" type="button" data-choice="${q.k}" data-v="${v}" aria-pressed="false">${{ yes: 'Yes', sort: 'Sort of', no: 'No' }[v]}</button>`).join('')}</div></div>`).join('')}</div><div id="aRes"></div><div id="aExplain"></div>`;
      const box = out.querySelector('.ask-qs'); chipGroup(box);
      box.addEventListener('qbchoice', () => {
        Q.forEach(q => { ans[q.k] = choiceOf(box, q.k); });
        $('aExplain').innerHTML = '';
        if (Q.some(q => !ans[q.k])) { $('aRes').innerHTML = ''; const nxt = Q.find(q => !ans[q.k]); return; }
        const s = entry.kind === 'deal' ? cfg.score(ans) : window.QBCheckScore(cfg, ans);
        const answer = (cfg.answers && cfg.answers[s.label]) || s.label;
        const WORD = { yes: 'Yes', sort: 'Sort of', no: 'No' };
        const grill = entry.kind === 'deal' ? (cfg.grill[s.weak.k] || [])[0] : (cfg.grill || {})[s.weak.k];
        const first = (s.moves && s.moves[0]) || cfg.noMove || '';
        const code = Q.map(q => ({ yes: 'y', sort: 's', no: 'n' })[ans[q.k]]).join('');
        const res = { cls: s.cls, answer, attack: s.attack || '', sub: s.sub || '', meta: s.meta || '', rows: [], answers: Q.map(q => ({ n: q.n, a: WORD[ans[q.k]] })), moves: (s.moves || []).slice(0, 3) };
        $('aRes').innerHTML = `<div class="verdict verdict-${s.cls}"><div class="verdict-word">${esc(answer)}</div><div class="verdict-meta">${esc(s.meta || '')}</div><div class="verdict-attack">${esc(s.attack || '')}</div>${s.sub ? `<div class="verdict-sub">${esc(s.sub)}</div>` : ''}</div>
          <div class="card">${grill ? `<span class="overline">${esc(cfg.askedBy || 'Your boss will ask')}</span><p class="lede">“${esc(grill)}”</p>` : ''}${first ? `<span class="overline" style="margin-top:16px;">Do this first</span><p class="lede">${esc(first)}</p>` : ''}</div>
          <button class="btn btn-primary btn-lg btn-full" id="aExplainBtn" type="button" style="margin-top:16px;">Explain it</button>
          <p class="startnote"><a href="${entry.url}#${code}">Open the full ${esc(entry.name)} →</a></p>`;
        $('aExplainBtn').onclick = () => explain(entry, res, []);
        scrollTo($('aRes'));
      });
      scrollTo(out);
    }

    async function explain(entry, res, inputs) {
      const box = $('aExplain'), b = $('aExplainBtn');
      busy(b, true, 'Explaining…'); box.innerHTML = '';
      track('ask_explain');
      const { data, error } = await post({ kind: 'qb_explain', question, slug: entry.slug, inputs, result: res });
      busy(b, false);
      if (error) return errorBox(box, error);
      const x = data.explain || {};
      const sec = (h, items) => items && items.length ? `<h3>${h}</h3><ul class="ask-list">${items.map(i => `<li>${esc(i.text)}${src(i.label)}</li>`).join('')}</ul>` : '';
      box.innerHTML = `<div class="card ask-explain" tabindex="-1">${sec('What stands out', x.see)}${sec("What's wrong", x.wrong)}${sec('What to do next', x.next)}
        <p class="fine ask-foot">Written by AI from the numbers above. The math is QuotaBird's. "A guess" means exactly that.${x.trimmed ? ' A line with a number that wasn\'t yours or the tool\'s was left out.' : ''}</p></div>`;
      if (b) b.hidden = true;
      const card = box.querySelector('.ask-explain'); scrollTo(card); try { card.focus({ preventScroll: true }); } catch {}
    }
  }

  /* ═════════════════════════ The workflow pages ═════════════════════════ */
  const MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
  const MNAME = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function quarters(start) {   // start: 1..12, the first month of the customer's fiscal year
    return [0, 1, 2, 3].map(q => { const a = (start - 1 + q * 3) % 12, b = (a + 2) % 12; return `Q${q + 1} (${MNAME[a]} to ${MNAME[b]})`; });
  }
  function parseOpps(text) {
    const pm = P().money || ((x) => 0);
    return String(text || '').split('\n').map(l => l.trim()).filter(Boolean).slice(0, 25).map(l => {
      const name = l.split(/[,;|\t]/)[0].replace(/\$.*$/, '').trim() || l.slice(0, 40);
      const m = l.match(/\$\s?\d[\d,]*(?:\.\d+)?\s?[kmb]?\b|\b\d[\d,]*(?:\.\d+)?\s?[kmb]\b/i);
      const value = m ? pm(m[0]) : 0;
      // whole month names or their usual short forms only, so "decision" or "marketing" never reads as a month
      const mo = l.toLowerCase().match(/\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b\.?/);
      return { name, value, month: mo ? MONTHS.indexOf(mo[1].slice(0, 3)) + 1 : 0 };
    });
  }

  function wfPage() {
    const page = CFG.page, form = $('wfForm'), btn = $('wfBtn'), out = $('wfOut'), mathBox = $('wfMath');
    chipGroup(form);
    const val = (id) => (($(id) || {}).value || '').trim();
    // prefill from Ask QuotaBird (#p=...), then clear the address so a reload starts clean
    const m = (location.hash || '').match(/^#p=([A-Za-z0-9_-]+)$/);
    if (m) {
      const pre = b64.dec(m[1]) || {};
      Object.entries(pre).forEach(([k, v]) => {
        if (typeof v !== 'string' || !/^[a-z]+$/i.test(k)) return;
        const el = form.querySelector(`input#${k}, textarea#${k}`);              // only this form's own fields
        if (el) { el.value = v.slice(0, +el.maxLength > 0 ? +el.maxLength : 2000); return; }
        const want = k === 'federal' ? (/yes|true|federal/i.test(v) ? 'yes' : 'no') : k === 'type' ? ({ forecast: 'forecast', miss: 'miss', monthly: 'monthly' }[(v.match(/forecast|miss|monthly/i) || [''])[0].toLowerCase()] || 'weekly') : v;
        const b = form.querySelector(`[data-choice="${k}"][data-v="${CSS.escape(want)}"]`); if (b) b.click();
      });
      try { history.replaceState(null, '', location.pathname); } catch {}
      track(page.replace(/-/g, '_') + '_from_ask');
    }
    if (page !== 'update-upward' && !choiceOf(form, 'federal')) { const b = form.querySelector('[data-choice="federal"][data-v="no"]'); if (b) { b.classList.add('on'); } }
    form.querySelectorAll('textarea').forEach(t => { const fit = () => { t.style.height = 'auto'; t.style.height = t.scrollHeight + 2 + 'px'; }; t.addEventListener('input', fit); fit(); });

    /* the page's own math, shown as you type and sent with the request; the AI can't change it */
    let math = { lines: [], quarters: [] };
    const pm = (id) => (P().money || (() => 0))(val(id));
    function doMath() {
      if (page === 'account-plan') {
        const T = pm('target'), w = (P().pct || (() => 0))(val('win')), fy = +(choiceOf(form, 'fy') || (choiceOf(form, 'federal') === 'yes' ? 10 : 1));
        const opps = parseOpps(val('opps')), pipe = opps.reduce((s, o) => s + o.value, 0);
        const qs = quarters(fy), byQ = [0, 0, 0, 0]; let undated = 0;
        opps.forEach(o => { if (!o.month) { undated += o.value; return; } byQ[Math.floor(((o.month - fy + 12) % 12) / 3)] += o.value; });
        const lines = [];
        if (T) lines.push(['Your number', money(T)]);
        if (opps.length) lines.push(['Open pipeline', `${money(pipe)} · ${opps.length} ${opps.length === 1 ? 'deal' : 'deals'}`]);
        if (T && pipe) lines.push(['Coverage', (pipe / T).toFixed(1) + 'X']);
        if (T && w) { const need = T / w, gap = Math.max(0, need - pipe); lines.push([`At your ${pct(w)} win rate you need`, money(need) + ' of pipeline']); lines.push(['The gap', gap ? money(gap) : 'None, you\'re covered']); }
        qs.forEach((q, i) => { if (byQ[i]) lines.push([`Closing in ${q}`, money(byQ[i])]); });
        if (undated) lines.push(['No close month given', money(undated)]);
        math = { lines, quarters: qs };
      } else if (page === 'update-upward') {
        const T = pm('target'), C = pm('closed'), F = pm('forecast'), lines = [];
        if (T) lines.push(['Your number', money(T)]);
        if (T && C) lines.push(['Closed so far', `${money(C)} · ${pct(C / T)} of the number`]);
        if (T && C < T) lines.push(['Left to close', money(T - C)]);
        if (T && C >= T) lines.push(['Over the number by', money(C - T)]);
        if (T && F) lines.push(['Your call', `${money(F)} · ${pct(F / T)} of the number`]);
        if (T && F && F < T) lines.push(['Short at your call', money(T - F)]);
        math = { lines, quarters: [] };
      }
      if (mathBox) mathBox.innerHTML = math.lines.length ? `<div class="list wf-math" aria-label="The math"><div class="list-item compact"><span class="headline">The math, done here</span></div>${math.lines.map(([k, v]) => `<div class="list-item"><span class="headline">${esc(k)}</span><span class="trailing strong">${esc(v)}</span></div>`).join('')}</div>` : '';
    }
    form.addEventListener('input', doMath); form.addEventListener('qbchoice', doMath); doMath();

    const fields = () => {
      const f = {}; form.querySelectorAll('input[id], textarea[id]').forEach(el => { f[el.id] = el.value.trim(); });
      form.querySelectorAll('[data-choice].on').forEach(b => { f[b.dataset.choice] = b.dataset.v; });
      return f;
    };
    const REQ = { 'meeting-prep': [['customer', 'the customer'], ['objective', 'what you want out of the meeting']], 'account-plan': [['account', 'the account'], ['target', 'your number for it']], 'update-upward': [['target', 'your number']] };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const miss = (REQ[page] || []).filter(([id]) => !val(id));
      if (miss.length) { errorBox(out, 'Add ' + miss.map(x => x[1]).join(' and ') + ' first.'); $(miss[0][0]).focus(); return; }
      busy(btn, true, 'Working on it…'); out.innerHTML = '<div class="ask-wait"><span class="dot"></span> Working on it. This takes about ten seconds.</div>';
      track(page.replace(/-/g, '_') + '_run');
      const kind = { 'meeting-prep': 'qb_meeting_prep', 'account-plan': 'qb_account_plan', 'update-upward': 'qb_update_upward' }[page];
      const { data, error } = await post({ kind, fields: fields(), math });
      busy(btn, false);
      if (error) { track(page.replace(/-/g, '_') + '_error'); return errorBox(out, error); }
      if (page === 'meeting-prep') renderMeeting(data.meeting || {});
      else if (page === 'account-plan') renderPlan(data.plan || {});
      else renderUpdate(data.update || {});
    });

    const ul = (items, f = (x) => esc(x)) => items && items.length ? `<ul class="ask-list">${items.map(i => `<li>${f(i)}</li>`).join('')}</ul>` : '';
    const foot = (x) => `<p class="fine ask-foot">Written by AI from what you typed. ${page === 'meeting-prep' ? '' : 'The math is QuotaBird\'s. '}"A guess" means exactly that: check it before you say it out loud.${x.trimmed ? ' A line with a number that wasn\'t yours was left out.' : ''}</p>`;
    function finish(html, textFn) {
      out.innerHTML = `<div class="wf-out" tabindex="-1">${html}</div>`;
      actions(out, textFn, page.replace(/-/g, '_'));
      const card = out.querySelector('.wf-out'); scrollTo(card); try { card.focus({ preventScroll: true }); } catch {}
    }
    const T = (h, items, f = (x) => x) => items && items.length ? `\n${h.toUpperCase()}\n` + items.map(i => '- ' + f(i)).join('\n') + '\n' : '';
    const lbl = (i) => i.text + (i.label && LABEL[i.label] ? ` (${LABEL[i.label].toLowerCase()})` : '');

    function renderMeeting(x) {
      const sections = `
        ${x.objective ? `<div class="card wf-lead"><span class="overline">The objective</span><p class="lede">${esc(x.objective)}</p></div>` : ''}
        <div class="card">${x.known && x.known.length ? `<h3>What you know</h3>${ul(x.known, (t) => esc(t) + src('you_said'))}` : ''}${x.unknown && x.unknown.length ? `<h3>What you don't know yet</h3>${ul(x.unknown)}` : ''}</div>
        ${x.priorities && x.priorities.length ? `<div class="card"><h3>What they probably care about</h3>${ul(x.priorities, (i) => esc(i.text) + src(i.label))}</div>` : ''}
        <div class="card"><h3>Questions to ask</h3><ol class="ask-list">${(x.questions || []).map(q => `<li>${esc(q)}</li>`).join('')}</ol></div>
        ${x.objections && x.objections.length ? `<div class="card"><h3>Objections to expect</h3>${ul(x.objections, (o) => `<strong>${esc(o.objection)}</strong><br>${esc(o.answer)}`)}</div>` : ''}
        ${x.landmines && x.landmines.length ? `<div class="card"><h3>Landmines</h3>${ul(x.landmines)}</div>` : ''}
        ${x.next_step ? `<div class="card wf-lead"><span class="overline">The next step to ask for</span><p class="lede">${esc(x.next_step)}</p></div>` : ''}
        ${foot(x)}`;
      finish(sections, () => `MEETING PREP: ${val('customer')}\n` + (x.objective ? `\nOBJECTIVE\n${x.objective}\n` : '') + T('What you know', x.known) + T("What you don't know yet", x.unknown)
        + T('What they probably care about', x.priorities, lbl) + T('Questions to ask', x.questions) + T('Objections to expect', x.objections, (o) => `${o.objection} → ${o.answer}`) + T('Landmines', x.landmines) + (x.next_step ? `\nTHE NEXT STEP TO ASK FOR\n${x.next_step}\n` : ''));
      track('meeting_prep_done');
    }
    function renderPlan(x) {
      const mathHtml = math.lines.length ? `<div class="list" aria-label="The math"><div class="list-item compact"><span class="headline">QuotaBird math</span></div>${math.lines.map(([k, v]) => `<div class="list-item"><span class="headline">${esc(k)}</span><span class="trailing strong">${esc(v)}</span></div>`).join('')}</div>` : '';
      const sections = `
        ${x.summary ? `<div class="card wf-lead"><span class="overline">${esc(val('account'))}</span><p class="lede">${esc(x.summary)}</p></div>` : ''}
        ${mathHtml}
        ${x.priorities && x.priorities.length ? `<div class="card"><h3>Their priorities, and where you fit</h3>${ul(x.priorities, (i) => esc(i.text) + src(i.label))}</div>` : ''}
        ${x.plays && x.plays.length ? `<div class="card"><h3>How you close the gap</h3>${ul(x.plays, (i) => esc(i.text) + src(i.label))}</div>` : ''}
        ${x.gaps && x.gaps.length ? `<div class="card"><h3>What you don't know yet</h3>${ul(x.gaps)}</div>` : ''}
        ${x.who_to_meet && x.who_to_meet.length ? `<div class="card"><h3>Who to meet next</h3>${ul(x.who_to_meet, (w) => `<strong>${esc(w.who)}</strong>. ${esc(w.why)}`)}</div>` : ''}
        ${x.milestones && x.milestones.length ? `<div class="list" aria-label="Milestones"><div class="list-item compact"><span class="headline">Milestones, on their fiscal year</span></div>${x.milestones.map(mm => `<div class="list-item ms"><span class="trailing">${esc(mm.quarter)}</span><span class="headline">${esc(mm.text)}</span></div>`).join('')}</div>` : ''}
        ${x.next_actions && x.next_actions.length ? `<div class="card wf-lead"><h3>The next two weeks</h3>${ul(x.next_actions)}</div>` : ''}
        ${foot(x)}`;
      finish(sections, () => `ACCOUNT PLAN: ${val('account')}\n` + (x.summary ? `\n${x.summary}\n` : '') + T('QuotaBird math', math.lines, (l) => `${l[0]}: ${l[1]}`) + T('Their priorities, and where you fit', x.priorities, lbl)
        + T('How you close the gap', x.plays, lbl) + T("What you don't know yet", x.gaps) + T('Who to meet next', x.who_to_meet, (w) => `${w.who}: ${w.why}`) + T('Milestones', x.milestones, (mm) => `${mm.quarter}: ${mm.text}`) + T('The next two weeks', x.next_actions));
      track('account_plan_done');
    }
    function renderUpdate(x) {
      const mathHtml = math.lines.length ? `<div class="list" aria-label="The numbers">${math.lines.map(([k, v]) => `<div class="list-item"><span class="headline">${esc(k)}</span><span class="trailing strong">${esc(v)}</span></div>`).join('')}</div>` : '';
      const sections = `
        ${x.headline ? `<div class="card wf-lead"><span class="overline">${esc({ weekly: 'Weekly update', forecast: 'Forecast call', miss: 'Calling a miss', monthly: 'Monthly review' }[x.type] || 'Update')}${val('period') ? ' · ' + esc(val('period')) : ''}</span><p class="lede">${esc(x.headline)}</p></div>` : ''}
        ${mathHtml}
        ${x.deals && x.deals.length ? `<div class="card"><h3>Top deals</h3>${ul(x.deals, (d) => `<strong>${esc(d.name)}</strong>. ${esc(d.status)}${d.next ? ` Next: ${esc(d.next)}` : ''}`)}</div>` : ''}
        ${x.blockers && x.blockers.length ? `<div class="card"><h3>What's in the way, and what I need</h3>${ul(x.blockers, (b) => `${esc(b.blocker)}<br><strong>Ask:</strong> ${esc(b.ask)}`)}</div>` : ''}
        ${x.recovery && x.recovery.length ? `<div class="card"><h3>What I've done, and the plan</h3>${ul(x.recovery)}</div>` : ''}
        ${x.questions && x.questions.length ? `<div class="card ask-prep"><h3>Your boss will ask</h3>${ul(x.questions, (q) => `<strong>${esc(q.q)}</strong><br>${esc(q.a)}`)}</div>` : ''}
        ${foot(x)}`;
      // what gets copied is the update itself, ready to paste; the boss's questions are prep, so they stay out
      finish(sections, () => (x.headline ? x.headline + '\n' : '') + (math.lines.length ? '\n' + math.lines.map(l => `${l[0]}: ${l[1]}`).join('\n') + '\n' : '')
        + T('Top deals', x.deals, (d) => `${d.name}: ${d.status}${d.next ? ' Next: ' + d.next : ''}`) + T("What's in the way, and what I need", x.blockers, (b) => `${b.blocker} Ask: ${b.ask}`) + T("What I've done, and the plan", x.recovery));
      track('update_upward_done');
    }
  }

  function init() { if (CFG.page === 'ask-quotabird') askPage(); else if (CFG.page) wfPage(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
