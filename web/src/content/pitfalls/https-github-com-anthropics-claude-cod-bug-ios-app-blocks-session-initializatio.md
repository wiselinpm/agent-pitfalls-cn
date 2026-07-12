---
title: "[BUG] iOS App blocks session initialization with \\\"GitHub app is not installed\\\" modal for non-admin repos authorized..."
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: critical
platforms:
- claude-code
categories:
- observability
- memory
- sandbox
symptoms:
- Authenticate Claude Code using a non-admin repository via the `claude /web-setup` command on a desktop terminal.
- Open a mobile browser (e.g., Chrome on iOS) and navigate to `claude.ai/code`.
- 'Initialize a new session on the target repository. *(Result: Success, session starts normally).*'
- Close the browser, open the native **Claude iOS App**, and attempt to initialize a brand-new session on that exact same repository.
root_causes:
- 'This is a known, persistent friction point that has been reported by several users under various symptoms, but all previous tracking tickets have been prematurely closed by automated repository maintenance:'
fixes: []
references:
- title: '[BUG] iOS App blocks session initialization with "GitHub app is not installed" modal for non-admin repos authorized via /web-setup'
  url: https://github.com/anthropics/claude-code/issues/76843
  source: github:anthropics/claude-code
tags:
- bug
- area:auth
- platform:ios
- area:claude-code-web
contributor: totalfrank
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] iOS App blocks session initialization with "GitHub app is not installed" modal for non-admin repos authorized via /web-setup](https://github.com/anthropics/claude-code/issues/76843) — github:anthropics/claude-code

## 摘要

### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x]

_来源热度：1_
