---
title: "PIIMiddleware: PIIMatch not exported from public package, and docs use wrong field names for custom detectors"
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
symptoms: []
root_causes: []
fixes:
- 'from langchain.agents.middleware._redaction import PIIMatch  # private API'
references:
- title: 'PIIMiddleware: PIIMatch not exported from public package, and docs use wrong field names for custom detectors'
  url: https://github.com/langchain-ai/langchain/issues/38718
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- external
contributor: zzbazzzbaz
discovered_at: '2026-07-08'
verified: false
---

- [PIIMiddleware: PIIMatch not exported from public package, and docs use wrong field names for custom detectors](https://github.com/langchain-ai/langchain/issues/38718) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
