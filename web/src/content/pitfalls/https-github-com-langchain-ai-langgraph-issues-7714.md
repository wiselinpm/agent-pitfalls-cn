---
title: "LangGraph checkpoint serialization produces 85% storage bloat and 37.8% token overhead with no opt-out path - ..."
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- context-window
- streaming
- cost
symptoms:
- 'langchain-ai/langchain #36764 - Token-efficient serialization for agent message passing (feature request, langchain-core)'
root_causes: []
fixes:
- 'I have implemented and benchmarked a drop-in extension that demonstrates the fix is viable today:'
references:
- title: LangGraph checkpoint serialization produces 85% storage bloat and 37.8% token overhead with no opt-out path - reproducible with drop-in fix
  url: https://github.com/langchain-ai/langgraph/issues/7714
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: makroumi
discovered_at: '2026-05-05'
verified: false
---

- [LangGraph checkpoint serialization produces 85% storage bloat and 37.8% token overhead with no opt-out path - reproducible with drop-in fix](https://github.com/langchain-ai/langgraph/issues/7714) — github:langchain-ai/langgraph

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangGraph rather tha
