---
title: "[BUG] Scroll-wheel SGR mouse report split across stdin reads leaks into prompt input (50ms incomplete-escape f..."
summary: '## Summary While scrolling the conversation with a mouse wheel / two-finger trackpad, fragments of the terminal''s SGR mouse reports get inserted into the prompt **as literal text** (e.g. `<65;92;34M5;92;34M;34M`). It''s intermittent, and it fires most often right after a large bl'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- memory
symptoms:
- '**Manual (intermittent):**'
root_causes:
- SGR mouse mode means each wheel tick arrives as `ESC [ < 65 ; col ; row M` (button 65 = wheel-down).
fixes:
- Don't treat a partial **multi-byte** escape sequence like a bare Esc in the flush timer. When
references:
- title: '[BUG] Scroll-wheel SGR mouse report split across stdin reads leaks into prompt input (50ms incomplete-escape flush timer force-emits the partial)'
  url: https://github.com/anthropics/claude-code/issues/76816
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:tui
contributor: KenMalloy
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Scroll-wheel SGR mouse report split across stdin reads leaks into prompt input (50ms incomplete-escape flush timer force-emits the partial)](https://github.com/anthropics/claude-code/issues/76816) — github:anthropics/claude-code

## 摘要

## Summary

While scrolling the conversation with a mouse wheel / two-finger trackpad, fragments of the
terminal's SGR mouse reports get inserted into the prompt **as literal text** (e.g.
`<65;92;34M5;92;34M;34M`). It's intermittent, and it fires most often right after a large bl

_来源热度：2_
