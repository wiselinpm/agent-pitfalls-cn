---
title: "[Bug] Claude Web''s GitHub API proxy also blocks GitHub Copilot"
summary: '**Bug Description** ## Title [BUG] Claude Code web/remote sandbox: GitHub API proxy rejects GitHub Copilot CLI''s internal auth endpoint (`/copilot_internal/*`) pre-authentication ## Summary Running GitHub Copilot CLI (`copilot`) from inside a Claude Code on the web / Claude Code'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- sandbox
symptoms: []
root_causes: []
fixes:
- Pass through `/copilot_internal/*` (and other unrecognized `api.github.com` paths) using the caller-supplied token instead of rejecting outright, or
- Document this as a known limitation of Claude Code web/remote sessions (e.g. in the network-config / claude-code-on-the-web docs) so plugin authors know Copilot-CLI-based tools aren't supported there.
- '**Environment Info**'
references:
- title: '[Bug] Claude Web''s GitHub API proxy also blocks GitHub Copilot'
  url: https://github.com/anthropics/claude-code/issues/76828
  source: github:anthropics/claude-code
tags:
- bug
- area:claude-code-web
- area:networking
- area:sandbox
contributor: lennart-bos
discovered_at: '2026-07-12'
verified: false
---

- [[Bug] Claude Web's GitHub API proxy also blocks GitHub Copilot](https://github.com/anthropics/claude-code/issues/76828) — github:anthropics/claude-code

## 摘要

**Bug Description**
## Title
[BUG] Claude Code web/remote sandbox: GitHub API proxy rejects GitHub Copilot CLI's internal auth endpoint (`/copilot_internal/*`) pre-authentication

## Summary
Running GitHub Copilot CLI (`copilot`) from inside a Claude Code on the web / Claude Code

_来源热度：1_
