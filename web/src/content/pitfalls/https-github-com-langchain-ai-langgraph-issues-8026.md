---
title: "[Feature Request]: Add a high-level ApprovalNode for Human-in-the-Loop workflows"
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangGraph rather tha'
severity: critical
platforms:
- langchain
- langgraph
categories:
- observability
- state
symptoms: []
root_causes: []
fixes:
- I propose adding a reusable `ApprovalNode` to `libs/prebuilt` that abstracts these patterns. Additionally, adding `pause()` and `resume()` convenience methods to the core `Pregel` class would simplify managing long-running agent threads.
references:
- title: '[Feature Request]: Add a high-level ApprovalNode for Human-in-the-Loop workflows'
  url: https://github.com/langchain-ai/langgraph/issues/8026
  source: github:langchain-ai/langgraph
tags:
- bug
- external
contributor: Shivani767
discovered_at: '2026-06-09'
verified: false
---

- [[Feature Request]: Add a high-level ApprovalNode for Human-in-the-Loop workflows](https://github.com/langchain-ai/langgraph/issues/8026) — github:langchain-ai/langgraph

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangGraph rather tha
