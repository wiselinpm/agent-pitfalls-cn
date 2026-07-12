---
title: "[BUG] \\\"Reset Application Data\\\" dialog understates destructiveness — permanently deletes all Cowork sessions, output..."
summary: '**What happened** The "Reset Application Data" confirmation dialog in the Claude desktop app says it will delete "settings, cache, and login information." It does not mention that it also permanently deletes: all Cowork session history and transcripts, all unsaved session output'
severity: medium
platforms:
- generic
categories:
- observability
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: '[BUG] "Reset Application Data" dialog understates destructiveness — permanently deletes all Cowork sessions, outputs, and local skills without warning'
  url: https://github.com/anthropics/claude-code/issues/65695
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:cowork
- data-loss
- area:desktop
- stale
contributor: vpacequanta
discovered_at: '2026-06-05'
verified: false
---

- [[BUG] "Reset Application Data" dialog understates destructiveness — permanently deletes all Cowork sessions, outputs, and local skills without warning](https://github.com/anthropics/claude-code/issues/65695) — github:anthropics/claude-code

## 摘要

**What happened**

The "Reset Application Data" confirmation dialog in the Claude desktop app says it will delete "settings, cache, and login information." It does not mention that it also permanently deletes: all Cowork session history and transcripts, all unsaved session output

_来源热度：2_
