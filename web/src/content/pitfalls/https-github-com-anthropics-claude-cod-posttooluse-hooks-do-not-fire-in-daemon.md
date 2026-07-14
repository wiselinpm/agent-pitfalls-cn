---
title: PostToolUse hooks do not fire in daemon/background-job sessions (PreToolUse + SessionStart do) — v2.1.208
summary: '## Summary In a **daemon-backed background session** (Claude Code''s background-job / daemon backend — `"backend": "daemon"` in the job state, `cliVersion` 2.1.208), **`PostToolUse` hooks configured in `settings.json` never fire**. `PreToolUse` and `SessionStart` hooks from the *'
severity: high
platforms:
- claude-code
categories:
- tool-use
- streaming
- observability
symptoms:
- 'In `settings.json`, register a `PostToolUse` hook with a `Bash` matcher that appends a marker, e.g.:'
root_causes: []
fixes:
- '## Summary


  In a **daemon-backed background session** (Claude Code''s background-job / daemon backend — `"backend": "daemon"` in the job state, `cliVersion` 2.1.208), **`PostToolUse` hooks configured in `settings.json` never fire**. `PreToolUse` and `SessionStart` hooks from the'
references:
- title: PostToolUse hooks do not fire in daemon/background-job sessions (PreToolUse + SessionStart do) — v2.1.208
  url: https://github.com/anthropics/claude-code/issues/77341
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:linux
- area:hooks
contributor: HiCraigChen
discovered_at: '2026-07-14'
verified: false
---

- [PostToolUse hooks do not fire in daemon/background-job sessions (PreToolUse + SessionStart do) — v2.1.208](https://github.com/anthropics/claude-code/issues/77341) — github:anthropics/claude-code

## 摘要

## Summary

In a **daemon-backed background session** (Claude Code's background-job / daemon backend — `"backend": "daemon"` in the job state, `cliVersion` 2.1.208), **`PostToolUse` hooks configured in `settings.json` never fire**. `PreToolUse` and `SessionStart` hooks from the *

_来源热度：1_
