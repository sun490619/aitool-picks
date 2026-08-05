#!/usr/bin/env python3
"""
Golden Master og 图合成脚本（2026-08-05 修正版 · 严格按 IMAGES-MANIFEST §标准模板）
输入：一张干净底图（真实照片 / 无水印AI图，铺满即可）
输出：1200x630 og 社交图，套品牌模板。

模板构成（来自 manifest ①-④）：
  ① 底图 LANCZOS 铺满 1200x630（整张画布都有照片，绝不只贴下半部）
  ② 品牌遮罩 = 深蓝径向暗角：中心 alpha≈0.45 → 四角≈0.70，颜色 B>G>R (25,38,58)
  ③ 左侧竖条 rect[80,90, 88,540] 8px 细蓝线，填充渐变蓝 (96,165,250)
  ④ 白色标题 46px 从 y=200 起、行距54、x=112、wrap30 最多5行；
     底部(112,560) 品牌标 "AI Tool Picks" 26px (148,163,184)；JPEG q88
"""
import sys, math, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

def find_font(size, bold=True):
    candidates = [
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Helvetica.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def make_og(base_path, title, out_path):
    base = Image.open(base_path).convert("RGB")
    base = base.resize((W, H), Image.LANCZOS)  # ① 铺满整张画布

    # ② 径向暗角蓝遮罩
    mask = Image.new("L", (W, H), 0)
    cx, cy = W / 2.0, H / 2.0
    maxd = math.hypot(cx, cy)
    mp = mask.load()
    step = 1
    for y in range(0, H, step):
        for x in range(0, W, step):
            d = math.hypot(x - cx, y - cy) / maxd  # 0 center -> 1 corner
            a = int((0.45 + d * (0.70 - 0.45)) * 255)
            mp[x, y] = a
    overlay = Image.new("RGB", (W, H), (25, 38, 58))  # 蓝色调 B>G>R
    img = Image.composite(overlay, base, mask)  # 中心=base(亮) 四角=overlay(暗蓝)

    draw = ImageDraw.Draw(img)

    # ③ 左侧竖条 8px (x:80..88, y:90..540)
    draw.rectangle([80, 90, 88, 540], fill=(96, 165, 250))

    # ④ 标题
    font_title = find_font(46)
    font_brand = find_font(26)
    import textwrap
    lines = textwrap.wrap(title, 30)[:5]
    y = 200
    for ln in lines:
        draw.text((112, y), ln, fill=(255, 255, 255), font=font_title)
        y += 54
    # 品牌标
    draw.text((112, 560), "AI Tool Picks", fill=(148, 163, 184), font=font_brand)

    img.save(out_path, "JPEG", quality=88)
    return out_path

if __name__ == "__main__":
    base_path, title, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    make_og(base_path, title, out_path)
    print(f"OK {out_path}")
