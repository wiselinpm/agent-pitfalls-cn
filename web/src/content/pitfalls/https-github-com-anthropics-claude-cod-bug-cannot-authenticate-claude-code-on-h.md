---
title: "[BUG]Cannot authenticate Claude Code on headless remote server (VPS)"
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: critical
platforms:
- claude-code
- claude-api
- gemini-api
categories:
- streaming
- cost
- security
symptoms:
- It is impossible to authenticate Claude Code on a remote headless server.
root_causes: []
fixes:
- The only working solution found is embedding the API key directly in a wrapper
references:
- title: '[BUG]Cannot authenticate Claude Code on headless remote server (VPS)'
  url: https://github.com/anthropics/claude-code/issues/65506
  source: github:anthropics/claude-code
tags:
- bug
- platform:linux
- area:auth
- stale
contributor: Gaizka-Hub
discovered_at: '2026-06-04'
verified: false
---

- [[BUG]Cannot authenticate Claude Code on headless remote server (VPS)](https://github.com/anthropics/claude-code/issues/65506) — github:anthropics/claude-code

## 摘要

### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x]

_来源热度：5_
