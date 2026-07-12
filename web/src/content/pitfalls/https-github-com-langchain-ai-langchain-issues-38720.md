---
title: _resolve_schemas processes a repeated state schema at its FIRST position, so the explicit state_schema can lose field co
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- state
symptoms:
- 'PR #37223 (merged 2026-05-06) introduced both the documented contract and the bug: its regression test `test_last_schema_wins_for_conflicting_field` covers three distinct schema types, but never a duplicated one.'
root_causes: []
fixes: []
references:
- title: _resolve_schemas processes a repeated state schema at its FIRST position, so the explicit state_schema can lose field conflicts to middleware
  url: https://github.com/langchain-ai/langchain/issues/38720
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- external
contributor: alex-feel
discovered_at: '2026-07-08'
verified: false
---

- [_resolve_schemas processes a repeated state schema at its FIRST position, so the explicit state_schema can lose field conflicts to middleware](https://github.com/langchain-ai/langchain/issues/38720) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
