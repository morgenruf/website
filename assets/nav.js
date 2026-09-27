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
