#!/usr/bin/env python3
"""
aitool-picks i18n 完整性校验器
================================
扫描全站 HTML，列出「应该有中文版但没有」的页面，技术总监发布前/后跑一遍即可，
不用人工逐个打开浏览器检查。

规则：
- 文章页 (posts/*.html 或含 .article-content/<article>) 必须有中文副本页，
  且英文页 <html> 上 data-zh-url 指向对应 -zh.html（非空即「已就绪」）。
- 中文副本页 (-zh.html) 的 data-zh-url 必须指回英文页（否则回切断裂）。
- 非文章页 (首页/分类/工具卡) 走 shared.js 映射表原地翻译，不要求副本，
  但要求 savedLang=zh 时能用映射表（本脚本不校验映射表覆盖率）。
"""
import re, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))

missing_article = []   # 文章页待翻中文版
ok_article = []        # 文章页已有中文版
zh_pages = []          # 中文副本页
broken_backlink = []   # 中文副本缺回链

for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    if 'node_modules' in f:
        continue
    rel = os.path.relpath(f, ROOT)
    try:
        t = open(f, encoding='utf-8').read()
    except Exception:
        continue
    m = re.search(r'<html[^>]*\sdata-zh-url="([^"]*)"', t)
    has_zh = bool(m and m.group(1).strip())
    is_article = ('/posts/' in rel) or ('article-content' in t) or ('<article' in t)

    if rel.endswith('-zh.html'):
        zh_pages.append(rel)
        if not has_zh:
            broken_backlink.append(rel)
        continue

    if is_article:
        if has_zh:
            ok_article.append(rel)
        else:
            missing_article.append(rel)

print("=== 文章页【已有中文版】(切换可用):", len(ok_article))
for x in ok_article:
    print("  ✓", x)
print("\n=== 文章页【待翻中文版】(当前隐藏切换, 不混杂):", len(missing_article))
for x in missing_article:
    print("  •", x)
print("\n=== 中文副本页 (-zh.html):", len(zh_pages))
for x in zh_pages:
    print("  ", x)
print("\n=== 中文副本【缺回链】(data-zh-url 为空, 回切会断):", len(broken_backlink))
for x in broken_backlink:
    print("  ⚠", x)

print("\n=== 汇总 ===")
print(f"  文章页总数(含副本): {len(ok_article)+len(missing_article)+len(zh_pages)}")
print(f"  已就绪(可切中文): {len(ok_article)}")
print(f"  待翻: {len(missing_article)}")
print(f"  副本回链异常: {len(broken_backlink)}")

if missing_article or broken_backlink:
    print("\n结论: 存在待处理项 (待翻文章 / 副本回链异常)。")
else:
    print("\n结论: 全站 i18n 完整, 所有文章均可中英文切换。")
