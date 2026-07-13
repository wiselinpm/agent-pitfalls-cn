# 组件库参考

> 所有 UI 组件的 class / 用途 / 示例代码。
> 定义位置：`web/src/styles/global.css` 的 `@layer components`。

## 目录

- [布局](#布局) — `.container-page`
- [卡片](#卡片) — `.card` / `.card-hover`
- [Badge](#badge) — `.badge` + `.badge-critical` / `.badge-high` / `.badge-medium` / `.badge-low`
- [Chip](#chip) — `.chip` + `[aria-pressed=true]` / `.is-active`
- [按钮](#按钮) — `.btn-console` / `.link-cta` / `.nav-link`
- [搜索框](#搜索框) — `.search-bar`
- [输入框](#输入框) — `.input-plain`
- [文本层级](#文本层级) — `.display` / `.section-title` / `.eyebrow`
- [代码块](#代码块) — `.code-block` + `.tok-*`
- [分隔线](#分隔线) — `.hairline`
- [状态指示](#状态指示) — `.pulse-dot` / `.pill-new`
- [动画](#动画) — `.stagger` / `prefers-reduced-motion`
- [Prose](#prose) — `.prose-tight`

---

## 布局

### `.container-page`

页面主容器，max-width 1200px，左右 padding 24px。

```html
<div class="container-page">
  <!-- 内容自动居中，左右各有 24px padding -->
</div>
```

**底层**：`@apply mx-auto w-full max-w-page px-6;`

---

## 卡片

### `.card`

基础卡片容器 — 白色底，1px lavender-mist 边框，8px 圆角。

```html
<div class="card">
  <h3>卡片标题</h3>
  <p>卡片内容...</p>
</div>
```

### `.card-hover`

可点击的卡片 — hover 时边框变深。

```html
<a href="..." class="card card-hover">
  <h3>可点击卡片</h3>
</a>
```

**底层**：
```css
.card {
  background: var(--color-paper);
  border: 1px solid var(--color-lavender-mist);
  border-radius: 8px;
  padding: 16px;
  transition: border-color 150ms ease;
}
.card-hover:hover { border-color: var(--color-mist); }
```

---

## Badge

严重程度 / 平台 / 分类标签。

```html
<!-- 基础 badge -->
<span class="badge">Claude Code</span>

<!-- 严重程度变体 -->
<span class="badge badge-critical">critical</span>
<span class="badge badge-high">high</span>
<span class="badge badge-medium">medium</span>
<span class="badge badge-low">low · 已验证</span>
```

**视觉**：
- 11px 大写 + tracking 0.056em
- 圆角 4px
- 1px 边框 + 6% 透明度底色
- 严重程度颜色：rust 红棕 / 橘色 / 暗黄 / teal

| Class | 颜色 | 用途 |
|---|---|---|
| `.badge-critical` | `#984e4d` | 数据丢失 / 安全漏洞 / 生产事故 |
| `.badge-high` | `#b56a1a` | 默认配置下大概率触发 |
| `.badge-medium` | `#8a7a30` | 特定条件下触发 |
| `.badge-low` | `#096e72` | 体验问题 / "已验证" 标签 |

---

## Chip

可切换的筛选器 / 标签按钮。

```html
<!-- 默认状态 -->
<button class="chip" data-value="langchain">LangChain</button>

<!-- 选中状态（aria-pressed=true 或 .is-active） -->
<button class="chip" data-value="langchain" aria-pressed="true">LangChain</button>
```

**视觉**：
- 12px，padding 4×12
- 圆角 4px
- 透明底 + 1px lavender-mist 边框
- hover：边框变 ink，文字变 ink
- pressed：边框变 ink + lavender-mist 底色 + ink 文字

**典型用法 — 避坑库分类多选**：
```html
<button class="chip filter-category" data-value="context-window" aria-pressed="false">
  #上下文窗口
</button>
```

---

## 按钮

### `.btn-console`

Header 上的 pill 风格按钮（RSS / 移动菜单）。

```html
<button class="btn-console" type="button">
  ☰
</button>

<a href="/rss.xml" class="btn-console">RSS</a>
```

**视觉**：13px / 圆角 4px / 1px 边框 / hover 加 lavender-mist 底

### `.link-cta`

文本链接式 CTA — 自动带 `>` 后缀，**没有填充背景**。

```html
<a href="/pitfalls" class="link-cta">浏览避坑库</a>
<!-- 渲染为：浏览避坑库 >  -->
```

**底层**：
```css
.link-cta::after {
  content: '>';
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 400;
}
.link-cta:hover { opacity: 0.7; text-decoration: none; }
```

### `.nav-link`

Header / Footer 导航链接。

```html
<a href="/pitfalls" class="nav-link" aria-current="page">避坑库</a>
```

**视觉**：14px fog 色 / hover 加 lavender-mist 底 + ink 文字 / `aria-current="page"` 时变 ink

---

## 搜索框

### `.search-bar`

Header 上的 pill 搜索入口。

```html
<button class="search-bar" id="search-shortcut">
  <svg><!-- search icon --></svg>
  <span class="placeholder">搜索…</span>
  <span class="kbd">⌘K</span>
</button>
```

**视觉**：圆角 9999px / lavender-mist 底 / min-width 180px / `.kbd` 是白底圆角 4px 的快捷键提示

---

## 输入框

### `.input-plain`

列表筛选表单的输入框。

```html
<input type="search" placeholder="按标题、症状、根因搜索…" class="input-plain pl-9" />
<select class="input-plain"><option>全部平台</option></select>
```

**视觉**：圆角 4px / 1px lavender-mist 边框 / focus 时边框变 ink

---

## 文本层级

### `.display`

48px 大标题，仅 Hero 使用。

```html
<h1 class="display">别再被同一个坑<br />绊倒两次。</h1>
```

### `.section-title`

20px 区块标题。

```html
<h2 class="section-title">最新收录</h2>
```

### `.eyebrow`

大写小标签（12px / tracking 0.056em / mist 色）。

```html
<span class="eyebrow">CONTRIBUTING</span>
```

---

## 代码块

### `.code-block`

Hero 艺术字 + 文章代码块容器。

```html
<div class="code-block">
<pre class="m-0 border-0 p-0 font-mono text-[13px]">
<span class="tok-comment"># 注释</span>
<span class="tok-key">title</span>: <span class="tok-string">"值"</span>
<span class="tok-key">severity</span>: <span class="tok-bool">critical</span>
<span class="tok-key">categories</span>: [<span class="tok-type">context-window</span>]
</pre>
</div>
```

**语法 token 颜色**：

| Token | 颜色 | 用途 |
|---|---|---|
| `.tok-string` | plum 紫 | 字符串值 |
| `.tok-key` | cobalt 蓝 | YAML key / 字段名 |
| `.tok-type` | teal 青 | 类型 / enum 值 |
| `.tok-bool` | rust 红棕 | 布尔值（true/false） |
| `.tok-comment` | mist 灰斜体 | 注释 |

---

## 分隔线

### `.hairline`

1px 水平分隔线（lavender-mist 色）。

```html
<hr class="hairline" />
```

---

## 状态指示

### `.pulse-dot`

"实时采集" 状态点（teal 色脉冲动画）。

```html
<span class="pulse-dot"></span>
```

### `.pill-new`

"NEW" 标签（10px / uppercase / 圆角 4px）。

```html
<span class="pill-new">NEW</span>
```

---

## 动画

### `.stagger`

列表项依次淡入（前 12 项有不同 delay）。

```html
<ul class="stagger grid gap-3">
  <li>...</li>
  <li>...</li>
  ...
</ul>
```

**底层**：
```css
.stagger > * {
  animation: fade-up 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.stagger > *:nth-child(1)  { animation-delay: 0ms; }
.stagger > *:nth-child(2)  { animation-delay: 30ms; }
/* ... 一直递增到 12 */
```

**减弱动画支持**：
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
  .pulse-dot::before { animation: none; }
}
```

---

## Prose

### `.prose-tight`

Markdown 正文样式（用于 `/about` / `/contributing` / `/schema` / 详情页正文）。

```html
<article class="prose-tight">
  <h2>标题</h2>
  <p>段落...</p>
  <ul>
    <li>列表项</li>
  </ul>
  <pre><code>代码块</code></pre>
</article>
```

**自动应用**：
- H2 20px / margin-top 1.6em / margin-bottom 0.6em
- H3 18px / margin-top 1.4em / margin-bottom 0.4em
- P margin 0.85em 上下
- UL 无项目符号，自定义圆形点
- Code lavender-mist 底 / 4px 圆角
- Pre lavender-mist 底 + 8px 圆角 + code shadow

---

## 自定义 Token

在 `global.css` 的 `:root` 修改即可全局生效：

```css
:root {
  /* 颜色 */
  --color-ink: #303055;
  --color-slate: #403f53;
  --color-fog: #767682;
  --color-mist: #a8a8b0;
  --color-paper: #ffffff;
  --color-lavender-mist: #e8e8f2;

  /* 严重程度 */
  --sev-critical: #984e4d;
  --sev-high: #b56a1a;
  --sev-medium: #8a7a30;
  --sev-low: #096e72;

  /* 圆角 */
  --radius-tags: 4px;
  --radius-cards: 8px;

  /* 阴影（仅 code-block 用） */
  --shadow-code: 0 0 0 1px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04);
}
```

### 暗色主题（参考实现）

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-paper: #1a1a24;
    --color-ink: #e8e8f2;
    --color-slate: #c8c8d0;
    --color-fog: #888894;
    --color-mist: #555560;
    --color-lavender-mist: #2a2a36;
    /* ... */
  }
}
```

---

## 组合示例

### 一条 pitfall 卡片

```html
<a href="/pitfalls/xxx" class="card card-hover group block">
  <div class="flex flex-wrap items-center gap-2">
    <span class="badge badge-critical">critical</span>
    <span class="badge">Claude Code</span>
    <span class="badge badge-low">已验证</span>
  </div>
  <h3 class="mt-3 text-[16px] font-semibold leading-snug text-ink">
    Agent 调试日志意外打印 API Key
  </h3>
  <p class="mt-2 line-clamp-3 text-[13px] leading-relaxed text-slate">
    在把 LangChain / OpenAI Agents SDK 的 verbose 模式打开后…
  </p>
  <div class="mt-4 flex flex-wrap gap-1.5">
    <span class="badge">#安全</span>
    <span class="badge">#可观测性</span>
  </div>
  <div class="mt-4 flex items-center justify-between border-t border-lavender-mist pt-3 text-[12px] text-fog">
    <span class="font-mono">2026-07-12</span>
    <span class="font-mono opacity-0 group-hover:opacity-100">read →</span>
  </div>
</a>
```

### 一个 CTA 按钮组

```html
<div class="mt-7 flex flex-wrap items-center gap-x-7 gap-y-3">
  <a href="/pitfalls" class="link-cta">浏览避坑库</a>
  <a href="/contributing" class="link-cta">如何贡献</a>
  <a href="https://github.com/..." rel="noopener" class="link-cta">GitHub</a>
</div>
```

### 一个完整的 stats 区块

```html
<hr class="hairline mt-12" />
<section class="py-8">
  <div class="grid grid-cols-2 gap-y-6 md:grid-cols-4">
    <div>
      <div class="font-mono text-[28px] font-semibold tabular-nums leading-none text-ink">
        7,893
      </div>
      <div class="mt-1.5 text-[12px] text-fog">已收录条目</div>
    </div>
    <!-- 重复 3 个 -->
  </div>
</section>
<hr class="hairline" />
```

---

## 实用工具 class

| class | 用途 |
|---|---|
| `.font-mono` | IBM Plex Mono |
| `.font-semibold` / `.font-medium` | 600 / 500 字重 |
| `.tabular-nums` | 等宽数字（避免数字跳动）|
| `.text-ink` / `.text-slate` / `.text-fog` / `.text-mist` | 4 级文字颜色 |
| `.text-rust` / `.text-cobalt` / `.text-teal` / `.text-obsidian` | 强调色 |
| `.border-lavender-mist` | 1px lavender-mist 边框 |
| `.bg-paper` / `.bg-lavender-mist` / `.bg-lavender-mist\/50` | 背景色 |
| `.container-page` | 主容器 |
| `.eyebrow` / `.section-title` / `.display` | 文本层级 |
| `.line-clamp-2` / `.line-clamp-3` | 文本截断 |
| `.rounded-lg` / `.rounded-md` | 圆角（8px / 6px） |
