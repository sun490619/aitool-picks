#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindMapAI 评测文封面 v3（2026-07-31）：
用户要求"真实照片风格 + 深色背景 + 思维导图相关"。
方案：真实思维导图照片(Wikimedia CC BY-SA) -> 灰度 -> 反相(白底变黑底、线条变浅)
-> 轻量深蓝品牌遮罩(alpha110, 既上蓝调又保留线条) -> 左侧品牌竖条 + 标题 + AI Tool Picks 标。
真实照片、深色底、主题贴合、无竞品水印。
"""
import os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import gen_og_today as G
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1200, 630
ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
OUT = os.path.join(ROOT, "images")
UA = {"User-Agent": "aitool-picks-image-bot/1.0 (contact: admin@aitool-picks.com)"}
SRC_URL = "https://upload.wikimedia.org/wikipedia/commons/9/97/A_Mind_Map_on_ICT_and_Pedagogy.jpg"


def font(sz):
    for p in ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/DejaVuSans-Bold.ttf",
              "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    raw = urllib.request.urlopen(urllib.request.Request(SRC_URL, headers=UA), timeout=40).read()
    photo = Image.open(__import__("io").BytesIO(raw)).convert("L")
    photo = ImageOps.invert(photo).resize((W, H), Image.LANCZOS)
    base = photo.convert("RGBA")

    # 轻量深蓝渐变遮罩（保留反相后的线条可见度）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    top, bot = (15, 23, 42), (30, 58, 138)
    for y in range(H):
        t = y / H
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        od.line([(0, y), (W, y)], fill=(r, g, b, 110))

    img = Image.alpha_composite(base, overlay).convert("RGB")
    d = ImageDraw.Draw(img)
    d.rectangle([80, 90, 88, 540], fill=(96, 165, 250))  # 左侧品牌竖条
    f = font(46)
    import textwrap
    for i, ln in enumerate(textwrap.wrap("MindMapAI Review 2026", 30)[:5]):
        d.text((112, 200 + i * 54), ln, font=f, fill=(255, 255, 255))
    d.text((112, 560), "AI Tool Picks", font=font(26), fill=(148, 163, 184))

    out = os.path.join(OUT, "og-mindmapai-review-2026.jpg")
    img.save(out, "JPEG", quality=88)
    print("WROTE", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
