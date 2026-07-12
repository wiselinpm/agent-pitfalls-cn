---
title: "[BUG] Entire ~/.claude deleted while client idle (2.1.207, Windows)"
summary: '# [BUG] Entire `~/.claude` deleted while client idle (2.1.207, Windows) — experienced as spontaneous logout ## Environment - Claude Code **2.1.207**, native install at `~/.local/bin/claude` (auto-updated on the `latest` channel at 00:09 local, same day) - Windows 11, Git Bash (M'
severity: critical
platforms:
- claude-code
categories:
- cost
- observability
- memory
symptoms:
- Unknown — occurred while idle with no user interaction. Suspect an auth-refresh or flag-gated cleanup/migration path in 2.1.207. Redacted copies of the pre- and post-event `.claude.json` snapshots are available on request.
root_causes:
- No Recycle Bin entries for the deleted tree (deletion was programmatic, not Explorer)
- No Windows Defender detections
- Binary unchanged since 00:09 — no reinstall at wipe time
fixes: []
references:
- title: '[BUG] Entire ~/.claude deleted while client idle (2.1.207, Windows)'
  url: https://github.com/anthropics/claude-code/issues/76825
  source: github:anthropics/claude-code
tags:
- bug
- platform:windows
- area:core
- high-priority
- data-loss
contributor: clarity-m
discovered_at: '2026-07-12'
verified: false
---

- [[BUG] Entire ~/.claude deleted while client idle (2.1.207, Windows)](https://github.com/anthropics/claude-code/issues/76825) — github:anthropics/claude-code

## 摘要

# [BUG] Entire `~/.claude` deleted while client idle (2.1.207, Windows) — experienced as spontaneous logout ## Environment - Claude Code **2.1.207**, native install at `~/.local/bin/claude` (auto-updated on the `latest` channel at 00:09 local, same day) - Windows 11, Git Bash (M
