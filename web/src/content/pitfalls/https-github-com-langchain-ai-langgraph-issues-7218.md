---
title: AsyncPostgresStore.abatch acquires unused connection and double-checks out from pool
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
- cursor
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: AsyncPostgresStore.abatch acquires unused connection and double-checks out from pool
  url: https://github.com/langchain-ai/langgraph/issues/7218
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: maheshpatchava
discovered_at: '2026-03-18'
verified: false
---

- [AsyncPostgresStore.abatch acquires unused connection and double-checks out from pool](https://github.com/langchain-ai/langgraph/issues/7218) — github:langchain-ai/langgraph

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangGraph rather tha
