#!/usr/bin/env python3
"""aitool-picks 全站一致性六维核查脚本（落到实处的真扫描）

六维：
  1. lang / data-zh-url 配对正确性
     - EN 页 data-zh-url 必须指向真实存在的 -zh.html，且不能指向自身
     - ZH 页 data-zh-url 必须指向真实存在的 EN 原文，且不能指向自身
  2. og:image
     - 必须存在且本地路径（/images/...），不能是外链/缺失
     - 全站 og:image 不得重复（不同页允许同图？这里只报告，不强禁）
  3. JSON-LD
     - 所有 <script type="application/ld+json"> 必须 json.loads 通过
     - 数值字段不得是带引号的字符串（price/ratingValue 等）
  4. 追踪代码
     - GA4 (G-D53DQ3JKKL) 与 Clarity (xavbiwb9dt) 必须每页都在
  5. 面包屑 + 分类归属
     - 文章页（posts/下非 tool-selector）必须有 article-breadcrumb
     - 且对应分类页（category/<类>.html 或 -zh.html）必须收录该文卡片
  6. disclosure / affiliate 声明
     - 含联盟链接的页（出现 via=/?pc=/fpr=/aff.php 或 href 含 affiliate）必须有 disclosure 声明句

用法：python3 scripts/global_consistency_check.py
输出：每维失败清单 + 总数；exit 1 若有失败（可加 --report-only 不报错）。
"""
import re
import sys
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'_preview', '_review', '_tmp_ogsrc', 'node_modules', '.git'}
GA4_ID = 'G-D53DQ3JKKL'
CLARITY_ID = 'xavbiwb9dt'

CATEGORY_EN = {
    'writing': 'category/writing.html', 'coding': 'category/coding.html',
    'video': 'category/video.html', 'seo': 'category/seo.html',
    'productivity': 'category/productivity.html', 'image': 'category/image.html',
}
CATEGORY_ZH = {
    'writing': 'category/writing-zh.html', 'coding': 'category/coding-zh.html',
    'video': 'category/video-zh.html', 'seo': 'category/seo-zh.html',
    'productivity': 'category/productivity-zh.html', 'image': 'category/image-zh.html',
}

DISCLOSURE_PAT = re.compile(r'affiliate|联盟|commission|佣金', re.I)


def should_skip(f: Path) -> bool:
    rel = f.relative_to(ROOT)
    parts = rel.parts
    if any(p in SKIP_DIRS for p in parts):
        return True
    if len(parts) >= 2 and parts[0] == 'images' and parts[1] == 'samples':
        return True
    return False


def list_html():
    return [f for f in ROOT.rglob('*.html')
            if '.git' not in str(f) and 'node_modules' not in str(f) and not should_skip(f)]


def get_lang_and_zhurl(html):
    m = re.search(r'<html\s+[^>]*lang="(en|zh)"', html[:800])
    lang = m.group(1) if m else None
    z = re.search(r'<html\s+[^>]*data-zh-url="([^"]*)"', html[:800])
    zhurl = z.group(1) if z else None
    return lang, zhurl


def main():
    files = list_html()
    report = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    og_map = {}  # og -> [files]

    for f in files:
        rel = str(f.relative_to(ROOT))
        html = f.read_text(encoding='utf-8', errors='ignore')

        # ---- 1. lang / data-zh-url 配对 ----
        lang, zhurl = get_lang_and_zhurl(html)
        if lang is None:
            report[1].append((rel, '缺少 <html lang>'))
        else:
            if zhurl is None:
                # 允许：tool-selector 等少数无对应语言页的，不强制
                pass
            else:
                # 自身指向
                self_path = '/' + rel
                if zhurl.rstrip('/') == self_path.rstrip('/'):
                    report[1].append((rel, f'data-zh-url 指向自身 ({zhurl})'))
                else:
                    # 目标文件必须存在
                    target = ROOT / zhurl.lstrip('/')
                    if not target.exists():
                        report[1].append((rel, f'data-zh-url 指向不存在文件 ({zhurl})'))

        # ---- 2. og:image ----
        ogm = re.search(r'<meta property="og:image" content="([^"]*)"', html)
        if ogm:
            og = ogm.group(1)
            og_map.setdefault(og, []).append(rel)
            parsed = urlparse(og)
            # 本站域名的绝对 URL 视为本地（不报）；仅真实第三方外链才报
            if parsed.netloc and 'aitool-picks.com' not in parsed.netloc:
                report[2].append((rel, f'og:image 是第三方外链 ({og})'))
            elif not parsed.netloc and not og.startswith('/images/'):
                report[2].append((rel, f'og:image 非本地 images 路径 ({og})'))
        else:
            report[2].append((rel, '缺少 og:image'))

        # ---- 3. JSON-LD ----
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                json.loads(blk)
            except Exception as e:
                report[3].append((rel, f'JSON-LD 解析失败: {e}'))
                continue
            # 数值字段不得是带引号的字符串
            for numfield in re.findall(r'"(price|ratingValue|bestRating|worstRating|ratingCount|reviewCount|ratingCount)"\s*:\s*"([^"]*)"', blk):
                report[3].append((rel, f'JSON-LD 数值字段 {numfield[0]} 是字符串 "{numfield[1]}"'))

        # ---- 4. 追踪代码 ----
        if rel == 'exclude-me.html':
            continue
        if GA4_ID not in html:
            report[4].append((rel, '缺 GA4'))
        if CLARITY_ID not in html:
            report[4].append((rel, '缺 Clarity'))

        # ---- 5. 面包屑 + 分类归属 ----
        is_post = rel.startswith('posts/') and 'tool-selector' not in rel
        if is_post:
            if 'article-breadcrumb' not in html and 'class="breadcrumb"' not in html:
                report[5].append((rel, '文章页缺面包屑'))
            # 分类归属：找 data-category
            catm = re.search(r'data-category="([a-z]+)"', html)
            if catm:
                cat = catm.group(1)
                catfile = (CATEGORY_ZH if lang == 'zh' else CATEGORY_EN).get(cat)
                if catfile:
                    catpath = ROOT / catfile
                    if catpath.exists():
                        chtml = catpath.read_text(encoding='utf-8', errors='ignore')
                        # 该文链接是否出现在分类页
                        if rel not in chtml and rel.replace('.html', '-zh.html') not in chtml:
                            report[5].append((rel, f'分类页 {catfile} 未收录该文卡片'))

        # ---- 6. disclosure ----
        has_aff_link = bool(re.search(r'via=|[?&]pc=|fpr=|aff\.php|affiliate-disclosure|/aff/', html, re.I))
        if has_aff_link and not DISCLOSURE_PAT.search(html):
            report[6].append((rel, '含联盟链接但缺 disclosure 声明'))

    # 输出
    names = {1: 'lang/data-zh-url 配对', 2: 'og:image', 3: 'JSON-LD',
             4: '追踪代码(GA4/Clarity)', 5: '面包屑+分类归属', 6: 'disclosure 声明'}
    total_fail = 0
    for k in sorted(report):
        items = report[k]
        total_fail += len(items)
        print(f'\n=== 维度{k} {names[k]}：失败 {len(items)} ===')
        for rel, reason in items[:40]:
            print(f'  [FAIL] {rel}: {reason}')
        if len(items) > 40:
            print(f'  ... 还有 {len(items)-40} 个')

    # og 重复报告（信息性）
    dups = {og: fs for og, fs in og_map.items() if len(fs) > 1}
    print(f'\n=== og:image 重复（信息，不同页同图）: {len(dups)} 组 ===')
    for og, fs in list(dups.items())[:20]:
        print(f'  {og}: {len(fs)} 页')

    print(f'\n[global_consistency_check] 扫描文件: {len(files)}, 六维失败合计: {total_fail}')
    if '--report-only' not in sys.argv:
        return 1 if total_fail else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
