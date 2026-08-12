#!/usr/bin/env python3
"""
aitool-picks 发布前强制门禁（pre-publish gate）。

把反复犯规的"软约束"编译成机器强制：
  ① 配图铁律（图库优先 / easyocr / 禁 tesseract / og=hero）
  ② 文章结构铁律（面包屑 / hero / 单一 article-meta / related-articles 唯一）
  ③ 日期 + JSON-LD 铁律（datePublished 必填且 = <time datetime> /
     dateModified >= datePublished / 数值字段为数字禁引号）
  ④ 列表页排序铁律（置顶第1 + 其余日期倒序）
  ⑤ 字数铁律（2026-08-13：正文 ≥1500 硬性下限，EN 计 word / ZH 计中文字符；
     新增文章 <1500 FAIL，修改存量 <1500 WARN；>1800 仅 WARN 不卡）

任何一次 push，若改动涉及【新增图】或【新增/修改 posts 文章】，
违规即拒绝推送。只检查本次改动的文件，不误伤存量已上线文章。

自检：python3 pre_publish_check.py --file posts/xxx.html
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

NUMERIC_FIELDS = r"(?:ratingValue|bestRating|worstRating|ratingCount|reviewCount|price|wordCount)"


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


def added_files():
    """返回本次【新增】文件（用于结构门禁仅卡新文章）。"""
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
        ["git", "diff", "--diff-filter=A", "--name-only", base, "HEAD"]
    ).decode().split()
    return [f for f in out if f.strip()]


def new_images(files):
    imgs = []
    for f in files:
        if re.match(r"^images/og-.*\.(jpg|png)$", f) or re.match(r"^images/.*hero.*\.(jpg|png)$", f):
            imgs.append(f)
    return imgs


def posts_referencing(files):
    return [f for f in files if re.match(r"^posts/.*\.html$", f)]


def og_image_of(post_path):
    try:
        with open(os.path.join(REPO, post_path)) as f:
            html = f.read()
    except Exception:
        return None, None
    m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    og = m.group(1) if m else None
    hm = re.search(r'<img[^>]+class="[^"]*hero[^"]*"[^>]+src="([^"]+)"', html)
    if not hm:
        hm = re.search(r'<img[^>]+src="([^"]+)"[^>]+class="[^"]*hero[^"]*"', html)
    hero = hm.group(1) if hm else None
    return og, hero


def normalize(src):
    if not src:
        return None
    s = src.split("?")[0]
    s = re.sub(r"^/?images/", "", s)  # 同时处理 /images/ 与 images/ 两种引用
    return s.lstrip("/")


def lib_has_category(cat):
    mapped = CATEGORY_MAP.get(cat)
    if not mapped:
        return False
    for f in os.listdir(LIB):
        if f.startswith(mapped):
            return True
    return False


# ---------------------------------------------------------------------------
# ② 文章结构门禁（对应"格式乱"根因）
# ---------------------------------------------------------------------------
def check_post_structure(rel):
    errs = []
    path = os.path.join(REPO, rel)
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return errs
    name = os.path.basename(rel)
    if "tool-selector" in name:
        return errs  # 工具页豁免结构组件要求

    if "article-breadcrumb" not in h:
        errs.append(f"[FAIL] {rel}: 缺面包屑 article-breadcrumb（§13.12B 强制组件）")
    if 'class="post-hero"' not in h:
        errs.append(f"[FAIL] {rel}: 缺 hero 图 post-hero（每篇必选，固定顶部）")
    meta = len(re.findall(r'class="article-meta"', h))
    if meta > 1:
        errs.append(f"[FAIL] {rel}: article-meta 重复({meta}个)，必须唯一")
    if 'class="related-articles"' not in h:
        errs.append(f"[FAIL] {rel}: 缺 related-articles 相关文章区块（§13.12B）")
    # ---- §八 edesk 视觉范本：组件级样式铁律（仅卡新增文章）----
    if '<script src="/scripts.js"' not in h:
        errs.append(f"[FAIL] {rel}: 缺 <script src=\"/scripts.js\">（汉堡菜单必须可用，§八）")
    if re.search(r'class="cta-box"[^>]*style=', h):
        errs.append(f"[FAIL] {rel}: cta-box 含 inline style（必须改用共享 .cta-box 灰底样式，§八）")
    if 'class="rating-bars"' in h and 'class="rating-pct"' not in h:
        errs.append(f"[FAIL] {rel}: 含 rating-bars 但缺 rating-pct 显式百分比（§八）")
    return errs


def check_post_dates(rel):
    """③ 日期 + JSON-LD 门禁：对所有改动文章生效（含仅改日期的存量），
    确保 datePublished 必填、= <time datetime>、dateModified≥datePublished、数值字段为数字。"""
    errs = []
    path = os.path.join(REPO, rel)
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return errs
    dp = re.search(r'"datePublished"\s*:\s*"([^"]*)"', h)
    td = re.search(r'<time[^>]*datetime="([^"]+)"', h)
    dm = re.search(r'"dateModified"\s*:\s*"([^"]*)"', h)
    if not dp or not dp.group(1):
        errs.append(f"[FAIL] {rel}: JSON-LD 缺 datePublished 或为空白")
    else:
        if td and td.group(1) and dp.group(1) != td.group(1):
            errs.append(f"[FAIL] {rel}: datePublished({dp.group(1)}) != <time datetime>({td.group(1)})")
        if dm and dm.group(1) and dp.group(1) and dm.group(1) < dp.group(1):
            errs.append(f"[FAIL] {rel}: dateModified({dm.group(1)}) 早于 datePublished({dp.group(1)})")
    for m in re.finditer(r'"\s*' + NUMERIC_FIELDS + r'\s*"\s*:\s*"(\d+\.?\d*)"', h):
        errs.append(f"[FAIL] {rel}: JSON-LD 数值字段 {m.group(1)} 被引号包裹(应为数字)")
    return errs


# ---------------------------------------------------------------------------
# ⑤ 字数铁律门禁（2026-08-13，对应"薄度 / 像诈骗站"根因）
#    规则：每篇正文 ≥1500（EN word / ZH 中文字符），硬性下限写死。
#    新增文章 <1500 → FAIL；修改存量 <1500 → WARN（不阻断）。>1800 仅 WARN。
# ---------------------------------------------------------------------------
MIN_WORDS = 1500
TARGET_MAX = 1800

def check_word_count(rel, is_new):
    errs, warns = [], []
    path = os.path.join(REPO, rel)
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return errs, warns
    if "tool-selector" in os.path.basename(rel):
        return errs, warns  # 工具页豁免字数要求
    is_zh = bool(re.search(r'<html[^>]*lang="zh"', h, re.I))
    body = re.sub(r'<script[\s\S]*?</script>', ' ', h, flags=re.I)
    body = re.sub(r'<style[\s\S]*?</style>', ' ', body, flags=re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    if is_zh:
        cnt = len(re.findall(r'[一-鿿]', body))
        unit = "中文字"
    else:
        cnt = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-]*", body))
        unit = "词"
    if cnt < MIN_WORDS:
        msg = f"{rel}: 正文 {cnt}{unit} < 硬性下限 {MIN_WORDS}（§13.13 / §九 字数铁律）"
        if is_new:
            errs.append(f"[FAIL] {msg} → 新文章不准 push，须扩写到 ≥{MIN_WORDS}{unit}")
        else:
            warns.append(f"[WARN] {msg} → 存量薄文整改 backlog，建议扩写（不阻断本次 push）")
    elif cnt > TARGET_MAX:
        warns.append(
            f"[WARN] {rel}: 正文 {cnt}{unit} > {TARGET_MAX}，建议精简到 {TARGET_MAX} 内（上限不卡，可多于）"
        )
    return errs, warns


# ---------------------------------------------------------------------------
# ④ 列表页排序门禁（对应"文章排序乱"根因）
#    规则：置顶文章(data-pinned="1")必须排第1位；其余卡片按日期倒序
#    （最新在上）。任何一次改动涉及首页/分类页都强制校验，杜绝"新文埋底"。
# ---------------------------------------------------------------------------
def check_listing_order(rel):
    errs = []
    path = os.path.join(REPO, rel)
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return errs
    if "post-card" not in h:
        return errs  # 非列表页跳过
    cards = re.findall(r'<article class="card post-card".*?</article>', h, re.S)
    if len(cards) < 2:
        return errs
    info = []
    for c in cards:
        pinned = 'data-pinned="1"' in c
        # 以 data-date 为准（每次重排都更新）；无则回退 <time datetime>
        tm = re.search(r'data-date="([^"]+)"', c) or re.search(r'<time[^>]*datetime="([^"]+)"', c)
        d = tm.group(1) if tm else "0000-00-00"
        info.append((pinned, d))
    if any(p for p, _ in info) and not info[0][0]:
        errs.append(f"[FAIL] {rel}: 置顶文章(data-pinned)必须排在第1位")
    seq = [d for p, d in info if not p]
    for i in range(1, len(seq)):
        if seq[i] > seq[i - 1]:
            errs.append(
                f"[FAIL] {rel}: 列表未按日期倒序（第{i+1}张比前一张更新，违反'最新在上'规则）"
            )
            break
    return errs


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--file":
        files = [sys.argv[2]]
    else:
        files = changed_files()

    prov = load_prov().get("images", {})
    imgs_new = new_images(files)
    posts = posts_referencing(files)

    # ---- ② 文章结构门禁：仅对【新增】文章生效（存量仅改日期的文章不卡，
    #        避免日期修复被"尚未铺开标准结构"的存量文章阻挡；存量结构统一在
    #        后续批量铺开任务中逐篇整改）----
    added = set(added_files())
    struct_errors = []
    for p in posts:
        if p in added:
            struct_errors += check_post_structure(p)
    errors = list(struct_errors)
    warnings = []

    # ---- ③ 日期/JSON-LD 门禁：对所有改动文章生效（含仅改日期的存量）----
    for p in posts:
        errors += check_post_dates(p)

    # ---- ⑤ 字数铁律门禁：新增文章硬卡(<1500 FAIL)，修改存量仅 WARN ----
    for p in posts:
        e, w = check_word_count(p, p in added)
        errors += e
        warnings += w

    # ---- ④ 列表页排序门禁 ----
    for f in files:
        if f == "index.html" or f == "index-zh.html" or re.match(r"^category/.*\.html$", f):
            errors += check_listing_order(f)

    # ---- ① 配图门禁（保留既有逻辑）----
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
        try:
            with open(os.path.join(REPO, p)) as f:
                cm = re.search(r'data-category="([^"]+)"', f.read())
                if cm:
                    post_cats[og_n or hero_n] = cm.group(1)
        except Exception:
            pass

    for img in sorted(need_check):
        rec = prov.get(img)
        if rec is None:
            if img in [normalize(i) for i in imgs_new]:
                errors.append(f"[FAIL] 新增图 {img} 在 image_provenance.json 无登记记录 → 必须先登记再 push")
            else:
                warnings.append(f"[WARN] 图 {img} 无溯源记录（历史图，不阻断；建议补登）")
            continue
        if rec.get("status") == "legacy_violation":
            warnings.append(f"[WARN] {img} 是已知历史违规(legacy_violation)，不阻断，但待补正")
            continue
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

    for img, cat in post_cats.items():
        rec = prov.get(img)
        if rec and rec.get("source") == "openverse" and lib_has_category(cat):
            errors.append(
                f"[FAIL] {img}: 文章归 '{cat}' 类，备用图片库 {CATEGORY_MAP.get(cat)} 有可用图，"
                f"必须先用图库真实照（除非 library_reason 充分说明不贴题）"
            )

    print("=" * 60)
    print("aitool-picks 发布前门禁（配图 + 结构 + 日期/JSON-LD + 字数）")
    print(f"改动文件 {len(files)} 个 | 需校验图 {len(need_check)} 张 | 文章 {len(posts)} 篇")
    print("=" * 60)
    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    if errors:
        print("\n❌ 门禁未通过：存在规则违规，推送被拒绝。请先按上面提示修正。")
        print("   这是机器强制，不是'再注意点'——不修正就无法 push 上线。")
        sys.exit(1)
    print("\n✅ 门禁通过：本次改动涉及的配图 / 结构 / 日期均符合铁律，可以推送。")
    sys.exit(0)


if __name__ == "__main__":
    main()
