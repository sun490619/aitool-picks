#!/usr/bin/env python3
"""生成 7 个分类页独立 og:image（1200x630，与全站 og 风格一致）。
分类页原本复用同名文章的 og 图 -> 跨内容重复，违反配图铁律。
现各分类一张独立图（EN/ZH 同分类共用一张图，属 lang-pair，合规）。
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = "images"

# (文件名, 主标题, 副标题/英文)
CATS = [
    ("og-category-video.jpg",       "Best AI Video Tools",       "Generate & edit video with AI"),
    ("og-category-seo.jpg",         "Best AI SEO Tools",         "Rank higher with AI workflows"),
    ("og-category-writing.jpg",     "Best AI Writing Tools",     "Write faster, edit smarter"),
    ("og-category-coding.jpg",      "Best AI Coding Tools",      "Ship code with an AI pair"),
    ("og-category-productivity.jpg","Best AI Productivity Tools","Reclaim your focused hours"),
    ("og-category-audio.jpg",       "Best AI Music & Audio",     "Voice, music & sound with AI"),
    ("og-category-image.jpg",       "Best AI Image Tools",       "Create & upscale images with AI"),
]

def font(sz):
    for p in ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Arial.ttf",
              "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except: pass
    return ImageFont.load_default()

def grad(draw):
    top, bot = (13, 17, 38), (27, 35, 74)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i]-top[i])*t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

os.makedirs(OUT, exist_ok=True)
for fname, title, sub in CATS:
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    grad(d)
    # accent bar
    d.rectangle([90, 250, 150, 380], fill=(99, 102, 241))
    # wordmark
    d.text((90, 150), "aitool-picks", font=font(34), fill=(148, 163, 184))
    # title
    d.text((90, 250), title, font=font(64), fill=(255, 255, 255))
    # subtitle
    d.text((90, 360), sub, font=font(34), fill=(165, 180, 252))
    # footer tag
    d.text((90, 540), "Honest, hands-on AI tool reviews", font=font(26), fill=(100, 116, 139))
    img.save(os.path.join(OUT, fname), "JPEG", quality=92)
    print("wrote", os.path.join(OUT, fname))
print("DONE", len(CATS), "category og images")
