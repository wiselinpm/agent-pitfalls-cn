# UI 设计参考

> 完整的站点 UI 设计参考 — 设计 token、组件库、布局、字体、颜色。
> 适合想要修改 UI / 自定义主题 / Fork 做新项目的开发者。

## 目录

- [设计哲学](#设计哲学)
- [设计 token](#设计-token) — 颜色 / 字体 / 间距 / 圆角 / 阴影
- [字体系统](#字体系统)
- [布局系统](#布局系统)
- [组件库概览](#组件库概览)
- [页面清单](#页面清单)
- [可访问性](#可访问性)

---

## 设计哲学

参考 **Stripe Press**、**Linear**、**Vercel Docs** 的简洁美学：

| 原则 | 体现 |
|---|---|
| **静噪优先** | 大量留白 + hairline 分隔线，不用阴影堆层次 |
| **去装饰化** | 圆角只用 4px / 8px，severity 颜色不抢戏 |
| **代码即艺术品** | 首页 hero 是真实 pitfall 的 YAML 语法高亮 |
| **零冗余按钮** | 所有 CTA 都是文字链接（`.link-cta`），不靠填充按钮 |
| **暗色友好** | 颜色全用 CSS variable，一行切换主题即可 |

> 注：本项目当前只有浅色主题，但所有颜色都基于 CSS variable，扩展暗色只需添加 `[data-theme="dark"]` 选择器。

---

## 设计 token

所有 token 定义在 `web/src/styles/global.css` 的 `:root`。

### 颜色（color）

```css
/* 主色 — 文本 */
--color-ink:        #303055   /* 主要文字 */
--color-slate:      #403f53   /* 次要文字 */
--color-fog:        #767682   /* 三级文字 / placeholder */
--color-mist:       #a8a8b0   /* 最浅文字 / 注释 */
--color-obsidian:   #111111   /* 强调文字 */

/* 背景 */
--color-paper:      #ffffff   /* 页面背景 */
--color-lavender-mist: #e8e8f2 /* 卡片底色 / hover / divider */

/* 代码语法高亮（仅用于 .code-block） */
--color-code-plum:  #8844ae   /* 字符串 */
--color-code-cobalt: #3b61b0  /* 键名 */
--color-code-teal:  #096e72   /* 类型 */
--color-code-rust:  #984e4d   /* 布尔 / 注释错误 */
```

### 严重程度（severity）

```css
--sev-critical: #984e4d   /* rust — 红棕，生产事故 */
--sev-high:     #b56a1a   /* 橘色，默认配置下大概率触发 */
--sev-medium:   #8a7a30   /* 暗黄，特定条件下触发 */
--sev-low:      #096e72   /* teal，体验问题 */
```

### 间距（layout）

```css
--page-max-width: 1200px   /* .container-page 容器宽度 */
--section-gap:    64px     /* 上下区块间距 */
```

### 圆角（radius）— 只用 4px / 8px

```css
--radius-tags:    4px      /* badge / chip */
--radius-buttons: 4px      /* btn-console */
--radius-inputs:  4px      /* input */
--radius-cards:   8px      /* card */
--radius-code:    8px      /* pre / code-block */
```

### 阴影（shadow）— 仅 code-block 使用

```css
--shadow-code:     0 0 0 1px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04)
--shadow-hairline: 0 0 0 1px rgba(0,0,0,0.04)
```

> **设计铁律**：除了 code-block，UI 上**不出现阴影**。所有层次感靠 1px 边框 + 颜色对比。

---

## 字体系统

```html
<!-- BaseLayout.astro head -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Rubik:wght@400;500;600&display=swap" />
```

| 用途 | 字体 | 字号 |
|---|---|---|
| 正文 / 标题 | **Rubik Variable** (sans) | 14px / 1.8 |
| 代码 / 键盘快捷键 | **IBM Plex Mono** | 13px / 1.65 |

### 字号阶梯

| 用途 | class | 实际 px |
|---|---|---|
| Hero 标题 | `.display` | **48px / 1.1** |
| H1 页面标题 | `.section-title` | 20px / 1.5 |
| H2 大标题 | — | 32px / 1.3 |
| 卡片标题 | — | 16px / 1.4 |
| 正文 | — | 14px / 1.8 |
| 注释 | — | 12px / 1.6 |
| Badge / kbd | — | 11px / uppercase tracking |

---

## 布局系统

### 容器

```css
.container-page {
  @apply mx-auto w-full max-w-page px-6;  /* max-width: 1200px, padding: 24px */
}
```

### 栅格

12 栏栅格用 Tailwind：

```astro
<section class="grid gap-12 md:grid-cols-12">
  <div class="md:col-span-7">...</div>  <!-- 左 7 栏 -->
  <div class="md:col-span-5">...</div>  <!-- 右 5 栏 -->
</section>
```

### Header / Footer

Header 高度 56px (`h-14`) sticky 顶部，Footer 单行 32px 高度，mt-20 与正文分隔。

---

## 组件库概览

完整组件文档见 [`UI-components.md`](./UI-components.md)。

### 主要组件

| 组件 | class | 用途 |
|---|---|---|
| 卡片 | `.card` / `.card-hover` | 通用容器 / 可点击卡片 |
| Badge | `.badge` + `.badge-critical` 等 | 严重程度 / 平台 / 分类标签 |
| Chip | `.chip` + `[aria-pressed=true]` | 可切换的筛选器 |
| 按钮 | `.btn-console` / `.link-cta` | Header CTA / 文本链接 |
| 导航 | `.nav-link` + `[aria-current=page]` | Header / Footer 链接 |
| 搜索框 | `.search-bar` | Header 搜索入口 |
| 输入框 | `.input-plain` | 列表筛选表单 |
| 标题小标签 | `.eyebrow` | 大写 tracking 小标签 |
| Section 标题 | `.section-title` | 20px 区块标题 |
| Display 标题 | `.display` | 48px Hero 标题 |
| Hairline 分隔 | `.hairline` | 1px 水平分隔 |
| 代码块 | `.code-block` + `.tok-*` | 首页 hero 艺术字 |
| Pulse 点 | `.pulse-dot` | "实时采集" 状态指示 |
| Stagger 动画 | `.stagger` > `*` | 列表项依次淡入 |
| Prose | `.prose-tight` | Markdown 正文样式 |

### 严重程度 Badge 一览

```css
.badge-critical { /* 红棕底，文字深红棕 */ }
.badge-high     { /* 橘色底 */ }
.badge-medium   { /* 暗黄底 */ }
.badge-low      { /* teal 底，已验证标签用这个 */ }
```

---

## 页面清单

完整页面文档见 [`UI-pages.md`](./UI-pages.md)。

| 路径 | 文件 | 用途 |
|---|---|---|
| `/` | `pages/index.astro` | 首页：Hero + Stats + 分类 + 最新收录 + 流水线 |
| `/pitfalls` | `pages/pitfalls/index.astro` | 避坑库：搜索 + 严重程度 + 平台 + 分类筛选 |
| `/pitfalls/[slug]` | `pages/pitfalls/[...slug].astro` | 单条 pitfall 详情 + 上下条 + 相关 + 侧栏 |
| `/advisories` | `pages/advisories/index.astro` | 安全公告列表 |
| `/patterns` | `pages/patterns/index.astro` | 应对模式列表 |
| `/about` | `pages/about.astro` | 关于项目 |
| `/contributing` | `pages/contributing.astro` | 贡献指南 |
| `/schema` | `pages/schema.astro` | 数据 schema 可视化 |
| `/404` | `pages/404.astro` | 404 错误页 |
| `/rss.xml` | `pages/rss.xml.js` | RSS 订阅源 |
| `/sitemap-index.xml` | 自动生成 | sitemap |

---

## 可访问性

| 维度 | 做法 |
|---|---|
| 语义 HTML | header / nav / main / article / aside / footer 正确使用 |
| ARIA | `aria-current="page"` / `aria-pressed` / `aria-label` / `aria-hidden` |
| 键盘导航 | 所有交互元素可 Tab + Enter；`Cmd+K` 全局聚焦搜索 |
| 焦点环 | `:focus-visible` 2px ink outline，offset 2px |
| 颜色对比 | 正文 4.5:1+；严重程度文字色与边框色对比 ≥ 4.5:1 |
| 减弱动画 | `@media (prefers-reduced-motion: reduce)` 自动禁用 |
| 多语言 | `<html lang="zh-CN">`；英文条目可翻译 |

---

## 修改指南

### 改主色

修改 `web/src/styles/global.css` 中所有 `--color-*` 变量即可，不需要改任何 .astro 文件。

### 加新组件

在 `global.css` 的 `@layer components` 中加 class，然后用 `<div class="...">` 引用。

### 加新页面

1. 在 `web/src/pages/` 新建 `xxx.astro`
2. 顶部 import `BaseLayout`：
   ```astro
   ---
   import BaseLayout from '../layouts/BaseLayout.astro';
   ---
   <BaseLayout title="..." description="...">
     <!-- 内容 -->
   </BaseLayout>
   ```
3. 写内容 → `npm run dev` 预览 → PR

### 改字体

修改 `BaseLayout.astro` 的 Google Fonts URL + `global.css` 的 `font-family`。

---

## 设计参考资源

- [Stripe Press](https://stripe.com/press) — 排版 / 留白
- [Linear](https://linear.app) — chip / 极简交互
- [Vercel Docs](https://vercel.com/docs) — 信息密度
- [Pico CSS](https://picocss.com) — 极简哲学
- [IBM Carbon](https://carbondesignsystem.com) — 设计 token 系统
