# Agent Pitfalls 🕳️

> **全网 AI Agent 开发避坑整合** — 不再重复踩同一个坑。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/fork)

[![Pitfalls](https://img.shields.io/badge/pitfalls-5%2C561-red)](https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/web/src/content/pitfalls)
[![Collectors](https://img.shields.io/badge/collectors-72-blue)](./collectors/)
[![Coverage](https://img.shields.io/badge/coverage-2016--2026-green)]()
[![Built with](https://img.shields.io/badge/built_with-Astro_5-orange)](https://astro.build)

```
🚨 5,561 pitfalls · 📡 72 collectors · 🌐 12+ languages · ⚡ 8s build
```

[English](./README.en.md) · [简体中文](./README.md) · [日本語](./README.ja.md) · [演示站点](https://github.com/wiselinpm/agent-pitfalls-cn) · [贡献指南](./CONTRIBUTING.md) · [Schema](./docs/SCHEMA.md)

---

## 📸 站点预览

![Agent Pitfalls 首页 — Hero 代码块 + Stats + 热门分类 + 最新收录](./docs/screenshots/home.png)

*[点击查看完整截图 →](./docs/screenshots/home.png)*

> 上图：首页一次截图 — Hero 区用真实 pitfall 的 YAML 语法高亮做"艺术字"、4 列统计、热门分类 chip、最新收录卡片（双列）、CTA 链接组。零 JS 框架、零 hydration、构建产物纯静态。

---

## 💡 为什么做这个？

每个做 AI Agent 的团队都会反复踩同一批坑：

- 😱 Context window 静默截断，关键信息丢失
- 💸 Tool call 空参数，token 成本爆炸 10×
- 🔓 Prompt 注入，agent 被恶意接管
- 🔁 Multi-agent 死循环，账单失控
- 🤐 Verbose 日志泄漏 API Key 到 Sentry
- 🧠 Memory 框架版本不兼容，凌晨 3 点排障
- ⏱️ Streaming timeout，没有 retry，websocket 莫名断开
- 📦 Embedding 模型升级，向量维度变化，全量重建
- 🎭 Jailbreak 绕过 system prompt，金融 agent 输出违规内容
- 🛠️ Function calling schema 不匹配，agent 永远调不到工具

这些坑散落在 **GitHub Issues / HackerNews / Reddit / 知乎 / 博客 / 学术论文** 等十几个平台，没人汇总过。

**Agent Pitfalls** 把它们汇集到一处 — 每一个坑都有 **症状 / 根因 / 修复 / 来源**，可搜索、可订阅。

---

## ✨ 一条典型的 pitfall 长什么样？

```yaml
---
title: Agent 调试日志意外打印 API Key / 用户隐私
summary: LangChain / OpenAI Agents SDK 的 verbose 模式会打印完整 prompt，
  含 system message 里的密钥与用户 PII，触发安全事故。
severity: critical
platforms: [langchain, openai-agents, generic]
categories: [security, observability]
symptoms:
  - '日志文件里出现 sk-proj-... 或用户邮箱'
  - CI 把 prompt 上传到 Sentry/Datadog
  - 团队截图调试输出时泄漏密钥
root_causes:
  - 'verbose=True / debug=True 默认打印所有 LLM 输入输出'
  - prompt 模板硬编码密钥或从 env 注入但仍被序列化
  - structlog/loguru 默认不脱敏
fixes:
  - 永远不在 prompt 模板硬编码密钥；用 secret manager 注入
  - 实现 RedactingFilter 拦截 sk-、Bearer、邮箱等模式
  - 生产关闭 verbose，调试用 dry_run 模式只打摘要
  - 团队规范：截图前先 grep 密钥
references:
  - title: LangChain Debugging 与日志
    url: https://python.langchain.com/docs/how_to/debugging/
  - title: Sentry data scrubbing
    url: https://docs.sentry.io/platforms/python/data-management/sensitive-data/
contributor: agent-pitfalls-bot
discovered_at: 2025-10-01
verified: true
---
```

完整的 RedactingFilter 实现、复现步骤、相关 issue 链接，全在这一份 markdown 里。

---

## 🎯 它适合谁？

| 你是… | 你能拿到什么 |
|---|---|
| **AI Agent 开发者** | 上线前对照检查 — 哪些坑还没规避 |
| **Tech Lead / 架构师** | 团队培训材料 — 真实案例比 PPT 更深刻 |
| **SRE / 运维** | 故障排查 — 看到现象就能定位到已知坑 |
| **研究员 / 学生** | 真实失败案例集 — 比论文里的 synthetic benchmark 有用 |
| **Agent 平台厂商** | 竞品 bug 追踪 — 看用户在哪里骂得最凶 |
| **CTO / 投资人** | 行业健康度 — 哪些问题已经被解决，哪些仍是开放问题 |

---

## 📊 数据规模

| 维度 | 数据 |
|---|---|
| **Pitfall 总数** | **5,561** |
| **覆盖年份** | 2016 - 2026（10 年） |
| **严重程度分布** | 🔴 critical 2,210 / 🟠 high 455 / 🟡 medium 2,786 / 🟢 low 110 |
| **Collector 数** | 72 个稳定可用 |
| **Source 引用种类** | 800+ 种（references.source 去重） |
| **构建产物** | 5,569 个静态页面 |
| **构建耗时** | 8.7s |

### 收录来源分布（top 10）

```
2,228  google-news          全网新闻索引（37 个双语 query）
  878  vercel-blog          Vercel 工程 blog（大量 AI 应用避坑）
  303  github               GitHub Issues（多个 agent repo）
  206  stackoverflow        QA 问答
  192  hn-search            HN Algolia 12 个 query 全量
  151  hackernews           HN 最新
  134  hn-algolia-ext       HN 全文搜索
  129  devto                dev.to 文章
  122  openai-blog          OpenAI 官方
  107  arxiv-cat            arXiv 分类
```

---

## 🛰️ 72 个 Collector — 覆盖国内外全网

### 国际主流
`github-issues` · `github-releases` · `rss` · `hackernews` · `hn-search` · `hn-comments` · `hn-algolia-extended` · `stackoverflow` · `devto` · `devto-latest` · `dev-community` · `medium` · `substack` · `youtube` · `lobsters` · `huggingface-papers` · `huggingface-blog` · `hf-trending` · `producthunt` · `official-status` · `vendor-blogs` · `newsletters` · `frameworks` · `tldr` · `forums` · `extra-en` · `meta-search` · `bilibili` · `weibo` · `bilibili-hot` · `communities`

### 学术
`arxiv` · `arxiv-v2` · `arxiv-categories` · `openreview` · `dblp` · `acl-anthology` · `papers-with-code` · `semantic-scholar`

### AI / 厂商
`openai-blog` · `anthropic-blog` · `anthropic-status` · `aws-ml` · `deepmind-blog` · `google-ai-blog` · `huggingface-blog` · `ai-research-blog` · `ai-newsletter` · `vendor-official` · `frameworks`

### 国内
`google-news` (双语) · `segmentfault` · `cnblogs` · `csdn` · `oschina` · `meituan` · `sspai` · `cloud-cn` · `sogou-wechat` · `infoq-cn` · `cn-eng-blog` · `cn-tech-media` · `zhihu` (旧/新) · `juejin` (旧/新)

### 个人 KOL / Newsletter / Podcast
`kol-blog` (Simon Willison / Ethan Mollick / Andrej Karpathy / Ben Thompson / a16z 等 16 个) · `podcast` (Lex Fridman / Latent Space / Changelog / Darknet Diaries / SE Daily 等) · `feed-aggregator` (30+ 边缘博客)

### 政府 / 安全
`gov-sec` (CISA / NVD / US-CERT / Exploit-DB / CVE Details)

### 趋势 / GitHub
`github-trending` (all/python/typescript/go × daily/weekly) · `feed-aggregator`

详见 [`collectors/SOURCES.md`](./collectors/SOURCES.md)。

---

## 🏗️ 架构

```
                    ┌─────────────────────────────────────────────┐
                    │       Sources（72 个 collector）            │
                    │   GitHub · HN · Dev.to · arXiv · ...        │
                    └────────────────────┬────────────────────────┘
                                         │ RawHit[]
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       normalize: RawHit → PitfallDraft       │
                    │   (统一字段、补 fingerprint)                  │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       三维度严格去重                          │
                    │   1. URL fingerprint (去除 utm_/fbclid)      │
                    │   2. 标题 SHA1 hash                           │
                    │   3. 标题 Jaccard/SequenceMatcher ≥ 0.85     │
                    │   + token 反向索引加速（4s 完成 1,559 比较）  │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       web/src/content/pitfalls/*.md          │
                    │   (5,561 个 Markdown，Zod schema 强校验)     │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       Astro 5 静态生成                        │
                    │   (5,569 pages · 8.7s · 零 JS hydration)    │
                    └─────────────────────────────────────────────┘
```

**关键设计**：
- ✅ **零后端** — 纯静态站，可一键部署到 GitHub Pages / Cloudflare Pages / Vercel
- ✅ **三维度严格去重** — 同一坑不会被 5 个来源重复收录
- ✅ **Zod schema 强校验** — CI 自动检查 frontmatter 合法性
- ✅ **采集幂等** — 重复跑不会覆盖人工编辑过的条目（除非显式 `--overwrite`）
- ✅ **抓取失败兜底** — 单个 source 挂掉不影响其它 source（`safe_collect`）

---

## 🚀 5 分钟跑起来

### 在线浏览

部署好的站点：[agent-pitfalls.dev](https://github.com/wiselinpm/agent-pitfalls-cn)（本地预览见下）

### 本地开发

```bash
# 1. 克隆
git clone https://github.com/wiselinpm/agent-pitfalls-cn.git
cd agent-pitfalls-cn

# 2. 安装依赖
npm install                          # Astro + Tailwind
pip install -r requirements-dev.txt  # Python 采集器

# 3. 启动站点
npm run dev                          # http://localhost:4321
```

### 自建站点

```bash
npm run build                        # 静态产物输出到 dist/
npm run preview                      # 本地预览生产构建
```

部署到 GitHub Pages：把 `dist/` 推到 `gh-pages` 分支，或开 Actions 自动部署。

### 重新采集

```bash
# 配 GitHub token 提高 rate limit（强烈建议）
export GITHUB_TOKEN=ghp_xxx

# 跑全部 collector
python -m collectors.run_all --out data/raw

# 三维度去重 + 写入 web/src/content/pitfalls/
python scripts/merge_round4.py --in-dirs data/raw* --apply
```

详见 [`collectors/README.md`](./collectors/README.md)。

---

## 📝 Schema 速查

每个 pitfall 文件的 frontmatter：

```yaml
---
title: 一句话描述（4-120 字）
summary: 2-3 句概览（10-300 字）
severity: critical | high | medium | low
platforms: [claude-code, langchain, ...]   # 14 个枚举
categories: [context-window, tool-use, ...] # 14 个枚举
symptoms: ['现象 1', '现象 2']
root_causes: ['根因 1']
fixes: ['修复 1', '修复 2']
references:
  - title: 来源标题
    url: https://...
    source: GitHub / HN / 知乎
discovered_at: 2026-01-15
verified: true               # 人工复核过
contributor: your-handle
---
```

完整枚举值见 [`docs/SCHEMA.md`](./docs/SCHEMA.md)。

---

## 🤝 贡献 — 任何形式的贡献都受欢迎

### 我想加一条 pitfall

1. 在 `web/src/content/pitfalls/` 新建 `kebab-case.md`
2. 复制上面的 frontmatter 模板填写
3. 正文写「复现步骤 / 为什么坑 / 修复代码」
4. 提 PR — CI 自动校验 schema、字段完整性、链接可达性
5. 维护者 review 后合并

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

### 我想加一个 collector

```python
# collectors/sources/my_source.py
from typing import Iterable
from ..base import RawHit

class MySourceCollector:
    name = "my-source"
    
    def collect(self) -> Iterable[RawHit]:
        for item in fetch_my_data():
            yield RawHit(
                title=item.title,
                url=item.url,
                source="my-source",
                summary=item.summary,
            )
```

在 `collectors/sources/__init__.py` 注册，pytest 加单测，PR。

### 我想改 UI / 文案

`web/src/pages/`、`web/src/components/`、`web/src/layouts/` — 改完发 PR 即可。

### 我想纠错

内容错误、链接失效、分类不当 — 直接开 issue 标 `correction`。

---

## 🗺️ Roadmap

- [x] Round 1: 基础采集（21 个 collector · 3,486 pitfalls）
- [x] Round 2: 增强采集（+13 collectors · 3,792 pitfalls）
- [x] Round 3: 学术补充（+8 collectors · 4,098 pitfalls）
- [x] Round 4: 全网扩展（+9 collectors · 5,427 pitfalls）
- [x] Round 5: 趋势 + 评论 + Tech news（+5 collectors · 5,509 pitfalls）
- [x] Round 6: 学术 + KOL + 政府安全（+7 collectors · 5,561 pitfalls）
- [ ] **Round 7**: Discord / Slack 官方频道接入
- [ ] **Round 8**: YouTube 字幕提取（开发者会议、技术分享）
- [ ] **Round 9**: 微信小程序 / 公众号合规接入
- [ ] **Round 10**: LLM 自动审核 + 严重程度分类
- [ ] 跨坑关联（一个坑触发另一个坑）
- [ ] 按 SDK 版本/模型版本筛选
- [ ] CLI 工具：`npx agent-pitfall search "context window"`
- [ ] VSCode 插件：编辑 agent 代码时实时提示
- [ ] 邮件周刊订阅

---

## 📈 它跟现有资源有什么不同？

| 资源 | Agent Pitfalls | Awesome-* lists | 博客文章 | arXiv 论文 |
|---|---|---|---|---|
| **结构化字段** | ✅ schema | ❌ 自由 markdown | ❌ 散文 | ❌ PDF |
| **症状 / 根因 / 修复分离** | ✅ | ❌ | ⚠️ 部分 | ⚠️ 部分 |
| **多源交叉验证** | ✅ 三维度去重 | ❌ | ❌ | ❌ |
| **可机器消费** | ✅ JSON-LD | ⚠️ | ❌ | ❌ |
| **持续更新** | ✅ 自动化 | ⚠️ 手动 | ⚠️ 手动 | ⚠️ 手动 |
| **中文覆盖** | ✅ 25% | ❌ | ⚠️ | ⚠️ |
| **可贡献** | ✅ 低门槛 PR | ⚠️ | ⚠️ | ⚠️ |
| **可订阅** | ✅ RSS | ❌ | ⚠️ | ⚠️ |

---

## 🔢 数据准确性

- ✅ 所有 pitfall 至少 1 条 `reference`（CI 校验 URL 可达）
- ✅ 所有 pitfall 至少 1 条 `fixes`（不只是现象描述）
- ✅ `severity=critical` 的条目必须 `verified=true` 才出现在首页推荐位
- ✅ 三维度去重后保留 score 最高的版本（同分保留更具体的 source）

但请注意：
- ⚠️ 大量条目由 LLM 半自动整理，可能有事实错误 — 请开 issue 标 `correction`
- ⚠️ `verified=false` 的条目未经人工复核，仅供参考

---

## 🛠️ 常见问题

<details>
<summary><b>为什么不收录微信公众号？</b></summary>

合规风险 — 微信内容版权属于发布者，且 RSS 抓取需登录态。当前用 Google News 中文 query 作为间接索引。
</details>

<details>
<summary><b>为什么不收录 Bilibili/微博？</b></summary>

2024 年起两家公开 RSS 全部 403，需要登录态。同样用 Google News 间接索引。
</details>

<details>
<summary><b>数据是手工整理还是自动抓取？</b></summary>

混合模式 — 72 个 collector 自动从全网抓取 → 三维度严格去重 → LLM 初步分类 → 人工抽检 verified 标记。
</details>

<details>
<summary><b>能不能商用？</b></summary>

可以。代码 MIT License；内容 CC-BY 4.0（默认）；如有第三方来源，引用时遵循各自协议。
</details>

<details>
<summary><b>有没有 API？</b></summary>

数据本身就是 markdown 文件，可直接 grep / 用 ripgrep 搜：`rg '"severity": "critical"' web/src/content/pitfalls/`。
后续会提供 JSON API（见 Roadmap）。
</details>

---

## 📜 License

- **代码**：[MIT](./LICENSE)
- **内容**（Markdown 条目）：[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)（默认）；如有第三方来源，引用时遵循各自协议

## 🙏 致谢

本项目站在巨人的肩膀上 — 所有内容的真正作者是那些在 GitHub Issues、Hacker News、知乎专栏、学术论文里分享踩坑经验的开发者们。我们只是搬运 + 整理 + 索引。

特别感谢所有 [contributors](https://github.com/wiselinpm/agent-pitfalls-cn/graphs/contributors) ❤️

## ⭐ Star History

如果这个项目帮到了你，欢迎点一个 ⭐ — 这是它被更多人看到的最好方式。

---

## English

**Agent Pitfalls** is the largest open collection of real-world AI agent development failure modes — 5,561 pitfalls across 72 sources (GitHub, HN, Reddit, arXiv, Chinese forums, vendor blogs, individual KOLs, podcasts, government security advisories, etc.).

Each entry has structured fields: **symptoms · root causes · fixes · references · severity**, validated by Zod schema and deduplicated by URL fingerprint + title hash + title similarity.

Built with Astro 5 + Tailwind, zero backend, deploy anywhere static.

```bash
git clone https://github.com/wiselinpm/agent-pitfalls-cn.git
cd agent-pitfalls-cn
npm install && npm run dev   # http://localhost:4321
```

**License**: MIT (code) + CC-BY 4.0 (content). PRs welcome.
