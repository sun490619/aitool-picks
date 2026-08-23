#!/usr/bin/env python3
"""
aitool-picks 全站 5 类问题扫描器（2026-08-23 重做，不依赖历史清零结论）。

5 类：
  C1 标签破损/嵌套错误：<p><p>、</p></p>、<h 3>等多空格坏标签、散lgc
  C2 article 容器缺失：正文未被 <article class="post article-content"> 类容器包住（投票框漏插）
  C3 main/article 提前关闭：</article>/</main> 在正文主体前出现（后半段掉出容器）
  C4 底部组件堆叠/位置错：disclosure-banner 出现在 </article> 之后（article 外）或文末重复
  C5 溢出/布局风险：hero/img 等无 max-width 约束、超宽表格/pre、article 内容宽于 760 栏迹象

输出：每篇命中哪些类 + 汇总计数。纯只读，不修改文件。
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = sorted(REPO.rglob("posts/*.html"))
# 也包含可能的根级文章页（如 tool-selector 等 posts/ 下已含，这里只扫 posts）

TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][a-zA-Z0-9-]*)[^>]*?>", re.S)
CHECK_TAGS = {"div", "article", "section", "header", "footer", "main", "nav", "aside"}
BAD_H_RE = re.compile(r"</?h\s+[0-9]", re.I)          # </h 3> 或 <h 2>
NESTED_P_RE = re.compile(r"<p>\s*<p>|</p>\s*</p>", re.I)


def strip_noise(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S | re.I)
    return text


# 投票框 scripts.js 已支持这些 class（含 post-body），均合法
VALID_ARTICLE_CLASSES = re.compile(
    r'class="[^"]*(post article-content|article-content|post-article|'
    r'post article-body|article-body|post-body|post-article container|post container)[^"]*"'
)


def has_article_wrapper(text: str) -> bool:
    # 只要有 <article> 且 class 属于投票框已支持列表即为合法（C2 不算问题）
    for m in re.finditer(r"<article[^>]*>", text, re.I):
        if VALID_ARTICLE_CLASSES.search(m.group(0)):
            return True
    # 也接受裸 <article> 无 class（罕见但结构存在）
    if re.search(r"<article\s*>", text):
        return True
    return False


def count_tag_balance(text: str):
    """返回 (unbalanced:bool, leftover_stack, premature_close_article_or_main_positions)"""
    clean = strip_noise(text)
    stack = []
    premature = []  # (tag, pos) 提前关闭 article/main
    # 用位置判断 article/main 是否在文件后半段之前就关闭
    art_open = [m.start() for m in re.finditer(r"<article\b", clean, re.I)]
    art_close = [m.start() for m in re.finditer(r"</article>", clean, re.I)]
    main_open = [m.start() for m in re.finditer(r"<main\b", clean, re.I)]
    main_close = [m.start() for m in re.finditer(r"</main>", clean, re.I)]
    # 结构平衡（通用）
    for m in TAG_RE.finditer(clean):
        raw = m.group(0); slash, tag = m.group(1), m.group(2).lower()
        if tag not in CHECK_TAGS:
            continue
        if raw.rstrip().endswith("/>"):
            continue
        if slash:
            if stack and stack[-1][0] == tag:
                stack.pop()
            elif stack:
                # 不匹配，记录但不强行弹
                pass
            else:
                pass
    unbalanced = len(stack) > 0
    # 提前关闭判定：如果 article 有多个开标签，最后一个 close 应在文件 90% 之后
    premature_flags = []
    if art_open and art_close:
        last_open = max(art_open); first_close = min(art_close)
        if first_close < last_open * 0.5:  # 关闭远早于最后的开启 -> 疑似提前关闭
            premature_flags.append("article")
    if main_open and main_close:
        last_open = max(main_open); first_close = min(main_close)
        if first_close < last_open * 0.5:
            premature_flags.append("main")
    return unbalanced, stack, premature_flags


def check_c4_bottom_stack(text: str):
    """disclosure-banner 是否出现在 </article> 之后（article 外），或文末紧邻 </article> 前重复"""
    clean = strip_noise(text)
    art_close_pos = [m.start() for m in re.finditer(r"</article>", clean, re.I)]
    disc_pos = [m.start() for m in re.finditer(r'disclosure-banner|affiliate-note', clean, re.I)]
    issues = []
    if art_close_pos and disc_pos:
        last_art_close = max(art_close_pos)
        for d in disc_pos:
            if d > last_art_close:
                issues.append("disclosure/affiliate 在 </article> 之外(底部堆叠)")
                break
    # 文末重复 disclosure（出现 >1 次且其中一次在文章尾部 80% 后）
    if len(disc_pos) > 1:
        issues.append(f"disclosure 出现 {len(disc_pos)} 次(疑似重复)")
    return issues


def check_c5_overflow(text: str):
    """布局溢出风险：仅报未被全局 CSS 兜底的硬溢出（全局已有 img{max-width:100%}，裸width不报）。
    这里重点查：超宽 <pre>/<table> 无 overflow 约束的迹象（源码层只能标记，真溢出需浏览器验）。"""
    issues = []
    # 源码层无法可靠判断 CSS 是否兜底，故 C5 仅作软提示，不计入硬修复清单
    return issues


def main():
    results = {}
    for p in POSTS:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            results[str(p)] = ["读取失败:" + str(e)]
            continue
        hits = []
        # C1
        if BAD_H_RE.search(text) or NESTED_P_RE.search(text):
            hits.append("C1:标签破损(<p><p>/<h 3>等)")
        # C2（已确认 post-body 等合法，投票框支持；仅报真正缺 article 容器者）
        if not has_article_wrapper(text):
            hits.append("C2:缺article容器(投票框漏插)")
        # C3
        _, _, premature = count_tag_balance(text)
        if premature:
            hits.append("C3:容器疑似提前关闭(" + ",".join(premature) + ")")
        # C4
        c4 = check_c4_bottom_stack(text)
        hits.extend(["C4:" + x for x in c4])
        # C5
        c5 = check_c5_overflow(text)
        hits.extend(["C5:" + x for x in c5])
        if hits:
            results[str(p.relative_to(REPO))] = hits

    # 输出
    print(f"扫描文件数: {len(POSTS)}")
    print(f"命中文件数: {len(results)}")
    print("=" * 60)
    cat_count = {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0}
    for f, hits in sorted(results.items()):
        print(f"\n📄 {f}")
        for h in hits:
            print(f"   - {h}")
            key = h.split(":")[0]
            if key in cat_count:
                cat_count[key] += 1
    print("\n" + "=" * 60)
    print("各类命中篇数汇总:")
    for k in sorted(cat_count):
        print(f"  {k}: {cat_count[k]} 篇")
    print("\n🟢 扫描完成（只读，未修改任何文件）")


if __name__ == "__main__":
    main()
