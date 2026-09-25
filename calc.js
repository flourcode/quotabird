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

  window.CalcTool = function (cfg) {
    const F = cfg.fields; let shared = false, touched = false, lastS = null;
    const fmt = { money, pct: (r) => (r * 100).toFixed(1).replace(/\.0$/, '') + '%', count: String, choice: String };
    const parse = { money: parseMoney, pct: parsePct, count: (v) => Math.max(0, parseInt(String(v || '').replace(/[^0-9]/g, ''), 10) || 0), choice: (v) => v };
    const read = () => { const v = {}; F.forEach(f => { v[f.id] = f.kind === 'choice' ? (document.querySelector(`[data-choice="${f.id}"].on`) || {}).dataset?.v ?? f.example : parse[f.kind]($(f.id).value); }); return v; };
    const encode = () => { const p = new URLSearchParams(); const v = read(); F.forEach(f => { if (v[f.id] !== 0 && v[f.id] !== '' && v[f.id] != null) p.set(f.id, f.kind === 'pct' ? Math.round(v[f.id] * 1000) / 10 : f.kind === 'money' ? Math.round(v[f.id]) : v[f.id]); }); return p.toString(); };
    function readHash() {
      const h = (location.hash || '').replace(/^#/, ''); if (!h || !/=/.test(h)) return false;
      const p = new URLSearchParams(h); let any = false;
      F.forEach(f => { if (!p.has(f.id)) return; any = true; const raw = p.get(f.id);
        if (f.kind === 'choice') document.querySelectorAll(`[data-choice="${f.id}"]`).forEach(b => b.classList.toggle('on', b.dataset.v === raw));
        else $(f.id).value = f.kind === 'pct' ? fmt.pct(parsePct(raw)) : f.kind === 'money' ? money(parseMoney(raw)) : raw; });
      return any;
    }
    const shareLink = () => (location.origin && location.origin !== 'null' ? location.origin + location.pathname : cfg.url) + '#' + encode();
    const shareBlock = (s) => `${cfg.name} · ${s.label}\n${s.attack}\n` + s.rows.map(r => `${r[0]}: ${r[1]}`).join('\n') + '\n' + shareLink();
    function render() {
      const s = cfg.compute(read()); lastS = s; const out = $('out');
      if (!s) { out.innerHTML = `<div class="empty">${esc(cfg.emptyText || 'Fill in the numbers above.')}</div>`; strip(null); return; }
      const h = typeof cfg.handoff === 'function' ? cfg.handoff(s) : cfg.handoff;
      out.innerHTML = `
    ${shared ? `<div class="banner">Someone sent you these numbers. Change any of them to run your own.</div>` : ''}
    <div class="verdict verdict-${s.cls}" id="verdict">
      ${s.big ? `<div class="verdict-number">${esc(s.big)}</div><div class="verdict-label">${esc(s.label)}</div>` : `<div class="verdict-word">${esc(s.label)}</div>`}
      <div class="verdict-attack">${esc(s.attack)}</div>
      ${s.sub ? `<div class="verdict-sub">${esc(s.sub)}</div>` : ''}
    </div>
    <div class="list" aria-label="The numbers">${s.rows.map(r => `<div class="list-item"><span class="headline">${esc(r[0])}</span><span class="trailing strong${r[2] ? ' ' + r[2] : ''}">${esc(r[1])}</span></div>`).join('')}</div>
    ${s.note ? `<p class="clock">${esc(s.note)}</p>` : ''}
    ${h ? `<div class="card card-accent"><span class="overline">${esc(h.overline)}</span><p class="lede">${esc(h.text)}</p><a class="btn btn-tonal btn-full" href="${h.href}" style="margin-top:14px;">${esc(h.label)}</a></div>` : ''}
    <div class="btn-row center" style="margin-top:8px;"><button class="btn btn-text" id="copy" type="button">Share</button></div>
    <div class="card" style="margin-top:20px;">
      <h3>${esc(cfg.mark.title(s))}</h3>
      <p>${esc(cfg.mark.body)}</p>
      <div class="preview mono" title="Tap to select">${esc(cfg.dm(s))}</div>
      <button class="btn btn-primary btn-lg btn-full" id="dmBtn" type="button" style="margin-top:14px;">Copy this &amp; DM me</button>
      <div class="btn-row center" style="margin-top:4px;"><a class="btn btn-text" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium=${cfg.slug}&utm_content=after_score&a1=${encodeURIComponent(cfg.bookNote(s))}" target="_blank" rel="noopener">Or book a call</a></div>
      <p class="fine" style="text-align:center;margin:4px 0 0;">Free either way. I answer LinkedIn faster than email.</p>
    </div>`;
      $('copy').onclick = (e) => { track(cfg.slug + '_share'); try { history.replaceState(null, '', '#' + encode()); } catch {} shareOut(e.currentTarget, shareBlock(s), cfg.name); };
      $('dmBtn').onclick = (e) => { const btn = e.currentTarget; track(cfg.slug + '_dm_copy'); copyText(cfg.dm(s)).then(() => { btn.textContent = 'Copied ✓'; window.open('https://www.linkedin.com/in/markflournoy/', '_blank', 'noopener'); }).catch(() => { btn.textContent = "Couldn't copy"; }); };
      out.querySelector('.preview').onclick = (e) => { const r = document.createRange(); r.selectNodeContents(e.currentTarget); const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); };
      strip(s);
    }
    /* the summary strip: on a phone the answer stays visible while you type */
    let verdictVisible = true;
    function strip(s) { const b = $('sumbar'); if (!b) return; if (!s) { b.hidden = true; return; } b.className = 'sumbar verdict-' + s.cls; b.innerHTML = `<b>${esc(s.big || s.label)}</b> ${esc(s.big ? s.label.toLowerCase() : s.stripText || '')}`; b.hidden = verdictVisible; }
    if ('IntersectionObserver' in window && $('sumbar')) {
      const io = new IntersectionObserver((es) => { const e = es[es.length - 1]; verdictVisible = e.isIntersecting || e.boundingClientRect.top < 0; strip(lastS); }, { threshold: 0.15 });
      const watch = () => { io.disconnect(); const v = $('verdict'); if (v) io.observe(v); };
      new MutationObserver(watch).observe($('out'), { childList: true });
    }
    const onEdit = () => { if (!touched) { touched = true; track(cfg.slug + '_edit'); const n = $('exnote'); if (n) n.textContent = ''; } if (shared) { shared = false; try { history.replaceState(null, '', location.pathname); } catch {} } render(); };
    F.forEach(f => { if (f.kind === 'choice') return; const el = $(f.id); el.addEventListener('input', onEdit);
      el.addEventListener('blur', () => { const v = parse[f.kind](el.value); if (v) el.value = fmt[f.kind](v); });
      el.addEventListener('focus', () => setTimeout(() => { try { el.select(); } catch {} }, 0)); });
    document.querySelectorAll('[data-choice]').forEach(b => b.onclick = () => { document.querySelectorAll(`[data-choice="${b.dataset.choice}"]`).forEach(x => x.classList.toggle('on', x === b)); onEdit(); });
    const form = $('f'); if (form) form.addEventListener('submit', (e) => e.preventDefault());
    if (readHash()) { shared = true; touched = true; const n = $('exnote'); if (n) n.textContent = ''; track(cfg.slug + '_verdict_shared'); }
    window.addEventListener('hashchange', () => { if (readHash()) { shared = true; render(); } });
    render();
    window.QB_TEST = { compute: cfg.compute, read };
  };
})();
