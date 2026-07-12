# 页面详细文档

> 每个页面的 ASCII mockup + 数据流 + 交互说明。

## 目录

- [`/` 首页](#首页) — `pages/index.astro`
- [`/pitfalls` 避坑库](#避坑库) — `pages/pitfalls/index.astro`
- [`/pitfalls/[slug]` 详情页](#详情页) — `pages/pitfalls/[...slug].astro`
- [`/advisories` 安全公告](#安全公告) — `pages/advisories/index.astro`
- [`/patterns` 应对模式](#应对模式) — `pages/patterns/index.astro`
- [`/about` 关于](#关于) — `pages/about.astro`
- [`/contributing` 贡献指南](#贡献指南) — `pages/contributing.astro`
- [`/schema` Schema](#schema) — `pages/schema.astro`
- [`/404` 错误页](#404) — `pages/404.astro`
- [`/rss.xml` RSS](#rss) — `pages/rss.xml.js`

---

## 首页

**文件**：`web/src/pages/index.astro`
**数据源**：`getCollection('pitfalls')` 全量
**模板**：`BaseLayout`

### ASCII Mockup

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ⚠ Agent Pitfalls        首页 避坑库 安全公告 应对模式 关于  GitHub ↗  🔍⌘K RSS│
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────┐   ● 实时采集 · 上次更新 今天     │
│  │ pitfalls/xxx.md                    │                                  │
│  │ ─────────────────────               │   别再被同一个坑                  │
│  │ # 一行描述问题                      │   绊倒两次。                       │
│  │ title: "[BUG] ConnectionRefused…"   │                                  │
│  │ summary: 在把 LangChain / OpenAI…   │   我们抓取 GitHub Issues、官方   │
│  │ severity: critical                  │   博客、Hacker News、Reddit、     │
│  │ platforms: [langchain, …]           │   知乎等全网关于 AI Agent 开发   │
│  │ fixes:                              │   的踩坑讨论，去重、归类、给出    │
│  │   - 永远不在 prompt 模板硬编码…     │   可执行的修复方案。               │
│  └─────────────────────────────────────┘                                  │
│  键名   字符串   类型   枚举   注释                浏览避坑库 > 如何贡献 > GitHub >
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│  5,561          2,210 critical      4,800 fixes     89 new                │
│  已收录条目     严重等级 + 高危 455  条目附带可执行修复  本周新增 · 6,500 已验证│
├──────────────────────────────────────────────────────────────────────────┤
│  热门分类                                              全部 >             │
│  #上下文窗口 245  #工具调用 198  #安全 167  #可观测性 142 …                │
├──────────────────────────────────────────────────────────────────────────┤
│  最新收录                          按收录时间倒序 · 共 5,561 条   全部 >  │
│  ┌──────────────────────────┐  ┌──────────────────────────┐             │
│  │ [严重] [Claude Code] 已验证│  │ [严重] [OpenAI Agents]   │             │
│  │ 长上下文静默截断导致…      │  │ Streaming timeout 没有 retry│           │
│  │ 上下文超过窗口 80% 时…     │  │ WebSocket 莫名断开…        │             │
│  │ #上下文窗口 #工具调用       │  │ #流式响应 #可靠性           │             │
│  │ 2026-07-12               →│  │ 2026-07-11               →│             │
│  └──────────────────────────┘  └──────────────────────────┘             │
├──────────────────────────────────────────────────────────────────────────┤
│  采集管线                                          三步走…                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│  │ [01] 采集   │  │ [02] 清洗去重│  │ [03] 结构化抽取│                     │
│  │ 72 source   │  │ URL 指纹+    │  │ 抓 symptoms/  │                     │
│  │ 并行抓取    │  │ 标题相似度    │  │ root_causes/  │                     │
│  │             │  │             │  │ fixes 三段    │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                        │
├──────────────────────────────────────────────────────────────────────────┤
│  CONTRIBUTING                                                                │
│  踩过坑？贡献你的发现                                                         │
│  PR-driven 工作流 — 任何人都能在 GitHub 上提交新坑…                          │
│  贡献指南 > 关于项目 > Schema >                                              │
├──────────────────────────────────────────────────────────────────────────┤
│ © 2026 Agent Pitfalls · MIT  关于  贡献  Schema  GitHub ↗  RSS ↗           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 关键数据流

```typescript
const all = await getCollection('pitfalls');  // 5,561 条
const totalCount = all.length;
const criticalCount = all.filter(p => p.severity === 'critical').length;
const verifiedCount = all.filter(p => p.verified).length;
const withFixesCount = all.filter(p => p.fixes.length > 0).length;
const recentCount = all.filter(p => /* 7 天内 */).length;

const categoryCount = new Map();
for (const p of all) for (const c of p.categories) categoryCount.set(c, ...);
const topCategories = [...categoryCount].sort().slice(0, 8);

const featured = all.slice(0, 6);  // 最新 6 条
const heroSample = featured[0];     // Hero 代码块展示用
```

### 设计要点

- **Hero 代码块**：真实 pitfall 文件的 frontmatter，用 syntax token 高亮（不是 mockup，是真数据）
- **统计数字**：使用 `.font-mono .tabular-nums` 等宽数字，避免数字跳动
- **分类 chip**：点击跳转到 `/pitfalls?category=xxx`（暂未实现 URL 参数过滤，但链接已就位）
- **stagger 动画**：6 个卡片依次淡入，延迟 30ms
- **CTA 都是 `.link-cta`**：纯文本带 `>` 后缀的链接，无填充按钮

---

## 避坑库

**文件**：`web/src/pages/pitfalls/index.astro`
**数据源**：`getCollection('pitfalls')` 全量，按 `discovered_at` 倒序
**模板**：`BaseLayout`

### ASCII Mockup

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ⚠ Agent Pitfalls        首页 避坑库 安全公告 应对模式 关于  GitHub ↗  🔍⌘K RSS│
├──────────────────────────────────────────────────────────────────────────┤
│ 避坑库                                                  ⌘ K 聚焦搜索      │
│ 5,561 / 5,561 条 · 按严重程度与平台筛选                                    │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 🔍 [按标题、症状、根因搜索…]                                         │  │
│ │                                                                    │  │
│ │ 严重程度                                                            │  │
│ │ [全部 5561] [严重 2210] [高 455] [中 2786] [低 110]                  │  │
│ │                                                                    │  │
│ │ 平台                                                                │  │
│ │ [全部平台 ▼]                                                       │  │
│ │                                                                    │  │
│ │ 分类（可多选）                                                       │  │
│ │ [#上下文窗口] [#工具调用] [#流式响应] [#成本] [#安全] [#可观测性]…  │  │
│ │                                                                    │  │
│ │ 已应用：[×严重  ×「context」]                              清空全部 │  │
│ └────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ [严重] [Claude Code] [OpenAI Agents] 已验证                          │  │
│ │ Agent 调试日志意外打印 API Key / 用户隐私                            │  │
│ │ 在把 LangChain / OpenAI Agents SDK 的 verbose 模式打开后…            │  │
│ │ #安全 #可观测性                              2026-07-12       →   │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ [严重] [OpenAI Agents]                                                 │  │
│ │ 多 agent 协作死循环，账单失控                                          │  │
│ │ AutoGen / CrewAI 多 agent 模式未设置 max_iterations…                │  │
│ │ #多智能体 #可靠性                                2026-07-11       → │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│ …（共 5,561 条）                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│ © 2026 Agent Pitfalls · MIT                                               │
└──────────────────────────────────────────────────────────────────────────┘
```

### 交互（纯 JavaScript，零依赖）

```javascript
// 搜索输入 — 实时过滤
search.addEventListener('input', apply);

// 严重程度 — 单选 chip
filterSeverity.forEach(btn => btn.addEventListener('click', () => {
  activeSeverity = btn.dataset.value;
  apply();
}));

// 平台 — select change
platform.addEventListener('change', apply);

// 分类 — 多选 chip
filterCategory.forEach(btn => btn.addEventListener('click', () => {
  if (activeCategories.has(btn.dataset.value)) activeCategories.delete(...);
  else activeCategories.add(...);
  apply();
}));

// ⌘K 全局快捷键
document.addEventListener('keydown', (e) => {
  if ((metaKey || ctrlKey) && e.key === 'k') {
    e.preventDefault();
    search.focus();
  }
});
```

### 过滤逻辑

```javascript
function apply() {
  const q = search.value.toLowerCase();
  let visible = 0;
  for (const li of items) {
    const matchQ = !q || li.dataset.title.includes(q) || li.dataset.summary.includes(q);
    const matchS = !activeSeverity || li.dataset.severity === activeSeverity;
    const matchP = !platform.value || li.dataset.platforms.split(',').includes(platform.value);
    const matchC = activeCategories.size === 0 || li.dataset.categories.split(',').some(c => activeCategories.has(c));
    const show = matchQ && matchS && matchP && matchC;
    li.style.display = show ? '' : 'none';
    if (show) visible++;
  }
  resultCount.textContent = String(visible);
  empty.classList.toggle('hidden', visible !== 0);
}
```

### 设计要点

- **零 JS 框架**：所有交互用 vanilla JS（`<script is:inline>`），构建产物零运行时
- **dataset 属性**：`data-title` / `data-summary` / `data-severity` / `data-platforms` / `data-categories` / `data-date`，前端不依赖后端排序
- **active filter chips**：底部展示当前过滤条件，可单独移除（× 按钮）
- **空状态**：404 风格提示 + 清空筛选按钮

---

## 详情页

**文件**：`web/src/pages/pitfalls/[...slug].astro`
**数据源**：`getStaticPaths()` 预生成所有 slug
**模板**：`BaseLayout`

### ASCII Mockup

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ⚠ Agent Pitfalls   …                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ← reading progress bar              │
├──────────────────────────────────────────────────────────────────────────┤
│ pitfalls/ / https-anthropics-claude-code-issues-76802                     │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────┐  ┌─────────────┐ │
│ │ [严重] [Claude Code] [OpenAI Agents] [已验证]       │  │ TL;DR        │ │
│ │                                                    │  │ 一句话概览…  │ │
│ │ Agent 调试日志意外打印 API Key / 用户隐私            │  │              │ │
│ │ 在把 LangChain / OpenAI Agents SDK 的 verbose 模式   │  │ 严重程度     │ │
│ │ 打开后，完整的 prompt…                              │  │ [严重]       │ │
│ │                                                    │  │              │ │
│ │ 01 症状                              怎么识别      │  │ 涉及平台     │ │
│ │ ┌──────────────────────────────────────────────┐   │  │ [Claude Code]│ │
│ │ │ · 日志文件里出现 sk-proj-... 或用户邮箱        │   │  │ [OpenAI…]   │ │
│ │ │ · CI 把 prompt 上传到 Sentry/Datadog          │   │  │              │ │
│ │ │ · 团队截图调试输出时泄漏密钥                  │   │  │ 分类         │ │
│ │ └──────────────────────────────────────────────┘   │  │ [#安全][#可…]│ │
│ │                                                    │  │              │ │
│ │ 02 根因                              为什么会发生  │  │ ─────────    │ │
│ │ ┌──────────────────────────────────────────────┐   │  │ 症状 3 │ 修复 5│ │
│ │ │ · verbose=True 默认打印所有 LLM 输入输出       │   │  │              │ │
│ │ │ └──────────────────────────────────────────────┘│  │ ✓ 已通过社区…│ │
│ │                                                    │  └─────────────┘ │
│ │ 03 修复 / 缓解                          推荐方案   │                    │
│ │ ┌──────────────────────────────────────────────┐   │  相关条目        │
│ │ │ ✓ 永远不在 prompt 模板硬编码密钥                │   │  ┌──────────┐ │
│ │ │ ✓ 实现 RedactingFilter 拦截…                  │   │  │[严重]    │ │
│ │ │ ✓ 生产关闭 verbose                             │   │  │ API Key…│ │
│ │ │ ✓ 团队规范：截图前先 grep 密钥                  │   │  └──────────┘ │
│ │ └──────────────────────────────────────────────┘   │                    │
│ │                                                    │  └─────────────┘ │
│ │ 04 参考来源                                        │                    │
│ │ ┌──────────────────────────────────────────────┐   │                    │
│ │ │ ↗ LangChain Debugging 与日志      [LangChain Docs] │                 │
│ │ │ ↗ Sentry data scrubbing          [Sentry]       │   │                │
│ │ └──────────────────────────────────────────────┘   │                    │
│ │                                                    │                    │
│ │ ───────────── prev                       next ─────────────           │
│ │ ┌──────────────────┐  ┌──────────────────┐                           │
│ │ │ ← prev            │  │ next →            │                           │
│ │ │ 多 agent 协作死循环 │  │ Long context 静默 │                           │
│ │ └──────────────────┘  └──────────────────┘                           │
│ │                                                    │                    │
│ │ 收录于 2025-10-01 · 贡献者 agent-pitfalls-bot    在 GitHub 上编辑 >   │
│ └────────────────────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 关键交互

```javascript
// Reading progress bar（顶部 1px）
function update() {
  const rect = article.getBoundingClientRect();
  const pct = Math.max(0, Math.min(1, (-rect.top + window.innerHeight * 0.2) / article.scrollHeight));
  bar.style.transform = `scaleX(${pct})`;
}
window.addEventListener('scroll', update, { passive: true });
```

### getStaticPaths

```typescript
export async function getStaticPaths() {
  const all = await getCollection('pitfalls');
  return all.map((entry, i) => ({
    params: { slug: entry.id },
    props: {
      entry,
      prev: i > 0 ? all[i - 1] : null,
      next: i < all.length - 1 ? all[i + 1] : null,
      related: all
        .filter(e => e.id !== entry.id && (
          e.data.categories.some(c => entry.data.categories.includes(c)) ||
          e.data.platforms.some(p => entry.data.platforms.includes(p))
        ))
        .slice(0, 4),
    },
  }));
}
```

### 设计要点

- **三栏布局**（桌面）：主内容 / 侧栏 sticky / 顶部 reading progress
- **section 编号** 01/02/03/04：mist 浅色 mono 小字，提供视觉锚点
- **症状/根因/修复** 用不同颜色的前缀符号：`·` 红棕 / `·` 钴蓝 / `✓` teal
- **侧栏 sticky**：TL;DR + 严重程度 + 平台 + 分类 + 症状/修复数 + 已验证徽章
- **相关条目**：基于 categories 或 platforms 相似度取 4 条
- **prev/next**：按收录时间顺序的相邻条目
- **在 GitHub 上编辑**：直接跳到 `web/src/content/pitfalls/{id}.md` 的 edit 页面

---

## 安全公告

**文件**：`web/src/pages/advisories/index.astro`
**数据源**：`getCollection('advisories')`

### Mockup

```
┌──────────────────────────────────────────────────┐
│ 安全公告                                          │
│ 共 N 条 · 按发布时间倒序                           │
├──────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────┐ │
│ │ [严重] Anthropic API 服务中断                  │ │
│ │ 2026-01-15                                    │ │
│ │ 涉及 [Claude API] [Claude Code]               │ │
│ │ ↗ Anthropic Status                              │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

---

## 应对模式

**文件**：`web/src/pages/patterns/index.astro`
**数据源**：`getCollection('patterns')`

类似安全公告的列表，每条 pattern 有 `use_when` / `pros` / `cons` / `example`。

---

## 关于

**文件**：`web/src/pages/about.astro`

简洁的 prose 页面，4 个编号 section：
1. 为什么不直接搜索
2. 数据流（采集 → 规范化 → 校验 → 发布）
3. 协议（MIT + CC-BY）
4. 如何参与

---

## 贡献指南

**文件**：`web/src/pages/contributing.astro`

完整的贡献流程说明 — 详见 `CONTRIBUTING.md`。

---

## Schema

**文件**：`web/src/pages/schema.astro`

可视化展示 Zod schema，4 个 section：
1. Pitfall 字段表
2. 分类取值表
3. 严重程度定义
4. 最小可提交 frontmatter 示例

---

## 404

**文件**：`web/src/pages/404.astro`

简单的 404 错误页：

```
┌──────────────────────────────────────────┐
│ 404                                      │
│ 页面不存在                                │
│ 该条目可能已被移除或链接错误                │
│                                          │
│ [返回首页 >]   [查看避坑库 >]              │
└──────────────────────────────────────────┘
```

---

## RSS

**文件**：`web/src/pages/rss.xml.js`

动态生成 RSS 2.0 feed，包含最新 50 条 pitfall：

```javascript
// pages/rss.xml.js
import rss from '@astrojs/rss';
export async function GET(context) {
  const all = await getCollection('pitfalls');
  return rss({
    title: 'Agent Pitfalls',
    description: '全网 AI Agent 开发避坑整合',
    site: context.site,
    items: all.slice(0, 50).map(p => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: p.data.discovered_at,
      link: `/pitfalls/${p.id}/`,
      categories: [p.data.severity, ...p.data.categories],
    })),
  });
}
```

---

## 全局导航与布局

所有页面都包裹在 `BaseLayout.astro` 里：

```
┌────────────────────────────────────────────────────────────────────────┐
│ ⚠ Agent Pitfalls        首页 避坑库 安全公告 应对模式 关于  GitHub ↗  🔍⌘K RSS│  ← Header (sticky h-14)
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            <slot />  ← 页面内容                          │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│ © 2026 Agent Pitfalls · MIT  关于  贡献  Schema  GitHub ↗  RSS ↗        │  ← Footer (mt-20 py-8)
└────────────────────────────────────────────────────────────────────────┘
```

### Header 行为

- **Sticky 顶部**：`sticky top-0 z-40 backdrop-blur-sm bg-paper/85`
- **品牌区**：左，`⚠` 圆角方块 + "Agent Pitfalls" 文字
- **导航**：中（≥md 显示），5 个主链接 + GitHub 外链
- **右侧工具**：搜索按钮 + RSS 链接 + 移动菜单按钮
- **搜索快捷键**：⌘K / Ctrl+K — 在 `/pitfalls` 页聚焦搜索框，其他页跳转到该页
- **移动端**：< md 隐藏导航，显示 ☰ 按钮触发折叠菜单

### Footer

- 单行（桌面），上下两行（移动）
- 左：版权 + License 链接
- 右：5 个链接（关于 / 贡献 / Schema / GitHub / RSS）

---

## 路由地图

```
/                                    → index.astro
/pitfalls                            → pitfalls/index.astro  (列表 + 过滤)
/pitfalls/<slug>                     → pitfalls/[...slug].astro  (详情，5,561 条预生成)
/pitfalls/<slug>/                    → 重定向到 /pitfalls/<slug> (Astro 默认)
/advisories                          → advisories/index.astro
/patterns                            → patterns/index.astro
/about                               → about.astro
/contributing                        → contributing.astro
/schema                              → schema.astro
/rss.xml                             → rss.xml.js (动态生成)
/sitemap-index.xml                   → 自动生成
/任何其他                             → 404.astro
```

---

## 性能数据

| 指标 | 值 |
|---|---|
| 总页面数 | **5,569** |
| 构建时间 | **8.7s** |
| 单页平均 HTML 大小 | ~6 KB |
| 避坑库列表页大小 | ~8.4 MB（含全部 pitfall dataset attributes） |
| JS 体积 | ~5 KB（仅 vanilla 搜索过滤） |
| 字体加载 | Google Fonts (Rubik + IBM Plex Mono) — 异步 |
| 图片 | 全部 SVG inline，无外链图 |
