---
title: Delete session button has no confirmation and sits 1px from edit button in VS Code session list
summary: '### Summary In the VS Code extension''s active sessions list, each session row has a pencil (edit) icon and a trash can (delete) icon placed directly adjacent to each other. Clicking approximately one pixel to the right of the edit icon hits the delete icon instead, and the sessio'
severity: high
platforms:
- claude-code
categories: []
symptoms:
- Open the Claude Code extension in VS Code.
- View the list of active/recent sessions.
- Hover over a session row to reveal the edit (pencil) and delete (trash can) icons.
- Click on or very near the edit icon — slightly off-target to the right.
root_causes: []
fixes:
- 'This feels like low-effort, high-impact: a confirmation modal or an undo toast would eliminate the failure mode entirely.'
references:
- title: Delete session button has no confirmation and sits 1px from edit button in VS Code session list
  url: https://github.com/anthropics/claude-code/issues/65703
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:ide
- platform:vscode
- user-experience
- stale
contributor: aasbra
discovered_at: '2026-06-05'
verified: false
---

- [Delete session button has no confirmation and sits 1px from edit button in VS Code session list](https://github.com/anthropics/claude-code/issues/65703) — github:anthropics/claude-code

## 摘要

### Summary
In the VS Code extension's active sessions list, each session row has a pencil (edit) icon and a trash can (delete) icon placed directly adjacent to each other. Clicking approximately one pixel to the right of the edit icon hits the delete icon instead, and the sessio

_来源热度：5_
