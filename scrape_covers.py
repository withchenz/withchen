#!/usr/bin/env python3
"""
微信文章封面图爬虫
=======================================
从 articles.json 里读取没有封面图的文章，访问每个 URL 抓取 og:image，
写回 articles.json。

运行：
  python3 scrape_covers.py

说明：
  - 浏览器会打开，如遇微信验证页面请手动通过
  - 每 20 篇自动保存一次，中断后再跑会跳过已有封面的文章
  - 建议先跑 process_excel.py 再跑这个
"""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

JSON_PATH = Path(__file__).parent / "articles.json"
DELAY_MS  = 800   # 每篇之间等待（毫秒）


async def get_cover(page, url: str) -> str:
    """访问文章页面，提取 og:image"""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(1200)

        cover = await page.evaluate("""
            () => {
                const selectors = [
                    'meta[property="og:image"]',
                    'meta[name="og:image"]',
                    'meta[property="twitter:image"]',
                    'meta[name="twitter:image"]',
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) {
                        const v = el.getAttribute('content') || '';
                        if (v && !v.startsWith('data:')) return v;
                    }
                }
                return '';
            }
        """)
        return cover or ""
    except Exception as e:
        print(f"    ⚠️  失败：{str(e)[:80]}")
        return ""


async def main():
    data = JSON_PATH.read_text(encoding="utf-8")
    articles = json.loads(data)

    need = [(i, a) for i, a in enumerate(articles) if not a.get("cover_img")]
    total = len(articles)
    print(f"共 {total} 篇，需抓封面图：{len(need)} 篇")

    if not need:
        print("全部已有封面图，无需爬取。")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=80,
            args=["--window-size=1280,900"],
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page = await context.new_page()

        success = 0
        for idx, (art_idx, art) in enumerate(need, 1):
            short_title = art["title"][:35]
            print(f"[{idx}/{len(need)}] {short_title}...", end=" ")

            cover = await get_cover(page, art["url"])
            if cover:
                articles[art_idx]["cover_img"] = cover
                success += 1
                print(f"✓")
            else:
                print(f"✗ (无封面)")

            # 每 20 篇保存一次防丢失
            if idx % 20 == 0:
                JSON_PATH.write_text(
                    json.dumps(articles, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"  💾 已保存进度 {success}/{idx}")

            await page.wait_for_timeout(DELAY_MS)

        await browser.close()

    # 最终写回
    JSON_PATH.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n✅ 完成！{success}/{len(need)} 篇封面图抓取成功")
    print(f"   articles.json 已更新：{JSON_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
