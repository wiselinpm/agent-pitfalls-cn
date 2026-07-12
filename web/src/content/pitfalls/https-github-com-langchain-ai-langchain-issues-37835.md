---
title: Importing langchain.agents breaks BaseLLM class construction on Pydantic main
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- openai-agents
- langchain
- langgraph
categories:
- streaming
- observability
symptoms: []
root_causes:
- 'In `libs/core/langchain_core/utils/pydantic.py`, `_create_subset_model_v2` writes `__annotations__` directly on a model class (verified on master `bc5f1517cf`, line 272):'
fixes: []
references:
- title: Importing langchain.agents breaks BaseLLM class construction on Pydantic main
  url: https://github.com/langchain-ai/langchain/issues/37835
  source: github:langchain-ai/langchain
tags:
- bug
- core
- external
contributor: alexmojaki
discovered_at: '2026-06-01'
verified: false
---

- [Importing langchain.agents breaks BaseLLM class construction on Pydantic main](https://github.com/langchain-ai/langchain/issues/37835) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
