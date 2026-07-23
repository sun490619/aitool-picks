#!/usr/bin/env python3
"""Batch fix footers across all aitool-picks HTML files to match index.html standard."""

import os
import re
import glob

BASE = "/Users/dawei/CodeBuddy/aitool-picks"

# Standard footer from index.html (5 columns: brand + 4 columns + bottom)
STD_FOOTER = '''    <footer class="site-footer" role="contentinfo">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="footer-logo"><span class="brand-mark">ATP</span>AI Tool Picks</a>
                    <p class="footer-desc">Honest comparisons & reviews of the best AI tools. Hand-tested, independently written, zero fluff.</p>
                    <div class="footer-social">
                        <a href="https://x.com" target="_blank" rel="noopener noreferrer" aria-label="X">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <a href="https://github.com/sun490619/aitool-picks" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
                        </a>
                        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                        </a>
                    </div>
                </div>

                <div class="footer-column">
                    <h4>Categories</h4>
                    <ul class="footer-links">
                        <li><a href="/category/writing.html">AI Writing Tools</a></li>
                        <li><a href="/category/coding.html">AI Coding Assistants</a></li>
                        <li><a href="/category/video.html">AI Video Generators</a></li>
                        <li><a href="/category/seo.html">AI SEO Tools</a></li>
                        <li><a href="/category/productivity.html">AI Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Popular Reviews</h4>
                    <ul class="footer-links">
                        <li><a href="/posts/jasper-vs-writesonic.html">Jasper vs Writesonic</a></li>
                        <li><a href="/posts/best-ai-seo-tools-2026.html">Best AI SEO Tools</a></li>
                        <li><a href="/category/writing.html">All Writing Tools</a></li>
                        <li><a href="/category/seo.html">All SEO Tools</a></li>
                        <li><a href="/category/productivity.html">All Productivity &amp; General</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Sister Sites</h4>
                    <ul class="footer-links">
                        <li><a href="https://mintshovels.com/" target="_blank" rel="noopener">MintShovels — Free SEO Audit Tool</a></li>
                        <li><a href="https://makerearn.com/" target="_blank" rel="noopener">makerearn — Free Money Calculators</a></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Resources</h4>
                    <ul class="footer-links">
                        <li><a href="/suggest-tool.html">Suggest a Tool</a></li>
                        <li><a href="/affiliate-disclosure.html">Affiliate Disclosure</a></li>
                        <li><a href="/privacy.html">Privacy Policy</a></li>
                        <li><a href="#bd-subscribe">Newsletter</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-bottom">
                <p>&copy; 2026 AI Tool Picks. All rights reserved.</p>
                <div class="flex gap-3">
                    <a href="/privacy.html">Privacy Policy</a>
                    <a href="/affiliate-disclosure.html">Affiliate Disclosure</a>
                </div>
            </div>
        </div>
    </footer>'''


def fix_contact_html(path):
    """Special handling for contact.html: move form back into main, then replace footer."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the orphaned form section (everything between </footer> and </body>)
    # Pattern: </footer> ... </body>
    match = re.search(r'(</footer>\s*)(.*?)(\s*</body>)', content, re.DOTALL)
    if match:
        orphaned = match.group(2).strip()
        # Remove the orphaned section from after footer
        content = content[:match.start(1)] + match.group(1) + match.group(3)
        # Insert the form before </main>
        content = content.replace('</main>', orphaned + '\n    </main>')

    # Now replace the old footer with standard footer
    content = replace_footer(content)
    return content


def replace_footer(content):
    """Replace any existing <footer>...</footer> with standard footer."""
    # Match any <footer ...>...</footer> tag (covers class="site-footer", class="footer", style="...", etc.)
    pattern = re.compile(r'<footer\b[^>]*>.*?</footer>', re.DOTALL)
    if pattern.search(content):
        return pattern.sub(STD_FOOTER, content)
    return content


def insert_footer(content):
    """Insert standard footer before </body> if no footer exists."""
    if not re.search(r'<footer\b', content, re.IGNORECASE):
        # Insert before </body> or </body > (with possible spaces)
        content = re.sub(r'(\s*</body\s*>)', '\n' + STD_FOOTER + '\n\\1', content, count=1)
    return content


def process_file(filepath):
    """Process a single HTML file."""
    relpath = os.path.relpath(filepath, BASE)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    if relpath == 'contact.html':
        content = fix_contact_html(filepath)
    else:
        content = replace_footer(content)
        content = insert_footer(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    # Find all HTML files excluding images/samples
    html_files = []
    for root, dirs, files in os.walk(BASE):
        # Skip images directory
        if 'images' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    fixed = []
    skipped = []

    for filepath in sorted(html_files):
        relpath = os.path.relpath(filepath, BASE)
        if process_file(filepath):
            fixed.append(relpath)
        else:
            skipped.append(relpath)

    print(f"Fixed {len(fixed)} files:")
    for f in fixed:
        print(f"  + {f}")
    print(f"\nUnchanged {len(skipped)} files:")
    for f in skipped:
        print(f"  - {f}")


if __name__ == '__main__':
    main()
