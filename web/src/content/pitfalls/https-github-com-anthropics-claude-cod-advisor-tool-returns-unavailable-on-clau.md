---
title: Advisor tool returns "unavailable" on claude-fable-5 whenever transcript exceeds ~100K tokens
summary: '## Summary The server-side advisor tool returns `advisor_tool_result_error` with `error_code: "unavailable"` whenever the request model is `claude-fable-5` and the conversation transcript exceeds roughly 100K tokens. Below that size the same configuration works. The result is th'
severity: high
platforms:
- claude-code
categories:
- context-window
- tool-use
- streaming
symptoms: []
root_causes: []
fixes: []
references:
- title: Advisor tool returns "unavailable" on claude-fable-5 whenever transcript exceeds ~100K tokens
  url: https://github.com/anthropics/claude-code/issues/67609
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:model
- area:core
contributor: mikeberlinworkshop
discovered_at: '2026-06-11'
verified: false
---

- [Advisor tool returns "unavailable" on claude-fable-5 whenever transcript exceeds ~100K tokens](https://github.com/anthropics/claude-code/issues/67609) — github:anthropics/claude-code

## 摘要

## Summary

The server-side advisor tool returns `advisor_tool_result_error` with `error_code: "unavailable"` whenever the request model is `claude-fable-5` and the conversation transcript exceeds roughly 100K tokens. Below that size the same configuration works. The result is th

_来源热度：58_
