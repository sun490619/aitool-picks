#!/usr/bin/env python3
"""
为 aitool-picks 全站生成「品牌化科技风」配图，替换原先与内容无关的
picsum 随机风景/人物图、以及老 unsplash 占位图。

设计语言：
- 深色科技渐变背景（深蓝紫 -> 近黑）
- 细网格 / 光点纹理（AI 科技感）
- 顶部品牌标识 "AI TOOL PICKS"
- 大标题 = 对应页面/工具标题（与内容强相关）
- 底部小标签（分类 / 年份）

所有图均为本地生成，零版权风险，且每张都精确对应页面主题。
"""
import os
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# ---------- 设计常量 ----------
W, H = 1200, 630
CARD_W, CARD_H = 800, 450  # 文章内文横图 / 分类卡片

BG_TOP = "#1b1f3b"
BG_BOT = "#0a0c1a"
ACCENT = "#6c8cff"
ACCENT2 = "#22d3ee"
TEXT = "#f5f7ff"
SUB = "#aab2d5"
BRAND = "#9db4ff"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def wrap_title(title, max_chars=22):
    """简单按词换行，每行不超过 max_chars。"""
    words = title.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:3]  # 最多 3 行


def svg_for(title, tag, w=W, h=H, brand="AI TOOL PICKS", subtitle=""):
    lines = wrap_title(title, max_chars=20 if w >= 1000 else 16)
    # 标题字号随行数自适应
    n = len(lines)
    fs = 72 if n <= 1 else (60 if n == 2 else 50)
    if w < 1000:
        fs = int(fs * 0.8)
    # 标题垂直居中偏下
    total_h = n * (fs + 12)
    start_y = h * 0.52 - total_h / 2 + fs
    title_svg = ""
    for i, ln in enumerate(lines):
        y = start_y + i * (fs + 12)
        title_svg += (
            f'<text x="{w*0.07:.0f}" y="{y:.0f}" font-family="Segoe UI, Helvetica, Arial, sans-serif" '
            f'font-size="{fs}" font-weight="800" fill="{TEXT}">{esc(ln)}</text>\n'
        )
    sub_svg = ""
    if subtitle:
        sy = start_y + total_h + 18
        sub_svg = (
            f'<text x="{w*0.07:.0f}" y="{sy:.0f}" font-family="Segoe UI, Helvetica, Arial, sans-serif" '
            f'font-size="{int(fs*0.4)}" font-weight="500" fill="{SUB}">{esc(subtitle)}</text>\n'
        )

    grid = ""
    step = 48
    for gx in range(0, w + 1, step):
        grid += f'<line x1="{gx}" y1="0" x2="{gx}" y2="{h}" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1"/>'
    for gy in range(0, h + 1, step):
        grid += f'<line x1="0" y1="{gy}" x2="{w}" y2="{gy}" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1"/>'

    # 光点
    dots = ""
    import random
    random.seed(hash(title) % 100000)
    for _ in range(26):
        cx = random.randint(0, w)
        cy = random.randint(0, h)
        r = random.randint(1, 3)
        op = random.uniform(0.05, 0.22)
        dots += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" fill-opacity="{op:.2f}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="55%" stop-color="#121634"/>
      <stop offset="100%" stop-color="{BG_BOT}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT}"/>
      <stop offset="100%" stop-color="{ACCENT2}"/>
    </linearGradient>
    <radialGradient id="glow" cx="80%" cy="18%" r="60%">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <g>{grid}</g>
  <g>{dots}</g>
  <!-- 品牌标识 -->
  <g transform="translate({w*0.07:.0f}, {h*0.13:.0f})">
    <rect x="0" y="-26" width="44" height="44" rx="10" fill="url(#acc)"/>
    <text x="58" y="6" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="30" font-weight="800" fill="{BRAND}" letter-spacing="1">{esc(brand)}</text>
  </g>
  <!-- 装饰刻度线 -->
  <rect x="{w*0.07:.0f}" y="{h*0.30:.0f}" width="64" height="5" rx="2.5" fill="url(#acc)"/>
  {title_svg}
  {sub_svg}
  <!-- 底部标签 -->
  <text x="{w*0.07:.0f}" y="{h*0.9:.0f}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="22" font-weight="600" fill="{ACCENT2}">{esc(tag)}</text>
</svg>'''
    return svg


def render(svg, out_path, w=W, h=H):
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                     write_to=out_path, output_width=w, output_height=h,
                     background_color=BG_BOT)


def gen(filename, title, tag, w=W, h=H, subtitle=""):
    out = os.path.join(IMG_DIR, filename)
    svg = svg_for(title, tag, w=w, h=h, subtitle=subtitle)
    render(svg, out, w=w, h=h)
    print(f"  -> {filename} ({w}x{h})")
    return out


# ============ 1) 全站 OG 图（文章 / 站点 / 工具 / 首页）============
print("== OG 图 ==")

# 首页
gen("og-aitool-picks-home.jpg", "Best AI Tools, Honestly Reviewed", "AI Tool Picks · 2026")

# 文章页 OG（文件名 -> 标题）
articles = {
    "og-ai-coding-assistants-2026": ("AI Coding Assistants 2026", "Comparison Guide"),
    "og-ai-coding-review-2026": ("AI Code Review Tools", "Hands-on Review"),
    "og-ai-customer-support-setup-2026": ("AI Customer Support Setup", "Step-by-step Guide"),
    "og-ai-productivity-tools-2026": ("AI Productivity Tools", "Best Picks 2026"),
    "og-ai-side-hustle-2026": ("AI Tools for Side Hustles", "Earn Smarter 2026"),
    "og-ai-tools-dropshipping-2026": ("AI Tools for Dropshipping", "Best Picks 2026"),
    "og-ai-tools-for-students-2026": ("AI Tools for Students", "Study Smarter 2026"),
    "og-ai-transcriber-meeting-notes-2026": ("AI Meeting Note Transcribers", "Best Picks 2026"),
    "og-ai-trip-planner-review-2026": ("AI Trip Planner Review", "Hands-on Test"),
    "og-ai-video-editing-tools-2026": ("AI Video Editing Tools", "Best Picks 2026"),
    "og-best-ai-avatar-video-tools-2026": ("Best AI Avatar Video Tools", "Top Picks 2026"),
    "og-best-ai-coding-assistants-2026": ("Best AI Coding Assistants", "Top Picks 2026"),
    "og-best-ai-email-writing-tools-2026": ("Best AI Email Writing Tools", "Top Picks 2026"),
    "og-best-ai-grammar-tools-2026": ("Best AI Grammar Tools", "Top Picks 2026"),
    "og-best-ai-image-upscalers-2026": ("Best AI Image Upscalers", "Top Picks 2026"),
    "og-best-ai-music-generators-2026": ("Best AI Music Generators", "Top Picks 2026"),
    "og-best-ai-note-taking-tools-2026": ("Best AI Note-Taking Tools", "Top Picks 2026"),
    "og-best-ai-presentation-tools-2026": ("Best AI Presentation Tools", "Top Picks 2026"),
    "og-best-ai-seo-tools-2026": ("Best AI SEO Tools", "Top Picks 2026"),
    "og-best-ai-tools-faceless-youtube-2026": ("AI Tools for Faceless YouTube", "Top Picks 2026"),
    "og-best-ai-tools-for-podcasters-2026": ("Best AI Tools for Podcasters", "Top Picks 2026"),
    "og-best-ai-tools-for-small-business-2026": ("Best AI Tools for Small Business", "Top Picks 2026"),
    "og-best-ai-tools-for-students-2026": ("Best AI Tools for Students", "Top Picks 2026"),
    "og-best-ai-translation-tools-2026": ("Best AI Translation Tools", "Top Picks 2026"),
    "og-best-ai-video-tools-2026": ("Best AI Video Tools", "Top Picks 2026"),
    "og-best-ai-voice-generator-tools-2026": ("Best AI Voice Generators", "Top Picks 2026"),
    "og-best-ai-writing-tools-non-native-english-2026": ("AI Writing for Non-Native English", "Top Picks 2026"),
    "og-best-free-ai-tools-content-creators-2026": ("Free AI Tools for Creators", "Top Picks 2026"),
    "og-best-free-ai-tools-freelancers-2026": ("Free AI Tools for Freelancers", "Top Picks 2026"),
    "og-best-free-ai-tools-students-2026": ("Free AI Tools for Students", "Top Picks 2026"),
    "og-canva-ai-review-2026": ("Canva AI Review", "Hands-on Review 2026"),
    "og-chatgpt-vs-claude-vs-gemini-2026": ("ChatGPT vs Claude vs Gemini", "Head-to-Head 2026"),
    "og-copy-ai-review-2026": ("Copy.ai Review", "Hands-on Review 2026"),
    "og-cursor-ai-code-editor-review-2026": ("Cursor AI Editor Review", "Hands-on Review 2026"),
    "og-deepl-review-2026": ("DeepL Review", "Hands-on Review 2026"),
    "og-deepseek-vs-claude-2026": ("DeepSeek vs Claude", "Head-to-Head 2026"),
    "og-descript-ai-review-2026": ("Descript AI Review", "Hands-on Review 2026"),
    "og-frase-review-2026": ("Frase Review", "Hands-on Review 2026"),
    "og-generative-engine-optimization-guide-2026": ("Generative Engine Optimization", "GEO Guide 2026"),
    "og-github-copilot-ai-review-2026": ("GitHub Copilot Review", "Hands-on Review 2026"),
    "og-grammarlygo-review-2026": ("GrammarlyGO Review", "Hands-on Review 2026"),
    "og-gumroad-review-2026": ("Gumroad Review", "Hands-on Review 2026"),
    "og-hugging-face-ai-review-2026": ("Hugging Face Review", "Hands-on Review 2026"),
    "og-jasper-ai-review-2026": ("Jasper AI Review", "Hands-on Review 2026"),
    "og-jasper-vs-writesonic": ("Jasper vs Writesonic", "Head-to-Head"),
    "og-kling-ai-review-2026": ("Kling AI Review", "Hands-on Review 2026"),
    "og-koalawriter-review-2026": ("KoalaWriter Review", "Hands-on Review 2026"),
    "og-langchain-ai-review-2026": ("LangChain Review", "Hands-on Review 2026"),
    "og-market-data-analysis-ai-2026": ("AI Market Data Analysis", "Best Picks 2026"),
    "og-mem-ai-review-2026": ("Mem AI Review", "Hands-on Review 2026"),
    "og-midjourney-v7-review-2026": ("Midjourney v7 Review", "Hands-on Review 2026"),
    "og-notion-ai-review-2026": ("Notion AI Review", "Hands-on Review 2026"),
    "og-open-source-ai-models-2026": ("Open-Source AI Models", "Best Picks 2026"),
    "og-originality-ai-review-2026": ("Originality.ai Review", "Hands-on Review 2026"),
    "og-perplexity-ai-review-2026": ("Perplexity AI Review", "Hands-on Review 2026"),
    "og-replit-ai-review-2026": ("Replit AI Review", "Hands-on Review 2026"),
    "og-runway-ai-review-2026": ("Runway AI Review", "Hands-on Review 2026"),
    "og-runway-ml-review-2026": ("Runway ML Review", "Hands-on Review 2026"),
    "og-rytr-review-2026": ("Rytr Review", "Hands-on Review 2026"),
    "og-track-brand-visibility-ai-search-2026": ("Track Brand in AI Search", "GEO Tool 2026"),
    "og-wordtune-review-2026": ("Wordtune Review", "Hands-on Review 2026"),
    "og-writesonic-review-2026": ("Writesonic Review", "Hands-on Review 2026"),
    "og-zapier-ai-review-2026": ("Zapier AI Review", "Hands-on Review 2026"),
    "og-sora-ai-review-2026": ("Sora AI Review", "Hands-on Review 2026"),
    "og-tool-jasper": ("Jasper AI", "AI Writing Tool"),
}

for fn, (title, tag) in articles.items():
    gen(fn + ".jpg", title, tag)

# 站点静态页 OG
site_pages = {
    "og-site-about": ("About AI Tool Picks", "Our Mission"),
    "og-site-affiliate-disclosure": ("Affiliate Disclosure", "Transparency First"),
    "og-site-audio": ("AI Audio Tools", "Category"),
    "og-site-best-ai-seo-tools": ("Best AI SEO Tools", "Category"),
    "og-site-best-ai-writing-tools": ("Best AI Writing Tools", "Category"),
    "og-site-coding": ("AI Coding Tools", "Category"),
    "og-site-contact": ("Contact AI Tool Picks", "Get in Touch"),
    "og-site-free-resources": ("Free AI Resources", "Downloads"),
    "og-site-jasper-vs-writesonic": ("Jasper vs Writesonic", "Comparison"),
    "og-site-koala-writer-alternative": ("KoalaWriter Alternatives", "Comparison"),
    "og-site-privacy": ("Privacy Policy", "AI Tool Picks"),
    "og-site-productivity": ("AI Productivity Tools", "Category"),
    "og-site-seo": ("AI SEO Tools", "Category"),
    "og-site-suggest-tool": ("Suggest a Tool", "We Review It"),
    "og-site-terms": ("Terms of Service", "AI Tool Picks"),
    "og-site-video": ("AI Video Tools", "Category"),
    "og-site-writing": ("AI Writing Tools", "Category"),
}
for fn, (title, tag) in site_pages.items():
    gen(fn + ".jpg", title, tag)

# ============ 2) 工具页内文图 + og（u0x 系列）============
print("== 工具页内文图 ==")
tools = {
    "u09": ("DeepL", "AI Translator"),
    "u11": ("AI SEO Tools", "Category"),
    "u08": ("AI Writing Tools", "Category"),
    "u15": ("AI Coding Tools", "Category"),
    "u24": ("AI Video Tools", "Category"),
    "u16": ("AI Productivity Tools", "Category"),
    "u13": ("Copy.ai", "AI Writing Tool"),
    "u14": ("Hemingway Editor", "Writing Tool"),
    "u19": ("Notion AI", "Workspace AI"),
    "u20": ("Writesonic", "AI Writing Tool"),
    "u22": ("Grammarly", "Writing Assistant"),
    "u23": ("LanguageTool", "Grammar Checker"),
    "u26": ("Rytr", "AI Writing Tool"),
    "u12": ("QuillBot", "AI Paraphraser"),
    "u04": ("Runway ML", "AI Video Generator"),
    "u02": ("AI Tool Picks", "Best AI Tools"),
}
for fn, (title, tag) in tools.items():
    # 内文横图 800x450
    gen(fn + ".jpg", title, tag, w=CARD_W, h=CARD_H)

# ============ 3) 其余 u0x 占位图（如有引用也一并品牌化）============
print("== 其余 u 系列 ==")
extra_u = {}
for i in range(1, 34):
    name = f"u{i:02d}"
    if name not in tools:
        extra_u[name] = ("AI Tool Picks", "Best AI Tools 2026")
for fn, (title, tag) in extra_u.items():
    gen(fn + ".jpg", title, tag, w=CARD_W, h=CARD_H)

print("\n全部品牌化图片生成完成。")
