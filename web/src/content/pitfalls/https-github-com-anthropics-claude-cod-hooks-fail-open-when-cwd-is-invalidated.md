---
title: Hooks fail open when CWD is invalidated (e.g. worktree deletion)
summary: '## Summary When the shell''s working directory becomes invalid — whether from an external process deleting it OR from a command within the same session (e.g., `git worktree remove`) — all hooks fail with `ENOENT: no such file or directory, posix_spawn ''/bin/sh''`. The harness trea'
severity: critical
platforms:
- claude-code
categories:
- tool-use
- state
symptoms:
- Launch Claude Code with a git worktree as the project root (or `cd` into one during the session)
- Run `git worktree remove <path>` from within the session, or delete the directory from another terminal
- Issue any subsequent tool call
- 'Observe: hooks error out with posix_spawn ENOENT, but the tool call proceeds as if allowed'
root_causes: []
fixes: []
references:
- title: Hooks fail open when CWD is invalidated (e.g. worktree deletion)
  url: https://github.com/anthropics/claude-code/issues/76808
  source: github:anthropics/claude-code
tags:
- bug
- duplicate
- platform:linux
- area:security
- area:hooks
contributor: in4mer
discovered_at: '2026-07-12'
verified: false
---

- [Hooks fail open when CWD is invalidated (e.g. worktree deletion)](https://github.com/anthropics/claude-code/issues/76808) — github:anthropics/claude-code

## 摘要

## Summary

When the shell's working directory becomes invalid — whether from an external process deleting it OR from a command within the same session (e.g., `git worktree remove`) — all hooks fail with `ENOENT: no such file or directory, posix_spawn '/bin/sh'`. The harness trea

_来源热度：1_
