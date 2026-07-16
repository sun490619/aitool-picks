#!/usr/bin/env python3
import os, re
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
bad = []
total = 0
img_re = re.compile(r'<img[^>]+src="([^"]+)"', re.I)
for dirpath, _, files in os.walk(ROOT):
    if any(p.startswith('.') for p in dirpath.split(os.sep)):
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dirpath, f)
        base_rel = '/' + os.path.relpath(fp, ROOT).replace(os.sep, '/')
        base_dir = os.path.dirname(fp)
        with open(fp, encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        for m in img_re.finditer(content):
            src = m.group(1)
            if src.startswith('http') or src.startswith('data:') or src.startswith('//'):
                continue
            total += 1
            if src.startswith('/'):
                tgt = os.path.normpath(os.path.join(ROOT, src.lstrip('/')))
            else:
                tgt = os.path.normpath(os.path.join(base_dir, src))
            if not os.path.exists(tgt):
                bad.append((base_rel, src, os.path.relpath(tgt, ROOT)))

print(f"Total local <img> refs: {total}")
print(f"BROKEN img refs: {len(bad)}")
for src, href, tgt in bad:
    print(f"  {src} -> {href} (->{tgt})")
