---
title: '[BUG] fullscreen TUI copies via OSC 52 only, bypassing the native pbcopy path — silent clipboard failure in Terminal.app'
summary: '### Summary With `"tui": "fullscreen"`, selection-copy is routed through **OSC 52 only**, bypassing the native (`pbcopy`) path that the platform selector would choose for a local macOS session. In Terminal.app — which has never implemented OSC 52 — the write is silently discarde'
severity: high
platforms:
- claude-code
categories:
- streaming
- memory
- state
symptoms:
- 'Set `"tui": "fullscreen"` in `~/.claude/settings.json`.'
- Open Claude Code in macOS Terminal.app (local session, no SSH, no tmux).
- Select text in the TUI (click-drag, or any selection) and copy (copy-on-select or Ctrl+Shift+C).
- 'Status line shows: `sent N chars via OSC 52 · if paste fails, hold Fn while selecting for native copy`.'
root_causes:
- 'The clipboard mode selector does the right thing in principle:'
fixes:
- 'In the fullscreen renderer''s copy path, use the same `JOr()` mode selection as the classic renderer: local macOS/Windows/WSL → native clipboard; OSC 52 only when `KOr()` (SSH) is true or no native path exists.'
- 'Consider a `clipboard` diagnostics line in `/doctor` (mechanism chosen, terminal OSC 52 capability known/unknown) — most of the pain in #66192 is users having no way to see *why* copy silently does nothing.'
references:
- title: '[BUG] fullscreen TUI copies via OSC 52 only, bypassing the native pbcopy path — silent clipboard failure in Terminal.app (local, non-SSH)'
  url: https://github.com/anthropics/claude-code/issues/76902
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:tui
contributor: v9ai
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] fullscreen TUI copies via OSC 52 only, bypassing the native pbcopy path — silent clipboard failure in Terminal.app (local, non-SSH)](https://github.com/anthropics/claude-code/issues/76902) — github:anthropics/claude-code

## 摘要

### Summary

With `"tui": "fullscreen"`, selection-copy is routed through **OSC 52 only**, bypassing the native (`pbcopy`) path that the platform selector would choose for a local macOS session. In Terminal.app — which has never implemented OSC 52 — the write is silently discarde

_来源热度：1_
