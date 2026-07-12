---
title: Long-running run getting cancelled by aggressive workers scale down
summary: Hi LangChain team, recently we are experiencing some issues related to some of our graph runs getting cancelled (asyncio.CancelledError) in the LangSmith tracing in our Production deployment. After some debugging using the server log, we found out that during the time these runs
severity: critical
platforms:
- langchain
- langgraph
categories:
- streaming
- observability
- memory
symptoms: []
root_causes: []
fixes: []
references:
- title: Long-running run getting cancelled by aggressive workers scale down
  url: https://forum.langchain.com/t/long-running-run-getting-cancelled-by-aggressive-workers-scale-down/4126
  source: langchain-forum
tags:
- forum
- langchain-forum
discovered_at: '2026-07-09'
verified: false
---

- [Long-running run getting cancelled by aggressive workers scale down](https://forum.langchain.com/t/long-running-run-getting-cancelled-by-aggressive-workers-scale-down/4126) — langchain-forum

## 摘要

Hi LangChain team, recently we are experiencing some issues related to some of our graph runs getting cancelled (asyncio.CancelledError) in the LangSmith tracing in our Production deployment.
After some debugging using the server log, we found out that during the time these runs
