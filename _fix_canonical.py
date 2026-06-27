#!/usr/bin/env python3
"""批量补充分类页/posts页/政策页缺失的 SEO 标签"""
import os

BASE = "/Users/dawei/aitool-picks"
BASE_URL = "https://sun490619.github.io/aitool-picks"

FIXES = [
    # (文件, 在</head>前插入的内容)
    # 分类页 - 都有 GA/OG/Twitter，只缺 canonical
    ("category/coding.html", '<link rel="canonical" href="' + BASE_URL + '/category/coding.html">\n'),
    ("category/seo.html", '<link rel="canonical" href="' + BASE_URL + '/category/seo.html">\n'),
    ("category/video.html", '<link rel="canonical" href="' + BASE_URL + '/category/video.html">\n'),
    # writing.html 缺很多: canonical + OG url + Twitter + GA
    ("category/writing.html", '''    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="''' + BASE_URL + '''/category/writing.html">
    <meta property="og:image" content="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1200&h=630&fit=crop">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AI Writing Tools — Reviews & Comparisons | AI Tool Picks">
    <meta name="twitter:description" content="Best AI writing tools compared: Grammarly, Jasper, Writesonic, Copy.ai, Rytr, QuillBot, LanguageTool, Hemingway and more.">
    <link rel="canonical" href="''' + BASE_URL + '''/category/writing.html">
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D53DQ3JKKL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-D53DQ3JKKL');
    </script>
'''),
    # Posts 页 - 都有 GA/OG/Twitter，只缺 canonical
    ("posts/best-ai-seo-tools-2026.html", '<link rel="canonical" href="' + BASE_URL + '/posts/best-ai-seo-tools-2026.html">\n'),
    ("posts/jasper-vs-writesonic.html", '<link rel="canonical" href="' + BASE_URL + '/posts/jasper-vs-writesonic.html">\n'),
    ("posts/koalawriter-review-2026.html", '<link rel="canonical" href="' + BASE_URL + '/posts/koalawriter-review-2026.html">\n'),
    ("posts/originality-ai-review-2026.html", '<link rel="canonical" href="' + BASE_URL + '/posts/originality-ai-review-2026.html">\n'),
    # 政策页 - 缺 canonical + OG url + Twitter
    ("affiliate-disclosure.html", '''    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Affiliate Disclosure | AI Tool Picks">
    <meta property="og:description" content="Affiliate Disclosure for AI Tool Picks. Transparency about our affiliate relationships and commissions.">
    <meta property="og:url" content="''' + BASE_URL + '''/affiliate-disclosure.html">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Affiliate Disclosure | AI Tool Picks">
    <meta name="twitter:description" content="Affiliate Disclosure for AI Tool Picks. Transparency about our affiliate relationships and commissions.">
    <link rel="canonical" href="''' + BASE_URL + '''/affiliate-disclosure.html">
'''),
    ("privacy.html", '''    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Privacy Policy | AI Tool Picks">
    <meta property="og:description" content="Privacy Policy for AI Tool Picks. How we collect, use, and protect your data.">
    <meta property="og:url" content="''' + BASE_URL + '''/privacy.html">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Privacy Policy | AI Tool Picks">
    <meta name="twitter:description" content="Privacy Policy for AI Tool Picks. How we collect, use, and protect your data.">
    <link rel="canonical" href="''' + BASE_URL + '''/privacy.html">
'''),
]

for filepath_rel, insert_content in FIXES:
    filepath = os.path.join(BASE, filepath_rel)
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert before </head>
    if insert_content in content:
        print(f"ALREADY PRESENT: {filepath_rel}")
        continue

    content = content.replace("</head>", insert_content + "</head>")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Fixed: {filepath_rel}")

print("\nDone!")
