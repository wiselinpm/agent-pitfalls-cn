---
title: "[BUG] Task list (TaskCreate/TaskList) not restored on --resume/--continue — task-list id resolves to a new runtime id"
summary: '## Environment - Claude Code version: 2.1.207 - Platform: macOS (darwin 25.4.0), zsh - Task system: the current `TaskCreate`/`TaskList`/`TaskUpdate` tools (not the deprecated `TodoWrite`) ## Bug description Tasks created with `TaskCreate` are not restored when a session is res'
severity: medium
platforms:
- claude-code
categories: []
symptoms:
- Start a session, have Claude create a task via `TaskCreate` ("Test task").
- 'Observe it persisted on disk: `~/.claude/tasks/session-<8-hex>/1.json`.'
- Exit the session.
- '`claude --resume <that-session>` (or `claude --continue`).'
root_causes: []
fixes: []
references:
- title: '[BUG] Task list (TaskCreate/TaskList) not restored on --resume/--continue — task-list id resolves to a new runtime id'
  url: https://github.com/anthropics/claude-code/issues/76844
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:core
contributor: whatrwewaitingf0r
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Task list (TaskCreate/TaskList) not restored on --resume/--continue — task-list id resolves to a new runtime id](https://github.com/anthropics/claude-code/issues/76844) — github:anthropics/claude-code

## 摘要

## Environment

- Claude Code version: 2.1.207
- Platform: macOS (darwin 25.4.0), zsh
- Task system: the current `TaskCreate`/`TaskList`/`TaskUpdate` tools (not the deprecated `TodoWrite`)

## Bug description

Tasks created with `TaskCreate` are not restored when a session is res

_来源热度：1_
