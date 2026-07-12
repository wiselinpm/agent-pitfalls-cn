---
description: 在 agent-pitfalls 知识库里查询避坑指南 — 支持平台 / 类别 / 严重度过滤
argument-hint: <query> [--platform claude-code,langchain] [--category context-window] [--severity critical]
allowed-tools: Bash(agent-pitfalls:*), Bash(python:*)
---

# /pitfall — 智能查询 agent 避坑知识

把 `$ARGUMENTS` 作为查询词传给 `agent-pitfalls search`。返回与当前任务最相关的 pitfalls（症状→根因→修复）。

## 用法

```
/pitfall claude code context overflow
/pitfall tool call empty arguments --platform openai-agents --severity high
/pitfall prompt injection --category prompt-injection
```

## 执行

```bash
agent-pitfalls search "$ARGUMENTS" --no-color
```

如果 `agent-pitfalls` 没安装，提示用户运行：

```bash
pip install agent-pitfalls     # 或
npm i -g agent-pitfalls        # 或
npx agent-pitfalls search "$ARGUMENTS"
```

## 输出格式

工具会输出形如：

```
🔍 N/5561 matches for '...'
  detected: platforms=[...] categories=[...]

1. <标题>  [<severity>]  score=...
   <摘要>
   platforms: ...
   categories: ...
   matched: title, summary, symptoms
   slug: <slug>
   ref: <url>

   ▸ <最匹配的一行症状/修复>
```

把最相关的 1-3 条贴进对话，直接用于：

- 让 agent 在写代码前「对照避坑」
- 把 root_cause / fixes 当作约束喂给子 agent
- 在 review 时引用 slug 作为 issue 标签