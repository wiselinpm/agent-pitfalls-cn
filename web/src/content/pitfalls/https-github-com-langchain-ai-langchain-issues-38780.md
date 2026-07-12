---
title: "`_parse_input` silently drops required fields resolved via `validation_alias` in `args_schema`"
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
symptoms: []
root_causes:
- 'In `langchain_core/tools/base.py`, `_parse_input()` lines 740-756:'
fixes:
- 'After `model_validate()` succeeds, any field in `result_dict` has been validated successfully. If it''s a real field (not synthetic), it should be included:'
references:
- title: '`_parse_input` silently drops required fields resolved via `validation_alias` in `args_schema`'
  url: https://github.com/langchain-ai/langchain/issues/38780
  source: github:langchain-ai/langchain
tags:
- bug
- core
- external
contributor: charan16
discovered_at: '2026-07-10'
verified: false
---

- [`_parse_input` silently drops required fields resolved via `validation_alias` in `args_schema`](https://github.com/langchain-ai/langchain/issues/38780) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
