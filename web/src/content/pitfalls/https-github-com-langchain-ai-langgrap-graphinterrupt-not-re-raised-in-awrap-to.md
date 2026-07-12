---
title: GraphInterrupt Not Re-raised in awrap_tool_call Wrapper Path
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- tool-use
- streaming
- observability
symptoms:
- No related issues or PRs found.
root_causes: []
fixes:
- 'Add the missing `except GraphBubbleUp: raise` guard to the wrapper path in'
references:
- title: GraphInterrupt Not Re-raised in awrap_tool_call Wrapper Path
  url: https://github.com/langchain-ai/langgraph/issues/8217
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: shivajith
discovered_at: '2026-06-29'
verified: false
---

- [GraphInterrupt Not Re-raised in awrap_tool_call Wrapper Path](https://github.com/langchain-ai/langgraph/issues/8217) — github:langchain-ai/langgraph

## 摘要

### Checked other resources

- [x] This is a bug, not a usage question.
- [x] I added a clear and descriptive title that summarizes this issue.
- [x] I used the GitHub search to find a similar question and didn't find it.
- [x] I am sure that this is a bug in LangGraph rather tha

_来源热度：10_
