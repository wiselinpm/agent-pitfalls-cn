---
title: "Desktop: MCP tool calls dispatched ~3-6 s apart while the server answers in 50 ms (CLI sessions unaffected)"
summary: '## Summary In Claude Code **Desktop** sessions, MCP tool calls to a local server are dispatched roughly **3–6 seconds apart**, while the same server answers direct requests in **~50 ms (p50)**. The overhead is specific to the desktop app''s MCP dispatch layer — terminal (CLI) ses'
severity: critical
platforms:
- claude-code
categories:
- tool-use
- cost
- sandbox
symptoms:
- Register any localhost MCP server whose tool can echo a server-side timestamp (e.g. a `run_python` that prints `time.time()`).
- In a **desktop** session, issue two such tool calls in one assistant turn; diff the echoed timestamps (~seconds apart).
- Repeat from a **terminal** `claude` session with the same server registered via `claude mcp add` (~tens of ms apart).
root_causes: []
fixes: []
references:
- title: 'Desktop: MCP tool calls dispatched ~3-6 s apart while the server answers in 50 ms (CLI sessions unaffected)'
  url: https://github.com/anthropics/claude-code/issues/76854
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:mcp
- area:desktop
contributor: taylor252627-glitch
discovered_at: '2026-07-12'
verified: false
---

- [Desktop: MCP tool calls dispatched ~3-6 s apart while the server answers in 50 ms (CLI sessions unaffected)](https://github.com/anthropics/claude-code/issues/76854) — github:anthropics/claude-code

## 摘要

## Summary

In Claude Code **Desktop** sessions, MCP tool calls to a local server are dispatched roughly **3–6 seconds apart**, while the same server answers direct requests in **~50 ms (p50)**. The overhead is specific to the desktop app's MCP dispatch layer — terminal (CLI) ses

_来源热度：1_
