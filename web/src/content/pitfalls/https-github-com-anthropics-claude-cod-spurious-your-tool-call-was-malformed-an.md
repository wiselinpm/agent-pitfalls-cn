---
title: Spurious "Your tool call was malformed and could not be parsed" injected after tool calls that actually executed
summary: '## Summary Repeatedly within a session, the message *"Your tool call was malformed and could not be parsed. Please retry."* is injected immediately after a tool call — but the tool **actually executed and returned normal output**. It appears to be a false positive from the tool-c'
severity: critical
platforms:
- claude-code
categories:
- tool-use
- reliability
symptoms:
- After a tool call (observed with single `Bash`, `Edit`, `Agent`, `SendMessage`, `AskUserQuestion`), a "malformed … Please retry" line is appended even though the tool ran and output came back.
- Frequency rose as the session grew longer / tool-call volume increased.
root_causes: []
fixes: []
references:
- title: Spurious "Your tool call was malformed and could not be parsed" injected after tool calls that actually executed
  url: https://github.com/anthropics/claude-code/issues/65787
  source: github:anthropics/claude-code
tags:
- bug
- duplicate
- platform:linux
- area:model
- stale
contributor: TKMD
discovered_at: '2026-06-06'
verified: false
---

- [Spurious "Your tool call was malformed and could not be parsed" injected after tool calls that actually executed](https://github.com/anthropics/claude-code/issues/65787) — github:anthropics/claude-code

## 摘要

## Summary
Repeatedly within a session, the message *"Your tool call was malformed and could not be parsed. Please retry."* is injected immediately after a tool call — but the tool **actually executed and returned normal output**. It appears to be a false positive from the tool-c

_来源热度：2_
