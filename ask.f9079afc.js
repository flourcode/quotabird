/* ask.js: Ask QuotaBird (Arti, the federal sales coach) and the three one-box pages
   (Meeting Prep, Account Plan, Update Upward). One plain-language box in, real coaching out.
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
      // text/plain keeps this a "simple" CORS request (no preflight), the same as SideFrog. The Lambda parses it as JSON.
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(body), signal: ctrl.signal });
      let data = null; try { data = await res.json(); } catch {}
      if (!res.ok || !data || data.error) return { error: (data && typeof data.error === 'string' && data.error.length < 200) ? data.error : 'Something went wrong. Try again.' };
      return { data };
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
  const enterSubmits = (t, form) => t.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit(); } });
  const ul = (items, f = (x) => esc(x), tag = 'ul') => items && items.length ? `<${tag} class="ask-list">${items.map(i => `<li>${f(i)}</li>`).join('')}</${tag}>` : '';
  const T = (h, items, f = (x) => x) => items && items.length ? `\n${h.toUpperCase()}\n` + items.map(i => '- ' + f(i)).join('\n') + '\n' : '';
  const P = (h, text) => text ? `\n${h.toUpperCase()}\n${text}\n` : '';
  const foot = '<p class="fine ask-foot">Coaching written by AI. Check names, vehicles and numbers before you repeat them to a customer.</p>';

  /* ═════════════ Ask QuotaBird: ask Arti anything ═════════════ */
  function askPage() {
    const form = $('askForm'), text = $('askText'), btn = $('askBtn'), out = $('askOut');
    let run = 0, situation = '';
    autosize(text, 110); enterSubmits(text, form);
    document.querySelectorAll('[data-example]').forEach(b => b.onclick = () => { text.value = b.dataset.example; text.dispatchEvent(new Event('input')); track('ask_example'); form.requestSubmit(); });
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = text.value.replace(/\s+/g, ' ').trim();
      if (q.length < 8) { errorBox(out, "Tell Arti what's going on. A sentence or two is plenty."); text.focus(); return; }
      situation = q; ask('', btn);
    });
    async function ask(scenario, button) {
      const id = ++run;
      busy(button, true, 'Thinking…');
      if (!scenario) wait(out, 'Arti is thinking it through. About fifteen seconds.'); else wait($('askWhatIfOut'), 'Rethinking it with that in mind…');
      track(scenario ? 'ask_whatif' : 'ask_coach');
      const { data, error } = await post({ kind: 'qb_coach', situation, scenario });
      if (id !== run) return;
      busy(button, false);
      if (error) { track('ask_error'); return errorBox(scenario ? $('askWhatIfOut') : out, error); }
      render(data.coach || {}, scenario);
    }
    function render(c, scenario) {
      const tool = c.tool ? `<a class="card ask-tool" href="${esc(c.tool.url)}"><span class="overline">Run your own numbers</span><span class="ask-tool-q">${esc(c.tool.question)}</span><span class="ask-tool-n">${esc(c.tool.name)} →</span></a>` : '';
      out.innerHTML = `<div class="wf-out coach" tabindex="-1">
        ${scenario ? `<p class="fine ask-scn">With: ${esc(scenario)}</p>` : ''}
        <div class="card wf-lead"><span class="overline">Arti's take</span><p class="lede">${esc(c.high_level_recommendation)}</p></div>
        ${(c.coaching_plan || []).map(p => `<div class="card persona"><h3>${esc(p.persona)}</h3><p class="pg">${esc(p.smart_goal)}</p>${p.talking_points && p.talking_points.length ? `<div class="tps">${p.talking_points.map(t => `<span class="tp">${esc(t)}</span>`).join('')}</div>` : ''}</div>`).join('')}
        ${tool}
        <form class="ask-form whatif" id="askWhatIf" autocomplete="off" novalidate>
          <label class="tf"><span class="tf-label">What if…</span><textarea id="askScenario" rows="2" maxlength="800" placeholder="e.g. The CO just told us the RFP slips to Q3, or our champion is leaving"></textarea></label>
          <button class="btn btn-lg btn-full" id="askWhatIfBtn" type="submit">Rethink it</button>
        </form>
        <div id="askWhatIfOut"></div>
        ${foot}
      </div>`;
      actions(out.querySelector('.wf-out'), () => `ARTI'S TAKE\n${c.high_level_recommendation || ''}\n` + (c.coaching_plan || []).map(p => `\n${p.persona.toUpperCase()}\n${p.smart_goal}\n${(p.talking_points || []).map(t => '- ' + t).join('\n')}`).join('\n'), 'ask');
      const wf = $('askWhatIf'), st = $('askScenario'); autosize(st, 60); enterSubmits(st, wf);
      wf.addEventListener('submit', (e) => { e.preventDefault(); const s = st.value.replace(/\s+/g, ' ').trim(); if (s.length < 4) { st.focus(); return; } ask(s, $('askWhatIfBtn')); });
      const card = out.querySelector('.wf-out'); scrollTo(card); try { card.focus({ preventScroll: true }); } catch {}
      track('ask_done');
    }
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
      if (situation.length < 8) { errorBox(out, 'Tell Arti a little more first. A few sentences is plenty.'); box.focus(); return; }
      busy(btn, true, 'Working on it…'); wait(out, 'Arti is on it. About fifteen seconds.');
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
      const name = (k) => ({ objective: 'A win looks like', read: "Arti's read", next_step: 'The next step to ask for', within_72_hours: 'Within 72 hours', who_to_meet: 'Who to meet', next_actions: 'Next actions' }[k] || (k.charAt(0).toUpperCase() + k.slice(1).replace(/_/g, ' ')));
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

  function init() { if (CFG.page === 'ask-quotabird') askPage(); else if (CFG.page) wfPage(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
