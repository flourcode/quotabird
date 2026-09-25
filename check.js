/* check.js: the five-question engine behind the checks (Rep, Partner, Territory, OLR, Brief).
   Each page passes a config: five questions, weights, a verdict function,
   attack lines and moves per pillar, a DM template and a hand-off.
   Deal Check and Pipeline Check keep their own scripts. See HANDOFF.md §16. */
'use strict';
(function () {
  const track = (n) => { if (typeof window.qbTrack === 'function') window.qbTrack(n); else (window.qbTrackQ = window.qbTrackQ || []).push(n); };
  const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const el = () => document.getElementById('screen');
  const show = (html) => { const e = el(); e.classList.remove('enter'); e.innerHTML = html; void e.offsetWidth; e.classList.add('enter'); focusScreen(e); window.scrollTo({ top: 0 }); };
  const VAL = { yes: 92, sort: 50, no: 8 };
  const CODE = { yes: 'y', sort: 's', no: 'n' }, UNCODE = { y: 'yes', s: 'sort', n: 'no' };
  const WORD = { yes: 'Yes', sort: 'Sort of', no: 'No' };
  const clearHash = () => { try { history.replaceState(history.state, '', location.pathname); } catch {} };
  /* ── shared behaviors: history, focus, native share, menu ── */
  let restoring = false;
  // Each screen is a history entry, so the phone's back gesture steps back a screen instead of leaving.
  function nav(st) {
    if (restoring) return;
    const cur = history.state && history.state.sc;
    const same = cur && JSON.stringify(cur) === JSON.stringify(st);
    try { (same ? history.replaceState : history.pushState).call(history, { sc: st }, '', location.href); } catch {}
  }
  // Focus the new screen's heading so keyboard and screen-reader users land where the content is.
  function focusScreen(e) {
    const f = e.querySelector('.question') || e.querySelector('.question-lg') || e.querySelector('.verdict') || e.querySelector('h1');
    if (f) { f.setAttribute('tabindex', '-1'); try { f.focus({ preventScroll: true }); } catch {} }
  }
  // On a phone, Share opens the share sheet (Slack, Teams, Messages). Elsewhere it copies.
  function shareOut(btn, block, title) {
    const lines = block.split('\n'); const url = lines[lines.length - 1]; const text = lines.slice(0, -1).join('\n').trim();
    const touch = window.matchMedia && matchMedia('(pointer: coarse)').matches;
    const copy = () => copyText(block).then(() => { btn.textContent = 'Copied ✓'; }).catch(() => { btn.textContent = "Couldn't copy"; });
    if (navigator.share && touch) {
      navigator.share({ title, text, url }).then(() => { btn.textContent = 'Shared ✓'; }).catch((e) => { if (!e || e.name !== 'AbortError') copy(); });
    } else copy();
  }
  document.addEventListener('click', (e) => { document.querySelectorAll('details.menu[open]').forEach(d => { if (!d.contains(e.target)) d.open = false; }); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') document.querySelectorAll('details.menu[open]').forEach(d => { d.open = false; d.querySelector('summary').focus(); }); });
  

  function copyText(text) {
    try {
      const ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;font-size:16px;';
      document.body.appendChild(ta);
      if (/iP(hone|ad|od)/.test(navigator.userAgent)) {
        ta.contentEditable = 'true'; ta.readOnly = false;
        const r = document.createRange(); r.selectNodeContents(ta);
        const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        ta.setSelectionRange(0, text.length);
      } else { ta.select(); }
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      if (ok) return Promise.resolve();
    } catch (e) {}
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return Promise.reject(new Error('no clipboard'));
  }


  /* Sticky start: once the start button scrolls out of view, a copy rides at the bottom of the screen.
     It disappears when the check starts and while the booking section is on screen. */
  function stickyStart() {
    const screen = document.getElementById('screen'); if (!screen || !('IntersectionObserver' in window)) return;
    const bar = document.createElement('div'); bar.className = 'startbar'; bar.hidden = true;
    bar.innerHTML = '<button class="btn btn-primary btn-lg" type="button"></button>';
    document.body.appendChild(bar);
    const btn = bar.querySelector('button');
    let prepOut = false, aboutIn = false;
    const update = () => { const prep = document.getElementById('prep'); if (prep) btn.textContent = prep.textContent; bar.hidden = !(prep && prepOut && !aboutIn); };
    const io = new IntersectionObserver((es) => {
      es.forEach(e => { if (e.target.id === 'prep') prepOut = !e.isIntersecting && e.boundingClientRect.top < 0; else aboutIn = e.isIntersecting; });
      update();
    });
    const watch = () => { io.disconnect(); prepOut = false; const prep = document.getElementById('prep'), about = document.getElementById('about');
      if (prep) io.observe(prep); if (about) io.observe(about); update(); };
    new MutationObserver(watch).observe(screen, { childList: true });
    watch();
    btn.onclick = () => { window.scrollTo({ top: 0 }); const prep = document.getElementById('prep'); if (prep) prep.click(); };
  }

  window.CheckTool = function (cfg) {
    const P = cfg.questions;
    let answers = {}, lastScore = null, shared = false;
    const INTRO_HTML = el().innerHTML;

    function score(a) {
      let total = 0, wsum = 0;
      P.forEach(p => { total += VAL[a[p.k]] * cfg.weights[p.k]; wsum += cfg.weights[p.k]; });
      total = Math.round(total / wsum);
      if (cfg.capOnNo !== false && P.some(p => a[p.k] === 'no')) total = Math.min(total, 74);
      const ranked = P.slice().sort((x, y) => (VAL[a[x.k]] - VAL[a[y.k]]) || (cfg.weights[y.k] - cfg.weights[x.k]));
      const weak = ranked[0];
      const v = cfg.verdict(a, total, weak);
      const moves = ranked.filter(p => a[p.k] !== 'yes').slice(0, 3).map(p => cfg.moves[p.k]);
      // The literal count: yes is one, sort of is a half. This is the number people see.
      const proven = P.reduce((n, p) => n + (a[p.k] === 'yes' ? 1 : a[p.k] === 'sort' ? .5 : 0), 0);
      const provenText = (proven % 1 ? Math.floor(proven) + '½' : String(proven)) + ' of ' + P.length + ' ' + (cfg.countNoun || 'proven');
      const meta = (cfg.count === false ? '' : provenText + '. ') + 'Weakest: ' + weak.n.toLowerCase() + '.';
      return Object.assign({ total, weak, moves, answers: a, proven, provenText, meta }, v);
    }
    const encode = () => P.map(p => CODE[answers[p.k]]).join('');
    function readHash() {
      const h = (location.hash || '').replace(/^#/, '');
      if (!/^[ysn]{5}$/.test(h)) return false;
      answers = {}; P.forEach((p, i) => answers[p.k] = UNCODE[h[i]]); return true;
    }
    const shareLink = () => (location.origin && location.origin !== 'null' ? location.origin + location.pathname : cfg.url) + '#' + encode();
    function shareBlock(s) {
      const dots = { yes: '●', sort: '◐', no: '○' };
      return `${cfg.name} · ${s.label}\n${s.meta}\n` + P.map(p => dots[answers[p.k]]).join(' ') + '\n' + P.map(p => p.n).join(' · ')
        + `\n\n${s.attack}\n${shareLink()}`;
    }

    function intro() { show(INTRO_HTML); bind(); }
    function home() { nav(['h']); answers = {}; clearHash(); intro(); }
    function bind() { const b = document.getElementById('prep'); if (b) b.onclick = () => { track(cfg.slug + '_start'); ask(0); }; }

    function ask(i) {
      nav(['q', i]);
      const p = P[i];
      show(`
    <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="${P.length}" aria-valuenow="${i + 1}">${P.map((_, j) => `<i class="${j <= i ? 'done' : ''}"></i>`).join('')}</div>
    <span class="overline">${p.n} · question ${i + 1} of ${P.length}</span>
    <div class="question">${esc(p.q)}</div>
    <div class="choice-group" role="group" aria-label="${esc(p.q)}">
      <button class="choice" data-v="yes" type="button">Yes</button>
      <button class="choice" data-v="sort" type="button">Sort of</button>
      <button class="choice" data-v="no" type="button">No</button>
    </div>
    ${i > 0 ? '<button class="btn btn-text" id="back" type="button">← Back</button>' : ''}`);
      el().querySelectorAll('.choice').forEach(b => b.onclick = () => {
        answers[p.k] = b.dataset.v;
        if (navigator.vibrate) navigator.vibrate(8);
        setTimeout(() => (i + 1 < P.length ? ask(i + 1) : result(false)), 120);
      });
      const back = document.getElementById('back'); if (back) back.onclick = () => history.back();
    }

    function result(isShared) {
      const s = score(answers); lastScore = s;
      nav(['r']);
      if (!restoring) track(cfg.slug + (isShared ? '_verdict_shared' : '_verdict'));   // a back/forward restore is not a new verdict
      const firstMove = s.moves[0] || cfg.noMove;
      show(`
    ${isShared ? `<div class="banner">Someone sent you this verdict. <button id="runMine" type="button">Run your own →</button></div>` : ''}
    <div class="verdict verdict-${s.cls}">
      <div class="verdict-word">${esc(s.label)}</div>
      <div class="verdict-meta">${esc(s.meta)}</div>
      <div class="verdict-attack">${esc(s.attack)}</div>
      ${s.sub ? `<div class="verdict-sub">${esc(s.sub)}</div>` : ''}
    </div>
    <div class="list" aria-label="Your answers">
      ${P.map(p => `<div class="list-item compact"><span class="headline">${p.n}</span><span class="trailing${answers[p.k] === 'no' ? ' v-no' : ''}">${WORD[answers[p.k]]}</span></div>`).join('')}
    </div>
    <div class="card">
      <span class="overline">${esc(cfg.askedBy)}</span>
      <p class="lede">“${esc(cfg.grill[s.weak.k])}”</p>
      <span class="overline" style="margin-top:16px;">Do this first</span>
      <p class="lede">${esc(firstMove)}</p>
    </div>
    ${(() => { const h = typeof cfg.handoff === 'function' ? cfg.handoff(s) : cfg.handoff; return h ? `<div class="card card-accent">
      <span class="overline">${esc(h.overline)}</span>
      <p class="lede">${esc(h.text)}</p>
      <a class="btn btn-tonal btn-full" href="${h.href}" style="margin-top:14px;">${esc(h.label)}</a>
    </div>` : ''; })()}
    ${cfg.grillSet ? `<button class="btn btn-primary btn-lg btn-full" id="grill" type="button" style="margin-top:16px;">${esc(cfg.grillLabel || 'Grill me')}</button>` : ''}
    <div class="btn-row center" style="margin-top:8px;">
      <button class="btn btn-text" id="copy" type="button">Share</button>
      <button class="btn btn-text" id="again" type="button">Start over</button>
    </div>
    <div class="useful" id="useful"><span>Useful?</span><button class="btn btn-text" data-u="yes" type="button">Yes</button><button class="btn btn-text" data-u="no" type="button">Not really</button></div>
    <div class="card" style="margin-top:24px;">
      <h3>${esc(cfg.mark.title(s))}</h3>
      <p>${esc(cfg.mark.body)}</p>
      <div class="preview mono" title="Tap to select">${esc(cfg.dm(s))}</div>
      <button class="btn btn-primary btn-lg btn-full" id="dmBtn" type="button" style="margin-top:14px;">Copy this &amp; DM me</button>
      <div class="btn-row center" style="margin-top:4px;">
        <a class="btn btn-text" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium=${cfg.slug}&utm_content=after_score&a1=${encodeURIComponent(cfg.name + ': ' + s.label.toLowerCase() + '. ' + s.meta)}" target="_blank" rel="noopener">Or book a call</a>
      </div>
      <p class="fine" style="text-align:center;margin:4px 0 0;">Free either way. I answer LinkedIn faster than email.</p>
    </div>`);
      const rm = document.getElementById('runMine'); if (rm) rm.onclick = () => { answers = {}; clearHash(); ask(0); };
      const u = document.getElementById('useful'); if (u) u.querySelectorAll('[data-u]').forEach(b => b.onclick = () => { track(cfg.slug + '_useful_' + b.dataset.u); u.innerHTML = '<span>Thanks.</span>'; });
      const g = document.getElementById('grill'); if (g) g.onclick = () => { track(cfg.slug + '_grill'); grillStep = 0; grillOuch = 0; shark = null; if (cfg.sharks) pickShark(); else grill(); };
      document.getElementById('again').onclick = () => { answers = {}; clearHash(); ask(0); };
      document.getElementById('copy').onclick = (e) => {
        const btn = e.currentTarget; track(cfg.slug + '_share');
        try { history.replaceState(history.state, '', '#' + encode()); } catch {}
        shareOut(btn, shareBlock(s), cfg.name);
      };
      document.getElementById('dmBtn').onclick = (e) => {
        const btn = e.currentTarget; track(cfg.slug + '_dm_copy');
        copyText(cfg.dm(s)).then(() => { btn.textContent = 'Copied ✓'; window.open('https://www.linkedin.com/in/markflournoy/', '_blank', 'noopener'); })
          .catch(() => { btn.textContent = "Couldn't copy"; });
      };
      el().querySelector('.preview').onclick = (e) => { const r = document.createRange(); r.selectNodeContents(e.currentTarget); const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); };
    }

    /* Grill: the room asks three questions about the weakest pillar */
    let grillStep = 0, grillOuch = 0, shark = null;
    function pickShark() {
      nav(['sh']);
      const s = lastScore;
      show(`
    <span class="overline">${esc(cfg.grillBy || 'The room')}</span>
    <div class="question">${esc(cfg.sharkPrompt || "Who's in the room?")}</div>
    <div class="choice-group" role="group" aria-label="Who is in the room">
      ${Object.keys(cfg.sharks).map(id => `<button class="choice" data-shark="${id}" type="button">${esc(cfg.sharks[id].name)}</button>`).join('')}
    </div>
    <button class="btn btn-text" id="back" type="button">← The verdict</button>`);
      el().querySelectorAll('[data-shark]').forEach(b => b.onclick = () => { shark = b.dataset.shark; track(cfg.slug + '_shark'); grillStep = 0; grillOuch = 0; grill(); });
      document.getElementById('back').onclick = () => result(false);
    }
    function grill() {
      const s = lastScore;
      const qs = (shark && cfg.sharks[shark].qs[s.weak.k]) || cfg.grillSet[s.weak.k];
      if (grillStep >= 3) return grillDone();
      nav(['g', grillStep, grillOuch, shark]);
      show(`
    <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="3" aria-valuenow="${grillStep + 1}">${[0,1,2].map(j => `<i class="${j <= grillStep ? 'done' : ''}"></i>`).join('')}</div>
    <span class="overline">${esc(shark ? cfg.sharks[shark].name : (cfg.grillBy || 'The room'))} · question ${grillStep + 1} of 3</span>
    <div class="question-lg">“${esc(qs[grillStep])}”</div>
    <div class="choice-group" role="group" aria-label="Can you answer this?">
      <button class="choice" data-v="ok" type="button">I can answer that</button>
      <button class="choice" data-v="ouch" type="button">Ouch</button>
    </div>`);
      el().querySelectorAll('.choice').forEach(b => b.onclick = () => {
        if (b.dataset.v === 'ouch') grillOuch++;
        if (navigator.vibrate) navigator.vibrate(8);
        grillStep++; setTimeout(grill, 120);
      });
    }
    function grillDone() {
      nav(['gd', grillOuch, shark]);
      const s = lastScore, w = s.weak;
      const L = cfg.grillLines || {};
      const verdict = grillOuch === 0 ? (L.clean || 'You would survive.') : grillOuch === 1 ? (L.one || 'You would mostly survive. One hole left.') : (L.bad || 'You wouldn\'t survive.');
      const who = shark ? cfg.sharks[shark].name : (cfg.grillBy || 'The room');
      const line = grillOuch === 0 ? (L.cleanSub || `Three ${w.n.toLowerCase()} questions, three answers. Bring the proof anyway.`)
                 : `You couldn't answer ${grillOuch} of 3 from ${who.startsWith('The ') ? who[0].toLowerCase() + who.slice(1) : who}. The one you can't bluff is ${w.n.toLowerCase()}.`;
      show(`
    <span class="overline">Verdict</span>
    <h1 style="margin-top:8px;">${esc(verdict)}</h1>
    <p class="dek">${esc(line)}</p>
    <div class="card"><span class="overline">${esc(cfg.fixLabel || 'Before the room')}</span>
      <p class="lede">${esc(cfg.fix[w.k])}</p></div>
    <div class="btn-row center" style="margin-top:8px;">
      <button class="btn btn-text" id="back2" type="button">← The verdict</button>
    </div>
    <div class="card" style="margin-top:24px;">
      <h3>${esc(cfg.mark.title(s))}</h3>
      <p>${esc(cfg.mark.body)}</p>
      <div class="preview mono" title="Tap to select">${esc(cfg.dmGrill ? cfg.dmGrill(s, grillOuch) : cfg.dm(s))}</div>
      <button class="btn btn-primary btn-lg btn-full" id="dmBtn" type="button" style="margin-top:14px;">Copy this &amp; DM me</button>
      <div class="btn-row center" style="margin-top:4px;">
        <a class="btn btn-text" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium=${cfg.slug}&utm_content=after_grill&a1=${encodeURIComponent(cfg.name + ': ' + s.label.toLowerCase() + '. ' + s.meta)}" target="_blank" rel="noopener">Or book a call</a>
      </div>
      <p class="fine" style="text-align:center;margin:4px 0 0;">Free either way. I answer LinkedIn faster than email.</p>
    </div>`);
      document.getElementById('back2').onclick = () => result(false);
      const text = cfg.dmGrill ? cfg.dmGrill(s, grillOuch) : cfg.dm(s);
      document.getElementById('dmBtn').onclick = (e) => { const btn = e.currentTarget; track(cfg.slug + '_dm_copy');
        copyText(text).then(() => { btn.textContent = 'Copied ✓'; window.open('https://www.linkedin.com/in/markflournoy/', '_blank', 'noopener'); }).catch(() => { btn.textContent = "Couldn't copy"; }); };
      el().querySelector('.preview').onclick = (e) => { const r = document.createRange(); r.selectNodeContents(e.currentTarget); const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); };
    }

    /* Boot */
    const lh = document.getElementById('logoHome'); if (lh) lh.onclick = home;
    stickyStart();
    bind();
    try { history.replaceState({ sc: ['h'] }, '', location.href); } catch {}
    if (readHash()) result(true);
    window.addEventListener('popstate', (e) => {
      const st = e.state && e.state.sc; restoring = true;
      const complete = P.every(p => answers[p.k]);
      try {
        if (!st || st[0] === 'h') intro();
        else if (st[0] === 'q') ask(st[1]);
        else if (st[0] === 'r' && complete) result(false);
        else if (st[0] === 'sh' && lastScore) pickShark();
        else if (st[0] === 'g' && lastScore) { grillStep = st[1]; grillOuch = st[2]; shark = st[3]; grill(); }
        else if (st[0] === 'gd' && lastScore) { grillStep = 3; grillOuch = st[1]; shark = st[2]; grillDone(); }
        else intro();
      } finally { restoring = false; }
    });
    window.addEventListener('hashchange', () => { if (readHash()) result(true); });
    window.QB_TEST = { score, P };
  };
})();
