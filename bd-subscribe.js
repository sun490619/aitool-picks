/**
 * 三站通用邮件订阅框（自包含）
 * 直接 POST 到 Buttondown 官方公开嵌入端点：
 *   https://buttondown.com/api/emails/embed-subscribe/sun490619
 * 无需 API key、不受 Worker 数据中心 IP 信誉拦截，请求来自访客真实浏览器/IP。
 * Buttondown 免费版会返回带反机器人挑战(Turnstile)的确认页 + 发确认邮件(double opt-in)，
 * 因此表单用 target="_blank" 在新标签打开确认页，让访客完成挑战+邮件确认
 * （不能用隐藏 iframe——挑战页在隐藏帧里无法完成，订阅会失败）。
 * 按域名自动适配品牌色与页脚位置，注入到每个页面页脚之前。
 * 接入方式：在 </body> 前加 <script src="/bd-subscribe.js" defer></script>
 */
(function () {
  'use strict';
  if (document.getElementById('bd-subscribe')) return; // 防止重复注入

  var host = (location.hostname || '').toLowerCase();

  // 按站点配置品牌色 / 页脚选择器 / 文案
  var CFG = {
    'aitool-picks': {
      brand: '#2f6df6', brandDark: '#1f4fc0',
      bg: '#0f172a', fg: '#e2e8f0', muted: '#94a3b8',
      title: 'Get the weekly drop in your inbox',
      sub: 'AI tools, side-hustle plays & money moves — straight to your email. No spam.',
      footerSel: '.site-footer'
    },
    'mintshovels': {
      brand: '#8b5cf6', brandDark: '#6d28d9',
      bg: '#0a0e17', fg: '#f1f5f9', muted: '#94a3b8',
      title: 'Get free SEO tips in your inbox',
      sub: 'Practical SEO checklists, AI-search tactics & audit walkthroughs. No spam.',
      footerSel: '.footer'
    },
    'makerearn': {
      brand: '#10b981', brandDark: '#047857',
      bg: '#0f172a', fg: '#e2e8f0', muted: '#94a3b8',
      title: 'Money moves, straight to your inbox',
      sub: 'New calculators, side-hustle ideas & plain-English money tips. No spam.',
      footerSel: '.site-footer'
    }
  };

  var KEY = 'default';
  for (var k in CFG) { if (host.indexOf(k) !== -1) { KEY = k; break; } }
  var c = CFG[KEY] || CFG['aitool-picks'];

  // 若 aitool-picks 旧版 formspree 订阅块仍在，先移除，避免重复
  if (KEY === 'aitool-picks') {
    var old = document.querySelector('section[aria-labelledby="newsletter"], form.newsletter-form');
    if (old) {
      var sec = old.closest('section') || old;
      if (sec && sec.parentNode) sec.parentNode.removeChild(sec);
    }
  }

  // 注入样式
  var style = document.createElement('style');
  style.textContent = [
    '.bd-subscribe{--brand:' + c.brand + ';--brand-d:' + c.brandDark + ';--bg:' + c.bg + ';--fg:' + c.fg + ';--muted:' + c.muted + ';',
    'margin:40px auto;max-width:720px;padding:28px 24px;border-radius:16px;background:var(--bg);color:var(--fg);',
    'text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.18);}',
    '.bd-subscribe__title{margin:0 0 6px;font-size:22px;font-weight:700;}',
    '.bd-subscribe__sub{margin:0 0 18px;color:var(--muted);font-size:14px;}',
    '.bd-subscribe__form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;}',
    '.bd-subscribe__input{flex:1 1 240px;min-width:0;padding:12px 14px;border-radius:10px;border:1px solid #334155;',
    'background:#0b1220;color:var(--fg);font-size:15px;}',
    '.bd-subscribe__input:focus{outline:2px solid var(--brand);outline-offset:1px;}',
    '.bd-subscribe__btn{padding:12px 22px;border:0;border-radius:10px;cursor:pointer;background:var(--brand);',
    'color:#fff;font-weight:700;font-size:15px;transition:background .15s ease;}',
    '.bd-subscribe__btn:hover{background:var(--brand-d);}',
    '.bd-subscribe__btn:disabled{opacity:.6;cursor:default;}',
    '.bd-subscribe__msg{min-height:18px;margin:12px 0 0;font-size:13px;color:var(--muted);}',
    '.bd-subscribe__msg.is-ok{color:#4ade80;}',
    '.bd-subscribe__msg.is-err{color:#f87171;}'
  ].join('');
  document.head.appendChild(style);

  // 构建组件（表单 target="_blank"：在新标签打开 Buttondown 确认页，
  // 让访客完成反机器人挑战 + 确认邮件；原站页面不跳走）
  var wrap = document.createElement('section');
  wrap.className = 'bd-subscribe';
  wrap.id = 'bd-subscribe';
  wrap.setAttribute('aria-label', 'Newsletter signup');
  wrap.innerHTML =
    '<div class="bd-subscribe__inner">' +
      '<h3 class="bd-subscribe__title">' + c.title + '</h3>' +
      '<p class="bd-subscribe__sub">' + c.sub + '</p>' +
      '<form class="bd-subscribe__form" id="bd-subscribe-form" ' +
        'action="https://buttondown.com/api/emails/embed-subscribe/sun490619" method="POST" target="_blank" rel="noopener" novalidate>' +
        '<input class="bd-subscribe__input" type="email" name="email" id="bd-subscribe-email" ' +
          'placeholder="you@example.com" autocomplete="email" required>' +
        '<input type="hidden" name="tag" value="web-signup">' +
        '<button class="bd-subscribe__btn" type="submit">Subscribe</button>' +
      '</form>' +
      '<p class="bd-subscribe__msg" id="bd-subscribe-msg" role="status" aria-live="polite"></p>' +
    '</div>';

  // 插入页脚之前（找不到页脚则追加到 body 末尾）
  var footer = document.querySelector(c.footerSel);
  if (footer && footer.parentNode) {
    footer.parentNode.insertBefore(wrap, footer);
  } else {
    document.body.appendChild(wrap);
  }

  // 表单逻辑：前端校验邮箱；通过后允许正常提交（新标签打开确认页），并提示查收邮件
  var form = document.getElementById('bd-subscribe-form');
  var input = document.getElementById('bd-subscribe-email');
  var btn = form.querySelector('button');
  var msg = document.getElementById('bd-subscribe-msg');

  form.addEventListener('submit', function (e) {
    var email = (input.value || '').trim();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      e.preventDefault();
      msg.textContent = 'Please enter a valid email.';
      msg.className = 'bd-subscribe__msg is-err';
      return;
    }
    // 校验通过：表单正常提交到新标签（Buttondown 确认页），原站提示查收邮件
    msg.textContent = "Almost there — confirm in the new tab, then check your inbox.";
    msg.className = 'bd-subscribe__msg is-ok';
    setTimeout(function () { input.value = ''; }, 400);
  });
})();
