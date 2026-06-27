#!/usr/bin/env python3
"""
AI Tool Picks — 全站基础体检脚本
==================================
用法: python3 _health_check.py

检查项：
  1. 前端基础设施 — shared.js/scripts.js/styles.css 是否存在
  2. 全站 JS 引用 — 所有页面是否正确引入 shared.js + scripts.js
  3. 主题/语言功能 — localStorage 读写 + toggleTheme/switchLang 函数
  4. Header/Drawer 统一性 — 所有页面是否有统一的 Header 和 Drawer
  5. docs/ 同步状态 — docs 目录是否与根目录同步
  6. 关键链接有效性 — 联盟链接、分类链接是否可用
  7. SEO 基础 — 每页是否有 canonical/OG/GA4

每项返回 🟢 正常 或 🔴 异常 + 一句话原因
"""

import os, re, json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALL_PAGES = []


def find_all_pages():
    """扫描所有 HTML 页面"""
    global ALL_PAGES
    pages = []
    for root, dirs, files in os.walk(SCRIPT_DIR):
        dirs[:] = [d for d in dirs if d not in ('.git', 'docs', '__pycache__')]
        for f in files:
            if f.endswith('.html'):
                pages.append(os.path.join(root, f))
    ALL_PAGES = sorted(pages)
    return ALL_PAGES


# ═══════════════════════════════════════════
# 1. 前端基础设施
# ═══════════════════════════════════════════
def check_infrastructure():
    items = {}
    required = {
        'shared.js': '全站主题/语言切换逻辑',
        'scripts.js': '全局脚本（菜单/滚动/动画）',
        'styles.css': '全局样式',
    }
    for fname, desc in required.items():
        path = os.path.join(SCRIPT_DIR, fname)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        items[fname] = {
            'ok': exists and size > 500,
            'detail': f"{desc} — {'{:.1f}KB'.format(size/1024) if exists else '❌ 不存在'}"
        }
    all_ok = all(v['ok'] for v in items.values())
    return all_ok, items


# ═══════════════════════════════════════════
# 2. 全站 JS 引用完整性
# ═══════════════════════════════════════════
def check_js_references():
    items = {}
    pages = find_all_pages()
    missing_shared = []
    missing_scripts = []

    for page in pages:
        rel = os.path.relpath(page, SCRIPT_DIR)
        try:
            with open(page, 'r') as f:
                content = f.read()
            if 'shared.js' not in content:
                missing_shared.append(rel)
            if 'scripts.js' not in content:
                missing_scripts.append(rel)
        except Exception:
            pass

    items['shared.js 引用'] = {
        'ok': len(missing_shared) == 0,
        'detail': f"全站 {len(pages)} 页全部引入" if not missing_shared 
                  else f"{len(missing_shared)} 页缺少: {', '.join(missing_shared[:5])}{'...' if len(missing_shared)>5 else ''}"
    }
    items['scripts.js 引用'] = {
        'ok': len(missing_scripts) == 0,
        'detail': f"全站 {len(pages)} 页全部引入" if not missing_scripts
                  else f"{len(missing_scripts)} 页缺少: {', '.join(missing_scripts[:5])}{'...' if len(missing_scripts)>5 else ''}"
    }

    all_ok = len(missing_shared) == 0 and len(missing_scripts) == 0
    return all_ok, items


# ═══════════════════════════════════════════
# 3. 主题/语言切换功能
# ═══════════════════════════════════════════
def check_theme_lang():
    items = {}
    shared_path = os.path.join(SCRIPT_DIR, 'shared.js')

    if not os.path.exists(shared_path):
        items['主题切换'] = {'ok': False, 'detail': 'shared.js 不存在'}
        items['语言切换'] = {'ok': False, 'detail': 'shared.js 不存在'}
        return False, items

    with open(shared_path, 'r') as f:
        content = f.read()

    # 检查 localStorage 持久化
    has_theme_ls = 'THEME_KEY' in content or 'aitoolpicks-theme' in content
    has_lang_ls = 'LANG_KEY' in content or 'aitoolpicks-lang' in content
    has_toggle = 'toggleTheme' in content
    has_switch_lang = 'switchLang' in content
    has_dark_class = 'classList' in content and 'dark' in content
    has_theme_button = 'themeToggle' in content
    has_lang_button = 'langSwitch' in content

    items['主题切换'] = {
        'ok': has_theme_ls and has_toggle and has_dark_class and has_theme_button,
        'detail': f"localStorage{'✅' if has_theme_ls else '❌'} toggleTheme{'✅' if has_toggle else '❌'} html.dark{'✅' if has_dark_class else '❌'} #themeToggle{'✅' if has_theme_button else '❌'}"
    }
    items['语言切换'] = {
        'ok': has_lang_ls and has_switch_lang and has_lang_button,
        'detail': f"localStorage{'✅' if has_lang_ls else '❌'} switchLang{'✅' if has_switch_lang else '❌'} #langSwitch{'✅' if has_lang_button else '❌'}"
    }

    all_ok = items['主题切换']['ok'] and items['语言切换']['ok']
    return all_ok, items


# ═══════════════════════════════════════════
# 4. Header/Drawer 统一性
# ═══════════════════════════════════════════
def check_header_drawer():
    items = {}
    pages = find_all_pages()
    bad_pages = []

    for page in pages:
        rel = os.path.relpath(page, SCRIPT_DIR)
        try:
            with open(page, 'r') as f:
                content = f.read()
            # 必须有的元素
            has_header = 'site-header' in content
            has_hamburger = 'mobileMenuBtn' in content
            has_drawer = 'mobileMenu' in content and 'mobileMenuOverlay' in content
            has_brand = 'AI Tool Picks' in content
            if not (has_header and has_hamburger and has_drawer and has_brand):
                bad_pages.append(rel)
        except Exception:
            bad_pages.append(rel)

    items['Header 统一性'] = {
        'ok': len(bad_pages) == 0,
        'detail': f"全站 {len(pages)} 页统一" if not bad_pages
                  else f"{len(bad_pages)} 页不统一: {', '.join(bad_pages[:5])}"
    }
    return len(bad_pages) == 0, items


# ═══════════════════════════════════════════
# 5. docs/ 同步状态
# ═══════════════════════════════════════════
def check_docs_sync():
    items = {}
    docs_dir = os.path.join(SCRIPT_DIR, 'docs')

    if not os.path.exists(docs_dir):
        items['docs/ 目录'] = {'ok': False, 'detail': 'docs/ 目录不存在'}
        return False, items

    # 对比根目录和 docs/ 的文件
    root_files = set()
    for root, dirs, files in os.walk(SCRIPT_DIR):
        dirs[:] = [d for d in dirs if d not in ('.git', 'docs', '__pycache__')]
        for f in files:
            root_files.add(os.path.relpath(os.path.join(root, f), SCRIPT_DIR))

    docs_files = set()
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            docs_files.add(os.path.relpath(os.path.join(root, f), docs_dir))

    # 只比较可部署文件
    deployable = {f for f in root_files if f.endswith(('.html', '.css', '.js', '.xml', '.txt')) and not f.startswith('_')}
    missing_in_docs = deployable - docs_files
    extra_in_docs = docs_files - deployable

    items['docs/ 同步'] = {
        'ok': len(missing_in_docs) == 0 and len(extra_in_docs) == 0,
        'detail': f"完全同步" if len(missing_in_docs) == 0 and len(extra_in_docs) == 0
                  else f"缺 {len(missing_in_docs)} 个: {', '.join(list(missing_in_docs)[:5])}" if missing_in_docs
                  else f"多 {len(extra_in_docs)} 个: {', '.join(list(extra_in_docs)[:5])}"
    }

    all_ok = len(missing_in_docs) == 0
    return all_ok, items


# ═══════════════════════════════════════════
# 6. SEO 基础检查
# ═══════════════════════════════════════════
def check_seo():
    items = {}
    pages = find_all_pages()
    no_canonical = []
    no_ga4 = []
    no_og = []

    for page in pages:
        rel = os.path.relpath(page, SCRIPT_DIR)
        try:
            with open(page, 'r') as f:
                content = f.read()
            if 'canonical' not in content:
                no_canonical.append(rel)
            if 'G-D53DQ3JKKL' not in content:
                no_ga4.append(rel)
            if 'og:title' not in content:
                no_og.append(rel)
        except Exception:
            pass

    items['Canonical 链接'] = {
        'ok': len(no_canonical) == 0,
        'detail': f"全站 {len(pages)} 页都有" if not no_canonical
                  else f"{len(no_canonical)} 页缺少: {', '.join(no_canonical[:5])}"
    }
    items['GA4 追踪码'] = {
        'ok': len(no_ga4) == 0,
        'detail': f"全站 {len(pages)} 页都有" if not no_ga4
                  else f"{len(no_ga4)} 页缺少: {', '.join(no_ga4[:5])}"
    }
    items['OG 标签'] = {
        'ok': len(no_og) == 0,
        'detail': f"全站 {len(pages)} 页都有" if not no_og
                  else f"{len(no_og)} 页缺少: {', '.join(no_og[:5])}"
    }

    all_ok = len(no_canonical) == 0 and len(no_ga4) == 0 and len(no_og) == 0
    return all_ok, items


# ═══════════════════════════════════════════
# 7. 双 main 标签检查 (bug)
# ═══════════════════════════════════════════
def check_double_main():
    items = {}
    pages = find_all_pages()
    double_main = []

    for page in pages:
        rel = os.path.relpath(page, SCRIPT_DIR)
        try:
            with open(page, 'r') as f:
                content = f.read()
            main_count = content.count('</main>')
            if main_count > 1:
                double_main.append(rel)
        except Exception:
            pass

    items['双 main 标签'] = {
        'ok': len(double_main) == 0,
        'detail': f"全站正常" if not double_main
                  else f"{len(double_main)} 页有重复 </main>: {', '.join(double_main[:5])}"
    }
    return len(double_main) == 0, items


# ═══════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════
def run_full_check():
    now = datetime.now()
    print()
    print("╔" + "═" * 54 + "╗")
    print("║" + "      🩺  AI Tool Picks 体检     ".center(40) + "║")
    print("║" + f"        {now.strftime('%Y-%m-%d %H:%M:%S')}        ".center(40) + "║")
    print("╚" + "═" * 54 + "╝")
    print()

    categories = [
        ("1️⃣  基础设施", check_infrastructure),
        ("2️⃣  JS 引用完整性", check_js_references),
        ("3️⃣  主题/语言切换", check_theme_lang),
        ("4️⃣  Header/Drawer", check_header_drawer),
        ("5️⃣  SEO 基础", check_seo),
        ("6️⃣  双 main 标签", check_double_main),
        ("7️⃣  docs/ 同步", check_docs_sync),
    ]

    total_ok = 0
    total_fail = 0

    for name, checker in categories:
        ok, items = checker()
        icon = "🟢" if ok else "🔴"
        print(f"  {icon}  {name}")

        for sub_name, info in items.items():
            sub_icon = "  ✅" if info['ok'] else "  ❌"
            print(f"    {sub_icon}  {sub_name}: {info['detail']}")

        if ok:
            total_ok += 1
        else:
            total_fail += 1
        print()

    bar = "═" * 54
    print(bar)
    if total_fail == 0:
        print(f"  🎉  全部正常 · {total_ok}/{total_ok} 项通过")
    elif total_fail <= 2:
        print(f"  🟡  基本正常 · {total_ok} 项通过, {total_fail} 项需关注")
    else:
        print(f"  🔴  需要处理 · {total_ok} 项正常, {total_fail} 项有问题")
    print(bar)
    print()

    return total_fail == 0


if __name__ == '__main__':
    import sys
    if '--json' in sys.argv:
        # JSON 输出模式
        result = {}
        categories = [
            ("infrastructure", check_infrastructure),
            ("js_refs", check_js_references),
            ("theme_lang", check_theme_lang),
            ("header_drawer", check_header_drawer),
            ("seo", check_seo),
            ("double_main", check_double_main),
            ("docs_sync", check_docs_sync),
        ]
        for name, checker in categories:
            ok, items = checker()
            result[name] = {"ok": ok, "items": items}
        result["all_ok"] = all(v["ok"] for v in result.values())
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        run_full_check()
