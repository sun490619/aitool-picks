#!/usr/bin/env python3
"""Composite the chosen candidate photos into branded OG/hero images (1200x630)."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
REV = os.path.join(ROOT, "_review")
OUT = os.path.join(ROOT, "images")

W, H = 1200, 630

def load_font(size, bold=True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

def cover(img, tw, th):
    """Resize-crop img to cover (tw, th) centered."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))

def gen(src, title, out_name):
    base = cover(Image.open(src).convert("RGB"), W, H)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # Left-to-right dark brand scrim for legibility
    for x in range(W):
        a = int(210 * (1 - x / W) + 70)
        d.line([(x, 0), (x, H)], fill=(13, 17, 23, a))
    # Left accent bar (brand #63a5fa -> (99,165,250))
    d.rectangle([0, 0, 12, H], fill=(99, 165, 250, 255))
    base = Image.alpha_composite(base.convert("RGBA"), ov)

    dd = ImageDraw.Draw(base)
    # AI Tool Picks label (bottom-left)
    lbl = load_font(30, bold=True)
    dd.text((44, H - 70), "AI Tool Picks", font=lbl, fill=(255, 255, 255, 255))
    # Title (left, vertically centered)
    tf = load_font(58, bold=True)
    # wrap title
    lines, cur = [], ""
    for w_ in title.split():
        if dd.textlength((cur + " " + w_).strip(), font=tf) > W - 120:
            lines.append(cur.strip()); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    if cur:
        lines.append(cur.strip())
    lines = lines[:3]
    y = H // 2 - (len(lines) * 70) // 2
    for ln in lines:
        dd.text((44, y), ln, font=tf, fill=(255, 255, 255, 255))
        y += 70
    base.convert("RGB").save(os.path.join(OUT, out_name), quality=92)
    print("wrote", out_name)

gen(os.path.join(REV, "nw-cand-2.jpg"), "NeuronWriter Review 2026", "og-neuronwriter-review-2026.jpg")
gen(os.path.join(REV, "cb-cand-1.jpg"), "Coursebox.ai Review 2026", "og-coursebox-review-2026.jpg")
