---
title: Agent with Checkpointer Reuses Tool Results in Multi-Turn Conversations
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- tool-use
- streaming
- observability
symptoms:
- '**No error is thrown**, but the behavior is incorrect.'
root_causes:
- 'When a `checkpointer` is provided to `createAgent`:'
fixes:
- 'The only working solution is to **manually manage checkpoints** and create the agent **without** the `checkpointer` parameter:'
references:
- title: Agent with Checkpointer Reuses Tool Results in Multi-Turn Conversations
  url: https://github.com/langchain-ai/langchain/issues/33936
  source: github:langchain-ai/langchain
tags:
- bug
- external
contributor: jledesma84
discovered_at: '2025-11-12'
verified: false
---

- [Agent with Checkpointer Reuses Tool Results in Multi-Turn Conversations](https://github.com/langchain-ai/langchain/issues/33936) — github:langchain-ai/langchain

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather tha
