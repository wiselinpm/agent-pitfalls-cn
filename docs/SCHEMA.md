# Schema 详细参考

> 这份文档的 zod 定义在 `web/src/content.config.ts`，是权威来源；这里只是人类可读版本。

## Pitfall（避坑条目）

| 字段 | 类型 | 必填 | 取值 / 说明 |
|------|------|------|------------|
| `title` | string (4-120) | ✓ | 一句话描述问题 |
| `summary` | string (10-300) | ✓ | 2-3 句概览 |
| `severity` | enum | ✓ | `critical` / `high` / `medium` / `low` |
| `platforms` | enum[] | | 受影响的 agent 平台 |
| `categories` | enum[] | | 分类标签 |
| `symptoms` | string[] | | 用户/Agent 看到的现象 |
| `root_causes` | string[] | | 为什么发生 |
| `fixes` | string[] | | 具体修复步骤 |
| `references` | object[] | | 公开来源链接 |
| `tags` | string[] | | 自由标签 |
| `discovered_at` | ISO date | | 首次发现日期 |
| `verified` | boolean | | 是否被人工复核 |
| `contributor` | string | | 贡献者 GitHub handle |

## 取值枚举

### `severity`

| 值 | 含义 |
|----|------|
| `critical` | 数据丢失、安全漏洞、生产事故 |
| `high` | 默认配置下大概率触发，难以绕过 |
| `medium` | 特定条件下触发，规避方案存在 |
| `low` | 体验/性能问题，影响有限 |

### `platforms`

`claude-code`, `openai-agents`, `langchain`, `autogen`, `crewai`,
`langgraph`, `open-interpreter`, `devin`, `cursor`, `aider`,
`claude-api`, `openai-api`, `gemini-api`, `generic`

### `categories`

`context-window`, `tool-use`, `streaming`, `cost`, `security`,
`observability`, `memory`, `multi-agent`, `prompt-injection`,
`sandbox`, `reliability`, `latency`, `state`, `tokenization`

### `references[]` 对象结构

```yaml
- title: 链接标题（必填）
  url: https://example.com/article（必填，必须是合法 URL）
  source: GitHub / HN / 知乎（可选，用于显示归属）
  accessed_at: 2026-01-15（可选，记录抓取时间）
```

## Advisory（安全公告）

```yaml
title: 简洁标题
summary: 一段话
severity: critical | high | medium | low
affected: [claude-api, claude-code]
published_at: 2026-01-09
references:
  - title: 公告标题
    url: https://...
```

## Pattern（应对模式）

```yaml
title: 模式名
summary: 一句话说明
use_when: 适用场景
pros: [优点 1, 优点 2]
cons: [代价 1, 代价 2]
example: |
  代码或伪代码示例（可选）
```

## 校验规则

- frontmatter 必须可被 zod schema 解析（CI 自动跑）
- 至少 1 条 `reference`，且 URL 必须 200
- 至少 1 条 `fix`（不能只是「现象描述」而无修复）
- `severity=critical` 时必须 `verified=true` 才会出现在首页推荐位