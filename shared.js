/**
 * AI Tool Picks — Shared Theme & Language Logic
 * 
 * This file handles cross-page state persistence:
 * 1. Dark/Light theme toggle (via html.dark class + localStorage)
 * 2. Language switch EN/中文 (via localStorage)
 * 3. Drawer menu panel integration
 * 
 * Load this BEFORE scripts.js on every page.
 */
(function() {
  'use strict';

  // ========================================
  // THEME: Dark/Light Toggle
  // ========================================
  const THEME_KEY = 'aitoolpicks-theme';
  const LANG_KEY = 'aitoolpicks-lang';

  // Apply saved theme on load
  (function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light') {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    } else {
      // Default: dark
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    }
    updateThemeButton();
  })();

  function toggleTheme() {
    const isLight = document.documentElement.classList.contains('light');
    if (isLight) {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
      localStorage.setItem(THEME_KEY, 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
      localStorage.setItem(THEME_KEY, 'light');
    }
    updateThemeButton();
  }

  function updateThemeButton() {
    const btn = document.getElementById('themeToggle');
    const label = document.getElementById('themeLabel');
    const icon = document.getElementById('themeIcon');
    if (!btn || !label) return;

    const isLight = document.documentElement.classList.contains('light');
    if (isLight) {
      label.textContent = 'Dark';
      if (icon) {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"/><g stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></g>';
      }
    } else {
      label.textContent = 'Light';
      if (icon) {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
      }
    }
  }

  // Bind theme toggle button (may not exist yet on DOMContentLoaded)
  document.addEventListener('click', function(e) {
    const toggle = e.target.closest('#themeToggle');
    if (toggle) {
      e.preventDefault();
      toggleTheme();
    }
  });

  // ========================================
  // LANGUAGE: EN / 中文 Switch
  // ========================================
  (function initLanguage() {
    const saved = localStorage.getItem(LANG_KEY) || 'en';
    updateLangButtons(saved);
  })();

  function switchLang(lang) {
    localStorage.setItem(LANG_KEY, lang);
    updateLangButtons(lang);
    // Future: apply translations dynamically
  }

  function updateLangButtons(activeLang) {
    const container = document.getElementById('langSwitch');
    if (!container) return;
    const buttons = container.querySelectorAll('button');
    buttons.forEach(btn => {
      const isActive = btn.getAttribute('data-lang') === activeLang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  // Bind lang switch clicks
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('#langSwitch button');
    if (btn) {
      e.preventDefault();
      const lang = btn.getAttribute('data-lang');
      if (lang) switchLang(lang);
    }
  });

  // ========================================
  // Expose globally
  // ========================================
  window.AIToolPicksTheme = {
    toggleTheme: toggleTheme,
    getTheme: () => localStorage.getItem(THEME_KEY) || 'dark',
    switchLang: switchLang,
    getLang: () => localStorage.getItem(LANG_KEY) || 'en'
  };

})();
