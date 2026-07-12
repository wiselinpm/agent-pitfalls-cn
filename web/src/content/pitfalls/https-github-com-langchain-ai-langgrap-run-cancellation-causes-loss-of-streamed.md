---
title: Run Cancellation Causes Loss of Streamed State Not Yet Persisted as a Checkpoint
summary: '### Checked other resources - [x] This is a bug, not a usage question. For questions, please use the LangChain Forum (https://forum.langchain.com/). - [x] I added a clear and detailed title that summarizes the issue. - [x] I read what a minimal reproducible example is (https://s'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- memory
symptoms: []
root_causes:
- Users see and may even start reading output as it’s streamed, but lose it entirely if they cancel—even if a majority of the output was streamed.
- Creates an inconsistent, surprising user experience for chat applications or any app with incremental streaming.
- Makes it difficult to build features that require exact “what you saw is what is saved” continuity.
fixes: []
references:
- title: Run Cancellation Causes Loss of Streamed State Not Yet Persisted as a Checkpoint
  url: https://github.com/langchain-ai/langgraph/issues/5672
  source: github:langchain-ai/langgraph
tags:
- bug
- pending
- external
contributor: ibbybuilds
discovered_at: '2025-07-25'
verified: false
---

- [Run Cancellation Causes Loss of Streamed State Not Yet Persisted as a Checkpoint](https://github.com/langchain-ai/langgraph/issues/5672) — github:langchain-ai/langgraph

## 摘要

### Checked other resources

- [x] This is a bug, not a usage question. For questions, please use the LangChain Forum (https://forum.langchain.com/).
- [x] I added a clear and detailed title that summarizes the issue.
- [x] I read what a minimal reproducible example is (https://s

_来源热度：41_
