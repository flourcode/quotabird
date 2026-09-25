/* QuotaBird analytics.
   Paste your Google Analytics 4 measurement ID below (it looks like G-XXXXXXXXXX).
   Leave it empty and nothing loads. Both pages include this file. */
var GA_ID = 'G-BF2DSESJGX';

(function () {
  if (!GA_ID) { window.qbTrack = function () {}; window.qbTrackQ = []; return; }

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
  document.head.appendChild(s);

  gtag('js', new Date());
  /* The URL fragment carries a shared verdict (#ysnys) or pipeline numbers.
     Google never receives it: page_location is set without the hash. */
  gtag('config', GA_ID, { page_location: location.origin + location.pathname, page_title: document.title });

  /* Named events with no parameters. Usage, never content. Events fired
     before this file loaded are queued by the page and flushed here. */
  window.qbTrack = function (name) { try { gtag('event', name); } catch (e) {} };
  (window.qbTrackQ || []).forEach(window.qbTrack); window.qbTrackQ = [];
})();
