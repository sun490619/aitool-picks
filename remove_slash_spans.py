#!/usr/bin/env python3
"""删除 posts/ 下所有 HTML 面包屑里的手动斜杠 span（双源 // 的真实根因）。
保留 styles.css 里 .article-breadcrumb > * + *::before 的 CSS 自动斜杠为唯一真源。
"""
import re, glob, os

PATTERN = re.compile(r'\s*<span[^>]*aria-hidden="true"[^>]*>\s*/\s*</span>\s*')

total_removed = 0
files_changed = 0
for path in sorted(glob.glob('posts/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    new_html, n = PATTERN.subn('', html)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        total_removed += n
        files_changed += 1

print(f"files_changed={files_changed} total_removed={total_removed}")
