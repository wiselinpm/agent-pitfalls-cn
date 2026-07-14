---
title: '[BUG] Mobile push notifications are never revoked after the session is answered on another device'
summary: '## Summary Mobile push notifications sent by Claude Code (Remote Control) are never revoked. When a session asks for input and I answer it **from the desktop**, the notification that was pushed to my phone stays in the iOS notification center indefinitely. It has to be dismissed'
severity: medium
platforms:
- claude-code
categories:
- streaming
- sandbox
- state
symptoms:
- 'Start a background session with Remote Control:'
root_causes: []
fixes: []
references:
- title: '[BUG] Mobile push notifications are never revoked after the session is answered on another device'
  url: https://github.com/anthropics/claude-code/issues/76900
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- platform:ios
contributor: arolus
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Mobile push notifications are never revoked after the session is answered on another device](https://github.com/anthropics/claude-code/issues/76900) — github:anthropics/claude-code

## 摘要

## Summary

Mobile push notifications sent by Claude Code (Remote Control) are never revoked. When a session asks for input and I answer it **from the desktop**, the notification that was pushed to my phone stays in the iOS notification center indefinitely. It has to be dismissed

_来源热度：1_
