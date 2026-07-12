---
title: "`RunResultStreaming` type not compatible with Pydantic `model_rebuild()`"
summary: '### Please read this first - **Have you read the docs?** Yes - [Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Yes - No existing issues found for this specific forward reference problem with RunResultStreaming and Age'
severity: critical
platforms:
- openai-agents
categories:
- streaming
- observability
- state
symptoms:
- '`result.py` imports `Agent` directly: `from .agent import Agent` (line 12)'
- '`agent.py` imports `RunResult` conditionally: `from .result import RunResult` (under `TYPE_CHECKING`, line 36)'
- This creates a circular dependency that Pydantic cannot resolve when introspecting `RunResultStreaming` during `model_rebuild()`
- Users are forced to use `Any` or `object` type annotations instead of the proper `RunResultStreaming` type, losing type safety and IDE support.
root_causes: []
fixes: []
references:
- title: '`RunResultStreaming` type not compatible with Pydantic `model_rebuild()`'
  url: https://github.com/openai/openai-agents-python/issues/2127
  source: github:openai/openai-agents-python
tags:
- bug
- feature:core
contributor: rsg73626
discovered_at: '2025-11-26'
verified: false
---

- [`RunResultStreaming` type not compatible with Pydantic `model_rebuild()`](https://github.com/openai/openai-agents-python/issues/2127) — github:openai/openai-agents-python

## 摘要

### Please read this first

- **Have you read the docs?** Yes - [Agents SDK docs](https://openai.github.io/openai-agents-python/)
- **Have you searched for related issues?** Yes - No existing issues found for this specific forward reference problem with RunResultStreaming and Age

_来源热度：5_
