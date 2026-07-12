---
title: Error "Item ‘rs_ABCD’ of type ‘reasoning’ was provided without its required..." when using CodeInterpreter
summary: '### Describe the bug We have started to experience error of type `"Item ‘rs_ABCD’ of type ‘reasoning’ was provided without its required following item"` when an agent does a handoff to another agent (`o4-mini` with `low` effort to `o4-mini` with `medium` effort). This error hap'
severity: medium
platforms:
- openai-agents
categories: []
symptoms:
- This error happens when the first agent reasons and uses the CodeInterpreter tool (if it doesn't it works well).
root_causes: []
fixes: []
references:
- title: Error "Item ‘rs_ABCD’ of type ‘reasoning’ was provided without its required..." when using CodeInterpreter
  url: https://github.com/openai/openai-agents-python/issues/985
  source: github:openai/openai-agents-python
tags:
- bug
- feature:core
contributor: molefrog
discovered_at: '2025-07-01'
verified: false
---

- [Error "Item ‘rs_ABCD’ of type ‘reasoning’ was provided without its required..." when using CodeInterpreter](https://github.com/openai/openai-agents-python/issues/985) — github:openai/openai-agents-python

## 摘要

### Describe the bug
We have started to experience error of type `"Item ‘rs_ABCD’ of type ‘reasoning’ was provided without its required following item"` when an agent does a handoff to another agent (`o4-mini` with `low` effort to `o4-mini` with `medium` effort). 

This error hap

_来源热度：14_
