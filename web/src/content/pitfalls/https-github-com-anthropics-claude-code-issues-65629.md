---
title: "[BUG] `/permissions` reports success when adding new Allow rules and writeable workspace dirs that managed pol..."
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: critical
platforms:
- claude-code
categories:
- streaming
- security
- observability
symptoms: []
root_causes: []
fixes:
- When `allowManagedPermissionRulesOnly` / `denyWorkspaceModification` are set, `/permissions` should disable the corresponding additions and/or show a "locked by managed policy" message instead of reporting
references:
- title: '[BUG] `/permissions` reports success when adding new Allow rules and writeable workspace dirs that managed policy forbids (misleading UI, not enforced; no privilege escalation)'
  url: https://github.com/anthropics/claude-code/issues/65629
  source: github:anthropics/claude-code
tags:
- bug
- platform:linux
- area:tui
- area:permissions
- stale
contributor: mirekphd
discovered_at: '2026-06-05'
verified: false
---

- [[BUG] `/permissions` reports success when adding new Allow rules and writeable workspace dirs that managed policy forbids (misleading UI, not enforced; no privilege escalation)](https://github.com/anthropics/claude-code/issues/65629) — github:anthropics/claude-code

## 摘要

### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]
