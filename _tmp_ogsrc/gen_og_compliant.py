import PIL.Image as Image, PIL.ImageDraw as ImageDraw, PIL.ImageFont as ImageFont
import textwrap, os

W, H = 1200, 630
OUT = "/Users/dawei/CodeBuddy/aitool-picks/images"

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

def gen(src_jpg, title, out_name):
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
    print("WROTE", out, os.path.getsize(out), "bytes")

gen("/Users/dawei/CodeBuddy/aitool-picks/_tmp_ogsrc/aff.jpg",
    "Best AI Tools for Affiliate Marketers 2026",
    "og-best-ai-tools-for-affiliate-marketers-2026.jpg")
gen("/Users/dawei/CodeBuddy/aitool-picks/_tmp_ogsrc/solo.jpg",
    "Best AI Tools for Solopreneurs 2026",
    "og-best-ai-tools-for-solopreneurs-2026.jpg")
print("OG-COMPLIANT-DONE")
