/* QuotaBird: small things the tool pages share (Nov 18).
   1. The explanations under a tool are folded into rows. A link to one (/pipeline/#risk, an old /risk/ link,
      a "See the fine print" button) opens that row and brings it into view.
   2. On a phone, once you've scrolled past the tool into the reading, a slim "Ask Mark about this" bar sits at
      the bottom, where your thumb is. It carries your result when there is one, like the button in the result. */
(function () {
  'use strict';
  var track = function (n) { if (typeof window.qbTrack === 'function') window.qbTrack(n); else (window.qbTrackQ = window.qbTrackQ || []).push(n); };

  function openFromHash(scroll) {
    var id = (location.hash || '').slice(1);
    if (!id || /[=&]/.test(id)) return;                 // shared results (#yysny, #base=...) and #ask= aren't sections
    var el; try { el = document.getElementById(decodeURIComponent(id)); } catch (e) { return; }
    if (!el) return;
    var d = el.tagName === 'DETAILS' ? el : el.closest('details.fold-row');
    if (!d) return;
    if (!d.open) d.open = true;
    if (scroll) requestAnimationFrame(function () { el.scrollIntoView({ block: 'start' }); });
  }
  openFromHash(true);
  window.addEventListener('hashchange', function () { openFromHash(true); });
  document.addEventListener('click', function (e) {          // a same-page link to a folded row opens it even if the hash didn't change
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a && a.getAttribute('href').length > 1 && ('#' + (location.hash || '').slice(1)) === a.getAttribute('href')) setTimeout(function () { openFromHash(true); }, 0);
  });
  Array.prototype.forEach.call(document.querySelectorAll('details.fold-row'), function (d) {
    d.addEventListener('toggle', function () { if (d.open) track('more_open_' + d.id.replace(/\W/g, '_')); });
  });

  // the phone's Ask Mark bar: tool pages only (the chat pages are the chat)
  if (document.body.classList.contains('ask-page') || !('IntersectionObserver' in window)) return;
  var screen = document.getElementById('screen'), foot = document.querySelector('.sitefoot');
  if (!screen) return;
  var bar = document.createElement('a');
  bar.className = 'askbar'; bar.href = '/ask-mark/'; bar.hidden = true;
  bar.innerHTML = '<img src="/mark.jpg" alt="" width="28" height="28"><span>Ask Mark about this</span><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  document.body.appendChild(bar);
  bar.addEventListener('click', function () {
    var seeded = document.getElementById('askMarkBtn');      // the result's own hand-off, with the numbers in it
    if (seeded && seeded.href) bar.href = seeded.href;
    track('askbar');
  });
  var pastTool = false, atFoot = false;
  var phone = window.matchMedia('(max-width: 879px)');
  var show = function () {
    var sum = document.getElementById('sumbar');
    bar.hidden = !(phone.matches && pastTool && !atFoot && (!sum || sum.hidden));
  };
  new IntersectionObserver(function (es) { pastTool = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; show(); }).observe(screen);
  if (foot) new IntersectionObserver(function (es) { atFoot = es[0].isIntersecting; show(); }).observe(foot);
  if (phone.addEventListener) phone.addEventListener('change', show);
})();
