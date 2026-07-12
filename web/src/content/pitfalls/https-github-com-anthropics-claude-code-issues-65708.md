---
title: "[Bug] NameError in orchestrator error handler crashes Bug Hunter review on agent failure"
summary: '**Bug Description** Ran `/code-review ultra 936` against PR stratis-technology/stratOS#936. The remote Bug Hunter review authenticated and started, then crashed after ~24s with 0 findings — and the root cause is in the orchestrator''s own error handler, not the reviewed PR. A work'
severity: high
platforms:
- generic
categories:
- observability
- multi-agent
symptoms: []
root_causes: []
fixes: []
references:
- title: '[Bug] NameError in orchestrator error handler crashes Bug Hunter review on agent failure'
  url: https://github.com/anthropics/claude-code/issues/65708
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- platform:vscode
- area:skills
- stale
contributor: gnahZnitsuJ
discovered_at: '2026-06-05'
verified: false
---

- [[Bug] NameError in orchestrator error handler crashes Bug Hunter review on agent failure](https://github.com/anthropics/claude-code/issues/65708) — github:anthropics/claude-code

## 摘要

**Bug Description** Ran `/code-review ultra 936` against PR stratis-technology/stratOS#936. The remote Bug Hunter review authenticated and started, then crashed after ~24s with 0 findings — and the root cause is in the orchestrator's own error handler, not the reviewed PR. A work
