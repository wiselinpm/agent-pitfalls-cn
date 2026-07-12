---
title: SandboxAgent run terminates early when the first turn returns text-only output (no tool calls in the same response)
summary: '### Bug description When using SandboxAgent (especially after a handoff), the run can end immediately after sandbox initialization if the model’s first response contains only assistant text (e.g. a preamble) and no tool calls in the same response.output. The SDK then returns Next'
severity: critical
platforms:
- openai-agents
categories:
- tool-use
- streaming
- observability
symptoms:
- This is easy to trigger with the default sandbox system prompt, which instructs the model to send a preamble before making tool calls.
root_causes:
- 'In agents/run_internal/turn_resolution.py, execute_tools_and_side_effects():'
fixes: []
references:
- title: SandboxAgent run terminates early when the first turn returns text-only output (no tool calls in the same response)
  url: https://github.com/openai/openai-agents-python/issues/3756
  source: github:openai/openai-agents-python
tags:
- bug
contributor: bombert
discovered_at: '2026-07-08'
verified: false
---

- [SandboxAgent run terminates early when the first turn returns text-only output (no tool calls in the same response)](https://github.com/openai/openai-agents-python/issues/3756) — github:openai/openai-agents-python

## 摘要

### Bug description
When using SandboxAgent (especially after a handoff), the run can end immediately after sandbox initialization if the model’s first response contains only assistant text (e.g. a preamble) and no tool calls in the same response.output. The SDK then returns Next

_来源热度：1_
