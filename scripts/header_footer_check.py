#!/usr/bin/env python3
"""aitool-picks 全局页眉页脚一致性检查脚本

用法：
  python3 scripts/header_footer_check.py

功能：
  1. 把 index.html / index-zh.html 当作 EN / ZH 的规范真源。
  2. 扫描全站所有 HTML 页面，核对以下结构与首页真源一致：
     - <html> 标签的 lang 属性
     - <html> 标签的 data-zh-url 属性（EN 页必须指向对应 ZH 页，ZH 页必须指向对应 EN 页；没有的允许为空）
     - 移动抽屉（mobile-menu-overlay + mobile-menu）整体结构
  3. 不一致时打印文件与差异线索，exit 1。

注意：
  语言判断只认 <html lang="...">，严禁用 hreflang 子串误匹配。
  与案例 22 / 案例 39（全局页眉页脚铁律）同源。
"""

import re
import sys
from pathlib import Path
from typing import Optional


def extract_mobile_drawer(html: str) -> Optional[str]:
    """从 overlay 开始提取到 mobile-menu 结束。"""
    start = html.find('<div class="mobile-menu-overlay"')
    if start == -1:
        return None
    menu_start = html.find('<div class="mobile-menu"', start)
    if menu_start == -1:
        return None
    first_gt = html.find('>', menu_start)
    if first_gt == -1:
        return None
    pos = first_gt + 1
    depth = 1
    while pos < len(html) and depth > 0:
        next_open = html.find('<div', pos)
        next_close = html.find('</div>', pos)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return html[start:pos]


def normalize_drawer(drawer: str, lang: str) -> str:
    """把 drawer 里会随页面变化的属性替换为占位符，只比较结构。"""
    # data-zh-url 指向不同页面
    drawer = re.sub(r'data-zh-url="[^"]*"', 'data-zh-url="..."', drawer)
    # active / aria-pressed 随当前语言变化
    drawer = re.sub(r'class="active"\s+data-lang="en"', 'CLASS_ACTIVE data-lang="en"', drawer)
    drawer = re.sub(r'class="active"\s+data-lang="zh"', 'CLASS_ACTIVE data-lang="zh"', drawer)
    drawer = re.sub(r'aria-pressed="(true|false)"', 'aria-pressed="BOOL"', drawer)
    # 连续空白统一
    drawer = re.sub(r'\s+', ' ', drawer)
    return drawer.strip()


def main() -> int:
    root = Path(__file__).resolve().parent.parent

    en_html = (root / 'index.html').read_text(encoding='utf-8')
    zh_html = (root / 'index-zh.html').read_text(encoding='utf-8')

    en_drawer = extract_mobile_drawer(en_html)
    zh_drawer = extract_mobile_drawer(zh_html)

    if not en_drawer or not zh_drawer:
        print('[FAIL] 首页或中文首页无法提取 mobile drawer，检查 index.html / index-zh.html 结构')
        return 1

    en_canonical = normalize_drawer(en_drawer, 'en')
    zh_canonical = normalize_drawer(zh_drawer, 'zh')

    SKIP_DIRS = {'_preview', '_review', '_tmp_ogsrc', 'node_modules', '.git'}
    def should_skip(f: Path) -> bool:
        rel = f.relative_to(root)
        parts = rel.parts
        if f.name == 'exclude-me.html':
            return True
        if any(part in SKIP_DIRS for part in parts):
            return True
        # images/samples 子目录
        if len(parts) >= 2 and parts[0] == 'images' and parts[1] == 'samples':
            return True
        return False
    files = [f for f in root.rglob('*.html')
             if '.git' not in str(f) and 'node_modules' not in str(f) and not should_skip(f)]

    failures = []
    checked = 0

    for f in files:
        html = f.read_text(encoding='utf-8')
        rel = str(f.relative_to(root))

        m = re.search(r'<html\s+[^>]*lang="(en|zh)"', html[:500])
        if not m:
            failures.append((rel, '无法判断语言（缺少 <html lang>）'))
            continue
        lang = m.group(1)

        # data-zh-url 规则：EN 页若有对应 ZH 文件则必须声明；ZH 页若有对应 EN 文件则必须声明
        zh_path = str(f).replace('.html', '-zh.html')
        en_path = str(f).replace('-zh.html', '.html')
        has_zh = Path(zh_path).exists()
        has_en = Path(en_path).exists()

        data_zh_m = re.search(r'<html\s+[^>]*data-zh-url="([^"]*)"', html[:500])
        has_data_zh = bool(data_zh_m)

        # —— 配对正确性硬检查（防复发：指向自身 / 指向不存在文件）——
        if has_data_zh:
            declared = data_zh_m.group(1).strip()
            self_path = '/' + rel
            if declared.rstrip('/') == self_path.rstrip('/'):
                failures.append((rel, f'data-zh-url 指向自身（{declared}），语言切换会自指，必须指向真实对应语言页'))
            elif not (root / declared.lstrip('/')).exists():
                failures.append((rel, f'data-zh-url 指向不存在文件（{declared}）'))

        if lang == 'en':
            if has_zh and not has_data_zh:
                failures.append((rel, f'EN 页有对应 ZH 文件，但缺少 data-zh-url（应为 /{rel.replace(".html", "-zh.html")}）'))
            elif not has_zh and has_data_zh:
                failures.append((rel, f'EN 页无对应 ZH 文件，却声明了 data-zh-url'))
        else:
            if has_en and not has_data_zh:
                failures.append((rel, f'ZH 页有对应 EN 文件，但缺少 data-zh-url（应为 /{rel.replace("-zh.html", ".html")}）'))
            elif not has_en and has_data_zh:
                failures.append((rel, f'ZH 页无对应 EN 文件，却声明了 data-zh-url'))

        # mobile drawer 结构一致性
        drawer = extract_mobile_drawer(html)
        if drawer is None:
            failures.append((rel, '缺少 mobile drawer（mobile-menu-overlay / mobile-menu）'))
            checked += 1
            continue

        norm = normalize_drawer(drawer, lang)
        canonical = en_canonical if lang == 'en' else zh_canonical
        if norm != canonical:
            failures.append((rel, f'mobile drawer 结构与首页 {lang.upper()} 真源不一致'))

        checked += 1

    print(f'[header_footer_check] 检查文件: {checked}, 失败: {len(failures)}')
    for rel, reason in failures[:30]:
        print(f'  [FAIL] {rel}: {reason}')
    if len(failures) > 30:
        print(f'  ... 还有 {len(failures) - 30} 个失败')

    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
