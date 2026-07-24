#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

IMG = "/Users/dawei/CodeBuddy/aitool-picks/images"
os.makedirs(IMG, exist_ok=True)

def vgrad(w, h, top, bot):
    base = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = y / h
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    return base

def fit_font(size):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
               "/System/Library/Fonts/HelveticaNeue.ttc",
               "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def gen(fname, title, accent, cat):
    W, H = 1200, 630
    img = vgrad(W, H, (17, 24, 39), (30, 41, 59))
    d = ImageDraw.Draw(img)
    d.rectangle([80, 250, 140, 380], fill=accent)
    fcat = fit_font(34)
    d.text((160, 255), cat, font=fcat, fill=(148, 163, 184))
    ftitle = fit_font(58)
    words = title.split()
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) > 22:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    y = 300
    for ln in lines[:3]:
        d.text((160, y), ln, font=ftitle, fill=(255, 255, 255))
        y += 66
    fd = fit_font(30)
    d.text((160, 560), "AI Tool Picks - Independent Review", font=fd, fill=(100, 116, 139))
    out = os.path.join(IMG, fname)
    img.save(out, "JPEG", quality=85)
    print("wrote", out, os.path.getsize(out), "bytes")

gen("og-synthesia-review-2026.jpg", "Synthesia Review 2026", (236, 72, 153), "AI VIDEO")
gen("og-make-com-review-2026.jpg", "Make.com Review 2026", (59, 130, 246), "AUTOMATION")
gen("og-getgenie-review-2026.jpg", "GetGenie Review 2026", (16, 185, 129), "AI WRITING")
gen("og-vidiq-review-2026.jpg", "VidIQ Review 2026", (255, 0, 0), "YOUTUBE")
print("done")
