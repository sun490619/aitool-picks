#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按 2026-07-29 已确认的标准模板（commit 1a02648 / gen_og_compliant.py）
只为今天两篇文章重做 og 封面：真实 CC0 场景照 + 品牌叠加层。
其他图片一律不动。
"""
import os, json, textwrap, urllib.request, urllib.parse
import PIL.Image as Image, PIL.ImageDraw as ImageDraw, PIL.ImageFont as ImageFont

W, H = 1200, 630
ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
OUT = os.path.join(ROOT, "images")
TMP = os.path.join(ROOT, "_tmp_ogsrc")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# 今天两篇：slug -> (标题, Openverse 搜索词候选)
JOBS = {
    "taskade-review-2026": (
        "Taskade Review 2026",
        ["team collaboration task board", "project planning workspace",
         "team meeting laptop planning", "office teamwork desk"],
    ),
    "mindmapai-review-2026": (
        "MindMapAI Review 2026",
        ["mind map brainstorming sticky notes", "whiteboard brainstorming diagram",
         "sticky notes planning wall", "notebook diagram planning"],
    ),
}


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


def variance(path):
    """颜色丰富度：真实照片通常 >3000，AI 渐变 <1500。"""
    import numpy as np
    im = Image.open(path).convert("RGB")
    a = np.array(im)
    samp = a[::8, ::8].reshape(-1, 3)
    return len(set(map(tuple, samp.tolist())))


def fetch_cc0(slug, queries):
    """从 Openverse 取真实 CC0 场景照，返回 (本地临时路径, 来源URL, 授权)。"""
    for q in queries:
        api = ("https://api.openverse.org/v1/images/?q=%s&license=cc0"
               "&page_size=20&mature=false" % urllib.parse.quote(q))
        try:
            req = urllib.request.Request(api, headers=UA)
            data = json.load(urllib.request.urlopen(req, timeout=30))
        except Exception as e:
            print("  API 失败 [%s]: %s" % (q, e))
            continue
        for r in data.get("results", []):
            url = r.get("url")
            if not url:
                continue
            dst = os.path.join(TMP, "src_%s.jpg" % slug)
            try:
                req = urllib.request.Request(url, headers=UA)
                raw = urllib.request.urlopen(req, timeout=40).read()
                with open(dst, "wb") as f:
                    f.write(raw)
                im = Image.open(dst)
                if im.width < 900 or im.height < 500:
                    continue
                im.convert("RGB").save(dst, "JPEG", quality=95)
                if variance(dst) < 3000:      # 必须是真实照片
                    continue
                print("  选中 [%s] %s (%dx%d)" % (q, url[:70], im.width, im.height))
                return dst, url, r.get("license", "cc0")
            except Exception:
                continue
    return None, None, None


def gen(src_jpg, title, out_name):
    """完全沿用 2026-07-29 已确认模板。"""
    photo = Image.open(src_jpg).convert("RGB")
    photo = photo.resize((W, H), Image.LANCZOS)
    base = photo.copy().convert("RGBA")

    # 半透明深色渐变遮罩（让文字可读，同时保留真实场景图）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    top = (15, 23, 42)      # 深蓝
    bot = (30, 58, 138)     # 中蓝
    for y in range(H):
        t = y / H
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        od.line([(0, y), (W, y)], fill=(r, g, b, 150))  # alpha 150 ≈ 59%

    img = Image.alpha_composite(base, overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # 左侧品牌强调竖条
    d.rectangle([80, 90, 88, 540], fill=(96, 165, 250))

    # 标题（白色粗体，自动换行）
    f = font(46)
    lines = textwrap.wrap(title, 30)[:5]
    y = 200
    for ln in lines:
        d.text((112, y), ln, font=f, fill=(255, 255, 255))
        y += 54

    # 品牌标
    d.text((112, 560), "AI Tool Picks", font=font(26), fill=(148, 163, 184))

    out = os.path.join(OUT, out_name)
    img.save(out, "JPEG", quality=88)
    print("  WROTE", out, os.path.getsize(out), "bytes")
    return out


def main():
    os.makedirs(TMP, exist_ok=True)
    records = []
    for slug, (title, queries) in JOBS.items():
        print("===", slug)
        src, url, lic = fetch_cc0(slug, queries)
        if not src:
            print("  !! 取图失败，跳过（不写坏图）")
            continue
        out = gen(src, title, "og-%s.jpg" % slug)
        records.append((os.path.basename(out), title, url, lic))
    print("\n=== 授权留痕（写入 IMAGES-MANIFEST） ===")
    for r in records:
        print(" |", " | ".join(str(x) for x in r))
    with open(os.path.join(TMP, "today_records.json"), "w") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
