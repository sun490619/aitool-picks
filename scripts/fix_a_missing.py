#!/usr/bin/env python3
"""A档结构层缺件补件(按规则§8.2.1,排除工具页豁免)。
处理:
  what-40 EN/ZH  : +related-articles +TOC
  dubbing EN/ZH   : +related-articles
  newsletter EN/ZH: +related-articles
  edesk-zh        : +how-we-test +TOC
related链接均指向真实存在的同分类文章(已ls确认)。
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def insert_after_nav_breadcrumb(text: str, block: str) -> str:
    m = re.search(r'(<nav[^>]*class="[^"]*article-breadcrumb[^"]*"[^>]*>.*?</nav>)', text, re.S | re.I)
    if not m:
        return text
    return text[:m.end()] + "\n\n" + block + text[m.end():]


def insert_before_article_close(text: str, block: str) -> str:
    m = re.search(r'</article>', text, re.I)
    if not m:
        return text
    return text[:m.start()] + "\n" + block + "\n" + text[m.start():]


TOC_WHAT40_EN = '''        <div class="toc" aria-label="Table of contents">
            <p class="toc-title">What we cover</p>
            <ul>
                <li><a href="#expand-w40-measured">What the 40-tool pass actually measured</a></li>
                <li><a href="#expand-w40-patterns">Patterns that held across tools</a></li>
                <li><a href="#faq">FAQ</a></li>
            </ul>
        </div>'''

TOC_WHAT40_ZH = '''        <div class="toc" aria-label="目录">
            <p class="toc-title">本期内容</p>
            <ul>
                <li><a href="#expand-w40-measured">40个工具实测到底测了什么</a></li>
                <li><a href="#expand-w40-patterns">跨工具反复出现的规律</a></li>
                <li><a href="#faq">常见问题</a></li>
            </ul>
        </div>'''

TOC_EDESK_ZH = '''        <div class="toc" aria-label="目录">
            <p class="toc-title">本期内容</p>
            <ul>
                <li><a href="#pricing">价格</a></li>
                <li><a href="#rating">评分</a></li>
                <li><a href="#verdict">结论</a></li>
                <li><a href="#expand-edesk-zh-market">适用市场</a></li>
                <li><a href="#expand-edesk-zh-limit">限制</a></li>
            </ul>
        </div>'''

HOW_WE_TEST = '''    <section class="how-we-test" aria-label="How we test">
                    <h2 id="how-we-test">How we test</h2>
                    <p>Every tool on this page was used hands-on for real tasks &mdash; not skimmed from a press release. We sign up, run the actual workflow (write, generate, audit, or edit), and note where it helps and where it doesn't. Prices are checked against each vendor's site and marked "approximate" when they change often. We only recommend tools we'd genuinely use ourselves, and some links are affiliate links that cost you nothing extra.</p>
                </section>'''

REL_WHAT40_EN = '''    <section class="related-articles" aria-label="Related articles">
      <h2 id="related-articles">Related articles</h2>
      <p class="sub">More hands-on AI writing tool coverage.</p>
      <div class="grid">
        <a href="../posts/best-ai-copywriting-tools-2026.html"><span class="r-title">Best AI Copywriting Tools in 2026</span><span class="r-cat">Writing</span></a><a href="../posts/best-ai-email-writing-tools-2026.html"><span class="r-title">Best AI Email Writing Tools in 2026</span><span class="r-cat">Writing</span></a><a href="../posts/best-ai-writing-tools-non-native-english-2026.html"><span class="r-title">Best AI Writing Tools for Non-Native English Speakers</span><span class="r-cat">Writing</span></a>
      </div>
    </section>'''

REL_WHAT40_ZH = '''    <section class="related-articles" aria-label="相关文章">
      <h2 id="related-articles">相关文章</h2>
      <p class="sub">更多 AI 写作工具实测。</p>
      <div class="grid">
        <a href="../posts/best-ai-copywriting-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 文案写作工具</span><span class="r-cat">写作</span></a><a href="../posts/best-ai-email-writing-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 邮件写作工具</span><span class="r-cat">写作</span></a><a href="../posts/best-ai-writing-tools-non-native-english-2026-zh.html"><span class="r-title">非英语母语者最佳 AI 写作工具</span><span class="r-cat">写作</span></a>
      </div>
    </section>'''

REL_DUBBING_EN = '''    <section class="related-articles" aria-label="Related articles">
      <h2 id="related-articles">Related articles</h2>
      <p class="sub">More AI video localization coverage.</p>
      <div class="grid">
        <a href="../posts/best-ai-video-tools-2026.html"><span class="r-title">Best AI Video Tools in 2026</span><span class="r-cat">Video</span></a><a href="../posts/best-ai-avatar-video-tools-2026.html"><span class="r-title">Best AI Avatar Video Tools in 2026</span><span class="r-cat">Video</span></a><a href="../posts/ai-video-editing-tools-2026.html"><span class="r-title">AI Video Editing Tools Compared</span><span class="r-cat">Video</span></a>
      </div>
    </section>'''

REL_DUBBING_ZH = '''    <section class="related-articles" aria-label="相关文章">
      <h2 id="related-articles">相关文章</h2>
      <p class="sub">更多 AI 视频本地化内容。</p>
      <div class="grid">
        <a href="../posts/best-ai-video-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 视频工具</span><span class="r-cat">视频</span></a><a href="../posts/best-ai-avatar-video-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 数字人视频工具</span><span class="r-cat">视频</span></a><a href="../posts/ai-video-editing-tools-2026-zh.html"><span class="r-title">AI 视频剪辑工具对比</span><span class="r-cat">视频</span></a>
      </div>
    </section>'''

REL_NEWSLETTER_EN = '''    <section class="related-articles" aria-label="Related articles">
      <h2 id="related-articles">Related articles</h2>
      <p class="sub">More AI writing &amp; newsletter tool coverage.</p>
      <div class="grid">
        <a href="../posts/best-ai-copywriting-tools-2026.html"><span class="r-title">Best AI Copywriting Tools in 2026</span><span class="r-cat">Writing</span></a><a href="../posts/best-ai-email-writing-tools-2026.html"><span class="r-title">Best AI Email Writing Tools in 2026</span><span class="r-cat">Writing</span></a><a href="../posts/best-ai-writing-tools-non-native-english-2026.html"><span class="r-title">Best AI Writing Tools for Non-Native English Speakers</span><span class="r-cat">Writing</span></a>
      </div>
    </section>'''

REL_NEWSLETTER_ZH = '''    <section class="related-articles" aria-label="相关文章">
      <h2 id="related-articles">相关文章</h2>
      <p class="sub">更多 AI 写作与邮件工具内容。</p>
      <div class="grid">
        <a href="../posts/best-ai-copywriting-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 文案写作工具</span><span class="r-cat">写作</span></a><a href="../posts/best-ai-email-writing-tools-2026-zh.html"><span class="r-title">2026 年最佳 AI 邮件写作工具</span><span class="r-cat">写作</span></a><a href="../posts/best-ai-writing-tools-non-native-english-2026-zh.html"><span class="r-title">非英语母语者最佳 AI 写作工具</span><span class="r-cat">写作</span></a>
      </div>
    </section>'''


def fix(p: Path, toc=None, rel=None, howtest=False):
    t = p.read_text(encoding="utf-8")
    orig = t
    if toc and 'class="toc"' not in t:
        t = insert_after_nav_breadcrumb(t, toc)
    if rel and 'related-articles' not in t:
        t = insert_before_article_close(t, rel)
    if howtest and 'how-we-test' not in t:
        t = insert_before_article_close(t, HOW_WE_TEST)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        return True
    return False


jobs = [
    ("posts/what-40-ai-writing-tools-taught-us-2026.html", dict(toc=TOC_WHAT40_EN, rel=REL_WHAT40_EN)),
    ("posts/what-40-ai-writing-tools-taught-us-2026-zh.html", dict(toc=TOC_WHAT40_ZH, rel=REL_WHAT40_ZH)),
    ("posts/best-ai-dubbing-video-localization-tools-2026.html", dict(rel=REL_DUBBING_EN)),
    ("posts/best-ai-dubbing-video-localization-tools-2026-zh.html", dict(rel=REL_DUBBING_ZH)),
    ("posts/best-ai-tools-for-newsletter-creators-2026.html", dict(rel=REL_NEWSLETTER_EN)),
    ("posts/best-ai-tools-for-newsletter-creators-2026-zh.html", dict(rel=REL_NEWSLETTER_ZH)),
    ("posts/edesk-review-2026-zh.html", dict(toc=TOC_EDESK_ZH, howtest=True)),
]

if __name__ == "__main__":
    for rel, kw in jobs:
        p = REPO / rel
        ok = fix(p, **kw)
        print(("✅ 已补" if ok else "⏭ 跳过(已有)"), rel)
