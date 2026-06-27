#!/usr/bin/env python3
"""批量修复 /tools/ 目录下9个工具页的 SEO head 标签"""
import os
import re

TOOLS_DIR = "/Users/dawei/aitool-picks/tools"

# 每个工具页的正确 SEO 数据
TOOLS = {
    "copy-ai": {
        "title": "Copy.ai Review 2026: Best AI Copywriting Tool for GTM Teams?",
        "desc": "Copy.ai review: AI-powered copywriting for GTM teams. 90+ templates, brand voice control, workflow automation. Plans from Free/Pro/Enterprise. Honest hands-on test.",
        "h1": "Copy.ai",
        "subtitle": "Copy.ai 为何是 GTM 团队的选择？"
    },
    "deepl": {
        "title": "DeepL Review 2026: Most Accurate AI Translation Tool?",
        "desc": "DeepL review: Industry-leading neural machine translation with unmatched accuracy. 30+ languages, document translation, glossary support. Plans from Free/Starter/Advanced/Ultimate.",
        "h1": "DeepL",
        "subtitle": "DeepL 凭什么是专业翻译的首选？"
    },
    "grammarly": {
        "title": "Grammarly Review 2026: Best AI Writing Assistant for 30M+ Users?",
        "desc": "Grammarly review: Full-sentence rewrites, tone detection, plagiarism checking, and generative AI. Trusted by 30M+ users. Plans from Free/Premium/Business.",
        "h1": "Grammarly",
        "subtitle": "Grammarly 为何是 3000 万用户的首选？"
    },
    "hemingway": {
        "title": "Hemingway Editor Review 2026: Best Tool for Clear, Bold Writing?",
        "desc": "Hemingway Editor review: Highlights passive voice, hard-to-read sentences, and adverbs. Makes your writing clear and bold. Desktop app and web version available.",
        "h1": "Hemingway Editor",
        "subtitle": "Hemingway 为何能让文风更清晰有力？"
    },
    "jasper": {
        "title": "Jasper AI Review 2026: Best Enterprise AI Writing Tool for Marketing?",
        "desc": "Jasper AI review: Enterprise-grade AI writing with brand voice, campaign workflows, and SEO mode. 50+ templates. Plans from Creator/Pro/Business. Honest comparison.",
        "h1": "Jasper AI",
        "subtitle": "Jasper 为何是营销团队的首选？"
    },
    "languagetool": {
        "title": "LanguageTool Review 2026: Best Open-Source Grammar Checker?",
        "desc": "LanguageTool review: Open-source grammar and style checker supporting 30+ languages. Privacy-focused with local processing option. Plans from Free/Premium.",
        "h1": "LanguageTool",
        "subtitle": "LanguageTool 为何是多语言/隐私用户的首选？"
    },
    "notion-ai": {
        "title": "Notion AI Review 2026: Best AI Inside Your Workspace?",
        "desc": "Notion AI review: AI writing, editing, and Q&A directly inside Notion. Summarize, translate, brainstorm without leaving your docs. Add-on for Notion plans.",
        "h1": "Notion AI",
        "subtitle": "Notion AI 为何是 Notion 用户的首选？"
    },
    "quillbot": {
        "title": "QuillBot Review 2026: Best AI Paraphrasing Tool for Academic Writing?",
        "desc": "QuillBot review: AI paraphrasing, grammar checker, summarizer, citation generator, and plagiarism checker. 7 paraphrasing modes. Plans from Free/Premium.",
        "h1": "QuillBot",
        "subtitle": "QuillBot 为何是学术与内容优化首选？"
    },
    "writesonic": {
        "title": "Writesonic Review 2026: Best AI Writer for SEO Content Teams?",
        "desc": "Writesonic review: AI article writer with real-time SEO data, competitor analysis, and brand voice. 100+ templates. Plans from Free/Individual/Teams. Honest test.",
        "h1": "Writesonic",
        "subtitle": "Writesonic 为何受 SEO 团队青睐？"
    },
}

OLD_HEAD = """    <title>Rytr Review 2026: Best Budget AI Writing Tool? — AI Tool Picks</title>
    <meta name="description" content="Rytr review: 40+ templates, 30+ languages, built-in plagiarism checker, AI images included. Plans from Free/$9/$29. Perfect for creators on a budget.">"""

NEW_HEAD_TEMPLATE = """    <title>{title} — AI Tool Picks</title>
    <meta name="description" content="{desc}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%232563eb'/><path d='M8 12h16M8 16h16M8 20h16' stroke='white' stroke-width='2' stroke-linecap='round'/></svg>">
    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title} — AI Tool Picks">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://sun490619.github.io/aitool-picks/tools/{slug}.html">
    <meta property="og:image" content="https://images.unsplash.com/photo-1677442136019-21780ecad994?w=1200&h=630&fit=crop">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} — AI Tool Picks">
    <meta name="twitter:description" content="{desc}">
    <link rel="canonical" href="https://sun490619.github.io/aitool-picks/tools/{slug}.html">
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D53DQ3JKKL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-D53DQ3JKKL');
    </script>"""

CSS_LINK = """    <link rel="stylesheet" href="/aitool-picks/styles.css">"""

for slug, data in TOOLS.items():
    filepath = os.path.join(TOOLS_DIR, f"{slug}.html")
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_head = NEW_HEAD_TEMPLATE.format(
        title=data["title"],
        desc=data["desc"],
        slug=slug
    )

    # Replace old head + CSS link with new head + CSS link
    old_block = OLD_HEAD + "\n" + CSS_LINK
    new_block = new_head + "\n" + CSS_LINK

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Fixed: {slug}.html")
    else:
        print(f"✗ NOT FOUND old block in: {slug}.html")

print("\nDone!")
