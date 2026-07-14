---
title: 'Workflow resume: prefix-based cache re-runs all successful agents after an early failure (docs imply per-call caching)'
summary: '## Environment - Claude Code v2.1.207, macOS (darwin 25.5.0) - Model: claude-fable-5 ## Scenario A workflow ran 102 parallel `agent()` calls via `pipeline()`. 100 succeeded; 2 failed with a terminal API error (`Output blocked by content filtering policy`). The 4th call in list o'
severity: high
platforms:
- claude-code
categories:
- cost
- reliability
- state
symptoms:
- '**The /workflows UI doesn''t distinguish cache-replays from live runs**, so the mass re-execution looks like normal progress; the duplicate spend is only discoverable from token counters.'
root_causes: []
fixes: []
references:
- title: 'Workflow resume: prefix-based cache re-runs all successful agents after an early failure (docs imply per-call caching)'
  url: https://github.com/anthropics/claude-code/issues/76907
  source: github:anthropics/claude-code
tags:
- bug
- area:agents
contributor: akl773
discovered_at: '2026-07-12'
verified: false
---

- [Workflow resume: prefix-based cache re-runs all successful agents after an early failure (docs imply per-call caching)](https://github.com/anthropics/claude-code/issues/76907) — github:anthropics/claude-code

## 摘要

## Environment
- Claude Code v2.1.207, macOS (darwin 25.5.0)
- Model: claude-fable-5

## Scenario
A workflow ran 102 parallel `agent()` calls via `pipeline()`. 100 succeeded; 2 failed with a terminal API error (`Output blocked by content filtering policy`). The 4th call in list o

_来源热度：1_
