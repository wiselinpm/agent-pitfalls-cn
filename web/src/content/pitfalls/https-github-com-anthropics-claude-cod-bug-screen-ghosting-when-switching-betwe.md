---
title: '[BUG] Screen ghosting when switching between agents view (FleetView) and REPL with alternate screen disabled'
summary: '## Environment - Claude Code: 2.1.202 – 2.1.206 (reproduced across versions) - OS: macOS (Darwin 25.5.0) - Terminal: Terminal.app - `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` (normal-flow mode) ## Description Switching between the background-agents view (`claude agents` / FleetVie'
severity: critical
platforms:
- claude-code
categories:
- state
symptoms:
- Run claude with `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` in Terminal.app
- Open the agents view (FleetView), then return to the REPL; repeat a few times
- Buffer shows interleaved remnants of both views
root_causes: []
fixes:
- Ctrl+L redraws correctly; resizing the window (SIGWINCH) also forces a clean redraw.
references:
- title: '[BUG] Screen ghosting when switching between agents view (FleetView) and REPL with alternate screen disabled'
  url: https://github.com/anthropics/claude-code/issues/76349
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:tui
- area:agent-view
contributor: halitcengizuzuner
discovered_at: '2026-07-10'
verified: false
---

- [[BUG] Screen ghosting when switching between agents view (FleetView) and REPL with alternate screen disabled](https://github.com/anthropics/claude-code/issues/76349) — github:anthropics/claude-code

## 摘要

## Environment
- Claude Code: 2.1.202 – 2.1.206 (reproduced across versions)
- OS: macOS (Darwin 25.5.0)
- Terminal: Terminal.app
- `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` (normal-flow mode)

## Description
Switching between the background-agents view (`claude agents` / FleetVie

_来源热度：2_
