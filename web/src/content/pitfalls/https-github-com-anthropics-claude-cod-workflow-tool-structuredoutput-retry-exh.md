---
title: 'Workflow tool: StructuredOutput retry exhaustion silently accepts degenerate placeholder that passes loose schema — no r'
summary: '## Summary In the Workflow tool (`agent()` with a `schema:` option), when the subagent repeatedly fails StructuredOutput schema validation and hits the retry cap, the model''s final give-up attempt — a minimal placeholder like `{"summary":"test","findings":[{"severity":"BLOCK","f'
severity: critical
platforms:
- claude-code
categories:
- streaming
- multi-agent
- reliability
symptoms:
- The model half (give-up stub emission after repeated validation failure) lives inside the harness retry loop and can't be driven externally; it is evidenced by 5 independent journal instances with the same 4-rejections-then-stub signature.
root_causes: []
fixes: []
references:
- title: 'Workflow tool: StructuredOutput retry exhaustion silently accepts degenerate placeholder that passes loose schema — no retry/degraded signal exposed'
  url: https://github.com/anthropics/claude-code/issues/76901
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:agents
contributor: charitarora
discovered_at: '2026-07-12'
verified: false
---

- [Workflow tool: StructuredOutput retry exhaustion silently accepts degenerate placeholder that passes loose schema — no retry/degraded signal exposed](https://github.com/anthropics/claude-code/issues/76901) — github:anthropics/claude-code

## 摘要

## Summary

In the Workflow tool (`agent()` with a `schema:` option), when the subagent repeatedly fails StructuredOutput schema validation and hits the retry cap, the model's final give-up attempt — a minimal placeholder like `{"summary":"test","findings":[{"severity":"BLOCK","f

_来源热度：1_
