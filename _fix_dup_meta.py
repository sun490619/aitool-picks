import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
files = ['index.html', 'category/coding.html', 'category/video.html', 'category/writing.html']

def get_meta_desc(href):
    if not href:
        return None
    rel = href.lstrip('/')
    full = os.path.join(ROOT, rel)
    try:
        html = open(full, encoding='utf-8').read()
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        if m:
            d = m.group(1).strip()
            # trim to a readable length
            if len(d) > 200:
                d = d[:197].rstrip() + '...'
            return d
    except Exception as e:
        print('  ! cannot read', full, e)
    return None

for f in files:
    path = os.path.join(ROOT, f)
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    last_href = None
    changed = 0
    for line in lines:
        mt = re.search(r'post-card-title"><a href="([^"]+)"', line)
        if mt:
            last_href = mt.group(1)
        mex = re.search(r'post-card-excerpt">Updated\s+.*?·\s*\d+\s*min read(.*?)</p>', line)
        if mex:
            rest = mex.group(1).lstrip()
            if rest.startswith('...'):
                rest = rest[3:].lstrip()
            if not rest or len(rest) < 12:
                desc = get_meta_desc(last_href)
                rest = desc or ''
            new_line = re.sub(
                r'post-card-excerpt">Updated\s+.*?·\s*\d+\s*min read.*?</p>',
                f'post-card-excerpt">{rest}</p>',
                line,
            )
            changed += 1
            if new_line != line:
                print(f'  [{f}] fixed -> {rest[:70]!r}')
            out.append(new_line)
        else:
            out.append(line)
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'{f}: {changed} excerpt(s) de-duplicated')
print('DONE')
