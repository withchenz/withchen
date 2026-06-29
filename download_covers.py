"""
download_covers.py
==================
把豆瓣封面图下载到本地 covers/ 目录，解决 hotlink 限制。

用法（在 个人网站 目录下运行）：
  python3 download_covers.py
"""

import json, os, time, urllib.request

COVERS_JSON = 'book_covers.json'
OUT_DIR     = 'covers'

os.makedirs(OUT_DIR, exist_ok=True)

with open(COVERS_JSON, encoding='utf-8') as f:
    data = json.load(f)

ok = fail = skip = 0

for item in data:
    url = item.get('cover_url', '')
    if not url:
        print(f'  ⚠  无封面 URL：{item["title"]}')
        fail += 1
        continue

    fname = url.split('/')[-1]
    dest  = os.path.join(OUT_DIR, fname)

    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f'  ⏭  已存在：{fname}')
        skip += 1
        continue

    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Referer':    'https://book.douban.com/',
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data_bytes = resp.read()
        if len(data_bytes) < 1000:
            raise ValueError(f'too small ({len(data_bytes)} bytes)')
        with open(dest, 'wb') as f:
            f.write(data_bytes)
        print(f'  ✓  {item["title"]} → {fname}  ({len(data_bytes)//1024} KB)')
        ok += 1
        time.sleep(0.3)
    except Exception as e:
        print(f'  ✗  {item["title"]}：{e}')
        fail += 1

print(f'\n完成：✓ {ok} 成功  ⏭ {skip} 已跳过  ✗ {fail} 失败')
print(f'封面目录：{os.path.abspath(OUT_DIR)}')
