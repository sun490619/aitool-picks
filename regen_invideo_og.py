#!/usr/bin/env python3
"""重做 og-invideo-review-2026.jpg：用 golden master 结构，但调亮标题区(规则§⑤要求97-127)，四角保持≤95深蓝。"""
import math, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
base_path = "_tmp_ogsrc/bases/realistic_photo_of_a_video_edi_2026-08-04T20-14-21.png"
title = "InVideo Review 2026: An AI Video Generator With 5,000+ Templates"
out_path = "images/og-invideo-review-2026.jpg"

def find_font(size):
    for p in ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

base = Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS)

# 径向暗角遮罩：中心 alpha 低(标题区亮)，四角 alpha 高(深蓝)
cx, cy = W/2, H/2
maxd = math.hypot(cx, cy)
step = 2
mask = Image.new("L", (W, H), 0)
mp = mask.load()
for y in range(0, H, step):
    for x in range(0, W, step):
        d = math.hypot(x-cx, y-cy)/maxd
        a = 0.22 + d*(0.62-0.22)   # 中心0.22 四角0.62
        mp[x, y] = int(a*255)
mask = mask.resize((W, H))
overlay = Image.new("RGB", (W, H), (25, 38, 58))
base.paste(overlay, (0, 0), mask)

draw = ImageDraw.Draw(base)
# 竖条
draw.rectangle([80, 90, 88, 540], fill=(96, 165, 250))
# 标题
ft = find_font(46)
fb = find_font(26)
lines = textwrap.wrap(title, 30)[:5]
y = 200
for ln in lines:
    draw.text((112, y), ln, fill=(255, 255, 255), font=ft)
    y += 54
draw.text((112, 560), "AI Tool Picks", fill=(148, 163, 184), font=fb)

base.save(out_path, "JPEG", quality=88)
print("OK", out_path)

# 验收
def reg(box):
    c=base.crop(box); px=list(c.getdata()); n=len(px)
    return tuple(sum(p[i] for p in px)//n for i in range(3))
print("title区(80-700,200-280):", reg((80,200,700,280)))
print("四角1:", reg((30,30,50,50)), "四角2:", reg((1150,30,1170,50)),
      "四角3:", reg((30,580,50,600)), "四角4:", reg((1150,580,1170,600)))
print("竖条(80-88,200-280):", reg((80,200,88,280)))
px=list(base.getdata()); print("unique_colors:", len(set(px)))
