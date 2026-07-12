---
title: ChatAnthropic.bind_tools mutates caller-provided tool_choice dictionary
summary: '### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather than m'
severity: critical
platforms:
- langchain
categories:
- tool-use
- streaming
- observability
symptoms: []
root_causes:
- 'The current implementation assigns the caller''s dictionary directly:'
fixes:
- 'Create a shallow copy of the provided dictionary before storing it in `kwargs`:'
references:
- title: ChatAnthropic.bind_tools mutates caller-provided tool_choice dictionary
  url: https://github.com/langchain-ai/langchain/issues/38779
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- anthropic
- external
contributor: Suneel-DK
discovered_at: '2026-07-10'
verified: false
---

- [ChatAnthropic.bind_tools mutates caller-provided tool_choice dictionary](https://github.com/langchain-ai/langchain/issues/38779) — github:langchain-ai/langchain

## 摘要

### Submission checklist - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather than m
