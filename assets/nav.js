/* Close the mobile menu after a tap on one of its links, and on Escape.
 * The menu is a <details> element and opens and closes without this file;
 * this only stops it staying open over the page after an in-page jump. */
(function () {
  document.addEventListener('click', function (ev) {
    var link = ev.target && ev.target.closest ? ev.target.closest('.nav-menu-panel a') : null;
    if (!link) return;
    var menu = link.closest('details');
    if (menu) menu.removeAttribute('open');
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    var menu = document.querySelector('.nav-menu[open]');
    if (menu) { menu.removeAttribute('open'); menu.querySelector('summary').focus(); }
  });
})();

/* Cookie choice for Google Analytics. Consent defaults to denied in the
 * inline tag in <head>, which also applies a stored "accept". This shows the
 * banner when nothing is stored, records the choice, and lets the footer's
 * "Cookie settings" link ask again. */
(function () {
  var KEY = 'mr-consent';
  var box = document.getElementById('consent');
  if (!box) return;
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { if (v) localStorage.setItem(KEY, v); else localStorage.removeItem(KEY); } catch (e) {} }
  if (!get()) box.hidden = false;
  document.addEventListener('click', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('[data-consent], [data-consent-open]') : null;
    if (!el) return;
    if (el.hasAttribute('data-consent-open')) {
      ev.preventDefault();
      set(null);
      box.hidden = false;
      box.querySelector('button').focus();
      return;
    }
    var choice = el.getAttribute('data-consent');
    set(choice);
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', { analytics_storage: choice === 'accept' ? 'granted' : 'denied' });
    }
    box.hidden = true;
  });
})();
