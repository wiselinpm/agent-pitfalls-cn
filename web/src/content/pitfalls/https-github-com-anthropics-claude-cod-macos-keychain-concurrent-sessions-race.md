---
title: 'macOS Keychain: concurrent sessions race on OAuth refresh; setup-token workaround strips claude.ai connectors, leaving n'
summary: '## Summary On macOS, multiple concurrent Claude Code processes sharing the Keychain item `Claude Code-credentials` (one subscription login) intermittently force each other logged out. The v2.1.133 / v2.1.136 fixes for the credential-refresh race ("parallel sessions all dead-endi'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- reliability
symptoms:
- Intermittent forced logouts of interactive sessions (and, historically,
root_causes:
- claude setup-token` / `CLAUDE_CODE_OAUTH_TOKEN` isolates headless jobs from
fixes:
- claude setup-token` / `CLAUDE_CODE_OAUTH_TOKEN` isolates headless jobs from
references:
- title: 'macOS Keychain: concurrent sessions race on OAuth refresh; setup-token workaround strips claude.ai connectors, leaving no viable headless pattern'
  url: https://github.com/anthropics/claude-code/issues/76905
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:auth
contributor: KillTheList
discovered_at: '2026-07-12'
verified: false
---

- [macOS Keychain: concurrent sessions race on OAuth refresh; setup-token workaround strips claude.ai connectors, leaving no viable headless pattern](https://github.com/anthropics/claude-code/issues/76905) — github:anthropics/claude-code

## 摘要

## Summary

On macOS, multiple concurrent Claude Code processes sharing the Keychain item
`Claude Code-credentials` (one subscription login) intermittently force each
other logged out. The v2.1.133 / v2.1.136 fixes for the credential-refresh race
("parallel sessions all dead-endi

_来源热度：2_
