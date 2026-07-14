---
title: 'Remote Control: session delisted ~10-15 min after viewer disconnect; session ID rotates on reconnect (both undocumented)'
summary: '## Environment - Claude Code v2.1.207, Windows 11 Pro, host machine always online (verified: no sleep/standby or network-profile disconnect events in Windows event logs during the incident window) - Session running locally on a home mini-PC, watched/controlled remotely from a wor'
severity: low
platforms:
- claude-code
categories:
- streaming
- observability
symptoms:
- A long-running session was active on the (always-online) host; I was watching it from a browser at work.
- My viewing laptop lost WiFi (left the building). The host machine never lost network.
- The session card at claude.ai/code stayed visible for roughly 10-15 minutes, then disappeared from the list.
- When I looked again from home (~30-40 min later), the session was not in the list at all — even though the CLI process on the host was still running fine and the conversation continued normally when addressed locally.
root_causes: []
fixes:
- '## Environment

  - Claude Code v2.1.207, Windows 11 Pro, host machine always online (verified: no sleep/standby or network-profile disconnect events in Windows event logs during the incident window)

  - Session running locally on a home mini-PC, watched/controlled remotely from a wor'
references:
- title: 'Remote Control: session delisted ~10-15 min after viewer disconnect; session ID rotates on reconnect (both undocumented)'
  url: https://github.com/anthropics/claude-code/issues/77340
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:claude-code-web
contributor: flylow3d
discovered_at: '2026-07-14'
verified: false
---

- [Remote Control: session delisted ~10-15 min after viewer disconnect; session ID rotates on reconnect (both undocumented)](https://github.com/anthropics/claude-code/issues/77340) — github:anthropics/claude-code

## 摘要

## Environment
- Claude Code v2.1.207, Windows 11 Pro, host machine always online (verified: no sleep/standby or network-profile disconnect events in Windows event logs during the incident window)
- Session running locally on a home mini-PC, watched/controlled remotely from a wor

_来源热度：1_
