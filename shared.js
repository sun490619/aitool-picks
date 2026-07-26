/**
 * AI Tool Picks — Shared Theme & Language Logic
 * 
 * Handles cross-page state persistence:
 * 1. Dark/Light theme toggle (via html.dark class + localStorage)
 * 2. Language switch EN/中文 (via localStorage + full-page text translation)
 * 
 * Translation approach: maintains a complete en→zh translation map,
 * scans ALL text nodes on the page, and replaces matching English text
 * with Chinese equivalents. This covers article content, tool descriptions,
 * navigation, footer, buttons — everything visible.
 * 
 * Load this BEFORE scripts.js on every page.
 */
(function() {
  'use strict';

  var THEME_KEY = 'aitoolpicks-theme';
  var LANG_KEY = 'aitoolpicks-lang';

  // ========================================
  // THEME: Dark/Light Toggle
  // ========================================

  function getSavedTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
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

  var currentTheme = getSavedTheme();
  applyTheme(currentTheme);

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

  document.addEventListener('click', function(e) {
    var toggle = e.target.closest('#themeToggle');
    if (toggle) {
      e.preventDefault();
      e.stopPropagation();
      toggleTheme();
    }
  });

  // ========================================
  // LANGUAGE: Switch between REAL bilingual pages only
  // ========================================
  // aitool-picks is English-primary. A curated set of article pages have a
  // dedicated, fully-translated Chinese counterpart, linked via the
  // `data-zh-url` attribute on <html>. The language switch ONLY navigates
  // between these real counterpart pages. Pages without a `data-zh-url` have
  // no Chinese version, so the switch is hidden there. This intentionally
  // removes the old in-place JS text-swap translation (the `enToZh` map),
  // which produced half-English/half-Chinese broken pages and was never
  // indexed by Google.

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

  // Navigate to the real counterpart page if one exists.
  function switchLang(lang) {
    localStorage.setItem(LANG_KEY, lang);
    updateLangButtons(lang);
    var zhUrl = document.documentElement.getAttribute('data-zh-url');
    var currentLang = document.documentElement.lang || 'en';
    // Only navigate when a true counterpart page is declared and we are not
    // already on it.
    if (zhUrl && lang !== currentLang) {
      window.location.href = zhUrl;
    }
    // Pages without a data-zh-url have no Chinese version — do nothing.
  }

  // Initialize language on page load
  var savedLang = getSavedLang();
  updateLangButtons(savedLang);

  function initLang() {
    var hasZh = !!document.documentElement.getAttribute('data-zh-url');
    var langSwitch = document.getElementById('langSwitch');
    if (!langSwitch) return;
    // aitool-picks is English-primary. The Language switch is only meaningful
    // on the curated article pages that have a real, fully-translated Chinese
    // counterpart (declared via data-zh-url). On every other page we hide the
    // ENTIRE Language section (label + pill, i.e. its parent wrapper) so the
    // drawer footer shows only the Theme toggle — no dangling dead "Language"
    // label with nothing under it.
    var section = langSwitch.parentElement;
    if (hasZh) {
      if (section) section.style.display = '';
      langSwitch.style.display = '';
    } else {
      if (section) section.style.display = 'none';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLang);
  } else {
    initLang();
  }

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
