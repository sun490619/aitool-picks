#!/usr/bin/env python3
"""生成 aitool-picks 的 RSS 2.0 feed.xml（含全部文章）。
Feedspot 等目录通过 RSS 里的 managingEditor/webMaster 邮箱发送所有权验证邮件，
故此处固定 sun490619@gmail.com，确保认领验证邮件能到达。"""
import os, re, subprocess, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "posts")
SITE = "https://aitool-picks.com"
EMAIL = "sun490619@gmail.com"
OUT = os.path.join(ROOT, "feed.xml")

NS_ATOM = 'xmlns:atom="http://www.w3.org/2005/Atom"'


def git_date(path):
    try:
        d = subprocess.check_output(
            ["git", "-C", ROOT, "log", "-1", "--format=%aI", "--", path],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if d:
            return d
    except Exception:
        pass
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_title(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r'<h1[^>]*class="article-title"[^>]*>(.*?)</h1>', txt, re.S | re.I)
    if not m:
        m = re.search(r'<title>(.*?)</title>', txt, re.S | re.I)
    if not m:
        return os.path.basename(path)
    t = re.sub(r"<[^>]+>", "", m.group(1))
    t = html.unescape(t).strip()
    # 去掉站点后缀 " | AI Tool Picks"
    t = re.sub(r"\s*\|\s*AI Tool Picks\s*$", "", t)
    return t


def esc(s):
    return html.escape(s, quote=True)


items = []
for fn in sorted(os.listdir(POSTS_DIR)):
    if not fn.endswith(".html"):
        continue
    p = os.path.join(POSTS_DIR, fn)
    title = extract_title(p)
    link = f"{SITE}/posts/{fn}"
    pub = git_date(p)
    try:
        pub_rfc = datetime.datetime.fromisoformat(pub.replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S +0000")
    except Exception:
        pub_rfc = pub
    items.append(
        f"    <item>\n"
        f"      <title>{esc(title)}</title>\n"
        f"      <link>{esc(link)}</link>\n"
        f"      <guid isPermaLink=\"true\">{esc(link)}</guid>\n"
        f"      <pubDate>{pub_rfc}</pubDate>\n"
        f"    </item>"
    )

now_rfc = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" {NS_ATOM}>
  <channel>
    <title>AI Tool Picks</title>
    <link>{SITE}/</link>
    <description>Honest, hands-on reviews and data on AI writing, coding, video, SEO and productivity tools.</description>
    <language>en-us</language>
    <managingEditor>{EMAIL} (AI Tool Picks)</managingEditor>
    <webMaster>{EMAIL} (AI Tool Picks)</webMaster>
    <atom:email>{EMAIL}</atom:email>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <generator>aitool-picks gen_feed.py</generator>
{chr(10).join(items)}
  </channel>
</rss>
"""
open(OUT, "w", encoding="utf-8").write(feed)
print(f"Wrote {OUT} with {len(items)} items")
