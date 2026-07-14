---
title: '[BUG] Japanese VM process name shows as mojibake in Activity Monitor (UTF-8 decoded as Shift-JIS) — still in 1.20186.1'
summary: '## Summary Still reproducible as of Claude desktop app **1.20186.1** (2026-07-12): when the app UI language is Japanese, the Cowork/sandbox VM helper process gets the localized display name **「Claudeの仮想マシンサービス」**, but macOS Activity Monitor shows it as mojibake: ``` Claude縺ｮ莉ｮ諠'
severity: critical
platforms:
- generic
categories:
- observability
- sandbox
- tokenization
symptoms: []
root_causes:
- 'The garbled string is exactly the UTF-8 bytes of the correct name decoded as Shift-JIS:'
fixes: []
references:
- title: '[BUG] Japanese VM process name shows as mojibake in Activity Monitor (UTF-8 decoded as Shift-JIS) — still in 1.20186.1'
  url: https://github.com/anthropics/claude-code/issues/76910
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:cowork
contributor: ishiiryo-bs
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Japanese VM process name shows as mojibake in Activity Monitor (UTF-8 decoded as Shift-JIS) — still in 1.20186.1](https://github.com/anthropics/claude-code/issues/76910) — github:anthropics/claude-code

## 摘要

## Summary

Still reproducible as of Claude desktop app **1.20186.1** (2026-07-12): when the app UI language is Japanese, the Cowork/sandbox VM helper process gets the localized display name **「Claudeの仮想マシンサービス」**, but macOS Activity Monitor shows it as mojibake:

```
Claude縺ｮ莉ｮ諠

_来源热度：1_
