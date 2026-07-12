---
title: "[Bug] Incorrect required field in params_json_schema causes tool misuse"
summary: '### Description When generating params_json_schema for tool definitions, the current implementation incorrectly includes all parameters in the required array, regardless of whether they are truly mandatory. This behavior may lead to unexpected or erroneous tool-calling behavior'
severity: critical
platforms:
- generic
categories:
- streaming
symptoms: []
root_causes: []
fixes: []
references:
- title: '[Bug] Incorrect required field in params_json_schema causes tool misuse'
  url: https://github.com/openai/openai-agents-python/issues/3733
  source: github:openai/openai-agents-python
tags:
- bug
contributor: gdisk
discovered_at: '2026-07-06'
verified: false
---

- [[Bug] Incorrect required field in params_json_schema causes tool misuse](https://github.com/openai/openai-agents-python/issues/3733) — github:openai/openai-agents-python

## 摘要

### Description
When generating params_json_schema for tool definitions, the current implementation incorrectly includes all parameters in the required array, regardless of whether they are truly mandatory.

This behavior may lead to unexpected or erroneous tool-calling behavior

_来源热度：2_
