---
title: "Checkpoint serialization rejects range and PurePath variants (TypeError) -- same gap as Fraction/complex in #8185"
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- state
symptoms:
- 'Same root cause as #8185 (Fraction/complex) -- JsonPlusSerializer''s _msgpack_default doesn''t handle these types, and PurePath variants slip past the existing isinstance(obj, pathlib.Path) check since they aren''t Path subclasses.'
root_causes: []
fixes: []
references:
- title: 'Checkpoint serialization rejects range and PurePath variants (TypeError) -- same gap as Fraction/complex in #8185'
  url: https://github.com/langchain-ai/langgraph/issues/8326
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: Janvita
discovered_at: '2026-07-11'
verified: false
---

- [Checkpoint serialization rejects range and PurePath variants (TypeError) -- same gap as Fraction/complex in #8185](https://github.com/langchain-ai/langgraph/issues/8326) — github:langchain-ai/langgraph

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangGraph rather tha
