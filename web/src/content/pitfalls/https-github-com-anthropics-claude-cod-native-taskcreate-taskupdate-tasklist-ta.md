---
title: Native TaskCreate/TaskUpdate/TaskList/TaskGet become permanently unavailable mid-session, survives /clear and a full pro
summary: '**Environment:** Claude Code 2.1.207 (macOS), confirmed already latest via `claude update`. **What happened:** Mid-session, the native task-tracker tools (`TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`) — which are lazy-loaded via the ToolSearch deferred-tool mechanism — stop'
severity: high
platforms:
- claude-code
categories:
- sandbox
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: Native TaskCreate/TaskUpdate/TaskList/TaskGet become permanently unavailable mid-session, survives /clear and a full process restart
  url: https://github.com/anthropics/claude-code/issues/76911
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:tools
contributor: fp
discovered_at: '2026-07-12'
verified: false
---

- [Native TaskCreate/TaskUpdate/TaskList/TaskGet become permanently unavailable mid-session, survives /clear and a full process restart](https://github.com/anthropics/claude-code/issues/76911) — github:anthropics/claude-code

## 摘要

**Environment:** Claude Code 2.1.207 (macOS), confirmed already latest via `claude update`.

**What happened:**
Mid-session, the native task-tracker tools (`TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`) —
which are lazy-loaded via the ToolSearch deferred-tool mechanism — stop

_来源热度：3_
