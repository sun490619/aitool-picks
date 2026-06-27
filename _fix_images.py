import os, glob, re

# ========== 定义替换映射 ==========

# 失效的 AI Video 图 → 新图
VIDEO_OLD = "1536240478700-b869070f9279"
VIDEO_NEW = "1579165466741-7f35e4755660"

# 失效的 AI 科技通用图 → 新图（多张不同的，避免所有页面用同一张）
AI_OLD = "1677442136019-21780ecad994"
AI_NEW_CANDIDATES = {
    "copy-ai":     "1620712943543-bcc4688e7485",
    "deepl":       "1485827404703-89b55fcc595e",
    "grammarly":   "1633356122544-f134324a6cee",
    "hemingway":   "1620712943543-bcc4688e7485",
    "jasper":      "1485827404703-89b55fcc595e",
    "languagetool":"1633356122544-f134324a6cee",
    "notion-ai":   "1620712943543-bcc4688e7485",
    "quillbot":    "1485827404703-89b55fcc595e",
    "rytr":        "1633356122544-f134324a6cee",
    "writesonic":  "1620712943543-bcc4688e7485",
    "coding":      "1633356122544-f134324a6cee",
    "jasper-vs-writesonic": "1485827404703-89b55fcc595e",
    "koalawriter-review-2026": "1620712943543-bcc4688e7485",
    "index":       "1633356122544-f134324a6cee",  # 首页的文章卡片图
}

# ========== 辅助函数 ==========

def replace_in_file(filepath, old_str, new_str):
    """安全替换文件中的字符串"""
    with open(filepath, 'r') as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# ========== 第一步：替换失效图片链接 ==========

print("=" * 60)
print("第一步：替换失效的 Unsplash 图片链接")
print("=" * 60)

files = glob.glob('**/*.html', recursive=True)
for f in files:
    filename = os.path.basename(f)
    
    # 替换 AI Video 图片
    if VIDEO_OLD in open(f).read():
        count = open(f).read().count(VIDEO_OLD)
        old_pattern = f"photo-{VIDEO_OLD}"
        new_pattern = f"photo-{VIDEO_NEW}"
        content = open(f).read()
        content = content.replace(old_pattern, new_pattern)
        with open(f, 'w') as fh:
            fh.write(content)
        print(f"  ✅ {filename}: 替换了 {count} 处 AI Video 图片")

print()

# 第二步：替换失效的 AI 科技图片（每个文件用不同的图）
print("=" * 60)
print("第二步：替换失效的 AI 科技通用图片（不同页面用不同图）")
print("=" * 60)

for f in files:
    content = open(f).read()
    if AI_OLD not in content:
        continue
    
    filename = os.path.basename(f)
    key = os.path.splitext(filename)[0]
    new_photo = AI_NEW_CANDIDATES.get(key, AI_NEW_CANDIDATES["index"])
    
    count = content.count(AI_OLD)
    old_pattern = f"photo-{AI_OLD}"
    new_pattern = f"photo-{new_photo}"
    content = content.replace(old_pattern, new_pattern)
    
    with open(f, 'w') as fh:
        fh.write(content)
    print(f"  ✅ {filename}: 替换了 {count} 处 → photo-{new_photo}")

# ========== 第三步：给没有内容图片的工具页/posts页添加 hero 图片 ==========

print()
print("=" * 60)
print("第三步：给缺少内容图片的页面添加 hero 图片")
print("=" * 60)

# 工具页的 hero 图片映射（用各页面 og:image 对应的图片，尺寸改为内容用）
TOOL_HERO_IMAGES = {
    "copy-ai": "1620712943543-bcc4688e7485",
    "deepl": "1485827404703-89b55fcc595e",
    "grammarly": "1633356122544-f134324a6cee",
    "hemingway": "1620712943543-bcc4688e7485",
    "jasper": "1485827404703-89b55fcc595e",
    "languagetool": "1633356122544-f134324a6cee",
    "notion-ai": "1620712943543-bcc4688e7485",
    "quillbot": "1485827404703-89b55fcc595e",
    "rytr": "1633356122544-f134324a6cee",
    "writesonic": "1620712943543-bcc4688e7485",
}

POST_HERO_IMAGES = {
    "koalawriter-review-2026": "1620712943543-bcc4688e7485",
    "originality-ai-review-2026": "1485827404703-89b55fcc595e",
}

for f in files:
    filename = os.path.basename(f)
    key = os.path.splitext(filename)[0]
    content = open(f).read()
    
    # 检查是否已有内容图片
    if '<img' in content:
        continue  # 已经有图片了
    
    # 找到 og:image 来确定用的哪个 photo id
    og_match = re.search(r'og:image.*?photo-(\w+)', content)
    if not og_match:
        continue
    
    photo_id = og_match.group(1)
    
    # 只在工具页和 posts 页添加
    is_tool = 'tools/' in f
    is_post = 'posts/' in f
    if not is_tool and not is_post:
        continue
    
    # 找到 <h1> 位置，在它前面插入图片
    h1_match = re.search(r'<h1[^>]*>', content)
    if not h1_match:
        continue
    
    # 确定 alt 文本
    alt_text = key.replace('-', ' ').title()
    
    img_html = f'<img src="https://images.unsplash.com/photo-{photo_id}?w=800&h=450&fit=crop" alt="{alt_text}" loading="lazy" style="width:100%;max-width:800px;height:auto;border-radius:12px;margin-bottom:2rem;">\n        '
    
    insert_pos = h1_match.start()
    content = content[:insert_pos] + img_html + content[insert_pos:]
    
    with open(f, 'w') as fh:
        fh.write(content)
    print(f"  ✅ {filename}: 添加了 hero 图片 (photo-{photo_id})")

print()
print("=" * 60)
print("修复完成！")
print("=" * 60)
