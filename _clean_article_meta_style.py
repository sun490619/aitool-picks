import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
STYLE = ' style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);"'

# 只匹配 article-meta 这一个精确 style 串，避免误伤其它 div
PAT = re.compile(re.escape('<div class="article-meta"') + re.escape(STYLE))

files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
total_fixed = 0
changed_files = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        txt = fh.read()
    n = len(PAT.findall(txt))
    if n:
        txt2 = PAT.sub('<div class="article-meta">', txt)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(txt2)
        total_fixed += n
        changed_files.append((f, n))

print(f"TOTAL_FIXED={total_fixed}")
print(f"CHANGED_FILES={len(changed_files)}")
for f, n in changed_files:
    print(f"  {n}  {os.path.relpath(f, ROOT)}")
