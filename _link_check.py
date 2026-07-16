#!/usr/bin/env python3
import os, re, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML_FILES = []
for dirpath, _, files in os.walk(ROOT):
    # skip hidden/helper dirs
    if any(part.startswith('.') for part in dirpath.split(os.sep)):
        continue
    for f in files:
        if f.endswith('.html'):
            HTML_FILES.append(os.path.join(dirpath, f))

# map of site-relative path -> abs path
rel_map = {}
for fp in HTML_FILES:
    rel = '/' + os.path.relpath(fp, ROOT).replace(os.sep, '/')
    rel_map[rel] = fp

link_re = re.compile(r'href="([^"]+)"')
broken = []
checked = 0
for fp in HTML_FILES:
    base_rel = '/' + os.path.relpath(fp, ROOT).replace(os.sep, '/')
    base_dir = os.path.dirname(fp)
    with open(fp, encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    for m in link_re.finditer(content):
        href = m.group(1)
        if href.startswith('http://') or href.startswith('https://') or href.startswith('mailto:') or href.startswith('#') or href.startswith('//') or href.startswith('data:'):
            continue
        if href.startswith('/'):
            target = os.path.normpath(os.path.join(ROOT, href.lstrip('/')))
        else:
            target = os.path.normpath(os.path.join(base_dir, href))
        checked += 1
        if not os.path.exists(target):
            broken.append((base_rel, href, os.path.relpath(target, ROOT)))

# orphan posts
posts_dir = os.path.join(ROOT, 'posts')
all_posts = set()
for f in os.listdir(posts_dir):
    if f.endswith('.html'):
        all_posts.add('/posts/' + f)

referenced = set()
for fp in HTML_FILES:
    with open(fp, encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    for m in link_re.finditer(content):
        href = m.group(1)
        if href.startswith('/posts/') and href.endswith('.html'):
            referenced.add(href.split('#')[0])

orphans = sorted(all_posts - referenced)

print(f"HTML files scanned: {len(HTML_FILES)}")
print(f"Internal links checked: {checked}")
print(f"\n=== BROKEN INTERNAL LINKS ({len(broken)}) ===")
for src, href, tgt in broken:
    print(f"  {src}  ->  {href}  (resolves: {tgt})")
print(f"\n=== ORPHAN POSTS (not linked from anywhere, {len(orphans)}) ===")
for o in orphans:
    print(f"  {o}")
