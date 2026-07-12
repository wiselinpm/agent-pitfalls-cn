---
title: LLM agent architectures fail silently as they grow
summary: 'I&#x27;ve been working with LLM-based agent systems (LangGraph-style, multi-node, long-running) and noticed a recurring failure mode that doesn&#x27;t show up in early prototypes.<p>As agent graphs grow: - state becomes implicitly shared - routing decisions become opaque - respon'
severity: medium
platforms:
- langgraph
categories:
- observability
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: LLM agent architectures fail silently as they grow
  url: https://news.ycombinator.com/item?id=46543021
  source: hn-algolia-ext:story
tags:
- hackernews
verified: false
---
- [LLM agent architectures fail silently as they grow](https://news.ycombinator.com/item?id=46543021) — hn-algolia-ext:story

## 摘要

I&#x27;ve been working with LLM-based agent systems (LangGraph-style, multi-node, long-running)
and noticed a recurring failure mode that doesn&#x27;t show up in early prototypes.<p>As agent graphs grow:
- state becomes implicitly shared
- routing decisions become opaque
- respon

_来源热度：2_
