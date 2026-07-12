---
title: "Windows: click-to-focus activates pending permission dialog option (click-through), submitting an unintended answer"
summary: '## Bug description When Claude Code is running with a **permission prompt pending** and the window does **not** have focus, the user''s *first click* on the window — intended only to give the window focus — lands on the permission dialog and **submits an answer** (approve/reject)'
severity: medium
platforms:
- claude-code
categories:
- tool-use
- observability
- multi-agent
symptoms:
- Start a task that triggers a permission prompt (e.g., a Bash tool call needing approval).
- While the prompt is pending, click away so the Claude Code window loses focus.
- Click once anywhere on the Claude Code window to bring it back into focus.
- 'Observe: the click is delivered to the permission dialog and an answer is registered (in our case, repeatedly a rejection), without any keyboard input.'
root_causes: []
fixes: []
references:
- title: 'Windows: click-to-focus activates pending permission dialog option (click-through), submitting an unintended answer'
  url: https://github.com/anthropics/claude-code/issues/76743
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:windows
- area:tui
- area:permissions
contributor: dmcnm
discovered_at: '2026-07-11'
verified: false
---

- [Windows: click-to-focus activates pending permission dialog option (click-through), submitting an unintended answer](https://github.com/anthropics/claude-code/issues/76743) — github:anthropics/claude-code

## 摘要

## Bug description When Claude Code is running with a **permission prompt pending** and the window does **not** have focus, the user's *first click* on the window — intended only to give the window focus — lands on the permission dialog and **submits an answer** (approve/reject)
