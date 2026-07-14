---
title: 'Remote Control: Android approval signal silently dropped — server never receives it (Linux/tmux, pure remote session)'
summary: '## Summary When approving a tool-use prompt via the Android app in a pure remote-control session (no local terminal), the approval is silently dropped — the server never receives it. The session blocks indefinitely until killed. ## Environment - **Claude Code version:** 2.1.15'
severity: low
platforms:
- claude-code
categories:
- tool-use
- streaming
- observability
symptoms:
- Start Claude Code in a tmux session on a remote Linux machine
- Connect via the Android app remote-control bridge (no local terminal watching)
- 'Trigger a tool-use requiring approval (in this case: Read tool)'
- Approval prompt appears in Android app
root_causes: []
fixes: []
references:
- title: 'Remote Control: Android approval signal silently dropped — server never receives it (Linux/tmux, pure remote session)'
  url: https://github.com/anthropics/claude-code/issues/64797
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:linux
- area:tui
- platform:android
- stale
contributor: chateauwaubun
discovered_at: '2026-06-02'
verified: false
---

- [Remote Control: Android approval signal silently dropped — server never receives it (Linux/tmux, pure remote session)](https://github.com/anthropics/claude-code/issues/64797) — github:anthropics/claude-code

## 摘要

## Summary

When approving a tool-use prompt via the Android app in a pure remote-control session (no local terminal), the approval is silently dropped — the server never receives it. The session blocks indefinitely until killed.

## Environment

- **Claude Code version:** 2.1.15

_来源热度：8_
