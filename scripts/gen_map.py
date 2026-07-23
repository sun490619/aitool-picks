#!/usr/bin/env python3
"""生成 文件名 -> Unsplash photo id 映射（顺序循环唯一分配）。
按文件名排序后，第 i 个目标用 idpool[i % len(pool)]，保证跨主题打散、复用对主题不同。
"""
import os

IMG = "/Users/dawei/CodeBuddy/aitool-picks/images"
POOL = [l.strip() for l in open("/tmp/idpool.txt") if l.strip()]

def theme_for(name):
    n = name.lower()
    if "vs" in n: return "comparison"
    if "seo" in n or "generative-engine" in n or "geo" in n: return "seo"
    if "writing" in n or "grammar" in n or "wordtune" in n or "copy" in n or "rytr" in n or "koala" in n or "quillbot" in n or "hemingway" in n or "languagetool" in n:
        if "grammar" in n: return "grammar"
        return "writing"
    if "translation" in n or "deepl" in n: return "translation"
    if "email" in n: return "email"
    if "video" in n or "runway" in n or "sora" in n or "kling" in n or "descript" in n:
        if "avatar" in n: return "avatar"
        if "faceless" in n: return "faceless"
        return "video"
    if "coding" in n or "cursor" in n or "copilot" in n or "replit" in n or "code" in n or "langchain" in n or "hugging" in n or "github" in n:
        if "open-source" in n or "hugging" in n: return "openmodel"
        return "coding"
    if "image" in n or "midjourney" in n or "upscaler" in n or "canva" in n:
        if "upscaler" in n: return "upscaler"
        return "image"
    if "music" in n: return "music"
    if "podcast" in n: return "podcast"
    if "voice" in n: return "voice"
    if "audio" in n: return "audio"
    if "note" in n or "notion" in n or "mem-ai" in n: return "note"
    if "presentation" in n: return "presentation"
    if "trip" in n or "planner" in n: return "trip"
    if "dropshipping" in n: return "dropshipping"
    if "support" in n or "customer" in n: return "support"
    if "side-hustle" in n or "sidehustle" in n: return "sidehustle"
    if "small-business" in n: return "smallbiz"
    if "student" in n: return "student"
    if "business" in n: return "business"
    if "productivity" in n or "zapier" in n: return "productivity"
    if "market" in n: return "market"
    if "visibility" in n or "brand" in n: return "visibility"
    if "home" in n: return "home"
    return "generic"

targets = []
for fn in sorted(os.listdir(IMG)):
    if fn.startswith("og-") and fn.endswith(".jpg"):
        targets.append((fn, 1200, 630))
    elif fn.startswith("u") and fn.endswith(".jpg") and fn[1:-4].isdigit():
        targets.append((fn, 800, 450))

lines = []
for i, (fn, tw, th) in enumerate(targets):
    pid = POOL[i % len(POOL)]
    lines.append(f"{fn}\t{pid}\t{theme_for(fn)}\t{tw}x{th}")

with open("/tmp/photomap.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

# 唯一性统计
used = [POOL[i % len(POOL)] for i in range(len(targets))]
from collections import Counter
c = Counter(used)
print(f"目标 {len(targets)} 个, 池 {len(POOL)} 个, 最大复用 {max(c.values())} 次, 唯一图 {len(set(used))}")
