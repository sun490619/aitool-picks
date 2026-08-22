#!/usr/bin/env python3
"""
aitool-picks HTML 容器标签平衡检查。

检查结构性容器标签（div / article / section / header / footer / main / nav / aside）
是否"开闭配对"。不匹配时打印文件、行号、标签栈，exit 1；全绿 exit 0。

用法：
  python3 scripts/html_structure_check.py           # 默认：检查 git 变更/新增的 HTML 文件
  python3 scripts/html_structure_check.py --all     # 全站检查（360° 检查用）
  python3 scripts/html_structure_check.py a.html b.html   # 指定文件

pre-push 门禁：默认模式只拦本次 push 涉及的 HTML 文件，避免历史遗留问题阻塞日常提交；
同时每周 360° 检查用 --all 逐步清历史遗留。
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECK_TAGS = {"div", "article", "section", "header", "footer", "main", "nav", "aside"}
TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][a-zA-Z0-9-]*)[^>]*?>", re.S)


def strip_non_html(text: str) -> str:
    """移除注释、script、style 内容，避免误匹配。"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S | re.I)
    return text


def check_file(path: Path) -> list[str]:
    errs = []
    stack: list[tuple[str, int]] = []
    try:
        text = strip_non_html(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{path}: 无法读取: {e}"]

    lines = text.splitlines()
    line_starts = [0]
    for ln in lines:
        line_starts.append(line_starts[-1] + len(ln) + 1)

    def line_no(pos: int) -> int:
        for i, start in enumerate(line_starts):
            if start > pos:
                return i
        return len(lines)

    for m in TAG_RE.finditer(text):
        raw = m.group(0)
        slash, tag = m.group(1), m.group(2).lower()
        if tag not in CHECK_TAGS:
            continue
        # HTML5 自闭合写法 <div /> 极为罕见且非法，直接跳过
        if raw.rstrip().endswith("/>"):
            continue
        ln = line_no(m.start())
        if slash:
            if not stack:
                errs.append(f"{path}:{ln} 多余的 </{tag}>")
            elif stack[-1][0] != tag:
                expected = stack[-1]
                errs.append(
                    f"{path}:{ln} 关闭 </{tag}> 与开启 <{expected[0]}>(行{expected[1]}) 不匹配"
                )
            else:
                stack.pop()
        else:
            stack.append((tag, ln))

    for tag, ln in reversed(stack):
        errs.append(f"{path}:{ln} <{tag}> 未闭合")
    return errs


def changed_html_files() -> list[Path]:
    """取 git 工作区/暂存区/HEAD 与上游差异中的 HTML 文件。pre-push 时 HEAD 与待 push 差异也可用。"""
    # 优先取已暂存/未暂存的变更（本地跑）
    for cmd in [
        ["git", "diff", "--name-only", "--cached", "--diff-filter=ACM"],
        ["git", "diff", "--name-only", "--diff-filter=ACM"],
    ]:
        try:
            out = subprocess.check_output(cmd, cwd=REPO, text=True, stderr=subprocess.DEVNULL)
            files = [REPO / p for p in out.strip().splitlines() if p.endswith(".html")]
            if files:
                return files
        except subprocess.CalledProcessError:
            pass
    # pre-push 环境拿不到工作区差异时，取 HEAD 与默认上游差异
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD", "@{upstream}"],
            cwd=REPO, text=True, stderr=subprocess.DEVNULL
        )
        return [REPO / p for p in out.strip().splitlines() if p.endswith(".html")]
    except subprocess.CalledProcessError:
        return []


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("--all", "-a"):
            files = sorted(REPO.rglob("*.html"))
            files = [p for p in files if not any(part.startswith(".") for part in p.relative_to(REPO).parts)]
        else:
            files = [Path(p) for p in sys.argv[1:]]
    else:
        files = changed_html_files()
        if not files:
            print("🟢 没有 HTML 文件变更，跳过 HTML 结构检查。")
            sys.exit(0)

    all_errs: list[str] = []
    for f in files:
        all_errs.extend(check_file(f))

    if all_errs:
        print("🔴 HTML 结构检查失败：")
        for e in all_errs:
            print("  " + e)
        sys.exit(1)
    print(f"🟢 HTML 结构检查全绿（{len(files)} 个文件）")


if __name__ == "__main__":
    main()
