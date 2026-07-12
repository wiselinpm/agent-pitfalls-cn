---
title: A LangGraph checkpointer with provable thread deletion (signed erasure receipts) — feedback welcome
summary: 'Hey all — sharing something I built for my own agents and finally cleaned up enough to put out there. I’d genuinely value feedback from anyone running stateful LangGraph in production. The problem that started it. My agent persists user threads with a checkpointer: great. Then a'
severity: critical
platforms:
- langgraph
categories:
- streaming
- memory
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: A LangGraph checkpointer with provable thread deletion (signed erasure receipts) — feedback welcome
  url: https://forum.langchain.com/t/a-langgraph-checkpointer-with-provable-thread-deletion-signed-erasure-receipts-feedback-welcome/4137
  source: langchain-forum
tags:
- forum
- langchain-forum
discovered_at: '2026-07-11'
verified: false
---

- [A LangGraph checkpointer with provable thread deletion (signed erasure receipts) — feedback welcome](https://forum.langchain.com/t/a-langgraph-checkpointer-with-provable-thread-deletion-signed-erasure-receipts-feedback-welcome/4137) — langchain-forum

## 摘要

Hey all — sharing something I built for my own agents and finally cleaned up enough to put out there. I’d genuinely value feedback from anyone running stateful LangGraph in production.
The problem that started it. My agent persists user threads with a checkpointer: great. Then a
