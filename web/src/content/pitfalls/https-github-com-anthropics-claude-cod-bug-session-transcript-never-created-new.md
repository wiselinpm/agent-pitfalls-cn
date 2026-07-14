---
title: "[BUG] Session transcript never created: new interactive sessions run for hours writing no JSONL and no history..."
summary: '## Summary Two interactive sessions (started ~10h apart, same folder) ran normally for hours but **never created a session transcript at all**. The session directory `~/.claude/projects/<project>/<session-id>/` was created and written to (tool-result externalisation landed there'
severity: high
platforms:
- claude-code
categories:
- streaming
- observability
- sandbox
symptoms:
- 'A follow-up session started in the same folder the next day exhibited the identical failure while investigating the first one: no transcript, no history entries. So it is not a one-off corruption of a single session.'
root_causes:
- The session dir exists with `tool-results/` populated (files written at 14:57), but no `.jsonl` ever appeared next to it.
- Nothing in Trash. No orphaned `.jsonl` anywhere on disk. No deleted-but-open file handle. No `cleanupPeriodDays` set. 140 GB free. Directory writable, not a symlink, same device.
- Of 114 transcripts on disk, these were the only sessions with no transcript at all.
fixes: []
references:
- title: '[BUG] Session transcript never created: new interactive sessions run for hours writing no JSONL and no history.jsonl entries (silent, unrecoverable conversation loss)'
  url: https://github.com/anthropics/claude-code/issues/76829
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:core
- data-loss
contributor: goat255
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Session transcript never created: new interactive sessions run for hours writing no JSONL and no history.jsonl entries (silent, unrecoverable conversation loss)](https://github.com/anthropics/claude-code/issues/76829) — github:anthropics/claude-code

## 摘要

## Summary

Two interactive sessions (started ~10h apart, same folder) ran normally for hours but **never created a session transcript at all**. The session directory `~/.claude/projects/<project>/<session-id>/` was created and written to (tool-result externalisation landed there

_来源热度：1_
