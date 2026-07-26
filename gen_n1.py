# -*- coding: utf-8 -*-
"""N1 替代品 AEO 板块：4 个核心"X 的替代品"页（中英 + FAQ + 直接回答型导语）。
目标：被 ChatGPT/Perplexity/国内 AI 当作"最佳替代品"答案源引用。
"""
from _gen_en import build as build_en
from _gen_zh import build as build_zh

def page(title, lead, why, list_items, choose, faq):
    """返回 (en_html, zh_html) 的 main_html，list_items 为 (name, zh_name, one, zh_one, url) 列表。"""
    en_items = "\n".join(
        '<li><strong><a href="%s">%s</a></strong> — %s</li>' % (u, n, o) for (n, zn, o, zo, u) in list_items)
    zh_items = "\n".join(
        '<li><strong><a href="%s">%s</a></strong> — %s</li>' % (u, zn, zo) for (n, zn, o, zo, u) in list_items)
    en = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">%s</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks Team</span><span>2026-07-27</span><span>7 min read</span>
        <span class="article-meta-item" style="margin-left:auto;">By AI Tool Picks Team</span>
      </div>
      <p class="post-lead">%s</p>
      <p class="post-meta">Updated July 27, 2026</p>
    </header>
    <p><strong>Disclosure:</strong> This page may contain <a href="/affiliate-disclosure.html">affiliate links</a>. We only list tools we have tested.</p>
    <h2>Why look for alternatives</h2>
    <p>%s</p>
    <h2>The best alternatives</h2>
    <ul>%s</ul>
    <h2>How to choose</h2>
    <p>%s</p>
    <section class="how-we-test" aria-label="How we pick">
      <h2>How we pick</h2>
      <p>We rank alternatives by real task fit, not hype: writing quality, context window, price, privacy, and ecosystem. Each is tested hands-on where possible. Links may be affiliate links and never cost you extra.</p>
    </section>
  </div>
</article>
</main>''' % (title, lead, why, en_items, choose)
    zh = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">%s</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks Team</span><span>2026-07-27</span><span>7 分钟阅读</span>
        <span class="article-meta-item" style="margin-left:auto;">作者：AI Tool Picks Team</span>
      </div>
      <p class="post-lead">%s</p>
      <p class="post-meta">更新于 2026 年 7 月 27 日</p>
    </header>
    <p><strong>披露：</strong>本页可能含<a href="/affiliate-disclosure.html">联盟链接</a>。我们只列亲手实测的工具。</p>
    <h2>为什么要找替代品</h2>
    <p>%s</p>
    <h2>最佳替代品</h2>
    <ul>%s</ul>
    <h2>怎么选</h2>
    <p>%s</p>
    <section class="how-we-test" aria-label="我们的挑选方法">
      <h2>我们的挑选方法</h2>
      <p>我们按真实任务适配而非热度排序：写作质量、上下文长度、价格、隐私和生态。每款都尽量亲手实测。链接可能为联盟链接，绝不会让你多花钱。</p>
    </section>
  </div>
</article>
</main>''' % (title, lead, why, zh_items, choose)
    return en, zh

# ---------- 1) ChatGPT alternatives ----------
slug = "chatgpt-alternatives-2026"
en_t = "Best ChatGPT Alternatives in 2026"
zh_t = "2026 年最佳 ChatGPT 替代品"
en_lead = "The best ChatGPT alternative in 2026 depends on your job: Claude for nuanced writing and safety, Gemini inside Google Workspace, Perplexity for cited research, and specialized tools for coding or images."
zh_lead = "2026 年最好的 ChatGPT 替代品取决于你的任务：Claude 适合细腻写作与安全、Gemini 适合谷歌生态、Perplexity 适合带引用的研究，编程或图像则有专用工具。"
en_why = "You may want an alternative for lower cost, a longer context window, stronger privacy, or a tool built for one task instead of a general assistant."
zh_why = "你可能因为更低价、更长上下文、更强隐私，或想要一个专做某件事而非通用助手的工具而寻找替代品。"
en_choose = "Pick by primary use: writing and safety → Claude; Google Workspace → Gemini; research with citations → Perplexity; coding → GitHub Copilot or Claude; images → Midjourney or DALL·E."
zh_choose = "按主要用途选：写作与安全 → Claude；谷歌生态 → Gemini；带引用的研究 → Perplexity；编程 → GitHub Copilot 或 Claude；图像 → Midjourney 或 DALL·E。"
items = [
    ("Claude (Anthropic)", "Claude（Anthropic）", "best for nuanced writing, long context, and safety guardrails", "细腻写作、长上下文与安全护栏最佳", "https://aitool-picks.com/tools/notion-ai.html"),
    ("Gemini", "Gemini", "best inside Google Workspace and for multimodal tasks", "谷歌生态与多模态任务最佳", "https://aitool-picks.com/posts/best-ai-seo-tools-2026.html"),
    ("Perplexity", "Perplexity", "best for research with linked citations", "带链接引用的研究最佳", "https://aitool-picks.com/posts/generative-engine-optimization-guide-2026.html"),
    ("GitHub Copilot", "GitHub Copilot", "best for in-editor coding", "编辑器内编程最佳", "https://aitool-picks.com/posts/github-copilot-ai-review-2026.html"),
    ("Microsoft Copilot", "Microsoft Copilot", "best inside Office 365", "Office 365 内最佳", "https://aitool-picks.com/"),
]
en_html, zh_html = page(en_t, en_lead, en_why, items, en_choose, None)
faq_en = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"What is the best free ChatGPT alternative?","acceptedAnswer":{"@type":"Answer","text":"Claude (free tier), Perplexity, and Meta AI all offer capable free tiers. Claude leads on writing quality; Perplexity on cited research."}},
  {"@type":"Question","name":"Which ChatGPT alternative is best for writing?","acceptedAnswer":{"@type":"Answer","text":"Claude is widely regarded as the strongest for long-form, nuanced writing and follows safety and style instructions closely."}},
  {"@type":"Question","name":"Which is best for coding?","acceptedAnswer":{"@type":"Answer","text":"GitHub Copilot for in-editor completion, and Claude or Cursor for larger refactoring tasks."}}
]}
faq_zh = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"最好的免费 ChatGPT 替代品是什么？","acceptedAnswer":{"@type":"Answer","text":"Claude（免费档）、Perplexity 和 Meta AI 都有能用的免费档。Claude 写作质量领先，Perplexity 擅长带引用的研究。"}},
  {"@type":"Question","name":"哪个 ChatGPT 替代品最适合写作？","acceptedAnswer":{"@type":"Answer","text":"Claude 普遍认为最强于长文、细腻写作，且能紧密遵循安全与风格指令。"}},
  {"@type":"Question","name":"哪个最适合编程？","acceptedAnswer":{"@type":"Answer","text":"编辑器内补全用 GitHub Copilot；较大规模重构用 Claude 或 Cursor。"}}
]}
build_en(slug, en_t, "The best ChatGPT alternatives in 2026 by task: Claude for writing, Gemini for Workspace, Perplexity for research, and specialized tools for coding or images.", "", "", en_html, faq_json=faq_en)
build_zh(slug, zh_t, "2026 年按任务选最佳 ChatGPT 替代品：写作用 Claude、谷歌生态用 Gemini、研究用 Perplexity，编程与图像各有专用工具。", "", "", zh_html, faq_json=faq_zh)

# ---------- 2) Notion AI alternatives ----------
slug = "notion-alternatives-2026"
en_t = "Best Notion AI Alternatives in 2026"
zh_t = "2026 年最佳 Notion AI 替代品"
en_lead = "The best Notion AI alternative depends on what you outgrew: Capacities or Obsidian for local-first notes, Coda for docs that act like apps, and Matter or Readwise for reading capture."
zh_lead = "最好的 Notion AI 替代品取决于你缺什么：本地优先笔记选 Capacities 或 Obsidian，像应用一样的文档选 Coda，阅读采集选 Matter 或 Readwise。"
en_why = "Users switch for offline/local-first storage, flatter pricing, or a workspace that behaves more like a database or app."
zh_why = "用户转换是因为要离线/本地存储、更平的定价，或想要更像数据库或应用的 workspace。"
en_choose = "Want local-first → Obsidian; want docs-as-apps → Coda; want AI writing inside docs → keep Notion AI or try Coda AI; want reading capture → Matter."
zh_choose = "要本地优先 → Obsidian；要文档即应用 → Coda；要文档内 AI 写作 → 留 Notion AI 或试 Coda AI；要阅读采集 → Matter。"
items = [
    ("Obsidian", "Obsidian", "local-first Markdown notes with AI plugins", "本地优先 Markdown 笔记，可加 AI 插件", "https://aitool-picks.com/tools/notion-ai.html"),
    ("Coda", "Coda", "docs that function like apps, with Coda AI", "像应用一样的文档，含 Coda AI", "https://aitool-picks.com/posts/best-ai-note-taking-tools-2026.html"),
    ("Capacities", "Capacities", "object-based, local-friendly PKM", "基于对象、偏本地的个人知识管理", "https://aitool-picks.com/posts/best-ai-note-taking-tools-2026.html"),
    ("Mem", "Mem", "AI-native note app with auto-organization", "AI 原生、自动整理的记忆型笔记", "https://aitool-picks.com/posts/mem-ai-review-2026.html"),
]
en_html, zh_html = page(en_t, en_lead, en_why, items, en_choose, None)
faq_en = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"Is there a free Notion AI alternative?","acceptedAnswer":{"@type":"Answer","text":"Obsidian is free for personal local-first notes and supports AI via plugins. Coda and Capacities have free tiers too."}},
  {"@type":"Question","name":"What is the best local-first Notion alternative?","acceptedAnswer":{"@type":"Answer","text":"Obsidian is the leading local-first option; Capacities is a friendlier object-based alternative."}},
  {"@type":"Question","name":"Which alternative is best for AI writing in docs?","acceptedAnswer":{"@type":"Answer","text":"Coda AI adds writing help inside docs; Mem auto-organizes notes with AI."}}
]}
faq_zh = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"有免费的 Notion AI 替代品吗？","acceptedAnswer":{"@type":"Answer","text":"Obsidian 个人本地笔记免费，可通过插件用 AI；Coda 和 Capacities 也有免费档。"}},
  {"@type":"Question","name":"最好的本地优先 Notion 替代品是什么？","acceptedAnswer":{"@type":"Answer","text":"Obsidian 是本地优先的首选；Capacities 是更友好的基于对象的替代品。"}},
  {"@type":"Question","name":"哪个替代品最适合文档内 AI 写作？","acceptedAnswer":{"@type":"Answer","text":"Coda AI 在文档内加写作辅助；Mem 用 AI 自动整理笔记。"}}
]}
build_en(slug, en_t, "Best Notion AI alternatives in 2026: Obsidian for local-first, Coda for docs-as-apps, Capacities for object-based PKM, and Mem for AI-native notes.", "", "", en_html, faq_json=faq_en)
build_zh(slug, zh_t, "2026 年最佳 Notion AI 替代品：本地优先选 Obsidian、文档即应用选 Coda、基于对象选 Capacities、AI 原生笔记选 Mem。", "", "", zh_html, faq_json=faq_zh)

# ---------- 3) Jasper alternatives ----------
slug = "jasper-alternatives-2026"
en_t = "Best Jasper AI Alternatives in 2026"
zh_t = "2026 年最佳 Jasper AI 替代品"
en_lead = "The best Jasper alternative is usually a cheaper, more flexible writer: Copy.ai or Writesonic for marketing teams, Rytr for low cost, and Notion AI or Claude for everyday drafting."
zh_lead = "最好的 Jasper 替代品通常是更便宜、更灵活的写作工具：营销团队用 Copy.ai 或 Writesonic，低成本用 Rytr，日常草稿用 Notion AI 或 Claude。"
en_why = "Jasper is powerful but priced for teams; solo users and small teams often want similar output at a lower cost or with a simpler workflow."
zh_why = "Jasper 很强但按团队定价；个人和小团队常想要相近产出但更低价或更简单的工作流。"
en_choose = "Marketing pipelines → Copy.ai or Writesonic; tight budget → Rytr; daily drafting → Notion AI or Claude; brand-voice control → Jasper still leads."
zh_choose = "营销流水线 → Copy.ai 或 Writesonic；预算紧 → Rytr；日常草稿 → Notion AI 或 Claude；品牌语气控制 → Jasper 仍领先。"
items = [
    ("Copy.ai", "Copy.ai", "marketing workflows and brand voices", "营销工作流与品牌语气", "https://aitool-picks.com/tools/copy-ai.html"),
    ("Writesonic", "Writesonic", "long-form + SEO articles at scale", "规模化长文与 SEO 文章", "https://aitool-picks.com/tools/writesonic.html"),
    ("Rytr", "Rytr", "low-cost everyday writing", "低成本的日常写作", "https://aitool-picks.com/tools/rytr.html"),
    ("Claude", "Claude", "high-quality drafting and editing", "高质量起草与润色", "https://aitool-picks.com/posts/jasper-vs-writesonic.html"),
]
en_html, zh_html = page(en_t, en_lead, en_why, items, en_choose, None)
faq_en = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"What is the cheapest Jasper alternative?","acceptedAnswer":{"@type":"Answer","text":"Rytr is the lowest-cost option for everyday writing; Copy.ai and Writesonic sit between Rytr and Jasper in price."}},
  {"@type":"Question","name":"Which Jasper alternative is best for SEO content?","acceptedAnswer":{"@type":"Answer","text":"Writesonic and Copy.ai both target long-form SEO content and are common Jasper replacements for content teams."}},
  {"@type":"Question","name":"Is Claude a good Jasper alternative?","acceptedAnswer":{"@type":"Answer","text":"For drafting and editing quality, Claude is excellent, though it lacks Jasper's built-in brand-voice marketing workflows."}}
]}
faq_zh = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"最便宜的 Jasper 替代品是什么？","acceptedAnswer":{"@type":"Answer","text":"Rytr 是日常写作最低价的选项；Copy.ai 与 Writesonic 价格介于 Rytr 与 Jasper 之间。"}},
  {"@type":"Question","name":"哪个 Jasper 替代品最适合 SEO 内容？","acceptedAnswer":{"@type":"Answer","text":"Writesonic 与 Copy.ai 都主打长文 SEO 内容，是内容团队常见的 Jasper 替代。"}},
  {"@type":"Question","name":"Claude 是好的 Jasper 替代品吗？","acceptedAnswer":{"@type":"Answer","text":"就起草与润色质量而言 Claude 很出色，但它缺少 Jasper 内置的品牌语气营销工作流。"}}
]}
build_en(slug, en_t, "Best Jasper AI alternatives in 2026: Copy.ai and Writesonic for marketing, Rytr for low cost, Claude for quality drafting.", "", "", en_html, faq_json=faq_en)
build_zh(slug, zh_t, "2026 年最佳 Jasper AI 替代品：营销用 Copy.ai 与 Writesonic、低成本用 Rytr、高质量起草用 Claude。", "", "", zh_html, faq_json=faq_zh)

# ---------- 4) Grammarly alternatives ----------
slug = "grammarly-alternatives-2026"
en_t = "Best Grammarly Alternatives in 2026"
zh_t = "2026 年最佳 Grammarly 替代品"
en_lead = "The best Grammarly alternative depends on need: QuillBot for paraphrasing, ProWritingAid for deep reports, LanguageTool for privacy, and Hemingway for blunt clarity."
zh_lead = "最好的 Grammarly 替代品取决于需求：改写用 QuillBot、深度报告用 ProWritingAid、隐私用 LanguageTool、直白清晰用 Hemingway。"
en_why = "Users switch for stronger paraphrasing, deeper style reports, offline/privacy handling, or a one-time price instead of a subscription."
zh_why = "用户转换是为了更强改写、更深风格报告、离线/隐私处理，或一次性买断而非订阅。"
en_choose = "Paraphrasing → QuillBot; deep editing reports → ProWritingAid; privacy/offline → LanguageTool; plain clarity → Hemingway Editor."
zh_choose = "改写 → QuillBot；深度编辑报告 → ProWritingAid；隐私/离线 → LanguageTool；直白清晰 → Hemingway Editor。"
items = [
    ("QuillBot", "QuillBot", "paraphrasing and summarizer", "改写与摘要", "https://aitool-picks.com/tools/quillbot.html"),
    ("ProWritingAid", "ProWritingAid", "in-depth style and structure reports", "深入的风格与结构报告", "https://aitool-picks.com/posts/best-ai-grammar-tools-2026.html"),
    ("LanguageTool", "LanguageTool", "privacy-friendly, many languages", "隐私友好、多语言", "https://aitool-picks.com/tools/languagetool.html"),
    ("Hemingway Editor", "Hemingway Editor", "forces bold, clear writing", "逼出简练清晰的写作", "https://aitool-picks.com/posts/best-ai-grammar-tools-2026.html"),
]
en_html, zh_html = page(en_t, en_lead, en_why, items, en_choose, None)
faq_en = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"What is the best free Grammarly alternative?","acceptedAnswer":{"@type":"Answer","text":"LanguageTool and QuillBot both have free tiers; Hemingway Editor has a free web editor. ProWritingAid offers a limited free tier."}},
  {"@type":"Question","name":"Which Grammarly alternative is best for paraphrasing?","acceptedAnswer":{"@type":"Answer","text":"QuillBot is the leading paraphrasing tool and a common Grammarly companion or alternative."}},
  {"@type":"Question","name":"Is there a privacy-first Grammarly alternative?","acceptedAnswer":{"@type":"Answer","text":"LanguageTool can run with stronger privacy and supports many languages, making it popular for sensitive writing."}}
]}
faq_zh = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"最好的免费 Grammarly 替代品是什么？","acceptedAnswer":{"@type":"Answer","text":"LanguageTool 与 QuillBot 都有免费档；Hemingway Editor 有免费网页版。ProWritingAid 有受限免费档。"}},
  {"@type":"Question","name":"哪个 Grammarly 替代品最适合改写？","acceptedAnswer":{"@type":"Answer","text":"QuillBot 是领先的改写工具，常作为 Grammarly 的搭档或替代品。"}},
  {"@type":"Question","name":"有隐私优先的 Grammarly 替代品吗？","acceptedAnswer":{"@type":"Answer","text":"LanguageTool 隐私更强且支持多语言，适合敏感写作。"}}
]}
build_en(slug, en_t, "Best Grammarly alternatives in 2026: QuillBot for paraphrasing, ProWritingAid for reports, LanguageTool for privacy, Hemingway for clarity.", "", "", en_html, faq_json=faq_en)
build_zh(slug, zh_t, "2026 年最佳 Grammarly 替代品：改写用 QuillBot、报告用 ProWritingAid、隐私用 LanguageTool、清晰用 Hemingway。", "", "", zh_html, faq_json=faq_zh)

print("=== N1 替代品 AEO 板块 4 页（中英 + FAQ）已生成 ===")
