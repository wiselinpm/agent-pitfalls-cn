---
title: "Delta Channels: How We’re Evolving our Runtime for Long-Running Agents"
summary: 'Long-running agents have a storage problem: checkpointing full state at every step grows at O(N²). DeltaChannel is a new primitive in LangGraph 1.2 that checkpoints only the diff each step and writes full snapshots periodically, keeping storage costs flat as sessions grow longer.'
severity: high
platforms:
- langgraph
categories:
- cost
- memory
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Delta Channels: How We’re Evolving our Runtime for Long-Running Agents'
  url: https://www.langchain.com/blog/delta-channels-evolving-agent-runtime
  source: langchain-blog
tags: []
discovered_at: '2026-06-03'
verified: false
---

- [Delta Channels: How We’re Evolving our Runtime for Long-Running Agents](https://www.langchain.com/blog/delta-channels-evolving-agent-runtime) — langchain-blog

## 摘要

Long-running agents have a storage problem: checkpointing full state at every step grows at O(N²). DeltaChannel is a new primitive in LangGraph 1.2 that checkpoints only the diff each step and writes full snapshots periodically, keeping storage costs flat as sessions grow longer.
