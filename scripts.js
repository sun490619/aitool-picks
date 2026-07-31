/**
 * AI Tool Picks — Shared JavaScript
 * Mobile menu, reading progress, smooth scroll, etc.
 */

(function() {
  'use strict';

  // ========================================
  // Mobile Menu
  // ========================================
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
  const mobileMenuClose = document.getElementById('mobileMenuClose');

  function openMobileMenu() {
    mobileMenu.classList.add('open');
    mobileMenuOverlay.classList.add('open');
    mobileMenuBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    // Focus first link for accessibility
    const firstLink = mobileMenu.querySelector('.mobile-nav-link');
    if (firstLink) firstLink.focus();
  }

  function closeMobileMenu() {
    mobileMenu.classList.remove('open');
    mobileMenuOverlay.classList.remove('open');
    mobileMenuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', openMobileMenu);
    mobileMenuOverlay?.addEventListener('click', closeMobileMenu);
    mobileMenuClose?.addEventListener('click', closeMobileMenu);

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        closeMobileMenu();
      }
    });

    // Close when clicking a link
    mobileMenu.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });
  }

  // ========================================
  // Reading Progress Bar
  // ========================================
  const progressBar = document.getElementById('progressBar');

  function updateProgressBar() {
    if (!progressBar) return;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.transform = `scaleX(${progress / 100})`;
  }

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateProgressBar();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Initial update
  updateProgressBar();

  // ========================================
  // Smooth Scroll for Anchor Links
  // ========================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        target.focus({ preventScroll: true });
      }
    });
  });

  // ========================================
  // Header Scroll Effect
  // ========================================
  const siteHeader = document.getElementById('siteHeader');
  let lastScrollY = window.scrollY;

  function handleHeaderScroll() {
    if (!siteHeader) return;
    const currentScrollY = window.scrollY;
    if (currentScrollY > 10) {
      siteHeader.classList.add('scrolled');
    } else {
      siteHeader.classList.remove('scrolled');
    }
    lastScrollY = currentScrollY;
  }

  window.addEventListener('scroll', handleHeaderScroll, { passive: true });
  handleHeaderScroll();

  // ========================================
  // Intersection Observer for Animations
  // ========================================
  const animatedElements = document.querySelectorAll('.animate-fade-in-up, .stagger-1, .stagger-2, .stagger-3, .stagger-4');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animatedElements.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(1rem)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(el);
    });
  } else {
    // Fallback for browsers without IntersectionObserver
    animatedElements.forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    });
  }

  // ========================================
  // Table of Contents Active Link Highlighting
  // ========================================
  const tocLinks = document.querySelectorAll('.toc-link');
  const headings = document.querySelectorAll('.article-body h2, .article-body h3');

  if (tocLinks.length > 0 && headings.length > 0 && 'IntersectionObserver' in window) {
    const headingObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          tocLinks.forEach(link => {
            link.classList.toggle('toc-active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });

    headings.forEach(h => headingObserver.observe(h));
  }

  // Add active style for TOC links
  const style = document.createElement('style');
  style.textContent = `
    .toc-link.toc-active {
      color: var(--accent);
      background: rgba(99, 102, 241, 0.1);
      font-weight: 600;
    }
  `;
  document.head.appendChild(style);

  // ========================================
  // Copy Code Block Button (progressive enhancement)
  // ========================================
  document.querySelectorAll('.article-body pre').forEach(pre => {
    if (pre.querySelector('.copy-code-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-code-btn';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"></path></svg>';
    btn.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 6px;
      background: rgba(0,0,0,0.3);
      border: none;
      border-radius: 6px;
      color: #cdd6f4;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s, background 0.2s;
      z-index: 10;
    `;
    pre.style.position = 'relative';
    pre.appendChild(btn);

    pre.addEventListener('mouseenter', () => btn.style.opacity = '1');
    pre.addEventListener('mouseleave', () => btn.style.opacity = '0');

    btn.addEventListener('click', async () => {
      const code = pre.querySelector('code')?.innerText || pre.innerText;
      try {
        await navigator.clipboard.writeText(code);
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M20 6L9 17l-5-5"></path></svg>';
        btn.style.color = '#10b981';
        setTimeout(() => {
          btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"></path></svg>';
          btn.style.color = '';
        }, 2000);
      } catch (e) {
        btn.style.color = '#ef4444';
      }
    });
  });

  // ========================================
  // Lazy Load Images (native + fallback)
  // ========================================
  if ('loading' in HTMLImageElement.prototype) {
    // Native lazy loading supported
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      img.loading = 'lazy';
    });
  } else {
    // Fallback IntersectionObserver
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imgObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imgObserver.unobserve(img);
        }
      });
    });
    lazyImages.forEach(img => imgObserver.observe(img));
  }

  // ========================================
  // Performance: Prefetch on Hover
  // ========================================
  document.querySelectorAll('a[href]').forEach(link => {
    if (link.origin !== window.location.origin) return;
    let prefetched = false;
    link.addEventListener('mouseenter', () => {
      if (prefetched) return;
      const href = link.getAttribute('href');
      if (href && !href.startsWith('#') && !href.startsWith('mailto:') && !href.startsWith('tel:')) {
        const linkEl = document.createElement('link');
        linkEl.rel = 'prefetch';
        linkEl.href = href;
        document.head.appendChild(linkEl);
        prefetched = true;
      }
    }, { once: true, passive: true });
  });

})();

// Make functions globally accessible if needed
window.AIToolPicks = {
  closeMobileMenu: () => {
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    mobileMenu?.classList.remove('open');
    mobileMenuOverlay?.classList.remove('open');
    mobileMenuBtn?.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
};
// Filter + Pagination for article grid
(() => {
  const grid = document.getElementById('postsGrid');
  const pagination = document.getElementById('pagination');
  if (!grid || !pagination) return;

  const cards = Array.from(grid.querySelectorAll('article.post-card'));
  // 分类由HTML的data-category属性决定（已在构建时正确标注），JS不再覆盖
  const PER_PAGE = 8;
  let currentCategory = 'all';
  let currentPage = 1;
  let currentSearch = '';

  // data-category 已在HTML中正确标注，无需JS再覆盖

  function matchesSearch(card) {
    if (!currentSearch) return true;
    const q = currentSearch.toLowerCase();
    const title = (card.querySelector('.post-card-title')?.textContent || '').toLowerCase();
    const excerpt = (card.querySelector('.post-card-excerpt')?.textContent || '').toLowerCase();
    return title.includes(q) || excerpt.includes(q);
  }

  function render() {
    let filtered = cards.filter(c => {
      const catOk = currentCategory === 'all' || c.dataset.category === currentCategory;
      return catOk && matchesSearch(c);
    });
    cards.forEach(c => { c.style.display = 'none'; });
    filtered.forEach(c => { c.style.display = ''; });
    const totalPages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
    if (currentPage > totalPages) currentPage = totalPages;
    const start = (currentPage - 1) * PER_PAGE;
    filtered.forEach((c, i) => {
      if (currentCategory === 'all') {
        c.style.display = (i >= start && i < start + PER_PAGE) ? '' : 'none';
      } else {
        const idx = filtered.indexOf(c);
        c.style.display = (idx >= start && idx < start + PER_PAGE) ? '' : 'none';
      }
    });
    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    if (totalPages <= 1) { pagination.innerHTML = ''; return; }
    let html = '';
    html += `<button class="page-btn" data-page="${currentPage - 1}" ${currentPage === 1 ? 'disabled' : ''}">Prev</button>`;
    // 省略号逻辑：始终显示首尾，当前页左右各1，其余用 …
    const pages = new Set();
    pages.add(1);
    pages.add(totalPages);
    pages.add(currentPage);
    if (currentPage - 1 >= 1) pages.add(currentPage - 1);
    if (currentPage + 1 <= totalPages) pages.add(currentPage + 1);
    const sorted = Array.from(pages).sort((a, b) => a - b);
    let prev = 0;
    for (const p of sorted) {
      if (p - prev > 1) html += `<span class="page-ellipsis">…</span>`;
      html += `<button class="page-btn ${p === currentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
      prev = p;
    }
    html += `<button class="page-btn" data-page="${currentPage + 1}" ${currentPage === totalPages ? 'disabled' : ''}>Next</button>`;
    pagination.innerHTML = html;
    pagination.querySelectorAll('.page-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const p = parseInt(btn.dataset.page, 10);
        if (p >= 1 && p <= totalPages) { currentPage = p; render(); }
      });
    });
  }

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      currentPage = 1;
      render();
    });
  });

  const searchInput = document.getElementById('postSearch');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      currentSearch = searchInput.value.trim();
      currentPage = 1;
      render();
    });
  }

  render();
})();

// ---- Post "Was this helpful?" vote widget (zero-backend, per-URL localStorage) ----
(function () {
  // 投票框只出现在【文章详情页】（/posts/ 下的页面）。
  // 列表页（首页 /category/）的卡片也用 <article class="post-card">，
  // 绝不能在列表页注入投票框——否则会污染卡片、挤掉 Read 链接。
  if (location.pathname.indexOf('/posts/') === -1) return;
  // 文章详情页正文容器：老页 article.post，新页 article.article-content。
  var article = document.querySelector('article.post, article.article-content');
  if (!article) return;
  // 防重复注入（若脚本被加载两次）
  if (article.querySelector('#voteUp')) return;
  var key = 'atp_vote_' + location.pathname;
  var box = document.createElement('div');
  box.style.cssText = 'margin:30px 0 8px;padding:18px 20px;border:1px solid #e2e8f0;border-radius:14px;background:#f8fafc;text-align:center;';
  box.innerHTML = '<div style="font-weight:700;margin-bottom:10px;">Was this review helpful?</div>' +
    '<button id="voteUp" style="cursor:pointer;font:inherit;font-weight:600;padding:9px 18px;border-radius:10px;border:1px solid #22c55e;background:#22c55e;color:#fff;margin:0 6px;">👍 Yes</button>' +
    '<button id="voteDown" style="cursor:pointer;font:inherit;font-weight:600;padding:9px 18px;border-radius:10px;border:1px solid #cbd5e1;background:#fff;color:#334155;margin:0 6px;">👎 Not really</button>' +
    '<div id="voteMsg" style="margin-top:10px;font-size:.9rem;color:#64748b;"></div>';
  article.appendChild(box);
  var up = document.getElementById('voteUp'), down = document.getElementById('voteDown'), msg = document.getElementById('voteMsg');
  var saved = localStorage.getItem(key);
  if (saved) {
    msg.textContent = saved === 'up' ? 'Thanks — you found this helpful.' : 'Thanks for the feedback — it helps us improve.';
    up.disabled = true; down.disabled = true;
  }
  up.addEventListener('click', function () {
    localStorage.setItem(key, 'up');
    msg.textContent = 'Thanks — you found this helpful.';
    up.disabled = true; down.disabled = true;
  });
  down.addEventListener('click', function () {
    localStorage.setItem(key, 'down');
    msg.textContent = 'Thanks for the feedback — it helps us improve.';
    up.disabled = true; down.disabled = true;
  });
})();
