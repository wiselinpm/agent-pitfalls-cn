---
title: 'V8 OOM: Claude Code CLI leaks memory until laptop crashes (113GB observed)'
summary: '## Bug Report ### Summary Claude Code CLI node process leaks memory unboundedly during sessions, eventually consuming all system RAM and crashing the machine. Observed **113.66 GB memory usage** from Terminal (housing the `claude` CLI process) on a **24 GB MacBook**, causing mac'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- memory
symptoms:
- Start `claude` CLI in Terminal
- Use it for an extended session (the process grows continuously)
- System eventually runs out of memory and macOS force-pauses everything or the machine locks up
root_causes: []
fixes:
- Setting `NODE_OPTIONS="--max-old-space-size=4096"` in shell profile caps V8 heap and prevents the machine crash, but doesn't fix the underlying leak.
references:
- title: 'V8 OOM: Claude Code CLI leaks memory until laptop crashes (113GB observed)'
  url: https://github.com/anthropics/claude-code/issues/56693
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:core
- perf:memory
- stale
contributor: kaufast
discovered_at: '2026-05-06'
verified: false
---

- [V8 OOM: Claude Code CLI leaks memory until laptop crashes (113GB observed)](https://github.com/anthropics/claude-code/issues/56693) — github:anthropics/claude-code

## 摘要

## Bug Report

### Summary
Claude Code CLI node process leaks memory unboundedly during sessions, eventually consuming all system RAM and crashing the machine. Observed **113.66 GB memory usage** from Terminal (housing the `claude` CLI process) on a **24 GB MacBook**, causing mac

_来源热度：8_
