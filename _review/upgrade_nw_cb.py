#!/usr/bin/env python3
"""Rebuild NW + CB review articles (EN/ZH) to the §13.12 gold standard template."""
import os, re

ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
POSTS = os.path.join(ROOT, "posts")

FILES = [
    "neuronwriter-review-2026.html",
    "neuronwriter-review-2026-zh.html",
    "coursebox-review-2026.html",
    "coursebox-review-2026-zh.html",
]

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
    </footer>'''

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
    </footer>'''

CAT_EN = {"seo.html": "AI SEO Tools", "productivity.html": "AI Productivity & General"}
CAT_ZH = {"seo-zh.html": "AI SEO 工具", "productivity-zh.html": "AI 生产力工具"}


def og_for(url):
    slug = url.split("/posts/")[1].replace(".html", "")
    return f"/images/og-{slug}.jpg"


def process(path):
    html = open(path, encoding="utf-8").read()
    is_zh = '<html lang="zh"' in html
    footer = ZH_FOOTER if is_zh else EN_FOOTER

    # 1) Article JSON-LD author -> Person Sam Porter
    html = re.sub(
        r'"author":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"AI Tool Picks Team"\s*\}',
        '"author": {"@type": "Person", "name": "Sam Porter"}', html, flags=re.S)

    # 2) Core fields
    title = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1).strip()
    meta = re.search(r'<div class="post-meta"><time datetime="([^"]+)">([^<]+)</time>\s*·\s*([^<]+)</div>', html, re.S)
    date, date_disp, read_time = meta.group(1), meta.group(2).strip(), meta.group(3).strip()
    author = re.search(r'<div class="post-author">(.*?)</div>', html, re.S).group(1).strip()
    lead = re.search(r'<p class="post-lead">(.*?)</p>', html, re.S).group(1).strip()
    bc = re.search(r'<a href="(/category/[^"]+)" class="breadcrumb">([^<]+)</a>', html)
    cat_href, cat_name = bc.group(1), bc.group(2).strip()
    # normalize category label to footer wording
    cat_key = cat_href.split("/category/")[1]
    cat_name = (CAT_ZH if is_zh else CAT_EN).get(cat_key, cat_name)
    hero = re.search(r'<img class="hero-img" src="([^"]+)" alt="([^"]+)"', html)
    hero_src, hero_alt = hero.group(1), hero.group(2)

    # 3) Body prose (first <h2> up to CTA paragraph)
    body = re.search(r'(<h2>.*?)<p style="margin-top:24px;">', html, re.S).group(1)
    cta = re.search(r'<p style="margin-top:24px;"><a class="btn btn-primary" href="([^"]+)"[^>]*>(.*?)</a></p>', html, re.S)
    cta_href, cta_text = cta.group(1).strip(), cta.group(2).strip()

    # 4) pros/cons
    pc = re.search(r'<section class="pros-cons">(.*?)</section>', html, re.S).group(1)
    pros = re.search(r'<div class="pros"><h3>.*?</h3><ul>(.*?)</ul>', pc, re.S).group(1).strip()
    cons = re.search(r'<div class="cons"><h3>.*?</h3><ul>(.*?)</ul>', pc, re.S).group(1).strip()

    # 5) verdict
    verdict = re.search(r'<section class="verdict">\s*<h2>Verdict</h2>\s*<p>(.*?)</p>\s*</section>', html, re.S).group(1).strip()

    # 6) faq
    faq = re.search(r'<section class="faq">(.*?)</section>', html, re.S).group(1)
    faq_items = re.findall(r'<div class="faq-item"><h3>(.*?)</h3><p>(.*?)</p></div>', faq, re.S)

    # 7) how we tested
    hwt = re.search(r'<section class="how-we-test">(.*?)</section>', html, re.S).group(1)
    hwt_text = re.search(r'<p>(.*?)</p>', hwt, re.S).group(1).strip()

    # 8) related
    rel = re.search(r'<section class="related">(.*?)</section>', html, re.S).group(1)
    rel_items = re.findall(r'<li><a href="([^"]+)">(.*?)</a></li>', rel, re.S)

    # 9) add ids to headings + build TOC
    toc = []
    cnt = [0]
    def h2repl(m):
        cnt[0] += 1; t = m.group(1).strip(); toc.append((f"h{cnt[0]}", t, 0))
        return f'<h2 id="h{cnt[0]}">{t}</h2>'
    def h3repl(m):
        cnt[0] += 1; t = m.group(1).strip(); toc.append((f"h{cnt[0]}", t, 1))
        return f'<h3 id="h{cnt[0]}">{t}</h3>'
    body = re.sub(r'<h2>(.*?)</h2>', h2repl, body, flags=re.S)
    body = re.sub(r'<h3>(.*?)</h3>', h3repl, body, flags=re.S)

    # 10) disclosure text
    if is_zh:
        disc_banner = '<strong>联盟声明：</strong>下方部分链接为联盟链接。若你通过它们注册，我们可能获得佣金，但不会增加你的费用。我们只推荐自己实测过的工具。'
        disc_bottom = '<strong>联盟声明：</strong>本页部分链接为联盟链接：若你注册，我们可能获得少量佣金，不会增加你的费用。我们只推荐亲自实测过的工具。'
        v_like, v_not = "我们喜欢的", "我们不喜欢的"
        faq_h = "常见问题"; verdict_h = "结论"; hwt_h = "我们如何实测"; rel_h = "相关文章"
        rel_sub = "更多我们亲手实测的对比评测。"
        toc_t = "本文内容"
    else:
        disc_banner = '<strong>Affiliate disclosure:</strong> Some links below are affiliate links. If you sign up through them we may earn a commission at no extra cost to you. We only recommend tools we’ve tested ourselves.'
        disc_bottom = '<strong>Affiliate disclosure:</strong> Some links on this page are affiliate links: if you sign up we may earn a small commission, at no extra cost to you. We only recommend tools we’ve personally tested.'
        v_like, v_not = "What we liked", "What we didn't"
        faq_h = "Frequently asked questions"; verdict_h = "Verdict"; hwt_h = "How we tested"; rel_h = "Related articles"
        rel_sub = "More hands-on comparisons you might find useful."
        toc_t = "In this review"

    toc_html = f'<div class="toc" aria-label="Table of contents">\n          <div class="toc-title">{toc_t}</div>\n          <ul>'
    for i, t, lvl in toc:
        cls = ' class="toc-sub"' if lvl else ''
        toc_html += f'\n            <li{cls}><a href="#{i}">{t}</a></li>'
    toc_html += "\n          </ul>\n        </div>"

    breadcrumb = (f'  <nav class="article-breadcrumb" aria-label="Breadcrumb">\n'
                  f'    <a href="/">Home</a> / <a href="{cat_href}">{cat_name}</a> / <span>{title}</span>\n'
                  f'  </nav>')

    faq_html = "\n".join(f'          <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq_items)
    rel_cards = "\n            ".join(
        f'<a class="related-card" href="{u}"><span class="r-thumb" style="background-image:url(\'{og_for(u)}\')"></span><span class="r-title">{t}</span><span class="r-cat">{cat_name}</span></a>'
        for u, t in rel_items)

    article = f'''  <article class="post article-content">
    <div class="container">
      <div class="article-content">
        <header class="post-header">
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">By <a href="/about.html">Sam Porter</a> · <time datetime="{date}">{date_disp}</time> · {read_time}</div>
          <p class="post-lead">{lead}</p>
        </header>
        <img src="{hero_src}" alt="{hero_alt}" class="post-hero" loading="lazy">
        <div class="disclosure-banner">
          {disc_banner}
        </div>
        {toc_html}
{body}
        <p><a class="btn btn-primary" href="{cta_href}" target="_blank" rel="nofollow noopener">{cta_text}</a></p>
        <div class="disclosure">
          {disc_bottom}
        </div>
        <div class="verdict">
          <h3 class="verdict-title">{v_like}</h3>
          <ul>{pros}</ul>
        </div>
        <div class="verdict bad">
          <h3 class="verdict-title">{v_not}</h3>
          <ul>{cons}</ul>
        </div>
        <h2 id="verdict">{verdict_h}</h2>
        <p>{verdict}</p>
        <section class="faq-section" id="faq">
          <h2>{faq_h}</h2>
{faq_html}
        </section>
        <section class="how-we-test">
          <h2 id="how-we-tested">{hwt_h}</h2>
          <p>{hwt_text}</p>
        </section>
        <section class="related-articles" aria-label="Related articles">
          <h2 id="related-articles">{rel_h}</h2>
          <p class="sub">{rel_sub}</p>
          <div class="grid">
            {rel_cards}
          </div>
        </section>
      </div>
    </div>
  </article>'''

    new_chunk = breadcrumb + "\n" + article
    # The pros/cons/verdict/faq/how-we-test/related sections live OUTSIDE </article>;
    # replace the whole chunk from <article> through the last </section> before footer.
    html = re.sub(r'<article class="post">.*</section>', new_chunk, html, flags=re.S, count=1)
    html = re.sub(r'<footer class="site-footer">.*?</footer>', footer, html, flags=re.S, count=1)

    # wrap breadcrumb+article in <main> if not already
    if "<main role=\"main\">" not in html:
        html = html.replace(breadcrumb + "\n" + article,
                             '  <main role="main">\n' + breadcrumb + "\n" + article + "\n  </main>", 1)

    open(path, "w", encoding="utf-8").write(html)
    print("rebuilt", os.path.basename(path), "(zh)" if is_zh else "(en)")


for f in FILES:
    process(os.path.join(POSTS, f))
print("DONE")
