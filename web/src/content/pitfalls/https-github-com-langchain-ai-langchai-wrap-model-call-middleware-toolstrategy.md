---
title: "`wrap_model_call` middleware ToolStrategy narrowing has no effect — model still sees all structured output too..."
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- tool-use
- streaming
- observability
symptoms: []
root_causes: []
fixes:
- 'In `_get_bound_model()`, filter structured output tools to only those present in `effective_response_format.schema_specs`:'
references:
- title: '`wrap_model_call` middleware ToolStrategy narrowing has no effect — model still sees all structured output tools'
  url: https://github.com/langchain-ai/langchain/issues/36568
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- external
contributor: leforebs95
discovered_at: '2026-04-06'
verified: false
---

- [`wrap_model_call` middleware ToolStrategy narrowing has no effect — model still sees all structured output tools](https://github.com/langchain-ai/langchain/issues/36568) — github:langchain-ai/langchain

## 摘要

### Checked other resources

- [x] This is a bug, not a usage question.
- [x] I added a clear and descriptive title that summarizes this issue.
- [x] I used the GitHub search to find a similar question and didn't find it.
- [x] I am sure that this is a bug in LangChain rather tha

_来源热度：8_
