---
title: "[BUG] iOS Remote Control: project/folder selection step disappeared when creating a new session on a connected Mac —..."
summary: '### Environment - Client: Claude mobile app (iOS), creating a new session via "+" → Remote Control → my Mac mini (now displayed as "Mac.AirPort") - Host: Mac mini, macOS (Darwin 25.5.0), Claude Code / Claude Desktop up to date - Started: after the Chat/Cowork merge rollout around'
severity: medium
platforms:
- claude-code
categories: []
symptoms:
- On iOS, tap "+" to create a new session.
- Choose Remote Control and select a connected Mac (shown as "<hostname>.AirPort").
- 'Observe: no project/folder picker is offered; the session starts immediately.'
- In the session, check the working directory — it is the user's home directory, and the intended project's CLAUDE.md / MCP servers are not loaded.
root_causes: []
fixes:
- Creating sessions directly on the Mac (desktop app) instead of from iOS, plus a bootstrap block in `~/.claude/CLAUDE.md` that redirects sessions landing in `$HOME` to the intended project rules.
references:
- title: '[BUG] iOS Remote Control: project/folder selection step disappeared when creating a new session on a connected Mac — sessions always start at $HOME'
  url: https://github.com/anthropics/claude-code/issues/76821
  source: github:anthropics/claude-code
tags:
- bug
- platform:ios
- area:cowork
contributor: sfminiclaw
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] iOS Remote Control: project/folder selection step disappeared when creating a new session on a connected Mac — sessions always start at $HOME](https://github.com/anthropics/claude-code/issues/76821) — github:anthropics/claude-code

## 摘要

### Environment
- Client: Claude mobile app (iOS), creating a new session via "+" → Remote Control → my Mac mini (now displayed as "Mac.AirPort")
- Host: Mac mini, macOS (Darwin 25.5.0), Claude Code / Claude Desktop up to date
- Started: after the Chat/Cowork merge rollout around

_来源热度：1_
