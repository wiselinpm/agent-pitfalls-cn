---
title: '[BUG] Frequent session freezes / connection drops on Claude Code (VS Code extension) under'
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: high
platforms:
- claude-code
- claude-api
categories:
- observability
- state
symptoms: []
root_causes:
- Appears related to the keepalive / socket handling of the underlying runtime
fixes:
- 'WSL "mirrored" networking mode is NOT a viable workaround: enabling it'
- broke the WSL environment entirely, so it had to be reverted. Please do not
references:
- title: '[BUG] Frequent session freezes / connection drops on Claude Code (VS Code extension) under'
  url: https://github.com/anthropics/claude-code/issues/65771
  source: github:anthropics/claude-code
tags:
- bug
- platform:vscode
- platform:wsl
- area:networking
- stale
contributor: mrctito
discovered_at: '2026-06-06'
verified: false
---

- [[BUG]  Frequent session freezes / connection drops on Claude Code (VS Code extension) under](https://github.com/anthropics/claude-code/issues/65771) — github:anthropics/claude-code

## 摘要

### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x]

_来源热度：4_
