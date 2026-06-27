/**
 * AI Tool Picks — Shared Theme & Language Logic
 * 
 * Handles cross-page state persistence:
 * 1. Dark/Light theme toggle (via html.dark class + localStorage)
 * 2. Language switch EN/中文 (via localStorage + data-i18n translation)
 * 
 * Load this BEFORE scripts.js on every page.
 */
(function() {
  'use strict';

  var THEME_KEY = 'aitoolpicks-theme';
  var LANG_KEY = 'aitoolpicks-lang';

  // ========================================
  // THEME: Dark/Light Toggle
  // CSS uses html.dark to override :root vars.
  // No html.dark = light mode (CSS :root defaults).
  // ========================================

  function getSavedTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
    // No saved preference → use system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
    return 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  function updateThemeUI() {
    var isDark = document.documentElement.classList.contains('dark');
    var label = document.getElementById('themeLabel');
    var icon = document.getElementById('themeIcon');
    if (label) {
      label.textContent = isDark ? 'Light' : 'Dark';
    }
    if (icon) {
      icon.innerHTML = isDark
        ? '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'
        : '<circle cx="12" cy="12" r="5"/><g stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></g>';
    }
  }

  // Initialize theme on page load
  var currentTheme = getSavedTheme();
  applyTheme(currentTheme);

  // Update UI after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateThemeUI);
  } else {
    updateThemeUI();
  }

  function toggleTheme() {
    var isDark = document.documentElement.classList.contains('dark');
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem(THEME_KEY, 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem(THEME_KEY, 'dark');
    }
    updateThemeUI();
  }

  // Delegated click handler for theme toggle button
  document.addEventListener('click', function(e) {
    var toggle = e.target.closest('#themeToggle');
    if (toggle) {
      e.preventDefault();
      e.stopPropagation();
      toggleTheme();
    }
  });

  // ========================================
  // LANGUAGE: EN / 中文 Switch
  // ========================================

  // Translation map: data-i18n key → { en, zh }
  var translations = {
    // Nav
    'nav_home':        { en: 'Home', zh: '首页' },
    'nav_writing':     { en: 'AI Writing', zh: 'AI 写作' },
    'nav_coding':      { en: 'AI Coding', zh: 'AI 编程' },
    'nav_video':       { en: 'AI Video', zh: 'AI 视频' },
    'nav_seo':         { en: 'AI SEO', zh: 'AI SEO' },
    'nav_categories':  { en: 'Categories', zh: '分类' },
    'nav_blog':        { en: 'Blog', zh: '博客' },
    // Hero
    'hero_title_line1': { en: 'Honest', zh: '真实的' },
    'hero_title_line2': { en: 'AI Tool Reviews', zh: 'AI 工具评测' },
    'hero_title_line3': { en: '& Comparisons', zh: '与对比' },
    'hero_subtitle':   { en: 'We test the top AI writing, coding, video, and SEO tools so you don\'t have to. No marketing fluff — just hands-on testing and honest verdicts.', zh: '我们替你测试顶级的 AI 写作、编程、视频和 SEO 工具。没有营销废话——只有亲手测试和真实结论。' },
    // Sections
    'section_latest':  { en: 'Latest Reviews', zh: '最新评测' },
    'section_categories': { en: 'Explore by Category', zh: '按分类浏览' },
    // Drawer
    'lang_label':      { en: 'Language', zh: '语言' },
    'theme_label':     { en: 'Theme', zh: '主题' },
    // Buttons
    'cta_explore':     { en: 'Explore Tools', zh: '探索工具' },
    'cta_compare':     { en: 'Compare Tools', zh: '对比工具' },
    'read_more':       { en: 'Read More', zh: '阅读更多' },
    'view_all':        { en: 'View All', zh: '查看全部' }
  };

  function getSavedLang() {
    return localStorage.getItem(LANG_KEY) || 'en';
  }

  function updateLangButtons(activeLang) {
    var container = document.getElementById('langSwitch');
    if (!container) return;
    var buttons = container.querySelectorAll('button');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var isActive = btn.getAttribute('data-lang') === activeLang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    }
  }

  function applyTranslations(lang) {
    // Translate all elements with data-i18n attribute
    var elements = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < elements.length; i++) {
      var el = elements[i];
      var key = el.getAttribute('data-i18n');
      if (translations[key] && translations[key][lang]) {
        el.textContent = translations[key][lang];
      }
    }
    // Also update html lang attribute
    document.documentElement.lang = lang;
  }

  function switchLang(lang) {
    localStorage.setItem(LANG_KEY, lang);
    updateLangButtons(lang);
    applyTranslations(lang);
  }

  // Initialize language on page load
  var savedLang = getSavedLang();
  updateLangButtons(savedLang);
  applyTranslations(savedLang);

  // Delegated click handler for lang switch buttons
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('#langSwitch button');
    if (btn) {
      e.preventDefault();
      e.stopPropagation();
      var lang = btn.getAttribute('data-lang');
      if (lang) switchLang(lang);
    }
  });

  // ========================================
  // Expose globally
  // ========================================
  window.AIToolPicksTheme = {
    toggleTheme: toggleTheme,
    getTheme: function() { return localStorage.getItem(THEME_KEY) || 'light'; },
    switchLang: switchLang,
    getLang: function() { return getSavedLang(); }
  };

})();
