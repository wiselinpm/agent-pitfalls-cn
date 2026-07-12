---
title: "\\\\'Remote Control: SessionStart hook sessionTitle output is delivered to the bridge but never applied to the session\\..."
summary: '## Environment Claude Code 2.1.207, Windows 11, `claude remote-control` server mode; SessionStart hook emitting the documented `sessionTitle` output field. ## Problem For Remote-Control-spawned sessions (including the server''s pre-created session), the SessionStart hook runs nor'
severity: critical
platforms:
- claude-code
categories:
- streaming
symptoms:
- Users who standardize session naming via the documented `sessionTitle` hook field (hooks.md) get conforming titles everywhere EXCEPT the Remote Control UI, where the title is the most user-visible.
root_causes: []
fixes: []
references:
- title: 'Remote Control: SessionStart hook sessionTitle output is delivered to the bridge but never applied to the session''s display title'
  url: https://github.com/anthropics/claude-code/issues/76812
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:hooks
contributor: drakontas-hgbot
discovered_at: '2026-07-12'
verified: false
---

- [Remote Control: SessionStart hook sessionTitle output is delivered to the bridge but never applied to the session's display title](https://github.com/anthropics/claude-code/issues/76812) — github:anthropics/claude-code

## 摘要

## Environment Claude Code 2.1.207, Windows 11, `claude remote-control` server mode; SessionStart hook emitting the documented `sessionTitle` output field. ## Problem For Remote-Control-spawned sessions (including the server's pre-created session), the SessionStart hook runs nor
