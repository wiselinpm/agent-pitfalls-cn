# Agent Pitfalls 🕳️

> **全网 AI Agent 开发避坑整合** — 不再重复踩同一个坑。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/fork)

[![Pitfalls](https://img.shields.io/badge/pitfalls-7%2C754-red)](https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/web/src/content/pitfalls)
[![Collectors](https://img.shields.io/badge/collectors-100-blue)](./collectors/)
[![Coverage](https://img.shields.io/badge/coverage-2016--2026-green)]()
[![Built with](https://img.shields.io/badge/built_with-Astro_5-orange)](https://astro.build)

```
🚨 7,893 pitfalls · 📡 100 collectors · 🌐 12+ languages · ⚡ 13s build
```

[English](./README.en.md) · [简体中文](./README.md) · [日本語](./README.ja.md) · [演示站点](https://github.com/wiselinpm/agent-pitfalls-cn) · [贡献指南](./CONTRIBUTING.md) · [Schema](./docs/SCHEMA.md)

---

### 🎯 一句话说清楚

你在开发 AI Agent 时遇到的每一个坑，这里都收录过 — **7,893 个真实踩坑案例**，每个都有 **症状 / 根因 / 修复 / 来源**，覆盖 Claude Code、OpenAI Agents SDK、LangChain、Cursor、Aider 等 14 个主流平台。

### 🚀 三种用法

| 用法 | 适合谁 | 怎么用 |
|------|--------|--------|
| **🌐 网站浏览** | 学习/培训/查阅 | 直接访问 [agent-pitfalls.dev](https://github.com/wiselinpm/agent-pitfalls-cn) |
| **🔍 CLI 即时查询** | 开发者 | `agent-pitfalls search "claude code context overflow"` |
| **🤖 插件集成** | Claude Code / Codex 用户 | `/pitfall <query>` 在会话里直接查 |

### 💡 核心价值

- **省时间**：遇到问题秒级定位 — 不用在 GitHub Issues、StackOverflow、Reddit 里翻半天
- **省 money**：提前规避 token 成本爆炸、rate limit 雪崩、context window 漂移等烧钱陷阱
- **省脑子**：每个坑都有结构化的 **症状→根因→修复**，不用自己分析
- **省事故**：prompt injection、密钥泄漏、sandbox 逃逸等安全问题提前预防

---

## 📸 站点预览

![Agent Pitfalls 首页 — Hero 代码块 + Stats + 热门分类 + 最新收录](./docs/screenshots/home.png)

*[点击查看完整截图 →](./docs/screenshots/home.png)*

> 上图：首页一次截图 — Hero 区用真实 pitfall 的 YAML 语法高亮做"艺术字"、4 列统计、热门分类 chip、最新收录卡片（双列）、CTA 链接组。零 JS 框架、零 hydration、构建产物纯静态。

---

## 📖 我们的故事与愿景

### 🕯️ 故事的起点

一切起源于一个普通的凌晨三点。

那天晚上，我们团队的一个 AI agent 在生产环境陷入了死循环。等值班同事发现的时候，OpenAI 的账单已经悄悄涨了 200 多美元。事后复盘，大家翻遍了 GitHub Issues、StackOverflow、Hacker News、知乎、掘金，却发现了一个尴尬的事实：

**这个坑别人早就踩过了。**

只是没有一个地方把它们汇总起来。坑散落在十几个平台的几十万条帖子、issue、博客、论文里，每个新团队都在用同一周时间踩同一批坑，写同一份事后报告，哭同一种「原来不止我一个人」的眼泪。

于是我们做了一个内部 wiki，把团队踩过的坑都记下来：**症状 / 根因 / 修复 / 参考链接**。每周 review 时拿出来对照，团队真的不再重复犯错了。

直到某一天我们意识到——

> **这件事不该只服务一个团队。整个 AI agent 生态都缺这一块拼图。**

### 🔥 我们看到的痛

2024 年起，AI agent 开发进入了「狂热建设期」。所有人都在堆工具、调 prompt、接 MCP、跑 multi-agent 编排。但狂热背后是一个尴尬的现实：

- 🩸 **Token 账单失血** — 一个未经审计的 agent，每月能悄悄烧掉几千到几万美元
- 🧨 **线上事故频发** — context window 静默截断、tool call 空参数、sandbox 逃逸、prompt injection，每一条都可能让产品下线
- 🤐 **知识不流通** — 别人踩过的坑，藏在某个 Discord 服务器的滚动消息里，或者三年前一条被遗忘的 HN 评论里
- 😩 **重复劳动** — 每个新团队都在「重新发明」那份事后报告，重复同样的调试、试错、复盘
- 📚 **学术与工业脱节** — arXiv 上有大量 agent 失败模式的研究，但没人翻译成「开发者今天就能用的知识」

**坑不是问题，坑不被记录才是问题。**

### 🌱 我们的愿景

我们想把 **Agent Pitfalls** 做成 AI agent 生态的 **「免疫系统」**：

> **当一个坑被某个人、某个团队、某篇论文踩过并解决了，它的「抗体」就应该永久沉淀下来，让下一个开发者不再踩同一个坑。**

具体来说，我们希望这个项目能成为：

- 📚 **最大的开放失败案例库** — 不只是堆数据，每个案例都有结构化的 **症状 → 根因 → 修复 → 来源**，让搜索、订阅、引用都成为可能
- 🤝 **开发者互助的协作平台** — 任何人都能 PR 一条新坑，CI 自动校验 schema、字段完整性、链接可达性
- 🛡️ **Agent 团队的「安全网」** — 上线前对照检查、新人入职培训教材、SRE 排障速查手册
- 🌐 **跨越语言与平台的边界** — Claude Code、OpenAI Agents SDK、LangChain、Cursor、Aider 等 14 个平台，跨 12+ 种语言，7,893+ 真实案例，一次收录
- 🧬 **机器可消费的知识** — JSON-LD、CLI JSON 输出、Python API、VSCode 实时提示，让 agent 自己也能查 pitfall

### 🪴 我们相信的事

- **失败比成功更有信息量** — 一个被修好的 bug，比十篇「如何用 LangChain」教程更值得记录
- **结构化胜过散文** — 只有 schema 化的知识，才能被搜索、被订阅、被引用、被 LLM 高效消费
- **开放优于闭源** — 坑是公共知识，避坑指南也应该是公共财产
- **自动化是规模化的前提** — 100 个 collector 7×24 自动抓取 + 三维度去重 + LLM 分类 + 人工抽检，是这个项目能跑到 7,893+ 条规模的唯一原因
- **中文社区同样值得被收录** — 知乎、掘金、CSDN、博客园里藏着大量没被英文世界看见的踩坑经验

### 🛤️ 已经走过的路

- ✅ **Round 1-6**：从 21 个 collector、3,486 条 pitfall 起步，一路扩到 100 个 collector、7,893 条结构化案例
- ✅ **三位一体**：静态站点 + Python CLI + Claude Code / Codex / OpenCode / Gemini 插件
- ✅ **严格去重**：URL fingerprint + 标题 SHA1 + 标题相似度，让同一条坑不被收录 5 遍
- ✅ **Zod schema 强校验**：CI 自动拦截不合格的 frontmatter
- ✅ **纯静态、零后端**：dist/ 推到 gh-pages 就是线上站点

### 🛰️ 接下来要走的路

- 🛰️ **采集更广** — Discord / Slack 官方频道、YouTube 字幕（开发者会议、技术分享）、微信公众号合规接入
- 🤖 **审核更准** — LLM 自动判断严重程度、自动抽取根因，把 `verified=true` 比例从现在的 ~10% 提升到 50%+
- 🪢 **关联更深** — 让 pitfall 之间产生因果链——「这个坑会触发那个坑」「这个修复缓解了那类问题」
- 🔌 **集成更紧** — VSCode 插件、JetBrains 插件，写 agent 代码时实时提示
- 📮 **触达更及时** — 周刊订阅，把每周新收录的 critical 坑推到你的邮箱
- 🌐 **社区更广** — 本地化（日语已上线，英语持续优化）、贡献者徽章、年度避坑报告

### 💌 一句话

> **让每一个被踩过的坑，都成为下一个开发者的台阶。**

---

## 💡 为什么做这个？

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
| **Pitfall 总数** | **7,893** |
| **覆盖年份** | 2016 - 2026（10 年） |
| **严重程度分布** | 🔴 critical 2,838 / 🟠 high 776 / 🟡 medium 4,135 / 🟢 low 144 |
| **Collector 数** | 100+ 个稳定可用 |
| **Source 引用种类** | 800+ 种（references.source 去重） |
| **构建产物** | 8,200+ 个静态页面 |
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

## 🛰️ 100+ 个 Collector — 覆盖国内外全网

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
                    │       Sources（100+ 个 collector）           │
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
                    │   (7,893 个 Markdown，Zod schema 强校验)     │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       Astro 5 静态生成                        │
                    │   (8,200+ pages · 8.7s · 零 JS hydration)   │
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

## 🖥️ CLI 工具 — 在开发期即时查询

**Agent Pitfalls CLI** 让你在 Claude Code / Codex / OpenCode / Gemini CLI 里直接查询避坑知识，不用离开终端。

### 安装

```bash
# 方式 1 — pip（推荐）
pip install agent-pitfalls

# 方式 2 — npx（自动找 Python）
npx agent-pitfalls search "context window overflow"

# 方式 3 — 一键脚本
curl -fsSL https://raw.githubusercontent.com/wiselinpm/agent-pitfalls-cn/main/install.sh | bash
```

### 实战场景：4 个真实案例

**场景 1：Claude Code 长会话行为漂移**

```bash
$ agent-pitfalls search "claude code 上下文漂移"

🔍 1/7893 matches for 'claude code 上下文漂移'

1. Claude Code 长会话中上下文被静默截断，模型「忘记」早期指令  [critical]
   症状：agent 在第 N 轮突然忽略最初设定的输出格式约束
   根因：客户端 SDK 默认在到达上限时丢弃最早的消息而非报错
   修复：每轮结束时显式计算 usage.input_tokens，设置 80% 警戒线
```

**场景 2：Tool call 空参数导致 JSON 解析崩溃**

```bash
$ agent-pitfalls search "tool call arguments empty"

🔍 1/7893 matches for 'tool call arguments empty'

1. OpenAI Chat Completions 工具调用 arguments 偶发返回空字符串  [high]
   症状：tool_calls[i].function.arguments 返回 ""，JSON 解析崩溃
   修复：累计 arguments += delta 直到 finish_reason=tool_calls
```

**场景 3：LangChain token 成本爆炸**

```bash
$ agent-pitfalls search "langchain token cost"

🔍 1/7893 matches for 'langchain token cost'

1. LangChain AgentExecutor 隐性 token 成本爆炸  [high]
   根因：每一步都把全部中间历史塞进 LLM 调用，O(n²) 增长
   修复：用 ConversationSummaryBufferMemory + max_iterations=10
```

**场景 4：Prompt injection 防护**

```bash
$ agent-pitfalls search "prompt injection 防护"

🔍 1/7893 matches for 'prompt injection 防护'

1. 工具返回内容里的 Prompt 注入可劫持 Agent 主流程  [critical]
   根因：工具结果与系统提示在同一个 prompt 拼接，没有边界
   修复：输入消毒 + 权限隔离 + 工具结果标记边界
```

### 子命令速览

```bash
agent-pitfalls build                              # 首次构建索引（秒级）
agent-pitfalls search "claude code context overflow"  # 智能查询
agent-pitfalls search "tool call" --platform openai-agents --severity high
agent-pitfalls list --category cost --limit 10    # 列表 + 过滤
agent-pitfalls show <slug>                        # 查看详情
agent-pitfalls check .                            # 项目避坑体检
agent-pitfalls platforms                          # 平台统计
agent-pitfalls categories                         # 类别统计
agent-pitfalls serve                              # 本地 HTTP 服务（MCP 通道）
```

### 智能查询逻辑

不是关键词匹配，而是 **多字段加权 BM25 + 语义扩展**：

| 字段 | 权重 | 说明 |
|------|------|------|
| `title` | 4.0 | 标题是用户最常匹配的目标 |
| `symptoms` | 3.0 | 用户报现象时常描述症状 |
| `summary` | 2.0 | 摘要点出主题 |
| `root_causes` / `fixes` | 1.5 | 解决方案 |
| 全文 | 1.0 | 兜底 |

加上：**平台匹配加成 ×1.5** · **类别匹配加成 ×1.3** · **中英文同义词扩展**（`token limit` ⇄ `上下文` ⇄ `context window`） · **严重度 + verified 加成** · **领域相关性过滤**（排除保险 agent、传销新闻等无关内容）。

### 项目避坑体检

```bash
agent-pitfalls check .               # 扫描当前项目
agent-pitfalls check src/ --json     # CI 用 JSON 输出
```

每条 issue 自动关联知识库里的相关 pitfall，附 slug / severity / URL：

```
● verbose 日志可能泄漏密钥/PII
  src/main.py:42
  > verbose=True
    → Agent 调试日志意外打印 API Key
      api-key-leaked-in-logs  [critical]
```

### 在主流 AI CLI 里使用

| CLI | 安装方式 | 使用 |
|-----|---------|------|
| **Claude Code** | `ln -s plugin ~/.claude/plugins/agent-pitfalls` | `/pitfall <query>` · `/pitfall-check .` |
| **Codex** | `cp -r plugin/codex/* ~/.codex/prompts/agent-pitfalls/` | `/pitfall <query>` |
| **OpenCode** | `ln -s plugin/opencode.json ~/.opencode/plugins/` | `/pitfall <query>` |
| **Gemini CLI** | `cp plugin/gemini-extension.json ~/.gemini/extensions/` | `/pitfall <query>` |

详见 [`plugin/README.md`](./plugin/README.md)。

### JSON 输出（给 LLM 调）

```bash
agent-pitfalls search "prompt injection" --json | jq '.hits[0].fixes'
agent-pitfalls check . --json | jq '.issues[] | {file, title}'
```

### Python API

```python
from agent_pitfalls_cli.search import search, scan_project
from agent_pitfalls_cli.index import load_records

records = load_records()
result = search(records, "context window overflow", top_k=5)
for hit in result.hits:
    print(f"{hit.score:.1f} | {hit.record.title} | {hit.record.severity}")
```

---

## 🗺️ Roadmap

- [x] Round 1: 基础采集（21 个 collector · 3,486 pitfalls）
- [x] Round 2: 增强采集（+13 collectors · 3,792 pitfalls）
- [x] Round 3: 学术补充（+8 collectors · 4,098 pitfalls）
- [x] Round 4: 全网扩展（+9 collectors · 5,427 pitfalls）
- [x] Round 5: 趋势 + 评论 + Tech news（+5 collectors · 5,509 pitfalls）
- [x] Round 6: 学术 + KOL + 政府安全（+7 collectors · 7,893 pitfalls）
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

混合模式 — 100+ 个 collector 自动从全网抓取 → 三维度严格去重 → LLM 初步分类 → 人工抽检 verified 标记。
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

**Agent Pitfalls** is the largest open collection of real-world AI agent development failure modes — 7,893 pitfalls across 72 sources (GitHub, HN, Reddit, arXiv, Chinese forums, vendor blogs, individual KOLs, podcasts, government security advisories, etc.).

Each entry has structured fields: **symptoms · root causes · fixes · references · severity**, validated by Zod schema and deduplicated by URL fingerprint + title hash + title similarity.

Built with Astro 5 + Tailwind, zero backend, deploy anywhere static.

```bash
git clone https://github.com/wiselinpm/agent-pitfalls-cn.git
cd agent-pitfalls-cn
npm install && npm run dev   # http://localhost:4321
```

**License**: MIT (code) + CC-BY 4.0 (content). PRs welcome.
