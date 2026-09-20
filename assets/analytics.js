/* Site analytics. Cookieless on purpose.
 *
 * persistence: 'memory' means nothing is written to the visitor's browser, so
 * the site stays out of consent-banner territory the same way the Cloudflare
 * counts already do. The price is that a returning visitor reads as a new one,
 * which is the right trade for a site whose only question is "did this page
 * send anyone to the install link".
 *
 * autocapture is off. Clicks worth counting are named below, one by one, so
 * nothing sweeps up the text of whatever someone happened to click.
 */
(function () {
  var KEY = 'phc_ARwdnaLcHimoQsHL9SsghTrKjuJssnQHzVpQe89zknD7';
  var HOST = 'https://us.i.posthog.com';
  var ASSETS = 'https://us-assets.i.posthog.com';

  // Delegated and attached now, so a click that lands before the SDK has
  // loaded is still counted once it arrives.
  document.addEventListener('click', function (ev) {
    var link = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!link || !window.posthog || !window.posthog.capture) return;
    var href = link.getAttribute('href') || '';
    if (href.indexOf('/install') !== -1) {
      window.posthog.capture('install_clicked', {
        page: location.pathname,
        label: (link.textContent || '').trim().slice(0, 60)
      });
    } else if (href.indexOf('github.com') !== -1) {
      window.posthog.capture('github_clicked', { page: location.pathname });
    }
  });

  var script = document.createElement('script');
  script.src = ASSETS + '/static/array.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  script.onload = function () {
    if (!window.posthog || !window.posthog.init) return;
    window.posthog.init(KEY, {
      api_host: HOST,
      ui_host: 'https://us.posthog.com',
      persistence: 'memory',
      autocapture: false,
      disable_session_recording: true,
      disable_surveys: true,
      capture_pageview: true,
      capture_pageleave: true,
      person_profiles: 'identified_only',
      respect_dnt: true
    });
  };
  document.head.appendChild(script);
})();
