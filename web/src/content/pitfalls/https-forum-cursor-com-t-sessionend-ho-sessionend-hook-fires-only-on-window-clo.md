---
title: sessionEnd hook fires only on window_close after shell-exec teardown — plugin hook commands can never execute
summary: Where does the bug appear (feature/product)? Cursor IDE Describe the Bug Our plugin registers a sessionEnd command hook (“node dist/src/index.js --hook session-end”) to generate a session recap. Registration, ${CLAUDE_PLUGIN_ROOT} expansion, and the stdin payload shape (session_i
severity: high
platforms:
- claude-code
- cursor
categories:
- cost
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: sessionEnd hook fires only on window_close after shell-exec teardown — plugin hook commands can never execute
  url: https://forum.cursor.com/t/sessionend-hook-fires-only-on-window-close-after-shell-exec-teardown-plugin-hook-commands-can-never-execute/165492
  source: cursor-forum
tags:
- cursor-forum
discovered_at: '2026-07-12'
verified: false
---

- [sessionEnd hook fires only on window_close after shell-exec teardown — plugin hook commands can never execute](https://forum.cursor.com/t/sessionend-hook-fires-only-on-window-close-after-shell-exec-teardown-plugin-hook-commands-can-never-execute/165492) — cursor-forum

## 摘要

Where does the bug appear (feature/product)? Cursor IDE Describe the Bug Our plugin registers a sessionEnd command hook (“node dist/src/index.js --hook session-end”) to generate a session recap. Registration, ${CLAUDE_PLUGIN_ROOT} expansion, and the stdin payload shape (session_i
