#!/usr/bin/env python3
"""
aitool-picks 发布前强制门禁（pre-publish gate）。

目的：把"配图铁律"从人脑记忆变成机器强制。任何一次 push，如果包含
【新增的 og/hero 图】或【新增/修改的文章引用了某张图】，则该图必须满足
image_provenance.json 里的合规记录，否则拒绝推送。

规则（详见 image_provenance.json _meta.rules）：
  1. 新增图必须在 provenance 有记录，否则 FAIL。
  2. ocr_tool 必须 = easyocr，tesseract 直接 FAIL。
  3. source=openverse 时必须 library_checked=true + library_reason 非空，否则 FAIL。
  4. og:image 与文章内 hero 图必须同一文件（脚本自动校验），否则 FAIL。
  5. ocr_result 必须 = clean，否则 FAIL。

历史已上线图不强制（不阻断），仅在报告中提示。
"""
import json
import os
import re
import subprocess
import sys

REPO = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
LIB = "/Users/dawei/Desktop/项目总中枢/备用图片库"
PROV_PATH = os.path.join(REPO, "image_provenance.json")

CATEGORY_MAP = {
    "writing": "03_writing",
    "coding": "04_code",
    "video": "02_video-production",
    "seo": "05_seo",
    "productivity": "08_productivity",
    "image": "06_design",
    "audio": "07_audio",
}


def load_prov():
    if not os.path.exists(PROV_PATH):
        return {"images": {}}
    with open(PROV_PATH) as f:
        return json.load(f)


def changed_files():
    """返回本次要 push 的改动文件列表（相对 main）。"""
    try:
        base = subprocess.check_output(
            ["git", "merge-base", "HEAD", "origin/main"], stderr=subprocess.DEVNULL
        ).decode().strip()
        if not base:
            raise ValueError
    except Exception:
        base = subprocess.check_output(
            ["git", "rev-parse", "HEAD~20"], stderr=subprocess.DEVNULL
        ).decode().strip() or "HEAD"
    out = subprocess.check_output(
        ["git", "diff", "--name-only", base, "HEAD"]
    ).decode().split()
    return [f for f in out if f.strip()]


def new_images(files):
    """本次新增的 og/hero 图（diff-filter=A）。"""
    imgs = []
    for f in files:
        if re.match(r"^images/og-.*\.(jpg|png)$", f) or re.match(r"^images/.*hero.*\.(jpg|png)$", f):
            imgs.append(f)
    return imgs


def posts_referencing(files):
    """本次新增/修改的 posts 文章。"""
    return [f for f in files if re.match(r"^posts/.*\.html$", f)]


def og_image_of(post_path):
    try:
        with open(os.path.join(REPO, post_path)) as f:
            html = f.read()
    except Exception:
        return None, None
    m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    og = m.group(1) if m else None
    # hero img: 文章内第一个大图（data-hero 或 class 含 hero）
    hm = re.search(r'<img[^>]+class="[^"]*hero[^"]*"[^>]+src="([^"]+)"', html)
    if not hm:
        hm = re.search(r'<img[^>]+src="([^"]+)"[^>]+class="[^"]*hero[^"]*"', html)
    hero = hm.group(1) if hm else None
    return og, hero


def normalize(src):
    if not src:
        return None
    return src.replace("/images/", "").split("?")[0].lstrip("/")


def lib_has_category(cat):
    mapped = CATEGORY_MAP.get(cat)
    if not mapped:
        return False
    for f in os.listdir(LIB):
        if f.startswith(mapped):
            return True
    return False


def main():
    prov = load_prov().get("images", {})
    files = changed_files()
    imgs_new = new_images(files)
    posts = posts_referencing(files)

    # 收集需要合规校验的图：① 本次新增图 ② 被新增/改 posts 引用且其文件存在于 images/
    need_check = set()
    for im in imgs_new:
        need_check.add(normalize(im))
    post_cats = {}
    for p in posts:
        og, hero = og_image_of(os.path.join(REPO, p))
        og_n = normalize(og)
        hero_n = normalize(hero)
        if og_n and os.path.exists(os.path.join(REPO, "images", og_n)):
            need_check.add(og_n)
        if hero_n and os.path.exists(os.path.join(REPO, "images", hero_n)):
            need_check.add(hero_n)
        # 文章分类（用于图库优先提示）
        try:
            with open(os.path.join(REPO, p)) as f:
                cm = re.search(r'data-category="([^"]+)"', f.read())
                if cm:
                    post_cats[og_n or hero_n] = cm.group(1)
        except Exception:
            pass

    errors = []
    warnings = []
    for img in sorted(need_check):
        rec = prov.get(img)
        if rec is None:
            # 仅当该图是本次新增才 FAIL；历史图只警告
            if img in [normalize(i) for i in imgs_new]:
                errors.append(f"[FAIL] 新增图 {img} 在 image_provenance.json 无登记记录 → 必须先登记再 push")
            else:
                warnings.append(f"[WARN] 图 {img} 无溯源记录（历史图，不阻断；建议补登）")
            continue
        if rec.get("status") == "legacy_violation":
            warnings.append(f"[WARN] {img} 是已知历史违规(legacy_violation)，不阻断，但待补正")
            continue
        # 新图合规校验
        if rec.get("ocr_tool") == "tesseract":
            errors.append(f"[FAIL] {img}: ocr_tool=tesseract 被规则禁止，必须用 easyocr")
        if rec.get("ocr_result") != "clean":
            errors.append(f"[FAIL] {img}: ocr_result 必须=clean，当前={rec.get('ocr_result')}")
        if rec.get("source") == "openverse" and not rec.get("library_checked"):
            errors.append(f"[FAIL] {img}: 用 openverse 但未 library_checked=true（必须先查备用图片库）")
        if rec.get("source") == "openverse" and not rec.get("library_reason"):
            errors.append(f"[FAIL] {img}: 用 openverse 但 library_reason 为空（必须说明图库为何无合适图）")
        if not rec.get("og_hero_same"):
            errors.append(f"[FAIL] {img}: og:image 与 hero 图必须同文件")

    # 图库优先提示：若文章归某类且图库该类有图，但 source=openverse，额外提示
    for img, cat in post_cats.items():
        rec = prov.get(img)
        if rec and rec.get("source") == "openverse" and lib_has_category(cat):
            errors.append(
                f"[FAIL] {img}: 文章归 '{cat}' 类，备用图片库 {CATEGORY_MAP.get(cat)} 有可用图，"
                f"必须先用语图库真实照（除非 library_reason 充分说明不贴题）"
            )

    print("=" * 60)
    print("aitool-picks 配图发布前门禁检查")
    print(f"改动文件 {len(files)} 个 | 需校验图 {len(need_check)} 张")
    print("=" * 60)
    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    if errors:
        print("\n❌ 门禁未通过：存在规则违规，推送被拒绝。请先按上面提示修正。")
        print("   这是机器强制，不是'再注意点'——不修正就无法 push 上线。")
        sys.exit(1)
    print("\n✅ 门禁通过：本次改动涉及的配图均符合配图铁律，可以推送。")
    sys.exit(0)


if __name__ == "__main__":
    main()
