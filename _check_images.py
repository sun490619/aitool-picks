import urllib.request, re, os, glob

# 收集所有唯一的 Unsplash URL
all_urls = set()
for f in glob.glob('**/*.html', recursive=True):
    with open(f) as fh:
        content = fh.read()
        urls = re.findall(r'https://images\.unsplash\.com/[^\s"\'>]+', content)
        for u in urls:
            # 清理 URL 末尾可能带的引号
            u = u.rstrip('"').rstrip("'")
            all_urls.add(u)

print(f'共 {len(all_urls)} 个不同的 Unsplash 图片链接\n')

ok_count = 0
fail_count = 0
failed_urls = []

for url in sorted(all_urls):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        size = len(resp.read())
        if resp.status == 200 and size > 5000:
            print(f'OK   {url}')
            ok_count += 1
        else:
            print(f'FAIL HTTP {resp.status}, {size}B  {url}')
            fail_count += 1
            failed_urls.append(url)
    except Exception as e:
        print(f'FAIL {e}  {url}')
        fail_count += 1
        failed_urls.append(url)

print(f'\n=== {ok_count} 张正常, {fail_count} 张失效 ===')

if failed_urls:
    print('\n失效的图片:')
    for u in failed_urls:
        print(f'  {u}')
