#!/usr/bin/env python3
"""Move disclosure-banner from bottom to top of article, remove duplicates and old affiliate-note."""
import re, glob, sys

PATTERN = re.compile(r'<div class="(?:disclosure-banner|affiliate-note)"[^>]*>', re.S)

def extract_div_block(text, start):
    """Extract outer div block starting at position start, handling nested divs."""
    m = re.search(r'<div\b', text[start:])
    if not m:
        return None
    # start is already at the opening <div, count from there
    counter = 0
    i = start
    n = len(text)
    while i < n:
        if text[i:i+4].lower() == '<div':
            counter += 1
            i += 4
        elif text[i:i+6].lower() == '</div>':
            counter -= 1
            i += 6
            if counter == 0:
                return start, i, text[start:i]
        else:
            i += 1
    return None

def normalize_disclosure_block(block):
    """Return inner HTML normalized to standard disclosure text."""
    m = re.search(r'<div[^>]*>(.*?)</div>', block, re.S)
    if not m:
        return '<strong>Disclosure:</strong> This post contains affiliate links. If you sign up or purchase through them, we may earn a commission at no extra cost to you. We only recommend tools we\'ve genuinely tested. See our <a href="/affiliate-disclosure.html">full affiliate disclosure</a>.'
    inner = m.group(1).strip()
    # Remove wrapping <p> tags
    inner = re.sub(r'^<p>\s*', '', inner)
    inner = re.sub(r'\s*</p>\s*$', '', inner)
    # Normalize affiliate-note variant
    inner = inner.replace('<strong>Affiliate note:</strong>', '<strong>Disclosure:</strong>')
    inner = inner.replace('<strong>Affiliate disclosure:</strong>', '<strong>Disclosure:</strong>')
    if not re.search(r'<strong>\s*Disclosure:', inner):
        inner = f'<strong>Disclosure:</strong> {inner}'
    return inner

def fix_file(path, dry_run=True):
    s = open(path, encoding='utf-8').read()
    mm = re.search(r'(<main[^>]*>)(.*?)(</main>)', s, re.S)
    if not mm:
        return s, 'no_main'
    main_open, main_body, main_close = mm.group(1), mm.group(2), mm.group(3)
    lenb = len(main_body)

    # Find all disclosure/affiliate blocks inside main
    blocks = []
    for m in PATTERN.finditer(main_body):
        block = extract_div_block(main_body, m.start())
        if block:
            start, end, txt = block
            blocks.append((start, end, txt, start / lenb))

    if not blocks:
        return s, 'no_disclosure'

    # Separate top (<=45%) and bottom (>45%) blocks; classify by original class
    top = [b for b in blocks if b[3] <= 0.45]
    bottom = [b for b in blocks if b[3] > 0.45]
    top_disclosure = [b for b in top if 'disclosure-banner' in b[2]]
    bottom_disclosure = [b for b in bottom if 'disclosure-banner' in b[2]]
    top_aff = [b for b in top if 'affiliate-note' in b[2]]
    bottom_aff = [b for b in bottom if 'affiliate-note' in b[2]]

    # If already a single disclosure in top, nothing to fix
    if len(top_disclosure) == 1 and not bottom_disclosure and not top_aff:
        return s, 'ok'

    # Canonical content: prefer top disclosure, else bottom disclosure, else affiliate-note
    canonical = None
    for b in top_disclosure + bottom_disclosure + top_aff + bottom_aff:
        canonical = b[2]
        break
    if not canonical:
        return s, 'no_canonical'

    inner_html = normalize_disclosure_block(canonical)
    new_block = (
        '        <div class="disclosure-banner" role="note">\n'
        f'          {inner_html}\n'
        '        </div>'
    )

    # Remove all old blocks (descending order)
    new_body = main_body
    for start, end, txt, rel in sorted(blocks, reverse=True):
        before = new_body[:start]
        after = new_body[end:]
        while before.endswith('\n'):
            before = before[:-1]
        while after.startswith('\n'):
            after = after[1:]
        new_body = before + after

    # Find insertion point inside main_body.
    # Prefer after the article-breadcrumb </nav> unless that nav sits inside <header>.
    insert_pos = None
    nav_match = re.search(r'<nav class="article-breadcrumb"[^>]*>.*?</nav>', new_body, re.S)
    if nav_match:
        before_nav = new_body[:nav_match.start()]
        opens = len(re.findall(r'<header\b', before_nav))
        closes = before_nav.count('</header>')
        if opens <= closes:
            insert_pos = nav_match.end()
    if insert_pos is None:
        header_match = re.search(r'</header>', new_body)
        if header_match:
            insert_pos = header_match.end()
    if insert_pos is None:
        h2_pos = new_body.find('<h2')
        if h2_pos != -1:
            insert_pos = h2_pos
    if insert_pos is None:
        insert_pos = 0

    new_body = new_body[:insert_pos] + '\n\n' + new_block + '\n' + new_body[insert_pos:]

    new_s = s[:mm.start()] + main_open + new_body + main_close + s[mm.end():]
    status = 'ok'
    if bottom_disclosure or bottom_aff:
        status = 'moved'
    elif len(top_disclosure) > 1 or top_aff:
        status = 'cleaned'
    return new_s, status

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    files = sorted(glob.glob('posts/*.html'))
    changed = []
    for path in files:
        new_s, status = fix_file(path, dry_run=dry_run)
        if status in ('moved', 'cleaned'):
            if not dry_run:
                open(path, 'w', encoding='utf-8').write(new_s)
            changed.append((path, status))
    print(f"{'Would change' if dry_run else 'Changed'} {len(changed)} files")
    for p, s in changed[:20]:
        print(f"  {p}: {s}")
    if len(changed) > 20:
        print(f"  ... and {len(changed)-20} more")
