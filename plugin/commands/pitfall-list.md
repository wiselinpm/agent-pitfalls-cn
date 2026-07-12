---
description: 列出 agent-pitfalls 知识库里的 pitfalls（支持按平台 / 类别 / 严重度过滤）
argument-hint: [--platform claude-code] [--category context-window] [--severity critical]
allowed-tools: Bash(agent-pitfalls:*), Bash(python:*)
---

# /pitfall-list — 浏览知识库

按条件列出 pitfalls，便于人工 review / 培训材料整理。

## 用法

```bash
agent-pitfalls list --platform langchain --severity critical
agent-pitfalls list --category cost --limit 20
agent-pitfalls list --json | jq '.[].slug'
```

## 元信息

- `agent-pitfalls platforms` — 所有平台及数量
- `agent-pitfalls categories` — 所有类别及数量