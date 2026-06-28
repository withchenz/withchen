# withchen.com · 项目交接 Memo
> 最后更新：2026-06-28

---

## 0. 基本信息

| 项目 | 内容 |
|---|---|
| 网站域名 | withchen.com |
| GitHub 仓库 | withchenz/withchen |
| GitHub PAT | 见本地密码管理器，勿存入 repo |
| 部署平台 | Vercel（绑 GitHub 自动部署）|
| CDN | Cloudflare（China 访问加速）|
| 本地文件夹 | /Users/adminx/Desktop/个人网站/ |

**安全规则：没有用户确认，不得 push 到 GitHub。**

---

## 0.5 核心目标

**articles.html 的核心目标是 SEO**，让用户在 Google / 百度 / 微信搜索「越南攻略」「老挝旅游」「新加坡生活」等关键词时能搜到 withchen 的文章。

SEO 设计要点（写代码时必须遵守）：
- articles.html 本身必须有静态可索引的文章内容，不能全靠 JS 动态渲染（爬虫看不到）
- 每篇文章应有独立的 `<a href>` 链接（不能只用 `onclick`），让爬虫能跟进
- 页面 `<title>` 和 `<meta description>` 需包含核心关键词（旅行、东南亚、攻略等）
- 文章卡片的标题必须是真实 `<h2>` 或 `<h3>` 标签，不能只是 `<div>`
- 封面图需要 `alt` 属性，包含文章标题关键词
- 考虑生成 sitemap.xml 让搜索引擎更快收录

---

## 1. 设计系统

### 颜色变量（所有页面统一）
```css
:root {
  --blue:       #74B9E8;
  --blue-deep:  #4A9BD4;
  --blue-light: #D0E9F7;
  --cream:      #F7F3EC;
  --ink:        #2C2C2C;
  --green:      #8BBF9F;
  --coral:      #E8734A;
  --purple:     #9B8BC4;
}
```

### 字体
- **Caveat** — 手写风格，用于标题、logo、数字装饰
- **Noto Sans SC 300** — 正文中文
- **Inter 300** — 英文辅助

字体通过 `fonts.loli.net` 加载（国内镜像，替代 Google Fonts）。

### 底部 pill 导航（6 项，全部页面统一）
```html
<nav class="site-nav">
  <a href="index.html"><span class="nn">01</span> 首页</a>
  <a href="about.html"><span class="nn">02</span> 关于我</a>
  <a href="articles.html"><span class="nn">03</span> 星星七便士</a>
  <a href="podcast.html"><span class="nn">04</span> 播客-小心思-</a>
  <a href="theater.html"><span class="nn">05</span> 心理探险家</a>
  <a href="consult.html"><span class="nn">06</span> 咨询预约</a>
</nav>
```

手机适配 CSS（所有页面都有）：
```css
@media (max-width: 600px) {
  .site-nav { gap: 0; padding: 0.22rem; }
  .site-nav a { font-size: 0; padding: 0.38rem 0.62rem; }
  .site-nav .nn { font-size: 0.7rem; opacity: 0.65; }
  .site-nav a.active .nn { opacity: 0.55; }
}
```
原理：`font-size: 0` 让中文文字消失（text node），`.nn` 上的 explicit `font-size` 恢复数字显示。

---

## 2. 页面清单与当前状态

### ✅ index.html — 首页
- 品牌蓝 `#74B9E8` 背景
- 大标题 "CHEN"（Caveat 字体）
- 鼠标探照灯效果（canvas）
- 星星 sparkle 背景动画
- 底部 6 项导航（首页 active）
- **已推送上线**

### ✅ about.html — 关于我
- 奶油色背景
- 顶部 `gouzihewo.png` 插画
- 白色卡片：ChenChen 自我介绍 + 身份标签（内容创作者 / 播客主播 / 存在人本取向咨询师）
- 联系邮件：zhengchencandy@gmail.com
- 底部 6 项导航（关于我 active）
- **已推送上线**

### ✅ articles.html — 星星与七便士（公众号文章）
- 奶油色背景
- 打字机动画标题 "星星与七便士"（Caveat，逐字显示，打完后光标消失）
- `fetch('./articles.json')` 读取文章数据
- skeleton loading（4个闪光占位卡片）
- 动态分类 tab（从 articles.json 的 `category` 字段自动生成）
- 2列响应式卡片网格（移动端 1 列）
- 卡片：16:9 封面图 + 精选/分类标签 + 2行标题 + 2行摘要 + 日期 + 箭头
- 点击卡片 → `window.open(url, '_blank')` 跳转微信公众号
- XSS 防护：`h()` escape 函数
- 底部 6 项导航（星星七便士 active）
- **代码已写好，但 articles.json 还没有（需要用户跑本地爬虫生成）**
- **尚未推送到 GitHub**

#### 公众号合集链接（5个，对应 articles.json 数据源）

| 合集名 | 链接 |
|---|---|
| 东南亚走走停停 | https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NTEwNzY3NQ==&action=getalbum&album_id=4115597889819377679#wechat_redirect |
| 新加坡生活 | https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NTEwNzY3NQ==&action=getalbum&album_id=3982328465012965391#wechat_redirect |
| 神游中国 | https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NTEwNzY3NQ==&action=getalbum&album_id=4107935031702847495#wechat_redirect |
| 亚洲吃饭故事 | https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NTEwNzY3NQ==&action=getalbum&album_id=3982329749728280578#wechat_redirect |
| 南洋文化林林总总 | https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NTEwNzY3NQ==&action=getalbum&album_id=3982330764011651073#wechat_redirect |

原始文档：`公众号文章合集.docx`（已存放在 `/Users/adminx/Desktop/个人网站/`）

#### articles.json 格式（用户本地爬虫输出）
```json
[
  {
    "url": "https://mp.weixin.qq.com/s/xxxxxx",
    "title": "文章标题",
    "pub_date": "2026年6月24日 13:15",
    "cover_img": "https://mmbiz.qpic.cn/...",
    "content_text": "纯文本正文（用于摘要显示）",
    "content_html": "<p>HTML 正文</p>",
    "scraped_at": "2026-06-28 10:00:00",
    "category": "旅行",     ← 可选，有值才显示分类 tab
    "featured": true        ← 可选，true 显示蓝色"✦ 精选"标签
  }
]
```

### ✅ podcast.html — 播客 -小心思-
- 奶油色背景
- INS 式中心轮播 + 横向列表行
- EP02–EP16 hardcoded（15集）
- 分类：书里的心理学灵感 / 旅行 / 电影 / 心理咨询师的存在与思考（**分集分配待用户确认**）
- 底部 6 项导航（播客 active）
- **已推送上线**

### ✅ theater.html — 心理探险家
- 奶油色背景
- 卡片式双模块：
  - Card 1：小红书研究 deck（密码：丹佛/Denver）→ `/deck/` 路径
  - Card 2：第四届存在主义大会飞书文档（密码：4&73158r）
- 底部 6 项导航（心理探险家 active）
- **已推送上线**

### ✅ consult.html — 心理咨询预约
- 奶油色背景
- **结构（从上到下）：**
  1. **写给你** — 叙事段落 + sailIn 动画的亚隆引言 + 小房子意象卡片 + 来访者画像（emoji 列表）+ 存在人本取向介绍
  2. **使用手册** — 设置四格 + 督导注记 + Q&A（含自我披露 Q）+ 暂不接待（含3个24小时危机热线）
  3. **简历** — 4个数据卡片（250+时/110+时/110h督导/60h自我体验）+ 长程/短程培训列表 + 学历
  4. **英雄结语** — 渐变背景卡片，"英雄"高亮蓝色，heroReveal 动效
- **预约/二维码部分已删除**（待芒种后台生成正式小程序码再加回）
- 底部 6 项导航（咨询预约 active）
- **代码已更新（含新 6 项导航），尚未推送到 GitHub**

#### consult.html 关键 CSS
```css
/* 亚隆引言 sail-in 动画 */
@keyframes sailIn {
  from { transform: translateX(26px); }
  to   { transform: translateX(0); }
}
.yalom-quote {
  animation: sailIn 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.55s;
}

/* 英雄结语 reveal 动画 */
@keyframes heroReveal {
  from { opacity: 0; transform: translateY(10px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.hero-closing {
  animation: heroReveal 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 1.3s;
  background: linear-gradient(135deg, rgba(116,185,232,0.09) 0%, rgba(247,243,236,0) 55%, rgba(155,139,196,0.07) 100%);
  border-radius: 1.75rem;
}
```

### ✅ splash.html — 电影开场动画（不在主导航内）
- 深海军蓝背景
- 动画：星空 → 帷幕 → Chen+狗子入场 → 胶片导航条
- 胶片 5 帧链接：
  - 帧1：关于我 → about.html ✅
  - 帧2：星星与七便士 → articles.html ← **目前是否已链接，需确认**
  - 帧3：小心思 → podcast.html ✅
  - 帧4：心理探险家 → theater.html ✅
  - 帧5：关于我的使用说明 → manual.html ← **页面未建**

---

## 3. 待办事项（按优先级）

### 立即待办
- [ ] **推送到 GitHub**：articles.html + consult.html（已更新 6 项导航）
  - 在确认推送前，先让用户看 articles.html 页面效果
- [ ] **articles.json**：用户跑本地爬虫，生成后放到 `/Users/adminx/Desktop/个人网站/articles.json`；可加 `category` 和 `featured` 字段

### 待建页面
- [ ] **manual.html** — 关于我的使用说明（info in memo section 三 below）
- [ ] **splash.html 帧2** — 链接到 articles.html（需确认是否已设置）

### 预约功能
- [ ] **小程序码**：需要芒种后台或微信开发者工具生成正式 `.png` 格式小程序码（不是普通二维码，不能用草料）
  - 小程序 URL 备忘：`小程序://芒种心理/fKoQotH9vzJjfYc`
  - 拿到图片后加回 consult.html 结尾

### 内容完善
- [ ] **podcast 分集分类**：用户手动把 EP02–EP16 分配到 4 个分类
- [ ] **SEO**：sitemap.xml + robots.txt + Google Search Console

---

## 4. manual.html — 关于我的使用说明（规划）

- **路由**：`manual.html`
- **内容**：
  - 我的工作方式（存在-人本取向，具体方法论）
  - 受训背景（学历、督导、认证等）
  - Q&A 使用说明
  - 预约方式（等小程序码就位后加）
- **交互设想**：进入时有信封/文件夹解锁 UI（可选）
- **注意**：预约必须用二维码图片，不能做可点击跳转链接（浏览器内打不开微信小程序）

---

## 5. 图片资源

| 文件 | 说明 |
|---|---|
| `gouzihewo.png` | ChenChen + 狗子插画（带背景）|
| `gouzihewo_nobg.png` | 去背版 |
| `chen.png` / `chen_nobg.png` | Chen 单人图 |
| `gouzi.png` / `gouzi_nobg.png` | 狗子单图 |
| `xiaoxinsi.png` | 小心思播客封面 |
| `og-cover.jpg` | Open Graph 分享封面图 |
| `qr-consult.png` | 旧的二维码（无效，微信不支持，暂不使用）|
| `4thcongress.JPG` | 存在主义大会照片 |

---

## 6. 技术说明

- **纯静态 HTML/CSS/JS**，无框架，无构建工具
- **内容加载**：articles.html 用 `fetch('./articles.json')` 读取，其余 hardcoded
- **中国访问**：Cloudflare CDN 加速，字体用 fonts.loli.net 国内镜像
- **GitHub → Vercel**：每次 push main 分支自动部署，约 1 分钟生效

---

*memo by Claude · withchen.com*
