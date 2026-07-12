---
title: "[BUG] Claude Code spawns duplicate channel plugin instances mid-session, causing 409 Conflict and tool loss"
summary: '### TL;DR Claude Code spawns a second Telegram channel plugin process ~3 minutes into a healthy session, with no crash or error preceding it. This triggers a cascade: 1. **Harness bug (this repo)**: Duplicate spawn with no apparent trigger. Tools not re-registered after the lif'
severity: critical
platforms:
- claude-code
categories:
- tool-use
- streaming
- observability
symptoms:
- 'Start Claude Code with a channel plugin:'
root_causes: []
fixes:
- '**Harness side (this repo):**'
references:
- title: '[BUG] Claude Code spawns duplicate channel plugin instances mid-session, causing 409 Conflict and tool loss'
  url: https://github.com/anthropics/claude-code/issues/36800
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:mcp
contributor: greghughespdx
discovered_at: '2026-03-20'
verified: false
---

- [[BUG] Claude Code spawns duplicate channel plugin instances mid-session, causing 409 Conflict and tool loss](https://github.com/anthropics/claude-code/issues/36800) — github:anthropics/claude-code

## 摘要

### TL;DR Claude Code spawns a second Telegram channel plugin process ~3 minutes into a healthy session, with no crash or error preceding it. This triggers a cascade: 1. **Harness bug (this repo)**: Duplicate spawn with no apparent trigger. Tools not re-registered after the lif
