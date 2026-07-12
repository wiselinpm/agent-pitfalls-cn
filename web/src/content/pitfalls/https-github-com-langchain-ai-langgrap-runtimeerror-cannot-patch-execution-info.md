---
title: "RuntimeError: Cannot patch execution_info before it has been set on LangGraph Cloud executor 0.7.96"
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- reliability
symptoms: []
root_causes:
- Executor 0.7.96 constructs `Runtime` with `execution_info=None` (in `langgraph_executor/_execute_task.py`)
- '`arun_with_retry` (in `langgraph/pregel/_retry.py:178`) calls `runtime.patch_execution_info(node_first_attempt_time=...)`'
- '`patch_execution_info` (in `langgraph/runtime.py:214`) raises because `self.execution_info is None`'
fixes: []
references:
- title: 'RuntimeError: Cannot patch execution_info before it has been set on LangGraph Cloud executor 0.7.96'
  url: https://github.com/langchain-ai/langgraph/issues/7420
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: rktechie
discovered_at: '2026-04-05'
verified: false
---

- [RuntimeError: Cannot patch execution_info before it has been set on LangGraph Cloud executor 0.7.96](https://github.com/langchain-ai/langgraph/issues/7420) — github:langchain-ai/langgraph

## 摘要

### Checked other resources

- [x] This is a bug, not a usage question.
- [x] I added a clear and descriptive title that summarizes this issue.
- [x] I used the GitHub search to find a similar question and didn't find it.
- [x] I am sure that this is a bug in LangGraph rather tha

_来源热度：12_
