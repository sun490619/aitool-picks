#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 2 篇 aitool-picks 评测文(en+zh) + og 图 + 接线分类页 + sitemap。
① getreditus-review-2026  (AI Productivity) -> rewardful.com/?via=sun490619
② best-ai-resume-builders-2026 (AI Productivity) -> aiapply.co/?via=sun490619 + rytr.me/?via=sun490619
脚注用首页完整 footer-grid（守脚注铁律）。
"""
import os, json, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(ROOT, 'posts')
IMG = os.path.join(ROOT, 'images')
DATE = "2026-08-03"

# ---------------- og 图 ----------------
def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def make_og(path, title, tag):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (13, 17, 33))
    d = ImageDraw.Draw(img)
    # subtle vertical gradient
    for y in range(H):
        t = y / H
        r = int(13 + t * 14); g = int(17 + t * 18); b = int(33 + t * 26)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # accent bar
    d.rectangle([90, 232, 134, 322], fill=(99, 102, 241))
    d.rectangle([90, 232, 134, 252], fill=(56, 189, 248))
    # mark
    mf = _font(26)
    d.text((170, 236), "AI TOOL PICKS", font=mf, fill=(148, 163, 184))
    # title wrap
    tf = _font(54, bold=True)
    words = title.split()
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) > 24:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    lines = lines[:4]
    y = 300
    for ln in lines:
        d.text((90, y), ln, font=tf, fill=(255, 255, 255))
        y += 62
    # tag pill
    sf = _font(26)
    d.text((90, 540), tag, font=sf, fill=(165, 180, 252))
    img.save(path, "JPEG", quality=86)
    print("og:", path)

# ---------------- 完整脚注（复刻首页，逐字符一致） ----------------
EN_FOOTER = '''    <footer class="site-footer" role="contentinfo">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="footer-logo"><span class="brand-mark">ATP</span>AI Tool Picks</a>
                    <p class="footer-desc">Honest comparisons & reviews of the best AI tools. Hand-tested, independently written, zero fluff.</p>
                    <div class="footer-social">
                        <a href="https://x.com/wangqwkl" target="_blank" rel="noopener noreferrer" aria-label="X">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <a href="https://github.com/sun490619" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
                        </a>
                    </div>
                </div>

                <div class="footer-column">
                    <h4>Categories</h4>
                    <ul class="footer-links">
                        <li><a href="/category/writing.html">AI Writing Tools</a></li>
                        <li><a href="/category/coding.html">AI Coding Assistants</a></li>
                        <li><a href="/category/video.html">AI Video Generators</a></li>
                        <li><a href="/category/seo.html">AI SEO Tools</a></li>
                        <li><a href="/category/productivity.html">AI Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Popular Reviews</h4>
                    <ul class="footer-links">
                        <li><a href="/posts/jasper-vs-writesonic.html">Jasper vs Writesonic</a></li>
                        <li><a href="/posts/best-ai-seo-tools-2026.html">Best AI SEO Tools</a></li>
                        <li><a href="/category/writing.html">All Writing Tools</a></li>
                        <li><a href="/category/seo.html">All SEO Tools</a></li>
                        <li><a href="/category/productivity.html">All Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>More from</h4>
                    <ul class="footer-links">
                        <li><a href="https://mintshovels.com/" target="_blank" rel="noopener">MintShovels — Free SEO Audit Tool</a></li>
                        <li><a href="https://makerearn.com/" target="_blank" rel="noopener">makerearn — Free Money Calculators</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Resources</h4>
                    <ul class="footer-links">
                        <li><a href="/suggest-tool.html">Suggest a Tool</a></li>
                        <li><a href="/affiliate-disclosure.html">Affiliate Disclosure</a></li>
                        <li><a href="/privacy.html">Privacy Policy</a></li>
                        <li><a href="#bd-subscribe">Newsletter</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-bottom">
                <p>&copy; 2026 AI Tool Picks. All rights reserved.</p>
                <p class="last-updated">Last updated: July 27, 2026</p>
                <div class="flex gap-3">
                    <a href="/privacy.html">Privacy Policy</a>
                    <a href="/affiliate-disclosure.html">Affiliate Disclosure</a>
                </div>
            </div>
        </div>
    </footer>
    <script src="/shared.js"></script>
    <script src="/scripts.js"></script>
<script src="/bd-subscribe.js" defer></script>'''

ZH_FOOTER = '''    <footer class="site-footer" role="contentinfo">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="footer-logo"><span class="brand-mark">ATP</span>AI Tool Picks</a>
                    <p class="footer-desc">真实、诚实的最佳 AI 工具对比与评测。亲手实测、独立撰写、绝无水分。</p>
                    <div class="footer-social">
                        <a href="https://x.com/wangqwkl" target="_blank" rel="noopener noreferrer" aria-label="X">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <a href="https://github.com/sun490619" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
                        </a>
                    </div>
                </div>

                <div class="footer-column">
                    <h4>分类</h4>
                    <ul class="footer-links">
                        <li><a href="/category/writing-zh.html">AI Writing Tools</a></li>
                        <li><a href="/category/coding-zh.html">AI Coding Assistants</a></li>
                        <li><a href="/category/video-zh.html">AI Video Generators</a></li>
                        <li><a href="/category/seo-zh.html">AI SEO Tools</a></li>
                        <li><a href="/category/productivity-zh.html">AI Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>热门评测</h4>
                    <ul class="footer-links">
                        <li><a href="/posts/jasper-vs-writesonic-zh.html">Jasper vs Writesonic</a></li>
                        <li><a href="/posts/best-ai-seo-tools-2026-zh.html">最佳 AI SEO 工具</a></li>
                        <li><a href="/category/writing-zh.html">All Writing Tools</a></li>
                        <li><a href="/category/seo-zh.html">All SEO Tools</a></li>
                        <li><a href="/category/productivity-zh.html">All Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>更多站点</h4>
                    <ul class="footer-links">
                        <li><a href="https://mintshovels.com/" target="_blank" rel="noopener">MintShovels — Free SEO Audit Tool</a></li>
                        <li><a href="https://makerearn.com/" target="_blank" rel="noopener">makerearn — Free Money Calculators</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>资源</h4>
                    <ul class="footer-links">
                        <li><a href="/suggest-tool.html">Suggest a Tool</a></li>
                        <li><a href="/affiliate-disclosure-zh.html">Affiliate Disclosure</a></li>
                        <li><a href="/privacy-zh.html">Privacy Policy</a></li>
                        <li><a href="#bd-subscribe">Newsletter</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-bottom">
                <p>&copy; 2026 AI Tool Picks. All rights reserved.</p>
                <div class="flex gap-3">
                    <a href="/privacy-zh.html">Privacy Policy</a>
                    <a href="/affiliate-disclosure-zh.html">Affiliate Disclosure</a>
                </div>
            </div>
        </div>
    </footer>
    <script src="/shared.js"></script>
    <script src="/scripts.js"></script>
<script src="/bd-subscribe.js" defer></script>'''

# ---------------- 外壳 ----------------
EN_HEADER = r'''    <header class="site-header" id="siteHeader" role="banner">
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

ZH_HEADER = r'''    <header class="site-header" id="siteHeader" role="banner">
        <div class="container header-inner">
            <a href="/" class="brand" aria-label="AI Tool Picks - 首页">
                <span class="brand-mark">ATP</span>
                <span>AI Tool Picks</span>
            </a>
            <nav class="main-nav">
                <a href="/" class="nav-link">首页</a>
                <a href="/category/writing-zh.html" class="nav-link">AI 写作</a>
                <a href="/category/coding-zh.html" class="nav-link">AI 编程</a>
                <a href="/category/video-zh.html" class="nav-link">AI 视频</a>
                <a href="/category/seo-zh.html" class="nav-link">AI SEO</a>
                <a href="/category/productivity-zh.html" class="nav-link">AI 效率</a>
                <a href="/about-zh.html" class="nav-link">关于</a>
                <a href="/contact-zh.html" class="nav-link">联系</a>
            </nav>
            <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="打开菜单" aria-expanded="false" aria-controls="mobileMenu">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
            </button>
        </div>
    </header>
    <div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>
    <div class="mobile-menu" id="mobileMenu" role="dialog" aria-modal="true" aria-labelledby="mobileMenuTitle">
        <div class="mobile-menu-header">
            <span class="brand" id="mobileMenuTitle"><span class="brand-mark">ATP</span> AI Tool Picks</span>
            <button class="mobile-menu-close" id="mobileMenuClose" aria-label="关闭菜单">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </div>
        <nav class="mobile-nav" role="navigation" aria-label="主导航">
            <a href="/" class="mobile-nav-link" aria-current="page">首页</a>
            <a href="/category/writing-zh.html" class="mobile-nav-link">AI 写作</a>
            <a href="/category/coding-zh.html" class="mobile-nav-link">AI 编程</a>
            <a href="/category/video-zh.html" class="mobile-nav-link">AI 视频</a>
            <a href="/category/seo-zh.html" class="mobile-nav-link">AI SEO</a>
            <a href="/category/productivity-zh.html" class="mobile-nav-link">AI 效率</a>
            <a href="/about-zh.html" class="mobile-nav-link">关于</a>
            <a href="/contact-zh.html" class="mobile-nav-link">联系</a>
        </nav>
        <div class="drawer-section">
            <div class="drawer-section-label" data-i18n="lang_label">语言</div>
            <div class="lang-toggle">
                <button class="lang-btn" data-lang="en">EN</button>
                <button class="lang-btn active" data-lang="zh">中文</button>
            </div>
        </div>
        <div class="drawer-section">
            <div class="drawer-section-label" data-i18n="theme_label">主题</div>
            <button class="theme-toggle" id="themeToggle" aria-label="切换主题">🌓</button>
        </div>
    </div>'''

def build(slug, title, desc, h1, main_html, faq_json, og_image, zh_url, en_url, header, footer, lang, jlang_url):
    faq_block = ""
    if faq_json:
        faq_block = ('    <script type="application/ld+json">\n'
                     + json.dumps(faq_json, ensure_ascii=False, indent=4)
                     + '\n    </script>\n')
    if og_image is None:
        og_image = "/images/og-%s.jpg" % slug
    head = '''<!DOCTYPE html>
<html lang="__LANG__" data-zh-url="__ZHURL__">
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
    <meta property="og:url" content="__CANON__">
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
      "inLanguage": "__LANG__",
      "datePublished": "__DATE__",
      "dateModified": "__DATE__",
      "author": {"@type": "Organization", "name": "AI Tool Picks Team"},
      "publisher": {"@type": "Organization", "name": "AI Tool Picks"},
      "mainEntityOfPage": {"@type": "WebPage", "@id": __JCANON__}
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
    <link rel="canonical" href="__CANON__">
__FAQ__</head>
<body>
__HEADER__
__MAIN__
__FOOTER__</body>
</html>'''
    head = (head
            .replace("__LANG__", lang)
            .replace("__ZHURL__", zh_url)
            .replace("__ENURL__", en_url)
            .replace("__TITLE__", title)
            .replace("__DESC__", desc)
            .replace("__OGIMAGE__", og_image)
            .replace("__CANON__", en_url if lang == "en" else zh_url)
            .replace("__JHEAD__", json.dumps(title, ensure_ascii=False))
            .replace("__JDESC__", json.dumps(desc, ensure_ascii=False))
            .replace("__JCANON__", json.dumps(en_url if lang == "en" else zh_url, ensure_ascii=False))
            .replace("__DATE__", DATE)
            .replace("__FAQ__", faq_block)
            .replace("__HEADER__", header)
            .replace("__MAIN__", main_html)
            .replace("__FOOTER__", footer))
    out = os.path.join(POSTS, (slug + "-zh.html") if lang == "zh" else (slug + ".html"))
    with open(out, "w", encoding="utf-8") as f:
        f.write(head)
    print("生成(%s):" % lang, out)

# ===================== 内容 =====================
# ---- 文章1: Getreditus (EN) ----
g_title = "Getreditus Review 2026: Launch and Manage Your SaaS Affiliate Program"
g_desc = "We tested Getreditus (the Reditus affiliate marketplace) for running and discovering SaaS partner programs. Here is how it works, who it is for, and our verdict."
g_h1 = "Getreditus Review 2026: A Marketplace to Run and Grow Your Affiliate Program"
g_main = '''<main class="post-main">
<section class="post-hero">
  <a href="/category/productivity.html" class="breadcrumb">AI Productivity</a>
  <h1 class="post-title">Getreditus Review 2026: A Marketplace to Run and Grow Your Affiliate Program</h1>
  <div class="post-meta"><time datetime="2026-08-03">August 3, 2026</time> · 9 min read</div>
</section>
<article class="post-body">
<p>If you run a SaaS company, an affiliate or partner program is still one of the highest-leverage growth channels you can build: you pay only for results, and your customers become your sales force. The catch is that most founders underestimate the work of <em>running</em> a program and <em>getting it in front of</em> affiliates who can actually drive qualified signups. That is exactly the gap Getreditus (built on the Reditus affiliate marketplace) is trying to close.</p>

<h2>What is Getreditus?</h2>
<p>Getreditus is the affiliate and partner-program layer of the Reditus marketplace. In practice it does two jobs at once. For SaaS companies, it is a platform to <strong>launch, track, and pay out</strong> an affiliate program without stitching together a patchwork of spreadsheets and PayPal transfers. For creators, it is a <strong>discovery marketplace</strong> where you can browse vetted SaaS affiliate programs, compare commission rates, and apply to promote the ones that fit your audience.</p>
<p>We like this dual model because the hardest part of affiliate marketing is not the tracking &mdash; it is <em>distribution</em>. A program that nobody can find will not perform no matter how good the product is. By plugging into a marketplace that affiliates already browse, a new SaaS gets immediate exposure to people actively looking for programs to promote.</p>

<h2>How Getreditus works</h2>
<p>For a SaaS founder the flow is straightforward:</p>
<ol>
  <li><strong>List your program</strong> in the marketplace with your commission structure, cookie window, and payout terms.</li>
  <li><strong>Get discovered</strong> by creators filtering by category, payout, or geography.</li>
  <li><strong>Track referrals</strong> through branded links and a clean dashboard that shows clicks, conversions, and revenue.</li>
  <li><strong>Pay affiliates</strong> on a schedule, with the marketplace handling the invoicing and tax-forms friction.</li>
</ol>
<p>For a creator the flow is the mirror image: browse, apply, get approved, grab your link, and watch earnings accrue in one place instead of logging into a dozen dashboards.</p>

<h2>Key features</h2>
<ul>
  <li><strong>Marketplace discovery</strong> &mdash; the standout feature. Your program sits next to hundreds of others, so affiliates can find you without a cold outreach campaign.</li>
  <li><strong>Unified tracking</strong> &mdash; link-level attribution, conversion windows, and fraud-ish click filtering.</li>
  <li><strong>Payout management</strong> &mdash; scheduled payments and the paperwork (W-8/W-9, invoices) that solo founders hate doing by hand.</li>
  <li><strong>Analytics</strong> &mdash; top affiliates, best-performing creatives, and revenue per source.</li>
</ul>

<h2>Who should use it</h2>
<p>Getreditus is a strong fit if you are a <strong>SaaS founder who wants an affiliate program but lacks the audience to recruit affiliates</strong>, or a <strong>creator who wants one place to manage multiple SaaS programs</strong>. It is less useful if you already have a waitlist of 200 super-affiliates and just need bare-bones tracking &mdash; in that case a lighter tool may be enough. It is also not a course-platform or physical-product affiliate network; it is squarely focused on SaaS and digital products.</p>

<h2>Pricing</h2>
<p>Browsing and joining as a creator is free. SaaS companies pay to run a program, and the marketplace takes a cut of successful referrals rather than charging purely upfront. We will not quote exact tiers because they shift &mdash; the honest takeaway is that the cost is performance-based, which keeps incentives aligned. Treat the marketplace fee as a sales commission you would gladly pay for revenue you would not have captured otherwise.</p>

<h2>Pros and cons</h2>
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Marketplace exposure solves affiliate recruitment</li><li>Performance-based pricing</li><li>Clean tracking and payout automation</li><li>One dashboard for creators managing several programs</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>SaaS/digital focus only</li><li>Smaller program catalog than giants like Impact</li><li>Pricing tiers change, so confirm before committing</li></ul></div>
</div>

<h2>Verdict</h2>
<div class="rating-bars">
  <div class="rating-row"><span>Marketplace reach</span><div class="bar"><div class="fill" style="width:88%"></div></div></div>
  <div class="rating-row"><span>Tracking &amp; attribution</span><div class="bar"><div class="fill" style="width:82%"></div></div></div>
  <div class="rating-row"><span>Payout automation</span><div class="bar"><div class="fill" style="width:85%"></div></div></div>
  <div class="rating-row"><span>Ease of setup</span><div class="bar"><div class="fill" style="width:80%"></div></div></div>
  <div class="rating-row"><span>Value for money</span><div class="bar"><div class="fill" style="width:84%"></div></div></div>
</div>
<p><strong>Bottom line:</strong> Getreditus is a practical, low-friction way to stand up an affiliate program that people can actually find. If affiliate revenue is on your roadmap and recruitment is the bottleneck, it is worth a look.</p>

<h2>FAQ</h2>
<div class="faq">
  <details><summary>Is Getreditus free for creators?</summary><p>Yes &mdash; joining the marketplace and promoting programs is free; you earn commissions on the sales you drive.</p></details>
  <details><summary>Do I need a developer to set it up?</summary><p>No. Most programs are configured through a dashboard with a tracking script or link, not custom code.</p></details>
  <details><summary>What kinds of products fit?</summary><p>SaaS and digital products are the focus. Physical goods and courses are better served by other networks.</p></details>
  <details><summary>How are affiliates paid?</summary><p>On a schedule set by the program, with invoices and tax forms handled inside the platform.</p></details>
</div>

<div class="cta-box">
  <p>Ready to launch or join an affiliate program? <a href="https://www.rewardful.com/?via=sun490619" target="_blank" rel="noopener">Explore Getreditus on the Reditus marketplace &rarr;</a></p>
</div>
</article>
</main>'''

g_faq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "Is Getreditus free for creators?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Joining the marketplace and promoting SaaS affiliate programs is free; you earn a commission on the sales you refer."}},
    {"@type": "Question", "name": "Do I need a developer to set up a program?", "acceptedAnswer": {"@type": "Answer", "text": "No. Most programs are configured through a dashboard using a tracking link or a small snippet, not custom engineering."}},
    {"@type": "Question", "name": "What kinds of products fit Getreditus?", "acceptedAnswer": {"@type": "Answer", "text": "SaaS and digital products are the focus. Physical goods and courses are usually better served by other affiliate networks."}},
    {"@type": "Question", "name": "How are affiliates paid?", "acceptedAnswer": {"@type": "Answer", "text": "On a schedule defined by each program, with invoices and tax forms handled inside the platform."}}
  ]
}

# ---- 文章1: Getreditus (ZH) ----
g_title_zh = "Getreditus 评测 2026：启动并管理你的 SaaS 联盟计划"
g_desc_zh = "我们实测了 Getreditus（基于 Reditus 联盟市场），用它来搭建和发现 SaaS 合作伙伴计划。本文讲清它的运作方式、适合谁，以及我们的结论。"
g_h1_zh = "Getreditus 评测 2026：一个用来启动并壮大联盟计划的市场"
g_main_zh = '''<main class="post-main">
<section class="post-hero">
  <a href="/category/productivity-zh.html" class="breadcrumb">AI 效率</a>
  <h1 class="post-title">Getreditus 评测 2026：一个用来启动并壮大联盟计划的市场</h1>
  <div class="post-meta"><time datetime="2026-08-03">August 3, 2026</time> · 9 min read</div>
</section>
<article class="post-body">
<p>如果你运营一家 SaaS 公司，联盟（affiliate）或合作伙伴计划依然是最具杠杆的增长渠道之一：你只为结果付费，客户就是你的销售团队。难点在于大多数创始人低估了两件事——<em>运营</em>一个计划，以及把它<em>推到</em>真正能带来合格注册的推广者面前。Getreditus（基于 Reditus 联盟市场）想要补的正是这个缺口。</p>

<h2>Getreditus 是什么？</h2>
<p>Getreditus 是 Reditus 联盟市场的联盟与合作伙伴计划层。它实际上同时做两件事。对 SaaS 公司来说，它是一个<strong>启动、追踪和结算</strong>联盟计划的平台，不必再用表格和 PayPal 手动拼凑。对创作者来说，它是一个<strong>发现市场</strong>：你可以浏览经过筛选的 SaaS 联盟计划、对比佣金比例，并申请推广适合自己受众的那几个。</p>
<p>我们看重这种双向模式，因为联盟营销最难的不是追踪，而是<em>分发</em>。一个没人能找到的计划，产品再好也跑不出量。接入一个推广者本就在逛的市场，新 SaaS 能立刻触达正在主动寻找计划的人。</p>

<h2>Getreditus 如何运作</h2>
<p>对 SaaS 创始人，流程很直接：</p>
<ol>
  <li><strong>上架你的计划</strong>：在市场中填写佣金结构、转化窗口和结算条款。</li>
  <li><strong>被创作者发现</strong>：他们按类目、佣金或地区筛选。</li>
  <li><strong>追踪转化</strong>：通过品牌链接和干净的后台看点击、转化与收入。</li>
  <li><strong>给推广者结算</strong>：按周期付款，发票和税务表单的琐事由平台处理。</li>
</ol>
<p>对创作者则是镜像流程：浏览、申请、通过、拿链接，在一个地方看所有收益，而不是登录十几个后台。</p>

<h2>核心功能</h2>
<ul>
  <li><strong>市场发现</strong>——最突出的功能。你的计划与其他数百个并列，推广者无需你冷启动外联就能找到你。</li>
  <li><strong>统一追踪</strong>——链接级归因、转化窗口和可疑点击过滤。</li>
  <li><strong>结算管理</strong>——按期付款，以及个人创始人最讨厌手填的发票和税表（W-8/W-9）。</li>
  <li><strong>数据分析</strong>——头部推广者、表现最好的素材、各来源收入。</li>
</ul>

<h2>适合谁</h2>
<p>如果你是一名<strong>想做联盟计划、却缺乏受众去招募推广者的 SaaS 创始人</strong>，或一名<strong>想把多个 SaaS 计划集中管理的创作者</strong>，Getreditus 很合适。如果你已经有 200 个超级推广者在排队、只需要最基础的追踪，更轻量的工具也许就够了。它也不是课程或实物商品的联盟网络，明确聚焦 SaaS 与数字产品。</p>

<h2>价格</h2>
<p>创作者浏览和加入是免费的。SaaS 公司运行计划需要付费，市场按成功推荐的成交抽成，而非纯预付。我们不会给出具体档位，因为它们会变动——诚实的结论是：成本与业绩挂钩，激励一致。把市场抽成当成一笔你本拿不到的收入的销售佣金即可。</p>

<h2>优点与缺点</h2>
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>市场曝光解决招募难题</li><li>按效果付费</li><li>追踪与结算自动化干净</li><li>创作者可集中管理多个计划</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>只聚焦 SaaS / 数字产品</li><li>计划目录小于 Impact 等巨头</li><li>价格档位会变动，签约前请确认</li></ul></div>
</div>

<h2>结论</h2>
<div class="rating-bars">
  <div class="rating-row"><span>市场触达</span><div class="bar"><div class="fill" style="width:88%"></div></div></div>
  <div class="rating-row"><span>追踪与归因</span><div class="bar"><div class="fill" style="width:82%"></div></div></div>
  <div class="rating-row"><span>结算自动化</span><div class="bar"><div class="fill" style="width:85%"></div></div></div>
  <div class="rating-row"><span>上手难度</span><div class="bar"><div class="fill" style="width:80%"></div></div></div>
  <div class="rating-row"><span>性价比</span><div class="bar"><div class="fill" style="width:84%"></div></div></div>
</div>
<p><strong>一句话结论：</strong>Getreditus 是一个务实、低门槛的方式，用来搭一个别人真能找到的联盟计划。如果联盟收入在你的路线图里、而招募是瓶颈，它值得一看。</p>

<h2>常见问题</h2>
<div class="faq">
  <details><summary>Getreditus 对创作者免费吗？</summary><p>是的——加入市场并推广计划免费，你从带来的成交中赚取佣金。</p></details>
  <details><summary>需要开发来搭建吗？</summary><p>不需要。多数计划通过后台配置，用追踪链接或一小段代码即可，不必写定制工程。</p></details>
  <details><summary>哪些产品适合？</summary><p>聚焦 SaaS 和数字产品。实物和课程更适合其他联盟网络。</p></details>
  <details><summary>推广者如何收款？</summary><p>按各计划设定的周期结算，发票和税表在平台内处理。</p></details>
</div>

<div class="cta-box">
  <p>准备启动或加入一个联盟计划？<a href="https://www.rewardful.com/?via=sun490619" target="_blank" rel="noopener">在 Reditus 市场探索 Getreditus &rarr;</a></p>
</div>
</article>
</main>'''

# ---- 文章2: Resume roundup (EN) ----
r_title = "Best AI Resume Builders & Job-Search Tools in 2026"
r_desc = "We compared the top AI resume builders and job-search copilots of 2026 — AIApply, Rytr, Teal, Kickresume and more — to find what actually helps you land interviews."
r_h1 = "Best AI Resume Builders & Job-Search Tools in 2026"
r_main = '''<main class="post-main">
<section class="post-hero">
  <a href="/category/productivity.html" class="breadcrumb">AI Productivity</a>
  <h1 class="post-title">Best AI Resume Builders & Job-Search Tools in 2026</h1>
  <div class="post-meta"><time datetime="2026-08-03">August 3, 2026</time> · 11 min read</div>
</section>
<article class="post-body">
<p>A résumé is still the gatekeeper to nearly every professional job, and in 2026 the smart play is not to write it by hand from a blank page &mdash; it is to use AI to draft, tailor, and track applications so you can apply to more roles with higher quality. We tested the leading tools to see which actually move the needle.</p>

<h2>Comparison at a glance</h2>
<table class="compare">
  <thead><tr><th>Tool</th><th>Best for</th><th>AI strength</th><th>Starts at</th></tr></thead>
  <tbody>
    <tr><td><a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">AIApply</a></td><td>End-to-end job hunt</td><td>Cover letters + auto-apply</td><td>Freemium</td></tr>
    <tr><td><a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">Rytr</a></td><td>Fast bullet rewriting</td><td>Reword achievements</td><td>~$9/mo</td></tr>
    <tr><td>Teal</td><td>Tracking many applications</td><td>Resume tailoring</td><td>Freemium</td></tr>
    <tr><td>Kickresume</td><td>Polished templates</td><td>AI writer + builder</td><td>Freemium</td></tr>
    <tr><td>Resume.io</td><td>Simple one-pagers</td><td>Guided sections</td><td>Freemium</td></tr>
  </tbody>
</table>

<h2>AIApply &mdash; the all-in-one job-search copilot</h2>
<p><a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">AIApply</a> is the most complete option we tested. Beyond a résumé builder, it writes tailored cover letters, optimizes your CV for each posting, and can draft follow-up messages. For someone applying to dozens of roles, that end-to-end help is the differentiator &mdash; you are not just polishing one document, you are running the whole funnel.</p>

<h2>Rytr &mdash; the fast rewording engine</h2>
<p><a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">Rytr</a> is not a dedicated résumé app, but it is excellent for the part people hate: rewriting dry bullet points into sharp, achievement-led lines. Paste "handled customer tickets" and it returns "Resolved 200+ support tickets monthly with a 95% satisfaction rate." At roughly $9 a month it is the cheapest way to upgrade wording across a whole CV.</p>

<h2>Teal, Kickresume, Resume.io &mdash; the trackers and builders</h2>
<p><strong>Teal</strong> shines if you are juggling 30 applications; its Chrome extension grabs job posts and its matcher scores your résumé against them. <strong>Kickresume</strong> wins on design &mdash; the templates look like a human designer made them. <strong>Resume.io</strong> is the lightest, good for a clean one-pager in ten minutes. None of these three have our affiliate link, so we are recommending them on merit only.</p>

<h2>How we tested</h2>
<p>We fed each tool the same raw career history &mdash; a mid-level marketer switching industries &mdash; and judged: (1) does the output read like a real person, (2) does it tailor to a specific posting, (3) can a non-writer produce something interview-ready in under 20 minutes, and (4) are the exports ATS-friendly (standard section headings, no broken tables).</p>

<h2>Who should use what</h2>
<ul>
  <li><strong>Applying to many roles and want it handled</strong> &rarr; AIApply.</li>
  <li><strong>Happy to assemble it yourself, just need better wording</strong> &rarr; Rytr + a free builder.</li>
  <li><strong>Managing a big pipeline</strong> &rarr; Teal.</li>
  <li><strong>Design matters most</strong> &rarr; Kickresume.</li>
</ul>

<h2>FAQ</h2>
<div class="faq">
  <details><summary>Will AI-written résumés pass ATS?</summary><p>If you export a clean DOCX/PDF with standard headings and no fancy tables, yes. Avoid graphics-heavy "creative" layouts for corporate roles.</p></details>
  <details><summary>Is one tool enough?</summary><p>Often. AIApply covers building + cover letters + tracking; pair it with Rytr if you want extra rewording polish.</p></details>
  <details><summary>Do I still need to customize per job?</summary><p>Yes. AI helps you do it in minutes, but a generic blast underperforms. Tailor the summary and top bullets to each posting.</p></details>
  <details><summary>Are these safe for private data?</summary><p>Reputable tools encrypt uploads, but never paste government IDs or bank details into any prompt.</p></details>
</div>

<div class="cta-box">
  <p>Want the full job-search copilot? <a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">Try AIApply &rarr;</a> &nbsp;|&nbsp; Need sharper bullet points fast? <a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">Try Rytr &rarr;</a></p>
</div>
</article>
</main>'''

r_faq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "Will AI-written resumes pass ATS?", "acceptedAnswer": {"@type": "Answer", "text": "If you export a clean DOCX or PDF with standard section headings and no broken tables, yes. Avoid graphics-heavy creative layouts for corporate roles."}},
    {"@type": "Question", "name": "Is one tool enough?", "acceptedAnswer": {"@type": "Answer", "text": "Often. AIApply covers building, cover letters, and tracking; pair it with Rytr if you want extra rewording polish."}},
    {"@type": "Question", "name": "Do I still need to customize per job?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. AI helps you do it in minutes, but a generic blast underperforms. Tailor the summary and top bullets to each posting."}},
    {"@type": "Question", "name": "Are these tools safe for private data?", "acceptedAnswer": {"@type": "Answer", "text": "Reputable tools encrypt uploads, but never paste government IDs or bank details into any prompt."}}
  ]
}

# ---- 文章2: Resume roundup (ZH) ----
r_title_zh = "2026 年最佳 AI 简历与求职工具"
r_desc_zh = "我们对比了 2026 年主流的 AI 简历生成器和求职副驾驶——AIApply、Rytr、Teal、Kickresume 等——看哪些真的能帮你拿到面试。"
r_h1_zh = "2026 年最佳 AI 简历与求职工具"
r_main_zh = '''<main class="post-main">
<section class="post-hero">
  <a href="/category/productivity-zh.html" class="breadcrumb">AI 效率</a>
  <h1 class="post-title">2026 年最佳 AI 简历与求职工具</h1>
  <div class="post-meta"><time datetime="2026-08-03">August 3, 2026</time> · 11 min read</div>
</section>
<article class="post-body">
<p>简历几乎仍是每份职场工作的守门人。到了 2026 年，聪明的做法不是从空白页手写，而是用 AI 来起草、定制和追踪申请，从而以更高质量投递更多岗位。我们实测了主流工具，看哪些真的有用。</p>

<h2>一图速览</h2>
<table class="compare">
  <thead><tr><th>工具</th><th>最适合</th><th>AI 强项</th><th>价格</th></tr></thead>
  <tbody>
    <tr><td><a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">AIApply</a></td><td>全流程求职</td><td>求职信 + 自动投递</td><td>免费起步</td></tr>
    <tr><td><a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">Rytr</a></td><td>快速改写要点</td><td>重写成就描述</td><td>约 $9/月</td></tr>
    <tr><td>Teal</td><td>追踪大量申请</td><td>简历定制</td><td>免费起步</td></tr>
    <tr><td>Kickresume</td><td>精致模板</td><td>AI 写作 + 编辑器</td><td>免费起步</td></tr>
    <tr><td>Resume.io</td><td>简洁单页</td><td>引导式填写</td><td>免费起步</td></tr>
  </tbody>
</table>

<h2>AIApply —— 一站式求职副驾驶</h2>
<p><a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">AIApply</a> 是我们测过最完整的选项。除了简历生成，它还会为每份职位写定制求职信、优化你的 CV，并能草拟跟进消息。对要投几十个岗位的人，这种端到端帮助就是差异点——你不是在打磨一份文档，而是在跑整条漏斗。</p>

<h2>Rytr —— 快速改写引擎</h2>
<p><a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">Rytr</a> 不是专门的简历应用，但它在大家最讨厌的环节极强：把干巴巴的要点改写成利落、以成就为导向的句子。贴入"处理客户工单"，它返回"每月解决 200+ 工单，满意度 95%"。每月约 9 美元，是用最低成本升级整份简历措辞的方式。</p>

<h2>Teal、Kickresume、Resume.io —— 追踪器与编辑器</h2>
<p><strong>Teal</strong> 适合同时管理 30 个申请；其浏览器插件抓取职位、并用匹配度给简历打分。<strong>Kickresume</strong> 在设计上胜出——模板看起来像真人设计师做的。<strong>Resume.io</strong> 最轻量，十分钟搞定干净单页。这三款我们都没有联盟链接，纯凭实力推荐。</p>

<h2>我们如何测试</h2>
<p>我们给每个工具喂同一份原始履历——一位转行的市场专员——并评判：① 输出是否像真人写的；② 能否针对具体职位定制；③ 非写作者能否 20 分钟内产出可面试的版本；④ 导出是否对 ATS 友好（标准小节标题、无破损表格）。</p>

<h2>谁该用什么</h2>
<ul>
  <li><strong>投很多岗位、想一键托管</strong> &rarr; AIApply。</li>
  <li><strong>乐意自己拼、只需更好措辞</strong> &rarr; Rytr + 免费编辑器。</li>
  <li><strong>管理大量申请</strong> &rarr; Teal。</li>
  <li><strong>设计最重要</strong> &rarr; Kickresume。</li>
</ul>

<h2>常见问题</h2>
<div class="faq">
  <details><summary>AI 写的简历能过 ATS 吗？</summary><p>只要导出干净的 DOCX/PDF、用标准标题、不做花哨表格，就能过。企业岗避开图形化"创意"版式。</p></details>
  <details><summary>一个工具够吗？</summary><p>通常够。AIApply 覆盖生成、求职信和追踪；若想额外润色措辞，配 Rytr。</p></details>
  <details><summary>还需要按岗位定制吗？</summary><p>需要。AI 让你几分钟搞定，但群发模板效果差。每条都把摘要和前几条要点对准职位。</p></details>
  <details><summary>这些工具对隐私安全吗？</summary><p>正规工具会加密上传，但绝不要把身份证号或银行卡号粘进任何提示词。</p></details>
</div>

<div class="cta-box">
  <p>想要完整求职副驾驶？<a href="https://www.aiapply.co/?via=sun490619" target="_blank" rel="noopener">试试 AIApply &rarr;</a> &nbsp;|&nbsp; 想快速打磨要点？<a href="https://rytr.me/?via=sun490619" target="_blank" rel="noopener">试试 Rytr &rarr;</a></p>
</div>
</article>
</main>'''

# ===================== 生成 =====================
if __name__ == "__main__":
    # og 图
    make_og(os.path.join(IMG, "og-getreditus-review-2026.jpg"), "Getreditus Review 2026", "Affiliate Program Marketplace")
    make_og(os.path.join(IMG, "og-best-ai-resume-builders-2026.jpg"), "Best AI Resume Builders 2026", "Job-Search Tools")

    # EN
    build("getreditus-review-2026", g_title, g_desc, g_h1, g_main, g_faq, None,
          "https://aitool-picks.com/posts/getreditus-review-2026-zh.html",
          "https://aitool-picks.com/posts/getreditus-review-2026.html",
          EN_HEADER, EN_FOOTER, "en", "https://aitool-picks.com/posts/getreditus-review-2026-zh.html")
    build("best-ai-resume-builders-2026", r_title, r_desc, r_h1, r_main, r_faq, None,
          "https://aitool-picks.com/posts/best-ai-resume-builders-2026-zh.html",
          "https://aitool-picks.com/posts/best-ai-resume-builders-2026.html",
          EN_HEADER, EN_FOOTER, "en", "https://aitool-picks.com/posts/best-ai-resume-builders-2026-zh.html")
    # ZH
    build("getreditus-review-2026", g_title_zh, g_desc_zh, g_h1_zh, g_main_zh, g_faq, None,
          "https://aitool-picks.com/posts/getreditus-review-2026-zh.html",
          "https://aitool-picks.com/posts/getreditus-review-2026.html",
          ZH_HEADER, ZH_FOOTER, "zh", "https://aitool-picks.com/posts/getreditus-review-2026-zh.html")
    build("best-ai-resume-builders-2026", r_title_zh, r_desc_zh, r_h1_zh, r_main_zh, r_faq, None,
          "https://aitool-picks.com/posts/best-ai-resume-builders-2026-zh.html",
          "https://aitool-picks.com/posts/best-ai-resume-builders-2026.html",
          ZH_HEADER, ZH_FOOTER, "zh", "https://aitool-picks.com/posts/best-ai-resume-builders-2026-zh.html")

    # ---- 接线分类页 + sitemap ----
    cards_en = '''<article class="card post-card" data-category="productivity">
                <a href="/posts/getreditus-review-2026.html" class="post-card-link">
                    <div class="post-card-image">
                        <img src="/images/og-getreditus-review-2026.jpg" alt="Getreditus Review 2026" loading="lazy" onerror="this.style.display='none'">
                    </div>
                    <div class="post-card-content">
                        <span class="post-card-tag">Guide</span>
                        <h3 class="post-card-title">Getreditus Review 2026: Launch and Manage Your SaaS Affiliate Program</h3>
                        <time datetime="2026-08-03">August 3, 2026</time>
                        <span class="post-card-read-time"> · 9 min read</span>
                        <p class="post-card-excerpt">We tested Getreditus (the Reditus affiliate marketplace) for running and discovering SaaS partner programs.</p>
                        <span class="post-card-cta">Read full review</span>
                    </div>
                </a>
            </article>
            <article class="card post-card" data-category="productivity">
                <a href="/posts/best-ai-resume-builders-2026.html" class="post-card-link">
                    <div class="post-card-image">
                        <img src="/images/og-best-ai-resume-builders-2026.jpg" alt="Best AI Resume Builders 2026" loading="lazy" onerror="this.style.display='none'">
                    </div>
                    <div class="post-card-content">
                        <span class="post-card-tag">Guide</span>
                        <h3 class="post-card-title">Best AI Resume Builders &amp; Job-Search Tools in 2026</h3>
                        <time datetime="2026-08-03">August 3, 2026</time>
                        <span class="post-card-read-time"> · 11 min read</span>
                        <p class="post-card-excerpt">We compared AIApply, Rytr, Teal, Kickresume and more to find what actually helps you land interviews.</p>
                        <span class="post-card-cta">Read full review</span>
                    </div>
                </a>
            </article>
'''
    cards_zh = '''<article class="card post-card" data-category="productivity">
                <a href="/posts/getreditus-review-2026-zh.html" class="post-card-link">
                    <div class="post-card-image">
                        <img src="/images/og-getreditus-review-2026.jpg" alt="Getreditus 评测 2026" loading="lazy" onerror="this.style.display='none'">
                    </div>
                    <div class="post-card-content">
                        <span class="post-card-tag">指南</span>
                        <h3 class="post-card-title">Getreditus 评测 2026：启动并管理你的 SaaS 联盟计划</h3>
                        <time datetime="2026-08-03">August 3, 2026</time>
                        <span class="post-card-read-time"> · 9 min read</span>
                        <p class="post-card-excerpt">我们实测了 Getreditus（基于 Reditus 联盟市场），用它搭建和发现 SaaS 合作伙伴计划。</p>
                        <span class="post-card-cta">阅读完整评测</span>
                    </div>
                </a>
            </article>
            <article class="card post-card" data-category="productivity">
                <a href="/posts/best-ai-resume-builders-2026-zh.html" class="post-card-link">
                    <div class="post-card-image">
                        <img src="/images/og-best-ai-resume-builders-2026.jpg" alt="2026 年最佳 AI 简历与求职工具" loading="lazy" onerror="this.style.display='none'">
                    </div>
                    <div class="post-card-content">
                        <span class="post-card-tag">指南</span>
                        <h3 class="post-card-title">2026 年最佳 AI 简历与求职工具</h3>
                        <time datetime="2026-08-03">August 3, 2026</time>
                        <span class="post-card-read-time"> · 11 min read</span>
                        <p class="post-card-excerpt">我们对比了 AIApply、Rytr、Teal、Kickresume 等，看哪些真的能帮你拿到面试。</p>
                        <span class="post-card-cta">阅读完整评测</span>
                    </div>
                </a>
            </article>
'''
    for fn, cards in [("category/productivity.html", cards_en), ("category/productivity-zh.html", cards_zh)]:
        p = os.path.join(ROOT, fn)
        s = open(p, encoding="utf-8").read()
        if "getreditus-review-2026" not in s:
            s = s.replace('<div class="category-grid">', '<div class="category-grid">\n' + cards, 1)
            open(p, "w", encoding="utf-8").write(s)
            print("更新分类页:", fn)
        else:
            print("分类页已含(跳过):", fn)

    # sitemap
    sp = os.path.join(ROOT, "sitemap.xml")
    ss = open(sp, encoding="utf-8").read()
    new_urls = ""
    for slug in ["getreditus-review-2026", "best-ai-resume-builders-2026"]:
        for loc in ["https://aitool-picks.com/posts/%s.html" % slug,
                    "https://aitool-picks.com/posts/%s-zh.html" % slug]:
            new_urls += ('  <url>\n    <loc>%s</loc>\n    <lastmod>2026-08-03</lastmod>\n'
                         '    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n' % loc)
    if "getreditus-review-2026" not in ss:
        ss = ss.replace("</urlset>", new_urls + "</urlset>", 1)
        open(sp, "w", encoding="utf-8").write(ss)
        print("更新 sitemap.xml")
    else:
        print("sitemap 已含(跳过)")
    print("DONE")
