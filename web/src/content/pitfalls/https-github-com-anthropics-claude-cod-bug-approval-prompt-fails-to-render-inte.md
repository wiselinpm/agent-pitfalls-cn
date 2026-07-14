---
title: '[Bug] Approval prompt fails to render intermittently, causing session to hang'
summary: '**Bug Description** Title: Permission/approval prompt intermittently fails to render. Severity: High. Session hangs, forcing an interrupt and reissuing of work. Summary: Relatively often, a tool call that requires approval (Edit/Write, Bash) gates internally but does not render'
severity: high
platforms:
- claude-code
categories:
- tool-use
- streaming
- sandbox
symptoms: []
root_causes: []
fixes: []
references:
- title: '[Bug] Approval prompt fails to render intermittently, causing session to hang'
  url: https://github.com/anthropics/claude-code/issues/65772
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:tui
- area:permissions
- stale
contributor: rhgg2
discovered_at: '2026-06-06'
verified: false
---

- [[Bug] Approval prompt fails to render intermittently, causing session to hang](https://github.com/anthropics/claude-code/issues/65772) — github:anthropics/claude-code

## 摘要

**Bug Description**
Title: Permission/approval prompt intermittently fails to render.  Severity: High. Session hangs, forcing an interrupt and reissuing of work.  Summary: Relatively often, a tool call that requires approval (Edit/Write, Bash) gates internally but does not render

_来源热度：4_
