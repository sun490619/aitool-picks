import re
from pathlib import Path

# Read index.html to use as the canonical drawer with Lang/Theme in footer
index_path = Path('/Users/dawei/aitool-picks/index.html')
index_html = index_path.read_text(encoding='utf-8')

# Extract the full drawer block (from mobile-menu-overlay through the closing div)
drawer_match = re.search(
    r'<div class="mobile-menu-overlay".*?</div>\n</div>\n</div>',
    index_html,
    re.DOTALL
)
if not drawer_match:
    raise SystemExit('ERROR: Could not extract drawer block from index.html')
drawer_block = drawer_match.group(0)

# Verify drawer_block still contains langSwitch + themeToggle
assert 'langSwitch' in drawer_block, 'drawer block missing langSwitch'
assert 'themeToggle' in drawer_block, 'drawer block missing themeToggle'

# Target directories to patch
base = Path('/Users/dawei/aitool-picks')
target_roots = []
for sub in ['', 'category/', 'posts/', 'tools/', 'docs', 'docs/category/', 'docs/posts/', 'docs/tools/', 'privacy.html', 'affiliate-disclosure.html', 'docs/privacy.html', 'docs/affiliate-disclosure.html']:
    p = base / sub if sub else base
    if p.is_dir():
        target_roots.append(p)

patched = []
skipped = []

for root in target_roots:
    if not root.exists():
        skipped.append(str(root))
        continue
    for path in sorted(root.glob('*.html')):
        text = path.read_text(encoding='utf-8')
        # Skip files already having drawer block with Lang+Theme
        if 'mobile-menu-overlay' in text and 'langSwitch' in text and 'themeToggle' in text:
            skipped.append(str(path.relative_to(base)))
            continue
        # Replace old drawer + overlay pair with canonical one
        new_text = re.sub(
            r'<div class="mobile-menu-overlay".*?</div>\n</div>\n</div>',
            drawer_block,
            text,
            flags=re.DOTALL
        )
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            patched.append(str(path.relative_to(base)))

print(f'PATCHED ({len(patched)}):')
for x in patched:
    print('  -', x)
print(f'SKIPPED ({len(skipped)}):')
for x in skipped:
    print('  -', x)
