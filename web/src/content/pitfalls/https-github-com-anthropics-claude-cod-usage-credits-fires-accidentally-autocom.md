---
title: /usage-credits fires accidentally — autocomplete prefix-collision with /usage (relocated from the closed /extra-usage vs
summary: '## Summary Typing `/usage` (to open the read-only usage / rate-limit view) can accidentally send a usage-credit-increase request to the org admin, because `/usage` and `/usage-credits` share a prefix and sit adjacent in the slash-command autocomplete menu. Pressing Enter/Tab acc'
severity: high
platforms:
- claude-code
categories:
- streaming
symptoms:
- At the prompt, type `/usage` (intending to open the usage view).
- Press Enter (or Tab) without carefully checking which entry is highlighted.
- /usage-credits` fires instead of `/usage`, sending a credit-limit-increase
- request to the org admin.
root_causes: []
fixes:
- Add a confirmation prompt before `/usage-credits` sends (default No). This was
- 'requested in #47768 and closed unaddressed.'
references:
- title: /usage-credits fires accidentally — autocomplete prefix-collision with /usage (relocated from the closed /extra-usage vs /exit issues)
  url: https://github.com/anthropics/claude-code/issues/76410
  source: github:anthropics/claude-code
tags:
- bug
- platform:linux
- platform:wsl
- area:cli
contributor: nebasuke
discovered_at: '2026-07-10'
verified: false
---

- [/usage-credits fires accidentally — autocomplete prefix-collision with /usage (relocated from the closed /extra-usage vs /exit issues)](https://github.com/anthropics/claude-code/issues/76410) — github:anthropics/claude-code

## 摘要

## Summary

Typing `/usage` (to open the read-only usage / rate-limit view) can accidentally
send a usage-credit-increase request to the org admin, because `/usage` and
`/usage-credits` share a prefix and sit adjacent in the slash-command autocomplete
menu. Pressing Enter/Tab acc

_来源热度：1_
