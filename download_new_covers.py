"""
download_new_covers.py
======================
下载新增书目的豆瓣封面到 covers/ 目录。
用法（在 个人网站 目录下运行）：
    python3 download_new_covers.py
"""
import urllib.request, os, time

OUT_DIR = 'covers'
os.makedirs(OUT_DIR, exist_ok=True)

# (书名, 封面 URL, 本地文件名)
NEW_COVERS = [
    # ── 存在取向 ─────────────────────────────
    ('祈望神话',                          'https://img3.doubanio.com/view/subject/l/public/s11277712.jpg',  's11277712.jpg'),
    ('存在∶精神病学和心理学的新方向',      'https://img3.doubanio.com/view/subject/l/public/s8935092.jpg',   's8935092.jpg'),
    ('人的自我寻求',                       'https://img9.doubanio.com/view/subject/l/public/s27134464.jpg',  's27134464.jpg'),
    ('存在之发现',                         'https://img9.doubanio.com/view/subject/l/public/s4544634.jpg',   's4544634.jpg'),
    ('自由与命运',                         'https://img3.doubanio.com/view/subject/l/public/s4404472.jpg',   's4404472.jpg'),
    ('给心理治疗师的礼物',                 'https://img9.doubanio.com/view/subject/l/public/s28914594.jpg',  's28914594.jpg'),
    ('日益亲近',                           'https://img9.doubanio.com/view/subject/l/public/s28248445.jpg',  's28248445.jpg'),
    ('在生命最深处与人相遇',               'https://img1.doubanio.com/view/subject/l/public/s35476718.jpg',  's35476718.jpg'),
    ('唤醒敬畏',                           'https://img2.doubanio.com/view/subject/l/public/s7645431.jpg',   's7645431.jpg'),
    ('存在主义世界的幸福',                 'https://img1.doubanio.com/view/subject/l/public/s10242198.jpg',  's10242198.jpg'),
    ('存在主义心理学的邀请',               'https://img3.doubanio.com/view/subject/l/public/s34270657.jpg',  's34270657.jpg'),
    ('存在主义治疗100个关键点与技巧',      'https://img3.doubanio.com/view/subject/l/public/s33525123.jpg',  's33525123.jpg'),
    # ── 人本取向 ─────────────────────────────
    ('以人为中心心理治疗',                 'https://img3.doubanio.com/view/subject/l/public/s7029217.jpg',   's7029217.jpg'),
    ('卡尔·罗杰斯论会心团体',             'https://img2.doubanio.com/view/subject/l/public/s1698061.jpg',   's1698061.jpg'),
    ('个人形成论',                         'https://img3.doubanio.com/view/subject/l/public/s6002743.jpg',   's6002743.jpg'),
    ('卡尔·罗杰斯传记',                   'https://img1.doubanio.com/view/subject/l/public/s28383150.jpg',  's28383150.jpg'),
    ('罗杰斯著作精粹',                     'https://img3.doubanio.com/view/subject/l/public/s2167413.jpg',   's2167413.jpg'),
    ('论人的成长',                         'https://img1.doubanio.com/view/subject/l/public/s27733788.jpg',  's27733788.jpg'),
    ('自由学习',                           'https://img9.doubanio.com/view/subject/l/public/s28027485.jpg',  's28027485.jpg'),
    ('卡尔·罗杰斯：对话录',               'https://img1.doubanio.com/view/subject/l/public/s3864818.jpg',   's3864818.jpg'),
    ('罗杰斯心理治疗—经典个案及专家点评', 'https://img9.doubanio.com/view/subject/l/public/s11272865.jpg',  's11272865.jpg'),
    ('罗杰斯：心理健康思想解析',          'https://img1.doubanio.com/view/subject/l/public/s28534089.jpg',  's28534089.jpg'),
    ('人性的迷失与复归',                   'https://img9.doubanio.com/view/subject/l/public/s1020914.jpg',   's1020914.jpg'),
    ('人性的彰显：人本主义心理学',        'https://img9.doubanio.com/view/subject/l/public/s26164755.jpg',  's26164755.jpg'),
    ('三种心理学',                         'https://img1.doubanio.com/view/subject/l/public/s4192050.jpg',   's4192050.jpg'),
    ('游戏治疗',                           'https://img9.doubanio.com/view/subject/l/public/s27850645.jpg',  's27850645.jpg'),
    ('生活本无应许之地',                   'https://img9.doubanio.com/view/subject/l/public/s34632075.jpg',  's34632075.jpg'),
    # ── 补充：原无封面的 4 本 ─────────────
    ('分裂的自我（莱恩）',                 'https://img1.doubanio.com/view/subject/l/public/s34229940.jpg',  's34229940.jpg'),
    ('知觉现象学（梅洛-庞蒂）',           'https://img9.doubanio.com/view/subject/l/public/s34351316.jpg',  's34351316.jpg'),
    ('存在—人本主义治疗（施奈德）',       'https://img9.doubanio.com/view/subject/l/public/s8968686.jpg',   's8968686.jpg'),
    ('总体与无限（列维纳斯）',             'https://img1.doubanio.com/view/subject/l/public/s29017959.jpg',  's29017959.jpg'),
    # ── 补充：仍缺封面的 3 本 ─────────────
    ('当事人中心治疗（罗杰斯）',           'https://img2.doubanio.com/view/subject/l/public/s1139391.jpg',   's1139391.jpg'),
    ('The Ethics of Ambiguity（波伏娃）', 'https://img2.doubanio.com/view/subject/l/public/s4200371.jpg',   's4200371.jpg'),
    ('存在主义心理学整合临床观（May）',    'https://img3.doubanio.com/view/subject/l/public/s11220262.jpg',  's11220262.jpg'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://book.douban.com/',
}

ok = fail = skip = 0
for title, url, fname in NEW_COVERS:
    dest = os.path.join(OUT_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f'  ⏭  已存在：{fname}')
        skip += 1
        continue
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        if len(data) < 1000:
            raise ValueError(f'图片太小 ({len(data)} bytes)')
        with open(dest, 'wb') as f:
            f.write(data)
        print(f'  ✓  {title} → {fname}  ({len(data)//1024} KB)')
        ok += 1
        time.sleep(0.3)
    except Exception as e:
        print(f'  ✗  {title}：{e}')
        fail += 1

print(f'\n完成：✓ {ok} 成功  ⏭ {skip} 已跳过  ✗ {fail} 失败')
print(f'封面目录：{os.path.abspath(OUT_DIR)}')
