---
title: "[BUG] AskUserQuestion preview pane renders blank when content starts with an HTML-block tag (XML / HTML / SVG ..."
summary: '## Preflight Checklist - [x] I have searched existing issues and this hasn''t been reported (only adjacent/different bugs exist — see References) - [x] This is a single bug report - [x] I am using the latest version of Claude Code ## What''s Wrong? When `AskUserQuestion` is invo'
severity: critical
platforms:
- claude-code
categories:
- streaming
- memory
- state
symptoms:
- 'I ran the same `AskUserQuestion` with 4 then 4-then-1 preview variants. Result is consistent:'
root_causes:
- 'The Claude Code CLI bundles a CommonMark parser. `strings` on the binary (`claude-code` 2.1.153) surfaces a contiguous block of parser-option names:'
fixes:
- 'Wrapping the same content in a fenced code block fixes the rendering for every format above:'
references:
- title: '[BUG] AskUserQuestion preview pane renders blank when content starts with an HTML-block tag (XML / HTML / SVG / Vue SFC)'
  url: https://github.com/anthropics/claude-code/issues/68834
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- area:tui
contributor: skatset
discovered_at: '2026-06-16'
verified: false
---

- [[BUG] AskUserQuestion preview pane renders blank when content starts with an HTML-block tag (XML / HTML / SVG / Vue SFC)](https://github.com/anthropics/claude-code/issues/68834) — github:anthropics/claude-code

## 摘要

## Preflight Checklist

- [x] I have searched existing issues and this hasn't been reported (only adjacent/different bugs exist — see References)
- [x] This is a single bug report
- [x] I am using the latest version of Claude Code

## What's Wrong?

When `AskUserQuestion` is invo

_来源热度：2_
