---
title: "[Bug] Claude regressing on file change detection and autonomous file inspection"
summary: '**Bug Description** Claude is missing making changes in files that it didn''t use to (e.g. upgrading terraform version but missing several upgrades it needs to do). It''s also often reporting back that I should check some specific files for something when previously it would automa'
severity: high
platforms:
- generic
categories: []
symptoms: []
root_causes: []
fixes: []
references:
- title: '[Bug] Claude regressing on file change detection and autonomous file inspection'
  url: https://github.com/anthropics/claude-code/issues/65613
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:model
- platform:intellij
- stale
contributor: nsutcliffe
discovered_at: '2026-06-05'
verified: false
---

- [[Bug] Claude regressing on file change detection and autonomous file inspection](https://github.com/anthropics/claude-code/issues/65613) — github:anthropics/claude-code

## 摘要

**Bug Description**
Claude is missing making changes in files that it didn't use to (e.g. upgrading terraform version but missing several upgrades it needs to do). It's also often reporting back that I should check some specific files for something when previously it would automa

_来源热度：4_
