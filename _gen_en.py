#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""英文版文章页生成器，派生自 _gen_zh.py（改 lang=en + 英文导航/页脚 + i18n 互指）。
用法: from _gen_en import build
"""
import os, json

POSTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')

# ---------- 可复用的英文外壳 ----------
CHROME_HEADER_EN = r'''    <header class="site-header" id="siteHeader" role="banner">
        <div class="container header-inner">
            <a href="/" class="brand" aria-label="AI Tool Picks - Home">
                <span class="brand-mark">ATP</span>
                <span>AI Tool Picks</span>
            </a>
            <nav class="main-nav">
                <a href="/" class="nav-link">Home</a>
                <a href="/category/writing.html" class="nav-link">AI Writing</a>
                <a href="/category/coding.html" class="nav-link">AI Coding</a>
                <a href="/category/video.html" class="nav-link">AI Video</a>
                <a href="/category/seo.html" class="nav-link">AI SEO</a>
                <a href="/category/productivity.html" class="nav-link">AI Productivity</a>
                <a href="/about.html" class="nav-link">About</a>
                <a href="/contact.html" class="nav-link">Contact</a>
            </nav>
            <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
            </button>
        </div>
    </header>
    <div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>
    <div class="mobile-menu" id="mobileMenu" role="dialog" aria-modal="true" aria-labelledby="mobileMenuTitle">
        <div class="mobile-menu-header">
            <span class="brand" id="mobileMenuTitle"><span class="brand-mark">ATP</span> AI Tool Picks</span>
            <button class="mobile-menu-close" id="mobileMenuClose" aria-label="Close menu">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </div>
        <nav class="mobile-nav" role="navigation" aria-label="Main Navigation">
            <a href="/" class="mobile-nav-link" aria-current="page">Home</a>
            <a href="/category/writing.html" class="mobile-nav-link">AI Writing</a>
            <a href="/category/coding.html" class="mobile-nav-link">AI Coding</a>
            <a href="/category/video.html" class="mobile-nav-link">AI Video</a>
            <a href="/category/seo.html" class="mobile-nav-link">AI SEO</a>
            <a href="/category/productivity.html" class="mobile-nav-link">AI Productivity</a>
            <a href="/about.html" class="mobile-nav-link">About</a>
            <a href="/contact.html" class="mobile-nav-link">Contact</a>
        </nav>
        <div class="drawer-section">
            <div class="drawer-section-label" data-i18n="lang_label">Language</div>
            <div class="lang-toggle">
                <button class="lang-btn active" data-lang="en">EN</button>
                <button class="lang-btn" data-lang="zh">中文</button>
            </div>
        </div>
        <div class="drawer-section">
            <div class="drawer-section-label" data-i18n="theme_label">Theme</div>
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">🌓</button>
        </div>
    </div>'''

CHROME_FOOTER_SCRIPTS_EN = r'''    <footer class="site-footer">
        <div class="container footer-inner">
            <p>&copy; 2026 AI Tool Picks. Independent reviews.</p>
            <nav class="footer-links" aria-label="Footer">
                <a href="/about.html">About</a>
                <a href="/contact.html">Contact</a>
                <a href="/privacy.html">Privacy</a>
                <a href="/affiliate-disclosure.html">Affiliate Disclosure</a>
            </nav>
        </div>
    </footer>
    <script src="/shared.js"></script>
    <script src="/scripts.js"></script>
    <script src="/bd-subscribe.js" defer></script>'''


def build(slug, title, desc, h1, dateline, main_html, faq_json=None, og_image=None):
    zh_url = "https://aitool-picks.com/posts/%s-zh.html" % slug
    en_url = "https://aitool-picks.com/posts/%s.html" % slug
    if og_image is None:
        og_image = "/images/og-%s.jpg" % slug

    faq_block = ""
    if faq_json:
        faq_block = ('    <script type="application/ld+json">\n'
                     + json.dumps(faq_json, ensure_ascii=False, indent=4)
                     + '\n    </script>\n')

    head = '''<!DOCTYPE html>
<html lang="en" data-zh-url="__ZHURL__">
<head>
    <link rel="alternate" hreflang="zh" href="__ZHURL__">
    <link rel="alternate" hreflang="en" href="__ENURL__">
    <link rel="alternate" hreflang="x-default" href="__ENURL__">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>__TITLE__</title>
    <meta name="description" content="__DESC__">
    <meta property="og:type" content="article">
    <meta property="og:title" content="__TITLE__">
    <meta property="og:description" content="__DESC__">
    <meta property="og:url" content="__ENURL__">
    <meta property="og:image" content="__OGIMAGE__">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESC__">
    <link rel="stylesheet" href="../styles.css?v=20260725l">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": __JHEAD__,
      "description": __JDESC__,
      "inLanguage": "en",
      "datePublished": "2026-07-26",
      "dateModified": "2026-07-26",
      "author": {"@type": "Organization", "name": "AI Tool Picks Team"},
      "publisher": {"@type": "Organization", "name": "AI Tool Picks"},
      "mainEntityOfPage": {"@type": "WebPage", "@id": __JENURL__}
    }
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D53DQ3JKKL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-D53DQ3JKKL');
    </script>
    <script type="text/javascript">
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", "xavbiwb9dt");
    </script>
    <link rel="canonical" href="__ENURL__">
__FAQ__</head>
<body>
__HEADER__
__MAIN__
__FOOTER__</body>
</html>'''

    head = (head
            .replace("__ZHURL__", zh_url)
            .replace("__ENURL__", en_url)
            .replace("__TITLE__", title)
            .replace("__DESC__", desc)
            .replace("__OGIMAGE__", og_image)
            .replace("__JHEAD__", json.dumps(title, ensure_ascii=False))
            .replace("__JDESC__", json.dumps(desc, ensure_ascii=False))
            .replace("__JENURL__", json.dumps(en_url, ensure_ascii=False))
            .replace("__FAQ__", faq_block)
            .replace("__HEADER__", CHROME_HEADER_EN)
            .replace("__MAIN__", main_html)
            .replace("__FOOTER__", CHROME_FOOTER_SCRIPTS_EN))

    out = os.path.join(POSTS, slug + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(head)
    print("生成(en):", out)


if __name__ == "__main__":
    pass
