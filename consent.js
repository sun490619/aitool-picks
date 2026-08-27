/* Cookie consent banner + Google Consent Mode v2.
   The "denied" default for EEA/UK is set inline in <head> (before gtag config)
   by the site build. This script shows the banner on first visit and updates
   consent when the visitor accepts/rejects, then exposes window.__adConsent. */
(function () {
  var KEY = 'ms_consent';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function grant() {
    if (window.gtag) window.gtag('consent', 'update', {
      ad_storage: 'granted', ad_user_data: 'granted',
      ad_personalization: 'granted', analytics_storage: 'granted'
    });
    window.__adConsent = 'granted';
  }
  function deny() {
    if (window.gtag) window.gtag('consent', 'update', {
      ad_storage: 'denied', ad_user_data: 'denied',
      ad_personalization: 'denied', analytics_storage: 'denied'
    });
    window.__adConsent = 'denied';
  }

  function build() {
    var css = document.createElement('link');
    css.rel = 'stylesheet'; css.href = '/consent.css';
    document.head.appendChild(css);

    var wrap = document.createElement('div');
    wrap.id = 'ms-consent-wrap';
    wrap.innerHTML =
      '<div id="ms-consent" role="dialog" aria-label="Cookie consent">' +
      '<p>We use cookies for analytics and to show relevant ads via Google AdSense. ' +
      'See our <a href="/privacy">Privacy Policy</a>. You can accept or reject non-essential cookies.</p>' +
      '<div class="ms-btns">' +
      '<button id="ms-reject" type="button">Reject</button>' +
      '<button id="ms-accept" type="button">Accept</button>' +
      '</div></div>';
    document.body.appendChild(wrap);

    function choose(v) {
      set(v);
      if (v === 'granted') grant(); else deny();
      if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
      showManage();
    }
    document.getElementById('ms-accept').addEventListener('click', function () { choose('granted'); });
    document.getElementById('ms-reject').addEventListener('click', function () { choose('denied'); });
  }

  function showManage() {
    if (document.getElementById('ms-manage')) return;
    var b = document.createElement('button');
    b.id = 'ms-manage'; b.type = 'button'; b.textContent = 'Cookie settings';
    b.addEventListener('click', function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
      window.__adConsent = undefined;
      if (document.getElementById('ms-consent-wrap')) return;
      build();
    });
    document.body.appendChild(b);
  }

  function init() {
    var c = get();
    if (c === 'granted') { grant(); showManage(); }
    else if (c === 'denied') { deny(); showManage(); }
    else { build(); }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
