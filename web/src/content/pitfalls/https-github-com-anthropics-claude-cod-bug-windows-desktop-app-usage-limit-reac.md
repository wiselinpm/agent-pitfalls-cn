---
title: "\\\\'[BUG] Windows desktop app: \\\\'\\\\'Usage limit reached\\\\'\\\\' persists ~18h while Usage page shows 0% session / 27% w..."
summary: '## Environment - Claude desktop app on Windows 10 Home (10.0.19045), entrypoint `claude-desktop` - Claude Agent SDK 0.3.205 - Plan: Max 20x - Occurred: evening of July 11 → July 12, 2026 (UTC+8), ~18 hours and counting ## Description Since the evening of July 11 (UTC+8), multipl'
severity: critical
platforms:
- claude-code
categories:
- multi-agent
- state
symptoms:
- 'Looks like the same family as #55544 (Windows desktop only), #61673 (desktop shows error while CLI works — state sync), #62125, #61828, #54177, #41084.'
root_causes: []
fixes: []
references:
- title: '[BUG] Windows desktop app: ''Usage limit reached'' persists ~18h while Usage page shows 0% session / 27% weekly / 51% Fable (Max 20x)'
  url: https://github.com/anthropics/claude-code/issues/76826
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:cost
- area:desktop
contributor: ekyo0224
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Windows desktop app: 'Usage limit reached' persists ~18h while Usage page shows 0% session / 27% weekly / 51% Fable (Max 20x)](https://github.com/anthropics/claude-code/issues/76826) — github:anthropics/claude-code

## 摘要

## Environment
- Claude desktop app on Windows 10 Home (10.0.19045), entrypoint `claude-desktop`
- Claude Agent SDK 0.3.205
- Plan: Max 20x
- Occurred: evening of July 11 → July 12, 2026 (UTC+8), ~18 hours and counting

## Description
Since the evening of July 11 (UTC+8), multipl

_来源热度：1_
