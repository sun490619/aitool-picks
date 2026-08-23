#!/usr/bin/env python3
"""
按《aitool-picks文章标准格式规范.md》§8.2.1 强制矩阵 + §一固定骨架 + §13.12 H 检查表，
全站扫描每篇文章的【缺件】（该有但缺失的组件）。
同时统计"建议有"组件(at-a-glance/tip/takeaway/rating)覆盖率，供技术总监判断是否升级为强制。

分类判定（规则§8.2.1 末）：
  slug 含 'review'         -> Review 评测文
  slug 含 best-/guide/deep -> Guide/榜单/Deep Dive
  其它 -> 其它（按 Review 处理，保守）

强制项矩阵（按类型）：
  Review: 面包屑, hero, Disclosure, TOC(H2>=4), TL;DR(at-a-glance), What/Who/Features,
          tip, A day with/takeaway, Pricing, CTA, rating(带数字), Pros/Cons, FAQ, How we test,
          Related, 语言切换, 页脚Last updated, 投票框/订阅块(JS注入不查HTML)
  Guide:  面包屑, hero, Disclosure, TOC(H2>=4), CTA, FAQ, How we test, Related, 语言切换, 页脚
          (TL;DR建议, tip/takeaway选配, Pricing/rating/ProsCons豁免)

用法: python3 scripts/scan_missing_components.py
"""
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
POSTS = sorted(REPO.rglob("posts/*.html"))


def classify(slug: str) -> str:
    if "review" in slug:
        return "Review"
    if any(k in slug for k in ("best-", "guide", "deep-dive", "deep")):
        return "Guide"
    return "Review"  # 保守：其它当评测文判强制


def count_h2(text: str) -> int:
    # 排除 hero/footer 区域的 H2；粗略计 <h2 标签
    return len(re.findall(r"<h2\b", text, re.I))


def has(text: str, *patterns):
    return all(re.search(p, text, re.I) for p in patterns)


def scan_file(p: Path):
    text = p.read_text(encoding="utf-8", errors="ignore")
    slug = p.stem
    typ = classify(slug)
    h2 = count_h2(text)
    need_toc = h2 >= 4

    missing = []
    # 通用强制
    if not re.search(r'article-breadcrumb', text, re.I):
        missing.append("面包屑")
    if not re.search(r'post-hero|class="card-image"', text, re.I):
        missing.append("hero图")
    if not re.search(r'disclosure-banner', text, re.I):
        missing.append("Disclosure")
    if not re.search(r'related-articles', text, re.I):
        missing.append("related-articles")
    if not re.search(r'data-zh-url|lang-toggle|class="lang', text, re.I):
        missing.append("语言切换")
    # 页脚更新日期：EN "Updated July 12, 2026" / ZH "更新于 2026 年 7 月 12 日" 均算达标
    if not re.search(r'Last updated|Updated [A-Z][a-z]+ \d|更新于 \d{4}', text, re.I):
        missing.append("页脚更新日期")
    if not re.search(r'how-we-test|How we test', text, re.I):
        missing.append("How we test")
    if not re.search(r'faq-section|class="faq"|id="faq"', text, re.I):
        missing.append("FAQ")
    if need_toc and not re.search(r'class="toc"|article-toc|id="toc"', text, re.I):
        missing.append(f"TOC(H2={h2}>=4)")

    # 按类型强制
    if typ == "Review":
        if not re.search(r'at-a-glance', text, re.I):
            missing.append("[评测]TL;DR速览框")
        if not re.search(r'atp-callout', text, re.I):
            missing.append("[评测]tip/takeaway提示框")
        if not re.search(r'rating-bars|rating-row', text, re.I):
            missing.append("[评测]评分条rating")
        if not re.search(r'pros|cons|Pros & Cons|pros-cons', text, re.I):
            missing.append("[评测]Pros/Cons")
        if not re.search(r'pricing|Pricing', text, re.I):
            missing.append("[评测]Pricing")
        if not re.search(r'cta-box|btn-primary', text, re.I):
            missing.append("[评测]CTA框")
        if not re.search(r'verdict|Verdict', text, re.I):
            missing.append("[评测]Verdict")

    return typ, h2, missing


def main():
    stats = {"Review": 0, "Guide": 0}
    missing_counter = defaultdict(int)
    suggest_counter = defaultdict(int)  # 建议有组件覆盖率
    files_missing = []
    for p in POSTS:
        typ, h2, missing = scan_file(p)
        stats[typ] += 1
        if missing:
            files_missing.append((p.name, typ, missing))
        for m in missing:
            missing_counter[m] += 1
        # 建议有组件统计（全站）
        t = p.read_text(encoding="utf-8", errors="ignore")
        for comp, pat in [("at-a-glance(TL;DR)", r'at-a-glance'),
                          ("atp-callout(tip/takeaway)", r'atp-callout'),
                          ("rating-bars(评分条)", r'rating-bars'),
                          ("verdict", r'verdict')]:
            if not re.search(pat, t, re.I):
                suggest_counter[comp] += 1

    print(f"扫描文章总数: {len(POSTS)} (Review={stats['Review']}, Guide={stats['Guide']})")
    print(f"有缺件的文件: {len(files_missing)}\n")
    print("=" * 64)
    print("【强制项缺件·全站分布】（按组件汇总缺多少篇）")
    for k, v in sorted(missing_counter.items(), key=lambda x: -x[1]):
        print(f"  {k}: 缺 {v} 篇")
    print("\n【建议有组件·全站缺失数】（非硬卡，供升级决策）")
    for k, v in sorted(suggest_counter.items(), key=lambda x: -x[1]):
        print(f"  {k}: 缺 {v} 篇 / 共 {len(POSTS)}")
    print("\n" + "=" * 64)
    print("【逐篇缺件明细】")
    for name, typ, missing in sorted(files_missing):
        print(f"  {name} [{typ}]: {', '.join(missing)}")
    print(f"\n🟢 扫描完成（只读）")


if __name__ == "__main__":
    main()
