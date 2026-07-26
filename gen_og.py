# -*- coding: utf-8 -*-
"""为 6 个新页（2 评测 + 4 替代品）生成 OG 图（1200x630 渐变 + 标题），中英文各一张。"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
FONT_EN = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_ZH = "/System/Library/Fonts/PingFang.ttc"

def wrap(text, zh, max_chars):
    if zh:
        lines, cur = [], ""
        for ch in text:
            cur += ch
            if len(cur) >= max_chars:
                lines.append(cur); cur = ""
        if cur: lines.append(cur)
        return lines
    words = text.split(" "); lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def make(slug, title, zh):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(18 + t * 24); g = int(22 + t * 28); b = int(40 + t * 46)
        d.line([(0, y), (W, y)], (r, g, b))
    d.rectangle([0, 0, 10, H], (90, 130, 255))  # 左侧强调条
    try:
        f = ImageFont.truetype(FONT_ZH if zh else FONT_EN, 58 if zh else 62)
        fsmall = ImageFont.truetype(FONT_EN, 30)
    except Exception:
        f = ImageFont.load_default(); fsmall = f
    lines = wrap(title, zh, 16 if zh else 24)
    lh = f.size + 20
    y = H // 2 - (len(lines) * lh) // 2 + 20
    for ln in lines:
        d.text((90, y), ln, font=f, fill=(255, 255, 255)); y += lh
    d.text((90, H - 96), "AI Tool Picks", font=fsmall, fill=(175, 188, 215))
    suffix = "-zh" if zh else ""
    out = os.path.join(OUT, "og-%s%s.jpg" % (slug, suffix))
    img.save(out, "JPEG", quality=88)
    print("OG:", out)

data = [
    ("elevenlabs-review-2026", "ElevenLabs Review 2026", "ElevenLabs 评测 2026"),
    ("fliki-review-2026", "Fliki Review 2026", "Fliki 评测 2026"),
    ("chatgpt-alternatives-2026", "Best ChatGPT Alternatives 2026", "2026 最佳 ChatGPT 替代品"),
    ("notion-alternatives-2026", "Best Notion AI Alternatives 2026", "2026 最佳 Notion AI 替代品"),
    ("jasper-alternatives-2026", "Best Jasper AI Alternatives 2026", "2026 最佳 Jasper AI 替代品"),
    ("grammarly-alternatives-2026", "Best Grammarly Alternatives 2026", "2026 最佳 Grammarly 替代品"),
]
for slug, en, zh in data:
    make(slug, en, False)
    make(slug, zh, True)
print("=== 12 张 OG 图生成完成 ===")
