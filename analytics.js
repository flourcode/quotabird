/* QuotaBird analytics. Google Analytics 4, loaded by the plain <script> tag in each page's head
   (Google's standard install). This file only configures it and counts named events.
   The URL fragment carries a shared verdict (#ysnys) or pipeline numbers; Google never receives it. */
var GA_ID = 'G-BG9NR9GXQZ';
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', GA_ID, { page_location: location.origin + location.pathname, page_title: document.title });

/* Named events with no parameters. Usage, never content. */
window.qbTrack = function (name) { try { gtag('event', name); } catch (e) {} };
(window.qbTrackQ || []).forEach(window.qbTrack); window.qbTrackQ = [];

/* Two more counts, attached to the specific elements: the Ask Mark chip and hand-off cards. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[href$=".pdf"]').forEach(function (a) { a.addEventListener('click', function () { var h = a.getAttribute('href') || ''; window.qbTrack(h.indexOf('leader') >= 0 ? 'leader_download' : h.indexOf('seller') >= 0 ? 'seller_download' : 'kit_download'); }); });
  document.querySelectorAll('.front-picks a').forEach(function (a) { a.addEventListener('click', function () { window.qbTrack('front_pick'); }); });
  document.querySelectorAll('a.chip-ask, .madeby-links a[href*="#ask"]').forEach(function (a) { a.addEventListener('click', function () { window.qbTrack('ask_mark_click'); }); });
  var out = document.getElementById('out2') || document.getElementById('out') || document.getElementById('screen');
  if (out) out.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.card-accent a')) window.qbTrack('related_tool_click'); });
});
