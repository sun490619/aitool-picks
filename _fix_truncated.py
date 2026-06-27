import os, glob, re

# 修复第三步中 og_match 匹配不完整导致的问题
# og:image 的 URL 是 .../photo-1620712943543-bcc4688e7485?w=1200...
# 但 regex 只匹配到 photo-1620712943543（缺少 -bcc4688e7485）
# 导致插入的 img src 变成 photo-1620712943543?w=800（缺少后半段 ID）

# 映射：短 ID → 完整 ID
SHORT_TO_FULL = {
    "1485827404703": "1485827404703-89b55fcc595e",
    "1558494949":    "1558494949-ef010cbdcc31",
    "1620712943543": "1620712943543-bcc4688e7485",
    "1633356122544": "1633356122544-f134324a6cee",
}

files = glob.glob('**/*.html', recursive=True)
fixed_count = 0

for f in files:
    content = open(f).read()
    original = content
    
    for short_id, full_id in SHORT_TO_FULL.items():
        # 修复 photo-{short_id}?w=... 格式（缺少完整 ID）
        bad_pattern = f"photo-{short_id}?"
        if bad_pattern in content:
            # 需要知道完整 ID 的后缀
            suffix = full_id[len(short_id):]  # e.g. "-bcc4688e7485"
            content = content.replace(
                f"photo-{short_id}?",
                f"photo-{full_id}?"
            )
    
    if content != original:
        with open(f, 'w') as fh:
            fh.write(content)
        fixed_count += 1
        print(f"  ✅ {os.path.basename(f)}")

print(f"\n共修复 {fixed_count} 个文件")
