#!/usr/bin/env python3
"""Align aitool-picks post pages: ensure each has a TOC + h2 ids, and wrap
real pros/cons sections in .verdict boxes. Content is derived ONLY from the
page's own <h2> text -- nothing is invented. Skips TOC insertion on pages that
already have one (class="toc" or article-toc)."""
import re, glob, sys

SKIP_TOC_MARKERS = ('class="toc"', 'article-toc')
# exact (case-insensitive) EN phrases to exclude from the TOC
TOC_EXCLUDE = {'how we test', 'related articles', 'related reads',
               'frequently asked questions', 'faq'}
# ZH phrases / prefixes to exclude
TOC_EXCLUDE_ZH = {'相关文章', '相关阅读', '常见问题'}
TOC_EXCLUDE_ZH_PREFIX = ('我们的测试', '我们如何')


def slugify(text):
    t = re.sub(r'<[^>]+>', '', text).lower()
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')[:48]


def has_toc(html):
    return any(m in html for m in SKIP_TOC_MARKERS)


def add_ids(html):
    counter = [0]
    seen = {}
    def unique(sid):
        if sid in seen:
            seen[sid] += 1
            return f"{sid}-{seen[sid]}"
        seen[sid] = 1
        return sid
    def repl(m):
        attrs, txt = m.group(1), m.group(2)
        counter[0] += 1
        if 'id=' in attrs and not re.search(r'id=""', attrs):
            # keep existing non-empty id, but dedupe collisions
            m2 = re.search(r'id="([^"]*)"', attrs)
            sid = unique(m2.group(1))
            attrs = re.sub(r'id="[^"]*"', f'id="{sid}"', attrs, count=1)
            return f'<h2{attrs}>{txt}</h2>'
        sid = slugify(txt) or re.sub(r'<[^>]+>', '', txt).strip() or f"sec-{counter[0]}"
        sid = unique(sid)
        if re.search(r'id=""', attrs):
            attrs = re.sub(r'id=""', f'id="{sid}"', attrs, count=1)
            return f'<h2{attrs}>{txt}</h2>'
        return f'<h2 id="{sid}"{attrs}>{txt}</h2>'
    return re.sub(r'<h2([^>]*)>(.*?)</h2>', repl, html, flags=re.S)


def _exclude_label(label, zh):
    low = label.lower()
    if zh:
        if label in TOC_EXCLUDE_ZH:
            return True
        if any(label.startswith(p) for p in TOC_EXCLUDE_ZH_PREFIX):
            return True
        return False
    return low in TOC_EXCLUDE


def build_toc(html, zh=False):
    heads = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', html, flags=re.S)
    items = []
    for sid, txt in heads:
        label = re.sub(r'<[^>]+>', '', txt).strip()
        if _exclude_label(label, zh):
            continue
        items.append(f'                <li><a href="#{sid}">{label}</a></li>')
    if not items:
        return None
    title = '本文覆盖什么' if zh else 'What we cover'
    return ('        <div class="toc" aria-label="Table of contents">\n'
            f'            <p class="toc-title">{title}</p>\n'
            '            <ul>\n' + '\n'.join(items) + '\n'
            '            </ul>\n        </div>\n')


def wrap_verdicts(html):
    if 'class="verdict' in html:
        return html  # already aligned; don't double-wrap
    h2s = list(re.finditer(r'<h2([^>]*)>(.*?)</h2>', html, flags=re.S))
    reps = []
    for i, m in enumerate(h2s):
        attrs, txt = m.group(1), m.group(2)
        label = re.sub(r'<[^>]+>', '', txt).strip()
        low = label.lower()
        bstart = m.end()
        bend = h2s[i + 1].start() if i + 1 < len(h2s) else len(html)
        block = html[bstart:bend]
        if 'pros' in low and 'cons' in low:
            rep = f'<h2{attrs}>{txt}</h2>\n<div class="verdict">\n{block}\n</div>\n'
            reps.append((m.start(), bend, rep))
        elif low == 'what impressed us':
            rep = f'<h2{attrs}>{txt}</h2>\n<div class="verdict">\n{block}\n</div>\n'
            reps.append((m.start(), bend, rep))
        elif low == 'where it falls short':
            rep = f'<h2{attrs}>{txt}</h2>\n<div class="verdict bad">\n{block}\n</div>\n'
            reps.append((m.start(), bend, rep))
    for s, e, rep in sorted(reps, reverse=True):
        html = html[:s] + rep + html[e:]
    return html


def process(path):
    html = open(path, encoding='utf-8').read()
    html = add_ids(html)  # idempotent; ensures every h2 has an anchor id
    zh = '-zh.' in path
    if has_toc(html):
        if zh and 'What we cover' in html:
            # ZH page generated earlier with an English title -> regenerate properly
            html = re.sub(r'\s*<div class="toc"[^>]*>.*?</div>\s*', '', html, flags=re.S)
        else:
            open(path, 'w', encoding='utf-8').write(html)
            return True
    toc = build_toc(html, zh)
    if toc:
        html = re.sub(r'(?s)(<h2[^>]*>.*?</h2>)', toc + r'\1', html, count=1)
    html = wrap_verdicts(html)
    open(path, 'w', encoding='utf-8').write(html)
    return True


if __name__ == '__main__':
    files = sys.argv[1:] or glob.glob('posts/*.html')
    done = 0
    for f in files:
        if process(f):
            done += 1
            print('aligned', f)
    print(f'TOTAL aligned: {done}')
