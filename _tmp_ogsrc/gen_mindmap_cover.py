#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindMapAI 评测文专属封面（2026-07-30 重做）：
用户指出此前"泛泛头脑风暴照"与文章(用文字生成思维导图、AI 展开节点)无关。
改为：品牌深色渐变底 + 右侧"从 AI 中心节点辐射展开分支"的思维导图示意 +
左侧标题 + 左侧品牌竖条 + 底部 AI Tool Picks 标。
完全代码绘制（非 AI 生成图、无水印、无版权问题），且深色底保证白字对比达标。
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
OUT = os.path.join(ROOT, "images")
TMP = os.path.join(ROOT, "_tmp_ogsrc")


def font(sz, bold=True):
    for p in ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/DejaVuSans-Bold.ttf",
              "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def round_rect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def main():
    # 深色品牌渐变底
    img = Image.new("RGB", (W, H), (15, 23, 42))
    d = ImageDraw.Draw(img)
    top = (15, 23, 42)
    bot = (30, 58, 138)
    for y in range(H):
        t = y / H
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # 左侧品牌竖条（与标准模板一致）
    d.rectangle([80, 90, 88, 540], fill=(96, 165, 250))

    # ---- 右侧思维导图 ----
    cx, cy = 905, 315
    nodes = [
        (1085, 165, "Text In",  (96, 165, 250)),
        (1135, 315, "Topics",   (52, 211, 153)),
        (1085, 465, "Expand",   (167, 139, 250)),
        (775, 165,  "Outline",  (244, 114, 182)),
        (775, 465,  "Export",   (251, 191, 36)),
    ]
    # 先画分支连线
    for (nx, ny, _, col) in nodes:
        d.line([(cx, cy), (nx, ny)], fill=col, width=4)
    # 中心节点
    d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=(30, 58, 138),
              outline=(96, 165, 250), width=4)
    fcnt = font(40)
    d.text((cx, cy), "AI", font=fcnt, fill=(255, 255, 255), anchor="mm")
    # 外节点（圆角矩形 + 标签）
    fn = font(22)
    for (nx, ny, label, col) in nodes:
        bw, bh = 150, 46
        box = [nx - bw // 2, ny - bh // 2, nx + bw // 2, ny + bh // 2]
        round_rect(d, box, 12, (15, 23, 42))
        d.rectangle([box[0], box[1], box[0] + 5, box[3]], fill=col)  # 左色条
        d.text((nx, ny), label, font=fn, fill=(226, 232, 240), anchor="mm")

    # ---- 左侧标题 ----
    ft = font(52)
    d.text((112, 205), "MindMapAI", font=ft, fill=(255, 255, 255))
    d.text((112, 268), "Review 2026", font=ft, fill=(255, 255, 255))
    # 小标签：点题"从文字生成思维导图"
    fsub = font(22)
    d.text((114, 340), "Text in. Mind map out.", font=fsub, fill=(148, 163, 184))

    # 底部品牌标
    d.text((112, 560), "AI Tool Picks", font=font(26), fill=(148, 163, 184))

    out = os.path.join(OUT, "og-mindmapai-review-2026.jpg")
    img.save(out, "JPEG", quality=88)
    print("WROTE", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
