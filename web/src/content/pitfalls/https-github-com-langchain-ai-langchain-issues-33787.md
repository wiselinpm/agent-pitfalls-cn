---
title: Agent re-attempts original tool call after HumanInTheLoopMiddleware edit decision
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather tha'
severity: critical
platforms:
- openai-agents
- langchain
- langgraph
categories:
- tool-use
- observability
- memory
symptoms:
- When an agent's tool call is interrupted by the `HumanInTheLoopMiddleware` and the human operator chooses the `edit` decision, the middleware successfully executes the *edited* tool call.
root_causes: []
fixes: []
references:
- title: Agent re-attempts original tool call after HumanInTheLoopMiddleware edit decision
  url: https://github.com/langchain-ai/langchain/issues/33787
  source: github:langchain-ai/langchain
tags:
- bug
- langchain
- external
contributor: lesong36
discovered_at: '2025-11-02'
verified: false
---

- [Agent re-attempts original tool call after HumanInTheLoopMiddleware edit decision](https://github.com/langchain-ai/langchain/issues/33787) — github:langchain-ai/langchain

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather tha
