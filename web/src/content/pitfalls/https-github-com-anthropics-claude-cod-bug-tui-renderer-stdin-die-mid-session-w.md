---
title: "[BUG] TUI renderer + stdin die mid-session while the engine keeps running (macOS, 2.1.207) — idle CPU, no SIGWINCH r..."
summary: '## Environment - Claude Code **2.1.207** - macOS **26.5.1**, Apple Silicon (arm64) - Reproduced under **both Ghostty 1.3.1 and tmux 3.7b** → terminal-independent - Interactive TUI, `/tui fullscreen` mode ## Summary Mid-session, Claude Code''s **terminal UI dies completely** —'
severity: critical
platforms:
- claude-code
categories:
- streaming
- state
symptoms:
- '**We do not have a deterministic reproduction, and I won''t pretend otherwise.** What we have is a consistent correlation across both occurrences:'
root_causes: []
fixes: []
references:
- title: '[BUG] TUI renderer + stdin die mid-session while the engine keeps running (macOS, 2.1.207) — idle CPU, no SIGWINCH redraw, transcript still being written'
  url: https://github.com/anthropics/claude-code/issues/76838
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:tui
contributor: astradevkin
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] TUI renderer + stdin die mid-session while the engine keeps running (macOS, 2.1.207) — idle CPU, no SIGWINCH redraw, transcript still being written](https://github.com/anthropics/claude-code/issues/76838) — github:anthropics/claude-code

## 摘要

## Environment

- Claude Code **2.1.207**
- macOS **26.5.1**, Apple Silicon (arm64)
- Reproduced under **both Ghostty 1.3.1 and tmux 3.7b** → terminal-independent
- Interactive TUI, `/tui fullscreen` mode

## Summary

Mid-session, Claude Code's **terminal UI dies completely** —

_来源热度：1_
