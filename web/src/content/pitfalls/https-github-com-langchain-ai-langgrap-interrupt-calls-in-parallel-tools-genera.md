---
title: "`interrupt()` calls in parallel tools generate identical IDs, making multi-interrupt resume impossible"
summary: '### Checked other resources - [x] This is a bug, not a usage question. For questions, please use the LangChain Forum (https://forum.langchain.com/). - [x] I added a clear and detailed title that summarizes the issue. - [x] I read what a minimal reproducible example is (https://s'
severity: critical
platforms:
- langchain
- langgraph
categories:
- tool-use
- observability
- memory
symptoms:
- unique_ids = set(intr.id for intr in all_interrupts)
root_causes:
- print("\n--- Attempting Resume ---")
fixes:
- 'Include the interrupt index in the ID generation:'
references:
- title: '`interrupt()` calls in parallel tools generate identical IDs, making multi-interrupt resume impossible'
  url: https://github.com/langchain-ai/langgraph/issues/6626
  source: github:langchain-ai/langgraph
tags:
- bug
- pending
contributor: AbhinaavRamesh
discovered_at: '2025-12-25'
verified: false
---

- [`interrupt()` calls in parallel tools generate identical IDs, making multi-interrupt resume impossible](https://github.com/langchain-ai/langgraph/issues/6626) — github:langchain-ai/langgraph

## 摘要

### Checked other resources

- [x] This is a bug, not a usage question. For questions, please use the LangChain Forum (https://forum.langchain.com/).
- [x] I added a clear and detailed title that summarizes the issue.
- [x] I read what a minimal reproducible example is (https://s

_来源热度：10_
