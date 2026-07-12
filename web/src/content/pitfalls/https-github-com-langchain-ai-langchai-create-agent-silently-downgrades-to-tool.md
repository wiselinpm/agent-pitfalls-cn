---
title: "`create_agent` silently downgrades to `ToolStrategy` for dated model snapshots"
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
- langgraph
categories:
- observability
symptoms:
- This bug has been introduced in https://github.com/langchain-ai/langchain/pull/38042
root_causes:
- 'In `langchain/agents/factory.py`, `_supports_provider_strategy()` first consults `model.profile["structured_output"]`; when that is unavailable it falls back to matching the model name against `FALLBACK_MODELS_WITH_STRUCTURED_OUTPUT`:'
fixes: []
references:
- title: '`create_agent` silently downgrades to `ToolStrategy` for dated model snapshots'
  url: https://github.com/langchain-ai/langchain/issues/38220
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- external
contributor: pedroig
discovered_at: '2026-06-17'
verified: false
---

- [`create_agent` silently downgrades to `ToolStrategy` for dated model snapshots](https://github.com/langchain-ai/langchain/issues/38220) — github:langchain-ai/langchain

## 摘要

### Submission checklist

- [x] This is a bug, not a usage question.
- [x] I added a clear and descriptive title that summarizes this issue.
- [x] I used the GitHub search to find a similar question and didn't find it.
- [x] I am sure that this is a bug in LangChain rather than m

_来源热度：1_
