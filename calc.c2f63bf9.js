/* calc.js: the live-calculator engine behind Quota Check, Discount Check and Commission Check.
   A page passes a config: fields (with example values), compute(values) → a verdict and rows,
   plus DM, booking note and hand-off. Everything updates on input; nothing is stored. */
'use strict';
(function () {
  const track = (n) => { if (typeof window.qbTrack === 'function') window.qbTrack(n); else (window.qbTrackQ = window.qbTrackQ || []).push(n); };
  const esc = (s) => String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const $ = (id) => document.getElementById(id);
  function parseMoney(raw) {
    if (!raw) return 0;
    let s = String(raw).toLowerCase().replace(/[\s,$_]/g, ''), mult = 1;
    if (/b$/.test(s)) { mult = 1e9; s = s.slice(0, -1); } else if (/m$/.test(s)) { mult = 1e6; s = s.slice(0, -1); } else if (/k$/.test(s)) { mult = 1e3; s = s.slice(0, -1); }
    const n = parseFloat(s); return (!isFinite(n) || n < 0) ? 0 : n * mult;
  }
  // percentages that can run past 100% (accelerators, caps): "150%", "150" and "1.5" all mean 1.5
  function parsePctX(raw) { let n = parseFloat(String(raw || '').replace(/[^0-9.]/g, '')); if (!isFinite(n) || n <= 0) return 0; return n > 10 ? n / 100 : n; }
  function parsePct(raw) { let n = parseFloat(String(raw || '').replace(/[^0-9.]/g, '')); if (!isFinite(n) || n < 0) return 0; if (n > 1) n = n / 100; return n < 1 ? n : 0; }
  function money(n) {
    if (!isFinite(n)) return '$0'; const neg = n < 0; n = Math.abs(n); let t;
    if (n >= 1e9) t = '$' + (n / 1e9).toFixed(2).replace(/\.?0+$/, '') + 'B';
    else if (n >= 1e6) t = '$' + (n / 1e6).toFixed(n >= 1e7 ? 1 : 2).replace(/\.?0+$/, '') + 'M';
    else if (n >= 1e3) t = '$' + Math.round(n / 1e3) + 'K';
    else t = '$' + Math.round(n);
    return (neg ? '-' : '') + t;
  }
  const pct = (r) => Math.round(r * 100) + '%';

  /* Money fields format as you type ($10,000,000), keep the caret where it was, and still accept
     shorthand like 10m or 500k (left alone until you leave the field). */
  const fullMoney = (n) => '$' + Math.round(n).toLocaleString('en-US');
  function liveMoney(el) {
    const raw = el.value;
    if (/[a-zA-Z]/.test(raw)) return;
    const digitsBefore = raw.slice(0, el.selectionStart || 0).replace(/[^0-9]/g, '').length;
    const s = raw.replace(/[^0-9.]/g, ''); const dot = s.indexOf('.');
    let ip = (dot >= 0 ? s.slice(0, dot) : s).replace(/^0+(?=\d)/, ''); const fr = dot >= 0 ? '.' + s.slice(dot + 1).replace(/\./g, '') : '';
    const out = (ip || fr) ? '$' + ip.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + fr : '';
    if (out === raw) return;
    el.value = out;
    let pos = 0, seen = 0; while (pos < out.length && seen < digitsBefore) { if (/[0-9]/.test(out[pos])) seen++; pos++; }
    try { el.setSelectionRange(pos, pos); } catch (e) {}
  }
  function copyText(text) {
    try {
      const ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;font-size:16px;';
      document.body.appendChild(ta);
      if (/iP(hone|ad|od)/.test(navigator.userAgent)) { ta.contentEditable = 'true'; ta.readOnly = false; const r = document.createRange(); r.selectNodeContents(ta); const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); ta.setSelectionRange(0, text.length); }
      else ta.select();
      const ok = document.execCommand('copy'); document.body.removeChild(ta); if (ok) return Promise.resolve();
    } catch (e) {}
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return Promise.reject(new Error('no clipboard'));
  }
  function shareOut(btn, block, title) {
    const lines = block.split('\n'), url = lines[lines.length - 1], text = lines.slice(0, -1).join('\n').trim();
    const touch = window.matchMedia && matchMedia('(pointer: coarse)').matches;
    const copy = () => copyText(block).then(() => { btn.textContent = 'Copied ✓'; }).catch(() => { btn.textContent = "Couldn't copy"; });
    if (navigator.share && touch) navigator.share({ title, text, url }).then(() => { btn.textContent = 'Shared ✓'; }).catch((e) => { if (!e || e.name !== 'AbortError') copy(); }); else copy();
  }
  document.addEventListener('click', (e) => { document.querySelectorAll('details.menu[open]').forEach(d => { if (!d.contains(e.target)) d.open = false; }); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') document.querySelectorAll('details.menu[open]').forEach(d => { d.open = false; d.querySelector('summary').focus(); }); });

  // the big result number stays on one line: shrink it just enough to fit its card ("+$98K", "$12.4M")
  function fitBig(root) { const el = root && root.querySelector('.verdict-number'); if (!el) return; el.style.fontSize = ''; let s = parseFloat(getComputedStyle(el).fontSize) || 96; while (el.scrollWidth > el.clientWidth + 1 && s > 34) { s -= 3; el.style.fontSize = s + 'px'; } }
  window.addEventListener('resize', () => document.querySelectorAll('.verdict').forEach(v => fitBig(v.parentNode)));
  window.CalcTool = function (cfg) {
    const answerOf = (s) => (cfg.answers && cfg.answers[s.label]) || s.label;   // the verdict, worded as an answer to the tool's question
    const F = cfg.fields; let shared = false, touched = false, lastS = null, prevLabel = null; const fromHash = new Set();
    const fmt = { money: fullMoney, pct: (r) => (r * 100).toFixed(1).replace(/\.0$/, '') + '%', pctx: (r) => (r * 100).toFixed(1).replace(/\.0$/, '') + '%', count: String, choice: String };
    const parse = { money: parseMoney, pct: parsePct, pctx: parsePctX, count: (v) => Math.max(0, parseInt(String(v || '').replace(/[^0-9]/g, ''), 10) || 0), choice: (v) => v };
    const read = () => { const v = {}; F.forEach(f => { v[f.id] = f.kind === 'choice' ? (document.querySelector(`[data-choice="${f.id}"].on`) || {}).dataset?.v ?? f.example : parse[f.kind]($(f.id).value); }); return v; };
    const encode = () => { const p = new URLSearchParams(); const v = read(); F.forEach(f => { if (v[f.id] !== 0 && v[f.id] !== '' && v[f.id] != null) p.set(f.id, (f.kind === 'pct' || f.kind === 'pctx') ? Math.round(v[f.id] * 1000) / 10 : f.kind === 'money' ? Math.round(v[f.id]) : v[f.id]); }); return p.toString(); };
    function readHash() {
      const h = (location.hash || '').replace(/^#/, ''); if (!h || !/=/.test(h)) return false;
      const p = new URLSearchParams(h); let any = false;
      // a shared link describes the whole form: a field it leaves out was blank for the sender, so it's blank here too, never an example
      if (F.some(f => p.has(f.id))) F.forEach(f => { if (f.kind !== 'choice' && !p.has(f.id) && $(f.id)) { $(f.id).value = ''; $(f.id).classList.remove('is-example'); } });
      F.forEach(f => { if (!p.has(f.id)) return; any = true; fromHash.add(f.id); const raw = p.get(f.id);
        if (f.kind === 'choice') document.querySelectorAll(`[data-choice="${f.id}"]`).forEach(b => { b.classList.toggle('on', b.dataset.v === raw); b.setAttribute('aria-pressed', b.dataset.v === raw ? 'true' : 'false'); });
        else $(f.id).value = (f.kind === 'pct' || f.kind === 'pctx') ? fmt[f.kind](parse[f.kind](raw)) : f.kind === 'money' ? fullMoney(parseMoney(raw)) : raw; });
      return any;
    }
    const shareLink = () => (location.origin && location.origin !== 'null' ? location.origin + location.pathname : cfg.url) + '#' + encode();
    const shareBlock = (s) => `${cfg.name} · ${answerOf(s)}\n${s.attack}\n` + s.rows.map(r => `${r[0]}: ${r[1]}`).join('\n') + '\n' + shareLink();
    function render() {
      const s = cfg.compute(read()); lastS = s; const out = $('out');
      const sameVerdict = !!(s && prevLabel && prevLabel === s.label); prevLabel = s ? s.label : null;
      if (s && s.msg) { lastS = null; prevLabel = null; }
      if (!s || s.msg) { out.innerHTML = `<div class="empty">${esc((s && s.msg) || cfg.emptyText || 'Fill in the numbers below.')}</div>`; const o2 = $('out2'); if (o2) o2.innerHTML = ''; strip(null); return; }
      const h = typeof cfg.handoff === 'function' ? cfg.handoff(s) : cfg.handoff;
      out.innerHTML = `
    ${shared ? `<div class="banner">Someone sent you these numbers. Change any of them to run your own.</div>` : ''}
    <div class="verdict verdict-${s.cls}" id="verdict">
      ${s.big ? `<div class="verdict-number">${esc(s.big)}</div><div class="verdict-label">${esc(answerOf(s))}</div>` : `<div class="verdict-word">${esc(answerOf(s))}</div>`}
      <div class="verdict-attack">${esc(s.attack)}</div>
      ${s.sub ? `<div class="verdict-sub">${esc(s.sub)}</div>` : ''}
    </div>`;
      fitBig(out); out.classList.toggle('no-anim', sameVerdict);   // the pop plays when the verdict changes, not on every keystroke
      const out2 = $('out2') || out;
      out2.innerHTML = `
    <div class="list" aria-label="The numbers">${s.rows.map(r => `<div class="list-item"><span class="headline">${esc(r[0])}</span><span class="trailing strong${r[2] ? ' ' + r[2] : ''}">${esc(r[1])}</span></div>`).join('')}</div>
    ${s.note ? `<p class="clock">${esc(s.note)}</p>` : ''}
<div class="card mark-card" style="margin-top:20px;">
      <h3>${esc(cfg.mark.title(s))}</h3>
      <p>${esc(cfg.mark.body)}</p>
      <a class="btn btn-primary btn-lg btn-full" id="bookBtn" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium=${cfg.slug}&utm_content=after_score&a1=${encodeURIComponent(cfg.bookNote(s))}" target="_blank" rel="noopener" style="margin-top:14px;">Grab 20 minutes</a>
      <p class="dm-alt"><button class="linkbtn" id="dmBtn" type="button">or message me on LinkedIn</button></p>
      <p class="fine" style="text-align:center;margin:8px 0 0;">It's free, and if I can't help, I'll say so. The LinkedIn link copies a short note you can paste.</p>
      ${(() => { const o = cfg.offer && cfg.offer(s); return o ? `<p class="offer-line">${esc(o.text)} <a href="${o.href}">${esc(o.label)} →</a></p>` : ''; })()}
    </div>
        ${h ? `<div class="card card-accent"><span class="overline">${esc(h.overline)}</span><p class="lede">${esc(h.text)}</p><a class="btn btn-tonal btn-full" href="${h.href}" style="margin-top:14px;">${esc(h.label)}</a></div>` : ''}
    <div class="btn-row center" style="margin-top:8px;"><button class="btn btn-text" id="copy" type="button">Share</button></div>
    `;
      $('copy').onclick = (e) => { track(cfg.slug + '_share'); try { history.replaceState(null, '', '#' + encode()); } catch {} shareOut(e.currentTarget, shareBlock(s), cfg.name); };
      { const bk = document.getElementById('bookBtn'); if (bk) bk.addEventListener('click', () => track(cfg.slug + '_book')); }
  $('dmBtn').onclick = (e) => { const btn = e.currentTarget; track(cfg.slug + '_dm_copy'); copyText(cfg.dm(s)).then(() => { btn.textContent = 'Copied ✓'; window.open('https://www.linkedin.com/in/markflournoy/', '_blank', 'noopener'); }).catch(() => { btn.textContent = "Couldn't copy"; }); };
      strip(s);
    }
    /* the summary strip: on a phone the answer stays visible while you type */
    let verdictVisible = true, formVisible = true;
    function strip(s) { const b = $('sumbar'); if (!b) return; if (!s) { b.hidden = true; return; } b.className = 'sumbar verdict-' + s.cls; b.innerHTML = `<b>${esc(s.big || s.label)}</b> ${esc(s.big ? (s.bar || s.label.toLowerCase()) : s.stripText || '')}`; b.hidden = verdictVisible || !formVisible; }
    if ('IntersectionObserver' in window && $('sumbar')) {
      // the verdict sits above the fields; the strip carries it while you're down in the fields
      const io = new IntersectionObserver((es) => { es.forEach(e => { if (e.target.id === 'verdict') verdictVisible = e.isIntersecting; else formVisible = e.isIntersecting; }); strip(lastS); }, { threshold: 0.1 });
      const watch = () => { io.disconnect(); const v = $('verdict'); if (v) io.observe(v); const f = $('f'); if (f) io.observe(f); };
      new MutationObserver(watch).observe($('out'), { childList: true });
    }
    const onEdit = () => { if (!touched) { touched = true; track(cfg.slug + '_edit'); const n = $('exnote'); if (n) n.textContent = ''; } if (shared) { shared = false; try { history.replaceState(null, '', location.pathname); } catch {} } render(); };
    F.forEach(f => { if (f.kind === 'choice') return; const el = $(f.id); el.addEventListener('input', () => { if (f.kind === 'money') liveMoney(el); onEdit(); });
      if (f.kind === 'money' && el.value) { const v0 = parseMoney(el.value); if (v0) el.value = fullMoney(v0); }
      el.addEventListener('blur', () => { const v = parse[f.kind](el.value); if (v) el.value = fmt[f.kind](v); });
      el.addEventListener('focus', () => setTimeout(() => { try { el.select(); } catch {} }, 0)); });
    document.querySelectorAll('[data-choice]').forEach(b => b.onclick = () => { document.querySelectorAll(`[data-choice="${b.dataset.choice}"]`).forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); onEdit(); });
    // preset chips fill a field the user can still edit
    document.querySelectorAll('[data-preset-for]').forEach(b => b.onclick = () => { const el = $(b.dataset.presetFor); el.value = b.dataset.v; el.dispatchEvent(new Event('input')); });
    const form = $('f'); if (form) form.addEventListener('submit', (e) => e.preventDefault());
    if (readHash()) { shared = true; touched = true; const n = $('exnote'); const allGiven = F.every(f => f.kind === 'choice' || fromHash.has(f.id) || !$(f.id).value); if (n && allGiven) n.textContent = ''; track(cfg.slug + '_verdict_shared'); }
    // Base, variable and quota carry between tools, remembered in this browser only (localStorage). Never sent anywhere.
    const SHARE = Object.assign({ base: 'base', variable: 'variable', quota: 'quota' }, cfg.share || {});
    const shareIds = F.filter(f => f.kind !== 'choice' && SHARE[f.id] && $(f.id)).map(f => f.id);
    const fromStore = new Set();
    const loadStore = () => { try { return JSON.parse(localStorage.getItem('qb-numbers') || '{}') || {}; } catch (e) { return {}; } };
    const saveStore = () => { try { const st = loadStore(); shareIds.forEach(id => { const el = $(id); if (el && !el.classList.contains('is-example')) { const v = parseMoney(el.value); if (v) st[SHARE[id]] = v; } }); localStorage.setItem('qb-numbers', JSON.stringify(st)); } catch (e) {} };
    if (!shared && shareIds.length) {
      const st = loadStore();
      shareIds.forEach(id => { const v = st[SHARE[id]]; if (v > 0) { $(id).value = fullMoney(v); fromStore.add(id); } });
      if (fromStore.size) { const n = $('exnote'); if (n) { n.innerHTML = 'Your numbers from another QuotaBird tool, remembered in this browser only. <button type="button" class="linkbtn" id="qbForget">Clear them</button>'; const b = $('qbForget'); if (b) b.onclick = () => { try { localStorage.removeItem('qb-numbers'); } catch (e) {} location.reload(); }; } }
    }
    shareIds.forEach(id => $(id).addEventListener('input', () => setTimeout(saveStore, 0)));
    // an optional-details panel opens by itself when one of its fields already has a real value
    document.querySelectorAll('details.more-fields').forEach(d => { if ([...d.querySelectorAll('input')].some(i => fromHash.has(i.id) || fromStore.has(i.id))) d.open = true; });
    // Example values look like defaults (quiet grey) until the user types in that field, so their own numbers stand out.
    F.forEach(f => { if (f.kind === 'choice') return; const el = $(f.id); if (!el) return;
      if (el.value && (!shared || !fromHash.has(el.id)) && !fromStore.has(el.id)) el.classList.add('is-example');
      el.addEventListener('input', () => el.classList.remove('is-example')); });
    window.addEventListener('hashchange', () => { if (readHash()) { shared = true; render(); } });
    render();
    window.QB_TEST = { compute: cfg.compute, read };
  };
})();
