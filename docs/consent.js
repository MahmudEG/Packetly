// Cookie consent banner. Consent Mode v2 defaults are set inline in the page
// head, before gtag.js and AdSense load, so nothing is stored until a choice
// is made here. Hand-authored; build.py does not generate this file.
(() => {
  const KEY = 'packetly-consent';

  const read = () => { try { return localStorage.getItem(KEY) } catch { return null } };
  const write = v => { try { localStorage.setItem(KEY, v) } catch { /* private mode */ } };

  const apply = v => {
    if (typeof gtag !== 'function') return;
    const g = v === 'granted' ? 'granted' : 'denied';
    gtag('consent', 'update', {
      ad_storage: g, ad_user_data: g, ad_personalization: g, analytics_storage: g
    });
  };

  // An earlier choice is already applied inline in the head; nothing to ask.
  const stored = read();
  if (stored === 'granted' || stored === 'denied') return;

  const bar = document.createElement('div');
  bar.className = 'consent';
  bar.setAttribute('role', 'dialog');
  bar.setAttribute('aria-label', 'Cookie choices');
  bar.innerHTML = '<p>Packetly uses Google Analytics and Google AdSense, which set cookies. '
    + 'Decline and they stay switched off. Your bookmarks and theme are kept on this device either way. '
    + '<a href="/privacy/">How we handle data</a></p>'
    + '<div class="consent-actions">'
    + '<button class="secondary" data-consent="denied">Decline</button>'
    + '<button class="primary" data-consent="granted">Accept</button>'
    + '</div>';

  bar.addEventListener('click', e => {
    const b = e.target.closest('[data-consent]');
    if (!b) return;
    const v = b.dataset.consent;
    write(v);
    apply(v);
    bar.remove();
  });

  const mount = () => document.body.append(bar);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
