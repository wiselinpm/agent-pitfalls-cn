---
title: ChatGroq._combine_llm_outputs mutates per-generation token_usage in place and mishandles None values (silent clobber / T
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
categories:
- streaming
- observability
symptoms:
- '#38482 — `langchain-mistralai` has the naive `+=` version of this merge (no nested-dict handling at all)'
- '#38648 / #38646 — the `langchain-fireworks` sibling (same naive `+=`) and its fix'
- '`langchain-groq` is the interesting case: it already *attempts* nested-dict handling and None-guarding, but both are implemented incorrectly (details below)'
root_causes: []
fixes: []
references:
- title: ChatGroq._combine_llm_outputs mutates per-generation token_usage in place and mishandles None values (silent clobber / TypeError)
  url: https://github.com/langchain-ai/langchain/issues/38659
  source: github:langchain-ai/langchain
tags:
- bug
- groq
- external
contributor: abcgco
discovered_at: '2026-07-04'
verified: false
---

- [ChatGroq._combine_llm_outputs mutates per-generation token_usage in place and mishandles None values (silent clobber / TypeError)](https://github.com/langchain-ai/langchain/issues/38659) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
