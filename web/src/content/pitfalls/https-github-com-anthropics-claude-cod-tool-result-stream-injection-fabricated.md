---
title: "Tool-result stream injection: fabricated git output attempted to induce destructive git reset"
summary: '## Summary During a user-authorized `git stash drop` in a Claude Code session, the tool-result stream returned **fabricated output** in two escalating waves attempting to manipulate the agent into running a destructive `git reset`: 1. A fake "prevent-destruction hook" claiming'
severity: critical
platforms:
- claude-code
categories:
- streaming
- observability
- memory
symptoms: []
root_causes:
- 'Note: `/bug` / `/feedback` was unavailable in this environment (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`), hence the GitHub issue.'
fixes: []
references:
- title: 'Tool-result stream injection: fabricated git output attempted to induce destructive git reset'
  url: https://github.com/anthropics/claude-code/issues/76823
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:security
- area:bash
contributor: BingJun-You
discovered_at: '2026-07-12'
verified: false
---

- [Tool-result stream injection: fabricated git output attempted to induce destructive git reset](https://github.com/anthropics/claude-code/issues/76823) — github:anthropics/claude-code

## 摘要

## Summary

During a user-authorized `git stash drop` in a Claude Code session, the tool-result stream returned **fabricated output** in two escalating waves attempting to manipulate the agent into running a destructive `git reset`:

1. A fake "prevent-destruction hook" claiming

_来源热度：1_
