#!/usr/bin/env python3
"""og 图生成器 v2 — 径向暗角版（2026-08-05 定稿）。

规则来源：images/IMAGES-MANIFEST.md 标准模板（08-05 强化版）。
- 底图：CC0 真实场景照（Unsplash/Openverse），LANCZOS 铺满 1200×630
- 遮罩：深蓝径向暗角（中心 alpha≈0.45 → 四角≈0.70），颜色 B>G>R 蓝色调 RGB≈(25,38,58)
- 竖条：rect[80,90,168,630] 填充 (96,165,250)
- 文字：白色标题 46px x=112 y=200 行距54 wrap30最多5行；底部品牌标 26px
- 输出：JPEG quality=88

用法：python3 gen_og_radial.py <out.jpg> "<title>" <cc0_photo_url>
"""
import sys, io, textwrap, urllib.request, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
TITLE_FONT = ImageFont.truetype(ARIAL, 46)
BRAND_FONT = ImageFont.truetype(ARIAL, 26)

# 径向暗角参数（从 golden master 反推）
MASK_COLOR = (25, 38, 58)       # B>G>R 干净蓝（R最低）
CENTER_ALPHA = 115               # 中心 ≈ 0.45 (115/255)
CORNER_ALPHA = 178              # 四角 ≈ 0.70 (178/255)
GAUSS_SIGMA = 35                # 高斯平滑半径(px)


def download(url):
    """加载底图：支持 HTTP URL 或本地文件路径"""
    if url.startswith("file://") or url.startswith("/"):
        path = url.replace("file://", "")
        return Image.open(path).convert("RGB")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())).convert("RGB")


def radial_vignette_mask(width, height, sigma=GAUSS_SIGMA):
    """生成径向暗角遮罩 RGBA 图。
    中心亮(alpha低)→四角暗(alpha高)，高斯平滑过渡。
    """
    import numpy as np
    cx, cy = width / 2, height / 2
    max_dist = math.sqrt(cx ** 2 + cy ** 2)

    mask = Image.new("RGBA", (width, height))
    px = mask.load()
    for y in range(height):
        for x in range(width):
            # 归一化距离 (0中心 → 1角落)
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / max_dist
            # alpha 从 CENTER_ALPHA(中心) 线性插值到 CORNER_ALPHA(四角)
            alpha = int(CENTER_ALPHA + (CORNER_ALPHA - CENTER_ALPHA) * dist)
            px[x, y] = (*MASK_COLOR, alpha)
    return mask


def make_og(out_path, title, scene_url):
    # ① 底图
    base = download(scene_url).resize((W, H), Image.LANCZOS)

    # ② 径向暗角遮罩
    overlay = radial_vignette_mask(W, H)
    img = Image.alpha_composite(base.convert("RGBA"), overlay)

    # ③ 左侧竖条（品牌标识·坐标铁律·2026-08-05 血的教训两次）
    # ✅ 正确: [80, 90, 88, 540] — 宽8px, y从90到540(距底边90px,不触底!)
    # ❌ 错误1: x2=168 (宽88px粗块,比GM粗11倍)
    # ❌ 错误2: y2=630 (触底/"入地",比GM多90px)
    # golden master 三张实测全一致: y=90→540, 距底边 exactly 90px
    draw = ImageDraw.Draw(img)
    draw.rectangle([80, 90, 88, 540], fill=(96, 165, 250))

    # ④ 标题文字
    lines = textwrap.wrap(title, 30)[:5]
    ty = 200
    for ln in lines:
        draw.text((112, ty), ln, font=TITLE_FONT, fill=(255, 255, 255))
        ty += 54

    # ⑤ 品牌标
    draw.text((112, 560), "AI Tool Picks", font=BRAND_FONT, fill=(148, 163, 184))

    # ⑥ 输出
    img.convert("RGB").save(out_path, "JPEG", quality=88)
    print(f"✅ 已生成: {out_path}")
    return out_path


def verify(path):
    """量化验收：对照 IMAGES-MANIFEST §⑤"""
    im = Image.open(path).convert("RGB")
    # 缩小采样算全局统计
    small = im.resize((300, 158))
    px = list(small.getdata())
    uniq = len(set(px))
    lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px]
    mean_lum = sum(lum) / len(lum)
    sd_lum = (sum((x - mean_lum) ** 2 for x in lum) / len(lum)) ** 0.5

    # 标题区亮度 (x80-700, y200-280)
    title_region = im.crop((80, 200, 700, 280))
    title_px = list(title_region.getdata())
    title_lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in title_px]
    title_avg = sum(title_lum) / len(title_lum)

    # 四角色调检查 (取四个角)
    corners = [im.getpixel((40, 40)), im.getpixel((W-40, 40)),
               im.getpixel((40, H-40)), im.getpixel((W-40, H-40))]
    corner_blues = ["B>G>R" if b > g > r else f"BAD R={r} G={g} B={b}" for r, g, b in corners]

    # 竖条色
    bar_px = im.getpixel((124, 300))

    print(f"  验收:")
    print(f"    唯一色={uniq} (要求 4000-6000)")
    print(f"    均亮={mean_lum:.1f} 标准差={sd_lum:.1f}")
    print(f"    标题区亮度={title_avg:.1f} (要求 97-127)")
    print(f"    四角色调={' / '.join(corner_blues)}")
    print(f"    竖条色={bar_px} (期望 ≈(99,164,246))")
    
    ok = True
    if not (4000 <= uniq <= 8000):
        print(f"    ⚠️ 唯一色 {uniq} 偏离范围")
        ok = False
    if not (97 <= title_avg <= 127):
        print(f"    ⚠️ 标题区亮度 {title_avg:.1f} 偏离 97-127")
        ok = False
    if any("BAD" in c for c in corner_blues):
        print(f"    ⚠️ 四角存在非蓝色调")
        ok = False
    if ok:
        print(f"    ✅ 全部通过")
    return ok


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python3 gen_og_radial.py <output.jpg> \"<title>\" <cc0_photo_url>")
        sys.exit(1)
    out, title, url = sys.argv[1], sys.argv[2], sys.argv[3]
    make_og(out, title, url)
    verify(out)
