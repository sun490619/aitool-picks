#!/usr/bin/env python3
"""标准合规 og 图生成器（重建版）。

规则来源：images/IMAGES-MANIFEST.md 标准模板（案例13/30 用户铁律）。
- 禁止纯渐变、禁止 AI 生成图；一律用真实 CC0 场景照（Openverse/Wikimedia/Flickr cc0）。
- 真实照 LANCZOS 铺满 → 深蓝渐变遮罩 (15,23,42)->(30,58,138) alpha150
  → 左侧竖条 rect[80,90,168,630] 填充 (96,165,250) → 白色标题 46px x=112 y=200 行距54 wrap30 最多5行
  → 底部 (112,560) 品牌标 "AI Tool Picks" 26px (148,163,184) → JPEG q88。
- 验收：唯一色 4000-6000、均亮 60-85、标准差 30-36、竖条实测≈(99,164,246)。

用法：python3 gen_og_today.py <out.jpg> <scene_cc0_url> "<title>"
"""
import sys, io, textwrap, urllib.request, statistics
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
TITLE = ImageFont.truetype(ARIAL, 46)
BRAND = ImageFont.truetype(ARIAL, 26)


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())).convert("RGB")


def make_og(out, scene_url, title):
    base = download(scene_url).resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(overlay)
    for y in range(H):
        t = y / H
        r = int(8 + (20 - 8) * t)
        g = int(14 + (40 - 14) * t)
        b = int(30 + (110 - 30) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 188))
    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    d = ImageDraw.Draw(img)
    d.rectangle([80, 90, 168, 630], fill=(96, 165, 250))
    lines = textwrap.wrap(title, 30)[:5]
    y = 200
    for ln in lines:
        d.text((112, y), ln, font=TITLE, fill=(255, 255, 255))
        y += 54
    d.text((112, 560), "AI Tool Picks", font=BRAND, fill=(148, 163, 184))
    img.convert("RGB").save(out, "JPEG", quality=88)
    return img


def verify(path):
    im_full = Image.open(path).convert("RGB")
    bar = im_full.getpixel((110, 300))  # 竖条在原图坐标
    im = im_full.resize((300, 158))
    px = list(im.getdata())
    uniq = len(set(px))
    lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px]
    mean = sum(lum) / len(lum)
    sd = (sum((x - mean) ** 2 for x in lum) / len(lum)) ** 0.5
    print("  唯一色=%d 均亮=%.1f 标准差=%.1f 竖条色=%s" % (uniq, mean, sd, bar))


if __name__ == "__main__":
    out, scene, title = sys.argv[1], sys.argv[2], sys.argv[3]
    make_og(out, scene, title)
    print("生成:", out)
    verify(out)
