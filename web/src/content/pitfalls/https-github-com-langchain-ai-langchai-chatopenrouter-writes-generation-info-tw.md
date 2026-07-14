---
title: '`ChatOpenRouter` writes `generation_info` twice causing double strings as values'
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- state
symptoms: []
root_causes:
- print(f"\n{'='*60}")
fixes:
- llm_no_stream = ChatOpenRouter(
references:
- title: '`ChatOpenRouter` writes `generation_info` twice causing double strings as values'
  url: https://github.com/langchain-ai/langchain/issues/38226
  source: github:langchain-ai/langchain
tags:
- bug
- external
- openrouter
contributor: shane-rand
discovered_at: '2026-06-17'
verified: false
---

- [`ChatOpenRouter` writes `generation_info` twice causing double strings as values](https://github.com/langchain-ai/langchain/issues/38226) — github:langchain-ai/langchain

## 摘要

### Submission checklist

- [x] This is a bug, not a usage question.
- [x] I added a clear and descriptive title that summarizes this issue.
- [x] I used the GitHub search to find a similar question and didn't find it.
- [x] I am sure that this is a bug in LangChain rather than m

_来源热度：6_
