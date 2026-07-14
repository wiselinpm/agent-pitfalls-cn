---
title: '[BUG] Terminal stuck in mouse-reporting mode after session ends, tied to .mcp.json project MCP auto-discovery'
summary: '## Summary When Claude Code auto-loads project-scoped MCP servers via `.mcp.json` + `enabledMcpjsonServers` (the normal project-discovery path), the terminal is left stuck in xterm mouse-reporting mode (`SGR 1000/1002/1003/1006`) after the session ends or is interrupted. Every s'
severity: high
platforms:
- claude-code
categories:
- sandbox
symptoms:
- In a project directory with a `.mcp.json` containing the servers above and
- 'both already approved via `enabledMcpjsonServers`, run:'
root_causes: []
fixes:
- '## Summary


  When Claude Code auto-loads project-scoped MCP servers via `.mcp.json` +

  `enabledMcpjsonServers` (the normal project-discovery path), the terminal is

  left stuck in xterm mouse-reporting mode (`SGR 1000/1002/1003/1006`) after

  the session ends or is interrupted. Every s'
references:
- title: '[BUG] Terminal stuck in mouse-reporting mode after session ends, tied to .mcp.json project MCP auto-discovery'
  url: https://github.com/anthropics/claude-code/issues/77344
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:tui
- area:mcp
contributor: thiagowolff
discovered_at: '2026-07-14'
verified: false
---

- [[BUG] Terminal stuck in mouse-reporting mode after session ends, tied to .mcp.json project MCP auto-discovery](https://github.com/anthropics/claude-code/issues/77344) — github:anthropics/claude-code

## 摘要

## Summary

When Claude Code auto-loads project-scoped MCP servers via `.mcp.json` +
`enabledMcpjsonServers` (the normal project-discovery path), the terminal is
left stuck in xterm mouse-reporting mode (`SGR 1000/1002/1003/1006`) after
the session ends or is interrupted. Every s

_来源热度：1_
