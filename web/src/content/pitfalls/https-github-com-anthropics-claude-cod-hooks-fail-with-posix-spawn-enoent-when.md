---
title: Hooks fail with posix_spawn ENOENT when session cwd is deleted; request fallback cwd before spawning hooks
summary: '## Summary When Claude Code spawns a hook, it appears to use `posix_spawn(''/bin/sh'', ..., {cwd: <session_cwd>})`. If `<session_cwd>` no longer exists at spawn time (common when a session was started inside a git worktree that has since been removed, or any directory deleted out'
severity: critical
platforms:
- claude-code
categories:
- streaming
symptoms:
- Start a session with cwd inside a directory that can be deleted (e.g. a git worktree).
- Delete that directory while the session is live (e.g. a worktree-cleanup step, a branch reaper, a concurrent process).
- Trigger any hook event (Stop, PreToolUse, etc.).
- 'Observed: `posix_spawn ''/bin/sh'' ... ENOENT`; the hook never executes.'
root_causes: []
fixes: []
references:
- title: Hooks fail with posix_spawn ENOENT when session cwd is deleted; request fallback cwd before spawning hooks
  url: https://github.com/anthropics/claude-code/issues/65378
  source: github:anthropics/claude-code
tags:
- bug
- area:hooks
contributor: Nickcom4
discovered_at: '2026-06-04'
verified: false
---

- [Hooks fail with posix_spawn ENOENT when session cwd is deleted; request fallback cwd before spawning hooks](https://github.com/anthropics/claude-code/issues/65378) — github:anthropics/claude-code

## 摘要

## Summary

When Claude Code spawns a hook, it appears to use `posix_spawn('/bin/sh', ..., {cwd: <session_cwd>})`. If `<session_cwd>` no longer exists at spawn time (common when a session was started inside a git worktree that has since been removed, or any directory deleted out

_来源热度：8_
