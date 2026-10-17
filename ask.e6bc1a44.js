/* ask.js: Ask Mark (a conversation with the AI version of Mark) and the three one-box pages
   (Meeting Prep, Account Plan, Update Upward). Plain language in, Mark's answer out.
   The AI runs on the shared Lambda (quotabird.mjs). Nothing typed is stored. */
'use strict';
(function () {
  const CFG = window.QB_ASK || {};
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const track = (n) => { if (typeof window.qbTrack === 'function') window.qbTrack(n); else (window.qbTrackQ = window.qbTrackQ || []).push(n); };
  const reduced = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  async function post(body, timeoutMs = 35000) {
    const ctrl = new AbortController(); const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      // text/plain keeps this a "simple" CORS request (no preflight). The Lambda parses it as JSON.
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(body), signal: ctrl.signal });
      let data = null; try { data = await res.json(); } catch {}
      if (!res.ok || !data || data.error) return { error: (data && typeof data.error === 'string' && data.error.length < 200) ? data.error : 'Something went wrong. Try again.' };
      return { data };
    } catch (e) {
      return { error: e && e.name === 'AbortError' ? 'That took too long. Try again.' : "Couldn't connect. Check your connection and try again." };
    } finally { clearTimeout(timer); }
  }
  // Ask for a streamed answer. The streaming Lambda sends newline-delimited JSON ({"t":"d","x":text} pieces, then
  // {"t":"done",...} or {"t":"error",...}); a Lambda that isn't streaming yet, or an error before the first word,
  // sends plain JSON, which is handled exactly like post().
  async function postStream(body, onDelta, timeoutMs = 40000) {
    const ctrl = new AbortController(); const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify({ ...body, stream: true }), signal: ctrl.signal });
      if (!/ndjson/.test(res.headers.get('content-type') || '') || !res.body) {
        let data = null; try { data = await res.json(); } catch {}
        if (!res.ok || !data || data.error) return { error: (data && typeof data.error === 'string' && data.error.length < 200) ? data.error : 'Something went wrong. Try again.' };
        return { data };
      }
      const reader = res.body.getReader(), dec = new TextDecoder(); let buf = '', data = null, error = null;
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let nl;
        while ((nl = buf.indexOf('\n')) >= 0) {
          const line = buf.slice(0, nl).trim(); buf = buf.slice(nl + 1); if (!line) continue;
          let m = null; try { m = JSON.parse(line); } catch { continue; }
          if (m.t === 'd' && typeof m.x === 'string') onDelta(m.x);
          else if (m.t === 'done') data = m;
          else if (m.t === 'error') error = typeof m.error === 'string' ? m.error : 'Something went wrong. Try again.';
        }
      }
      if (!data && !error) error = 'The answer got cut off. Try again.';
      return error ? { error } : { data };
    } catch (e) {
      return { error: e && e.name === 'AbortError' ? 'That took too long. Try again.' : "Couldn't connect. Check your connection and try again." };
    } finally { clearTimeout(timer); }
  }
  function busy(btn, on, text) { if (!btn) return; if (!btn.dataset.label) btn.dataset.label = btn.textContent; btn.disabled = on; btn.textContent = on ? text : btn.dataset.label; }
  const errorBox = (where, msg) => { where.innerHTML = `<div class="banner ask-error" role="alert">${esc(msg)}</div>`; };
  const wait = (where, msg) => { where.innerHTML = `<div class="ask-wait"><span class="dot"></span> ${esc(msg)}</div>`; };
  const scrollTo = (el) => { if (!el) return; const top = el.getBoundingClientRect().top; if (top < 0 || top > window.innerHeight * .6) el.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'start' }); };
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
  function autosize(t, min) { const fit = () => { t.style.height = 'auto'; t.style.height = Math.max(min || 0, t.scrollHeight + 2) + 'px'; }; t.addEventListener('input', fit); fit(); }
  // Enter sends on a keyboard; on a phone, return makes a new line and the send button sends, the way messaging apps work
  const touch = () => window.matchMedia && matchMedia('(pointer: coarse)').matches;
  const enterSubmits = (t, form) => t.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && !touch()) { e.preventDefault(); form.requestSubmit(); } });
  const ul = (items, f = (x) => esc(x), tag = 'ul') => items && items.length ? `<${tag} class="ask-list">${items.map(i => `<li>${f(i)}</li>`).join('')}</${tag}>` : '';
  const T = (h, items, f = (x) => x) => items && items.length ? `\n${h.toUpperCase()}\n` + items.map(i => '- ' + f(i)).join('\n') + '\n' : '';
  const P = (h, text) => text ? `\n${h.toUpperCase()}\n${text}\n` : '';
  const foot = '<p class="fine ask-foot">Written by the AI version of Mark, not the real one. Check names, vehicles and numbers before you repeat them to a customer.</p>';

  /* ═════════════ Ask Mark: a conversation ═════════════ */
  function askPage() {
    const slug = String(CFG.page || 'ask').replace(/-/g, '_');
    const WORKFLOW = !!CFG.page && !['home', 'ask-mark'].includes(CFG.page);   // the pages with a job to do (Meeting Prep, Partner Check...); home and ask-mark are the plain chat
    const form = $('askForm'), text = $('askText'), btn = $('askBtn'), chat = $('chat'), fresh = $('askNew'), bar = $('chatBar'), examples = $('askExamples'), next = $('askNext');
    const PH_FIRST = text.getAttribute('placeholder') || 'Ask Mark anything about selling', PH_MORE = 'Ask a follow-up';
    const history = [];   // {role:'user'|'mark', text}
    let run = 0, last = { followups: [], tool: null };
    // Kept in sessionStorage: this tab only, gone when the tab closes, never sent anywhere but the Lambda. It means
    // "Run your numbers", a header link or Back doesn't throw the conversation away. Home and Ask Mark share one.
    const KEY = 'qb-chat-' + (WORKFLOW ? CFG.page : 'mark');
    const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify({ history: history.slice(-24), last })); } catch (e) {} };
    const forget = () => { try { sessionStorage.removeItem(KEY); } catch (e) {} };
    // Starting over keeps the last conversation one tap away, in case the logo or Start over was a slip
    const PREV = KEY + '-prev';
    const archive = (h, l) => { try { if (h && h.length) sessionStorage.setItem(PREV, JSON.stringify({ history: h.slice(-24), last: l })); } catch (e) {} };
    const readPrev = () => { try { const p = JSON.parse(sessionStorage.getItem(PREV) || 'null'); return p && Array.isArray(p.history) && p.history.length ? p : null; } catch (e) { return null; } };
    const prevRow = document.createElement('p'); prevRow.className = 'ask-prev'; prevRow.hidden = true;
    prevRow.innerHTML = '<button class="linkbtn" type="button">\u21a9 Pick up your last conversation</button>';
    examples.parentNode.insertBefore(prevRow, examples);
    const showPrev = () => { prevRow.hidden = !(history.length === 0 && readPrev()); };
    const CAL = 'https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium=' + slug + '&utm_content=in_chat';
    const fit = () => { text.style.height = 'auto'; text.style.height = Math.min(200, text.scrollHeight) + 'px'; };
    text.addEventListener('input', fit); fit();
    enterSubmits(text, form);
    const paras = (t) => String(t || '').split(/\n{2,}/).map(p => p.trim()).filter(Boolean);
    function bubble(role, parts, extraHtml) {
      const el = document.createElement('div'); el.className = 'msg msg-' + role;
      el.innerHTML = (role === 'mark' ? '<img class="msg-face" src="../mark.jpg" alt="" width="36" height="36">' : '')
        + `<div class="msg-body">${parts.map(p => `<p>${esc(p)}</p>`).join('')}${extraHtml || ''}</div>`;
      chat.appendChild(el); return el;
    }
    // a message handed over by a tool ("I just ran your Quota Check. ...") shows its first line; the numbers fold under it
    function userBubble(q) {
      const ps = paras(q);
      if (/^I just ran your /.test(q) && ps.length > 2) {
        const el = bubble('user', [ps[0]], `<details class="msg-more"><summary>The numbers</summary>${ps.slice(1, -1).map(p => `<p>${esc(p)}</p>`).join('')}</details><p>${esc(ps[ps.length - 1])}</p>`);
        return el;
      }
      return bubble('user', ps);
    }
    // Mark's bubble: paragraphs, then a quiet Copy (people forward his answer, or paste the words he gave them)
    function fillMark(el, reply) {
      el.classList.remove('is-thinking', 'is-streaming');
      const body = el.querySelector('.msg-body');
      body.innerHTML = reply.map(p => `<p>${esc(p)}</p>`).join('');
      const b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn-text msg-copy'; b.textContent = 'Copy';
      b.onclick = () => { track(slug + '_copy'); copyText(reply.join('\n\n')).then(() => { b.textContent = 'Copied \u2713'; setTimeout(() => { b.textContent = 'Copy'; }, 2000); }, () => { b.textContent = "Couldn't copy"; }); };
      body.appendChild(b);
      return el;
    }
    const markBubble = (reply) => fillMark(bubble('mark', []), reply);
    function thinking() {
      const el = bubble('mark', []); el.classList.add('is-thinking');
      el.querySelector('.msg-body').innerHTML = '<span class="dots" role="status" aria-label="Mark is thinking"><i></i><i></i><i></i></span><span class="msg-wait" aria-live="polite"></span>';
      // a slow answer says so, instead of leaving three dots for twenty seconds
      const say = (t) => { const w = el.querySelector('.msg-wait'); if (w) w.textContent = t; };
      el._timers = [setTimeout(() => say('Thinking it through.'), 6000), setTimeout(() => say('Taking longer than usual. Hang on.'), 16000)];
      return el;
    }
    // keep the newest message in view without hiding it under the composer
    const reveal = (el) => { if (!el) return; const pad = form.offsetHeight + 24; const r = el.getBoundingClientRect(); if (r.bottom > window.innerHeight - pad || r.top < 0) window.scrollBy({ top: Math.min(r.top - 96, r.bottom - (window.innerHeight - pad)), behavior: reduced() ? 'auto' : 'smooth' }); };
    const ROWS = text.rows || 1;   // a workflow page opens with a taller box; once the conversation starts it's a one-line composer
    // once the conversation starts the intro collapses (the answer gets the room) and the box becomes a one-line composer
    const started = (on) => { if (on && typeof prevRow !== 'undefined') prevRow.hidden = true; bar.hidden = !on; examples.hidden = on; form.classList.toggle('is-sticky', on); document.body.classList.toggle('is-chatting', on); text.placeholder = on ? PH_MORE : PH_FIRST; text.rows = on ? 1 : ROWS; fit(); };
    // What to ask next: Mark's own follow-up suggestions as chips (tap to send), and the one tool that runs
    // their numbers as the outlined chip at the end. Sits between his reply and the box so the box reads as "reply".
    const send = (q, why) => { text.value = q; fit(); track(why); form.requestSubmit(); };
    function offer(followups, tool) {
      next.innerHTML = ''; next.hidden = true;
      const ups = (Array.isArray(followups) ? followups : []).map(f => String(f || '').trim()).filter(Boolean).slice(0, 3);
      if (!ups.length && !tool) return;
      ups.forEach(f => { const b = document.createElement('button'); b.type = 'button'; b.className = 'ask-ex'; b.textContent = f; b.onclick = () => send(f, 'ask_followup_chip'); next.appendChild(b); });
      // the one calculator or check that runs their numbers: the advice came first, this is the optional next step
      if (tool) { const a = document.createElement('a'); a.className = 'ask-ex ask-ex-tool'; a.href = tool.url; a.innerHTML = '<small>Run your numbers</small>' + esc(tool.name) + ' \u2192'; a.title = tool.question || ''; a.onclick = () => { save(); track('ask_tool_click'); }; next.appendChild(a); }
      // three answers in, they're invested: offer the real one, once, quietly
      if (history.filter(m => m.role === 'mark').length === 3) { const r = document.createElement('p'); r.className = 'ask-real'; r.innerHTML = `<a href="${CAL}" target="_blank" rel="noopener">Want the real Mark on this one? Twenty minutes, free.</a>`; r.querySelector('a').onclick = () => track('ask_real_mark'); next.appendChild(r); }
      next.hidden = false;
    }
    document.querySelectorAll('[data-example]').forEach(b => b.onclick = () => { text.value = b.dataset.example; fit(); track('ask_example'); form.requestSubmit(); });
    // A starter (a [data-starter] button lower on the page, or /page/#draft=<words>): the words go in the box,
    // ready to finish, and nothing is sent until the person sends it.
    const draft = (t) => { text.value = t.slice(0, 2500); fit(); form.scrollIntoView({ behavior: 'smooth', block: 'center' }); text.focus({ preventScroll: true }); try { text.setSelectionRange(text.value.length, text.value.length); } catch (e) {} };
    document.querySelectorAll('[data-starter]').forEach(b => b.onclick = () => { draft(b.dataset.starter); track('ask_starter'); });
    function startOver(why) {
      run++; archive(history.slice(), last);
      history.length = 0; last = { followups: [], tool: null }; forget();
      chat.innerHTML = ''; offer([], null); started(false); text.value = ''; fit(); showPrev();
      window.scrollTo({ top: 0, behavior: 'auto' });
      if (!touch()) text.focus({ preventScroll: true });
      track(why || 'ask_new');
    }
    fresh.onclick = () => startOver('ask_new');
    // the logo means "home, clean slate": it links to /#start, which starts over here (Back still restores)
    const freshStart = () => { if (location.hash === '#start') { try { window.history.replaceState(null, '', location.pathname); } catch (e) {} return true; } return false; };
    window.addEventListener('hashchange', () => { if (freshStart()) startOver('ask_logo_restart'); });
    prevRow.querySelector('button').onclick = () => {
      const p = readPrev(); if (!p) return;
      run++; archive(history.slice(), last);
      history.length = 0; chat.innerHTML = '';
      p.history.forEach(m => { history.push({ role: m.role === 'mark' ? 'mark' : 'user', text: m.text }); m.role === 'mark' ? markBubble(paras(m.text)) : userBubble(m.text); });
      last = p.last || { followups: [], tool: null }; save(); started(true); prevRow.hidden = true;
      if (history[history.length - 1].role === 'mark') offer(last.followups, last.tool); else ask();
      track('ask_prev_restored');
    };
    // A tool handing over its result: /ask-mark/#ask=<the person's numbers as their first message>. The fragment
    // never reaches the server or analytics; it's dropped from the address bar as soon as it's read, and sent once.
    let seed = '', starter = '';
    { const m = /(?:^#|&)ask=([^&]*)/.exec(location.hash || ''); if (m) { try { seed = decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch (e) {} try { window.history.replaceState(null, '', location.pathname); } catch (e) {} } }
    { const m = /(?:^#|&)draft=([^&]*)/.exec(location.hash || ''); if (m) { try { starter = decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch (e) {} try { window.history.replaceState(null, '', location.pathname); } catch (e) {} } }
    async function ask() {
      const id = ++run;
      btn.disabled = true; const wait = thinking(); reveal(wait);
      let live = '', shown = 0;
      const onDelta = (x) => {
        if (id !== run) return;
        if (!live) { (wait._timers || []).forEach(clearTimeout); wait.classList.remove('is-thinking'); wait.classList.add('is-streaming'); }
        live += x;
        const ps = paras(live);
        wait.querySelector('.msg-body').innerHTML = ps.map(p => `<p>${esc(p)}</p>`).join('');
        if (ps.length !== shown) { shown = ps.length; reveal(wait); }   // keep up with new paragraphs, not every word
      };
      const req = WORKFLOW ? { kind: 'qb_mark', page: CFG.page, messages: history.slice(-16) } : { kind: 'qb_mark', messages: history.slice(-16) };
      const { data, error } = await postStream(req, onDelta);
      (wait._timers || []).forEach(clearTimeout);
      if (id !== run) return;
      btn.disabled = false;
      if (error || !data) wait.remove();
      if (error) {
        // their message stays where it is; one tap sends it again
        track('ask_error');
        const el = bubble('mark', [error], '<button class="btn btn-text msg-retry" type="button">Try again</button>'); el.classList.add('is-error');
        el.querySelector('.msg-retry').onclick = () => { el.remove(); track('ask_retry'); ask(); };
        reveal(el); return;
      }
      const reply = Array.isArray(data.reply) ? data.reply : paras(data.reply);
      history.push({ role: 'mark', text: reply.join('\n\n') });
      last = { followups: Array.isArray(data.followups) ? data.followups.slice(0, 3) : [], tool: data.tool || null };
      const el = fillMark(wait, reply);   // the streamed bubble settles to the final answer in place
      offer(last.followups, last.tool); save();
      reveal(el); if (!touch()) text.focus({ preventScroll: true });   // on a phone, don't pop the keyboard over the answer
      track('ask_done');
    }
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = text.value.trim();
      if (q.length < 3) { text.focus(); return; }
      if (btn.disabled) return;
      chat.querySelectorAll('.msg.is-error').forEach(x => x.remove());   // a new message replaces a failed attempt's error
      history.push({ role: 'user', text: q });
      userBubble(q); save();
      text.value = ''; fit(); started(true); offer([], null);
      track((CFG.page === 'ask-mark' ? 'ask' : slug) + (history.filter(m => m.role === 'user').length === 1 ? '_first' : '_followup'));   // home_first, ask_first, meeting_prep_first...
      ask();
    });
    // back from a tool, a link or a reload in the same tab: the conversation is where they left it.
    // Arriving from the logo (/#start): the old conversation is archived and the page starts clean.
    const cleanStart = !WORKFLOW && freshStart();
    if (cleanStart) { try { const old = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (old) archive(old.history, old.last); } catch (e) {} forget(); track('ask_logo_restart'); }
    try {
      const saved = cleanStart ? null : JSON.parse(sessionStorage.getItem(KEY) || 'null');
      if (saved && Array.isArray(saved.history) && saved.history.length) {
        saved.history.forEach(m => { if (!m || typeof m.text !== 'string') return; history.push({ role: m.role === 'mark' ? 'mark' : 'user', text: m.text }); m.role === 'mark' ? markBubble(paras(m.text)) : userBubble(m.text); });
        if (history.length) { started(true); last = saved.last || last; if (history[history.length - 1].role === 'mark') offer(last.followups, last.tool); else if (!seed.trim()) ask(); track('ask_restored'); }
      }
    } catch (e) {}
    showPrev();
    if (seed.trim().length >= 3) { text.value = seed.slice(0, 2500); fit(); track('ask_from_tool'); form.requestSubmit(); }
    else if (starter.trim()) { draft(starter); track('ask_from_starter'); }
  }

  /* ═════════════ The one-box pages ═════════════ */
  function wfPage() {
    const page = CFG.page, form = $('wfForm'), btn = $('wfBtn'), out = $('wfOut'), box = $('situation');
    const slug = page.replace(/-/g, '_');
    autosize(box, 150);
    form.querySelectorAll('[data-choice]').forEach(b => b.addEventListener('click', () => {
      form.querySelectorAll(`[data-choice="${b.dataset.choice}"]`).forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    }));
    const choice = (k) => { const on = form.querySelector(`[data-choice="${k}"].on`); return on ? on.dataset.v : ''; };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const situation = box.value.trim();
      if (situation.length < 8) { errorBox(out, 'Tell Mark a little more first. A few sentences is plenty.'); box.focus(); return; }
      busy(btn, true, 'Working on it…'); wait(out, 'Mark is on it. About fifteen seconds.');
      track(slug + '_run');
      const kind = { 'meeting-prep': 'qb_meeting_prep', 'account-plan': 'qb_account_plan', 'update-upward': 'qb_update_upward' }[page];
      const { data, error } = await post({ kind, situation, type: choice('type') });
      busy(btn, false);
      if (error) { track(slug + '_error'); return errorBox(out, error); }
      // the current Lambda sends sections; an older one sends { meeting | plan | update: {...} }, which still gets shown
      const secs = Array.isArray(data.sections) ? data.sections : legacySections(data.meeting || data.plan || data.update);
      if (!secs.length) { track(slug + '_empty'); return errorBox(out, "The answer came back empty. Try again in a moment."); }
      renderSections(secs, data.type || (data.update && data.update.type));
      track(slug + '_done');
    });
    function finish(html, textFn) {
      out.innerHTML = `<div class="wf-out" tabindex="-1">${html}${foot}</div>`;
      actions(out.querySelector('.wf-out'), textFn, slug);
      const card = out.querySelector('.wf-out'); scrollTo(card); try { card.focus({ preventScroll: true }); } catch {}
    }
    function legacySections(o) {
      if (!o || typeof o !== 'object') return [];
      const name = (k) => ({ objective: 'A win looks like', read: "Mark's read", next_step: 'The next step to ask for', within_72_hours: 'Within 72 hours', who_to_meet: 'Who to meet', next_actions: 'Next actions' }[k] || (k.charAt(0).toUpperCase() + k.slice(1).replace(/_/g, ' ')));
      const line = (v) => typeof v === 'string' ? v : v && typeof v === 'object' ? Object.values(v).filter(x => typeof x === 'string').join(': ') : '';
      return Object.entries(o).filter(([k]) => !['type', 'trimmed'].includes(k)).map(([k, v]) => ({ heading: name(k), body: Array.isArray(v) ? v.map(line).filter(Boolean).map(x => '- ' + x).join('\n') : line(v) })).filter(x => x.body);
    }
    // Arti picks the sections; each body is short paragraphs or "- " lists.
    const bodyHtml = (t) => {
      const out = []; let list = [];
      const flush = () => { if (list.length) { out.push(`<ul class="ask-list">${list.map(i => `<li>${esc(i)}</li>`).join('')}</ul>`); list = []; } };
      String(t || '').split('\n').forEach(l => { if (/^- /.test(l)) list.push(l.slice(2)); else { flush(); if (l.trim()) out.push(`<p class="pg">${esc(l)}</p>`); } });
      flush(); return out.join('');
    };
    function renderSections(secs, type) {
      const isUpdate = page === 'update-upward';
      const html = secs.map((x, i) => `<div class="card${i === 0 ? ' wf-first' : ''}${isUpdate && /boss will ask/i.test(x.heading) ? ' ask-prep' : ''}"><h3>${esc(x.heading)}</h3>${bodyHtml(x.body)}</div>`).join('');
      // for an update, Copy gives the message itself (ready to paste); the boss's questions are prep
      finish(html, () => isUpdate && secs.length ? secs.filter(x => !/boss will ask/i.test(x.heading)).map(x => /^the update$/i.test(x.heading) ? x.body : `${x.heading.toUpperCase()}\n${x.body}`).join('\n\n')
        : secs.map(x => `${x.heading.toUpperCase()}\n${x.body}`).join('\n\n'));
    }
  }

  function init() { if ($('askForm')) askPage(); else if (CFG.page && $('wfForm')) wfPage(); }   // every page is the chat now; wfPage stays for an old build
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
