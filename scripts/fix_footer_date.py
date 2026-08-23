#!/usr/bin/env python3
"""A档: 补页脚 Updated 日期(规则§一⑫必备)。
真实日期取自该文 <time datetime="YYYY-MM-DD"> 标签(发布日=最后更新日,真实不编造)。
EN: "Updated July 12, 2026"  /  ZH: "更新于 2026 年 7 月 12 日"
插入位置: article-meta 块之后(与 ai-coding 范本一致)。
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = sorted(REPO.rglob("posts/*.html"))
DRY = "--dry" in sys.argv

MONTHS = {"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June",
          "07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"}
MONTHS_ZH = {"01":"1","02":"2","03":"3","04":"4","05":"5","06":"6","07":"7","08":"8","09":"9","10":"10","11":"11","12":"12"}

DATE_RE = re.compile(r'<time datetime="(\d{4})-(\d{2})-(\d{2})"')

def fix_one(p: Path):
    t = p.read_text(encoding="utf-8")
    if re.search(r'Updated [A-Z][a-z]+ \d|更新于 \d{4}', t, re.I):
        return False, "已有"
    m = DATE_RE.search(t)
    if not m:
        return False, "无time"
    y, mo, d = m.group(1), m.group(2), m.group(3)
    # 仅认 <html lang="zh"> 作为中文页判定(排除 hreflang="zh" 误判)
    is_zh = bool(re.search(r'<html[^>]*lang="zh"', t, re.I))
    if is_zh:
        snippet = f'        <p class="post-meta">更新于 {y} 年 {MONTHS_ZH[mo]} 月 {int(d)} 日</p>'
    else:
        snippet = f'        <p class="post-meta">Updated {MONTHS[mo]} {int(d)}, {y}</p>'
    # 插入到 article-meta 块后(找最后一个 </div> 紧跟 min read 的块之后)
    meta = re.search(r'(<div class="article-meta">.*?</div>)', t, re.S | re.I)
    if not meta:
        # 兜底:插到 <h1 后
        return False, "无meta锚点"
    new = t[:meta.end()] + "\n" + snippet + t[meta.end():]
    if not DRY:
        p.write_text(new, encoding="utf-8")
    return True, snippet


if __name__ == "__main__":
    done = 0
    for p in POSTS:
        ok, msg = fix_one(p)
        if ok:
            done += 1
            if DRY:
                print(f"[DRY] {p.name}: {msg}")
    print(f"\n{'[DRY] ' if DRY else ''}补日期完成: {done} 篇")
