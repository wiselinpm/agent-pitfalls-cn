---
title: 'Workflow tool: args passed as a JSON array reaches the script as a JSON-encoded string'
summary: '## Environment - Claude Code v2.1.207, macOS (darwin 25.5.0) - Model: claude-fable-5 ## Bug The `Workflow` tool''s `args` parameter documents: *"Pass arrays/objects as actual JSON values in the tool call, NOT as a JSON-encoded string"*. The model passed an actual JSON array in th'
severity: high
platforms:
- claude-code
categories:
- tool-use
- streaming
- sandbox
symptoms:
- 'The `Workflow` tool''s `args` parameter documents: *"Pass arrays/objects as actual JSON values in the tool call, NOT as a JSON-encoded string"*. The model passed an actual JSON array in the tool call, e.g.:'
root_causes: []
fixes:
- 'Defensive parse at the top of every workflow script:'
references:
- title: 'Workflow tool: args passed as a JSON array reaches the script as a JSON-encoded string'
  url: https://github.com/anthropics/claude-code/issues/76906
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:core
contributor: akl773
discovered_at: '2026-07-12'
verified: false
---

- [Workflow tool: args passed as a JSON array reaches the script as a JSON-encoded string](https://github.com/anthropics/claude-code/issues/76906) — github:anthropics/claude-code

## 摘要

## Environment
- Claude Code v2.1.207, macOS (darwin 25.5.0)
- Model: claude-fable-5

## Bug
The `Workflow` tool's `args` parameter documents: *"Pass arrays/objects as actual JSON values in the tool call, NOT as a JSON-encoded string"*. The model passed an actual JSON array in th

_来源热度：1_
