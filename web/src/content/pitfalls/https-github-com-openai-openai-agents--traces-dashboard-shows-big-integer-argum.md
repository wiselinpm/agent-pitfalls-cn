---
title: Traces dashboard shows big integer arguments incorrectly in tool calling traces
summary: '### Describe the bug When passing big integers (like still within int64 range but beyond JS number''s precision) to functions, the library passes the precise numbers but the traces dashboard (https://platform.openai.com/logs/trace) shows truncated numbers. Context: I was testing'
severity: medium
platforms:
- openai-agents
categories:
- tool-use
- streaming
- observability
symptoms:
- When passing big integers (like still within int64 range but beyond JS number's precision) to functions, the library passes the precise numbers but the traces dashboard (https://platform.openai.com/logs/trace) shows truncated numbers.
root_causes: []
fixes: []
references:
- title: Traces dashboard shows big integer arguments incorrectly in tool calling traces
  url: https://github.com/openai/openai-agents-python/issues/2094
  source: github:openai/openai-agents-python
tags:
- bug
- wontfix
- feature:tracing
- server issue
contributor: cuihaoleo
discovered_at: '2025-11-18'
verified: false
---

- [Traces dashboard shows big integer arguments incorrectly in tool calling traces](https://github.com/openai/openai-agents-python/issues/2094) — github:openai/openai-agents-python

## 摘要

### Describe the bug

When passing big integers (like still within int64 range but beyond JS number's precision) to functions, the library passes the precise numbers but the traces dashboard (https://platform.openai.com/logs/trace) shows truncated numbers.

Context: I was testing

_来源热度：3_
