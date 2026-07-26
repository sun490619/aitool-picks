#!/usr/bin/env python3
"""为英文文章页补 i18n 接线：加 data-zh-url + hreflang（机械操作，不涉及翻译）。
用法: python3 _gen_zh_en.py <slug1> <slug2> ...
"""
import re, sys, os

POSTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
slugs = sys.argv[1:]
changed = 0
for slug in slugs:
    f = os.path.join(POSTS, slug + '.html')
    if not os.path.isfile(f):
        print('SKIP 不存在:', slug)
        continue
    t = open(f, encoding='utf-8').read()
    t2 = t
    # 1) <html lang="en" ...> 的 data-zh-url 设为本页中文版（空值或缺失都填）
    def html_repl(m):
        tag = m.group(0)
        if 'data-zh-url' not in tag:
            if tag.rstrip().endswith('>'):
                return tag.rstrip()[:-1] + ' data-zh-url="%s-zh.html">' % slug
            return tag
        return re.sub(r'data-zh-url="[^"]*"', 'data-zh-url="%s-zh.html"' % slug, tag)
    t2 = re.sub(r'<html[^>]*\blang="en"[^>]*>', html_repl, t2, count=1)
    # 2) 缺 hreflang 则补 en/zh/x-default
    if 'hreflang="zh"' not in t2:
        alt = (
            '\n    <link rel="alternate" hreflang="en" href="https://aitool-picks.com/posts/%s.html">\n'
            '    <link rel="alternate" hreflang="zh" href="https://aitool-picks.com/posts/%s-zh.html">\n'
            '    <link rel="alternate" hreflang="x-default" href="https://aitool-picks.com/posts/%s.html">\n'
        ) % (slug, slug, slug)
        t2 = t2.replace('<head>', '<head>\n' + alt, 1)
    if t2 != t:
        open(f, 'w', encoding='utf-8').write(t2)
        changed += 1
        print('OK 已接线:', slug)
    else:
        print('无变化:', slug)
print('=== 共处理 %d，改动 %d ===' % (len(slugs), changed))
