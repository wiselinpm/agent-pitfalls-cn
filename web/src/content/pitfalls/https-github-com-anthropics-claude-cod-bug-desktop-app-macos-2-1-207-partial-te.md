---
title: '[BUG] Desktop app (macOS, 2.1.207): partial text selection copies whole paragraphs — bug persists while all prior report'
summary: '## Summary In the Claude Code desktop app on macOS, selecting a single line (or partial text) inside a rendered assistant message and copying it puts **multiple paragraphs — often the whole message block — on the clipboard** instead of the highlighted text. This bug has been re'
severity: critical
platforms:
- claude-code
categories:
- memory
symptoms:
- Have the assistant produce a normal multi-paragraph markdown reply (e.g. a drafted email).
- Click and drag to select one line or sentence inside it.
- Cmd+C and paste into any other app.
root_causes: []
fixes:
- '## Summary


  In the Claude Code desktop app on macOS, selecting a single line (or partial text) inside a rendered assistant message and copying it puts **multiple paragraphs — often the whole message block — on the clipboard** instead of the highlighted text.


  This bug has been re'
references:
- title: '[BUG] Desktop app (macOS, 2.1.207): partial text selection copies whole paragraphs — bug persists while all prior reports (#48168, #50386, #53975) closed NOT_PLANNED'
  url: https://github.com/anthropics/claude-code/issues/77347
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- regression
- area:ui
- area:desktop
contributor: ktimesk1776
discovered_at: '2026-07-14'
verified: false
---

- [[BUG] Desktop app (macOS, 2.1.207): partial text selection copies whole paragraphs — bug persists while all prior reports (#48168, #50386, #53975) closed NOT_PLANNED](https://github.com/anthropics/claude-code/issues/77347) — github:anthropics/claude-code

## 摘要

## Summary

In the Claude Code desktop app on macOS, selecting a single line (or partial text) inside a rendered assistant message and copying it puts **multiple paragraphs — often the whole message block — on the clipboard** instead of the highlighted text.

This bug has been re

_来源热度：1_
