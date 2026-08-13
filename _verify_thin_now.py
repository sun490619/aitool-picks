import re, glob, os

def body_words(html):
    # 放宽容匹配：<article ...>...</article>，或 <div class="article-content">...</div>
    m = re.search(r'<article\b.*?</article>', html, re.S)
    if m:
        body = m.group(0)
    else:
        m2 = re.search(r'<div[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*?)</div>', html, re.S)
        if not m2:
            return None
        body = m2.group(1)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = text.strip()
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    noncjk = len(re.findall(r'[A-Za-z0-9]+', text))
    return cjk + noncjk

files = sorted(glob.glob('/Users/dawei/CodeBuddy/aitool-picks/posts/*.html'))
total=0; thin=[]
for f in files:
    html=open(f,encoding='utf-8',errors='ignore').read()
    w=body_words(html)
    if w is None:
        print(f"  [无正文容器] {os.path.basename(f)}")
        continue
    total+=1
    if w<800:
        thin.append((os.path.basename(f), w))

print(f"评测文扫描总数(有正文容器): {total}")
print(f"<800词篇数: {len(thin)}")
for name,w in sorted(thin, key=lambda x:x[1]):
    print(f"  {name}: {w}")
