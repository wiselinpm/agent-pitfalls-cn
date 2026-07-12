---
title: "Background processes leak as orphans (kill %1 silently fails in non-interactive shell)"
summary: '## Summary Claude Code leaks orphaned background processes when executing commands containing `&` (background jobs) followed by a `kill %1`. The kill silently fails because Claude Code''s non-interactive shell snapshot execution disables job control, so `%1` is never a valid job'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- memory
symptoms:
- 'Claude generated a command shaped like this (real command from a session investigating a macOS proxy tampering issue):'
root_causes:
- '**Reparenting to init.** The parent `zsh -c` exits as soon as the `eval` completes. The orphaned `fs_usage` (and its `sudo` wrapper) are reparented to PID 1 with no mechanism to reclaim them.'
fixes:
- 'Manually find and kill the orphans:'
references:
- title: Background processes leak as orphans (kill %1 silently fails in non-interactive shell)
  url: https://github.com/anthropics/claude-code/issues/76814
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:bash
contributor: slamdunk111
discovered_at: '2026-07-12'
verified: false
---

- [Background processes leak as orphans (kill %1 silently fails in non-interactive shell)](https://github.com/anthropics/claude-code/issues/76814) — github:anthropics/claude-code

## 摘要

## Summary

Claude Code leaks orphaned background processes when executing commands containing `&` (background jobs) followed by a `kill %1`. The kill silently fails because Claude Code's non-interactive shell snapshot execution disables job control, so `%1` is never a valid job

_来源热度：1_
