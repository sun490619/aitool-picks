#!/usr/bin/env python3
"""
批量修复 5 类扫描出的真问题：C1(<p><p>/</p></p> 嵌套破损) + C4(disclosure 在 article 外/重复)。
C2/C3/C5 已确认无误报或已清零，不在此处理。

策略：
  C1: 将连续的 <p><p> 压成 <p>，</p></p> 压成 </p>。
      （HTML 解析器本就会自动闭合前一个 <p>，这里只是清掉冗余开闭标签，使源码干净、门禁通过）
  C4: 将 article 外的 disclosure-banner/affiliate-note 移到 article 内合适位置；
      若文末 disclosure 重复（>1 次），保留顶部那个、删除 article 外/文末多余副本。

用法：
  python3 scripts/fix_5cat_batch.py --dry      # 只打印将改的文件
  python3 scripts/fix_5cat_batch.py             # 实际修改
"""
import re
import sys
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = sorted(REPO.rglob("posts/*.html"))

DRY = "--dry" in sys.argv

# ---- C1 修复 ----
C1_OPEN = re.compile(r"<p>\s*<p>", re.I)
C1_CLOSE = re.compile(r"</p>\s*</p>", re.I)


def fix_c1(text: str) -> str:
    # 连续多个 <p> 开头压成一个；连续多个 </p> 结尾压成一个
    new = C1_OPEN.sub("<p>", text)
    new = C1_CLOSE.sub("</p>", new)
    # 处理 <p><p> 跨行 + 中间有空白的情况已覆盖；再处理三连
    new = re.compile(r"(<p>\s*){2,}").sub("<p>", new)
    new = re.compile(r"(\s*</p>){2,}").sub("</p>", new)
    return new


# ---- C4 修复 ----
def extract_block(text: str, start: int) -> tuple[str, int]:
    """从 start（<div 位置）提取一个平衡 div 块，返回 (block, end_index)"""
    depth = 0
    i = start
    m = re.compile(r"<div\b|</div>", re.I)
    for mm in m.finditer(text, start):
        if mm.group(0).lower().startswith("<div"):
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            return text[start:mm.end()], mm.end()
    return text[start:], len(text)


def fix_c4(text: str) -> str:
    """统一规范：删除所有 disclosure-banner/affiliate-note 块，在文章顶部 </header> 之后
    插入一个规范 disclosure（取原 article 内的，否则取第一个出现的作为真源文案）。"""
    disc_re = re.compile(r'<div[^>]*class="[^"]*(disclosure-banner|affiliate-note)[^"]*"', re.I)
    blocks = []
    for m in disc_re.finditer(text):
        block, end = extract_block(text, m.start())
        blocks.append((m.start(), end, block))

    if not blocks:
        return text

    # 找 article 内/外的分界（用 </article> 判断，但删除时不需要）
    art_close = [m.start() for m in re.finditer(r"</article>", text, re.I)]
    last_art_close = max(art_close) if art_close else len(text)

    # 选真源：优先 article 内（start < last_art_close），否则取首个
    inside = [b for b in blocks if b[0] < last_art_close]
    canonical = (inside[0][2] if inside else blocks[0][2]).strip()

    # 删除所有 disclosure 块（从后往前删，避免位移）
    new_text = text
    for s, e, blk in sorted(blocks, key=lambda x: x[0], reverse=True):
        new_text = new_text[:s] + new_text[e:]

    # 规范锚点：article-breadcrumb 的 </nav> 之后（与 fda25b0 范本一致），否则 <article> 开始后
    breadcrumb_nav = re.search(r'<nav[^>]*class="[^"]*article-breadcrumb[^"]*"[^>]*>.*?</nav>', new_text, re.I | re.S)
    if breadcrumb_nav:
        insert_at = breadcrumb_nav.end()
    else:
        art = re.search(r"<article[^>]*>", new_text, re.I)
        if art:
            insert_at = art.end()
        else:
            return text  # 结构异常，不动
    new_text = new_text[:insert_at] + "\n\n        " + canonical + "\n" + new_text[insert_at:]
    return new_text


def main():
    changed = []
    for p in POSTS:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        new = fix_c1(text)
        new = fix_c4(new)
        if new != text:
            changed.append(p)
            if not DRY:
                p.write_text(new, encoding="utf-8")
    if DRY:
        print(f"[DRY] 将修改 {len(changed)} 篇:")
        for p in changed:
            print("  " + str(p.relative_to(REPO)))
    else:
        print(f"✅ 实际修改 {len(changed)} 篇")
        for p in changed:
            print("  " + str(p.relative_to(REPO)))
    # git diff 统计
    if not DRY and changed:
        out = subprocess.run(["git", "diff", "--stat"], cwd=REPO, capture_output=True, text=True)
        print(out.stdout)


if __name__ == "__main__":
    main()
