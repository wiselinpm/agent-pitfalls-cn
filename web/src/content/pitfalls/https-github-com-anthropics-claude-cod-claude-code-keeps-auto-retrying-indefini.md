---
title: Claude Code keeps auto-retrying indefinitely after hitting usage/token limit instead of stopping
summary: '## Bug description When Claude Code hits a token/usage limit during a running turn, it does not stop. It keeps auto-retrying indefinitely and I have to manually press the stop button every time. Expected behavior per docs: usage-limit-reached should be a hard stop, not retried.'
severity: medium
platforms:
- claude-code
categories:
- context-window
- reliability
symptoms:
- Run a long task until the usage/token limit is reached mid-turn
- Observe Claude Code showing retry countdowns and retrying repeatedly instead of stopping
- Manual stop is required to end the loop
- 'Possibly related: #35744, #36320, #23115'
root_causes: []
fixes: []
references:
- title: Claude Code keeps auto-retrying indefinitely after hitting usage/token limit instead of stopping
  url: https://github.com/anthropics/claude-code/issues/76837
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:core
- platform:vscode
contributor: likeperple7
discovered_at: '2026-07-12'
verified: false
---

- [Claude Code keeps auto-retrying indefinitely after hitting usage/token limit instead of stopping](https://github.com/anthropics/claude-code/issues/76837) — github:anthropics/claude-code

## 摘要

## Bug description
When Claude Code hits a token/usage limit during a running turn, it does not stop. It keeps auto-retrying indefinitely and I have to manually press the stop button every time. Expected behavior per docs: usage-limit-reached should be a hard stop, not retried.

_来源热度：1_
