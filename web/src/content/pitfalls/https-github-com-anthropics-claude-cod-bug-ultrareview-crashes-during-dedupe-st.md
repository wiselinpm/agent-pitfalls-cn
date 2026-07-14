---
title: '[Bug] Ultrareview crashes during dedupe step without delivering final report'
summary: '**Bug Description** Title: Ultrareview crashed during dedupe step — free usage consumed despite no final report Body: ## Summary Ran `/ultrareview` on a branch (`full-review` → `main`). The verify step completed successfully (15 candidates → 12 confirmed, 3 refuted), but'
severity: high
platforms:
- generic
categories:
- observability
symptoms:
- 'Session ID: `session_01CXxDytbGihRP4My3nwiRR1`'
- 'Session URL: https://claude.ai/code/session_01CXxDytbGihRP4My3nwiRR1'
- 'Scope: 166 files changed, 75,014 insertions'
- 'Branch: `full-review` → `main`'
root_causes: []
fixes: []
references:
- title: '[Bug] Ultrareview crashes during dedupe step without delivering final report'
  url: https://github.com/anthropics/claude-code/issues/55615
  source: github:anthropics/claude-code
tags:
- bug
- duplicate
- area:cost
- area:claude-code-web
- platform:web
- area:skills
- stale
contributor: HackyThings
discovered_at: '2026-05-02'
verified: false
---

- [[Bug] Ultrareview crashes during dedupe step without delivering final report](https://github.com/anthropics/claude-code/issues/55615) — github:anthropics/claude-code

## 摘要

**Bug Description**
Title:
  Ultrareview crashed during dedupe step — free usage consumed despite no final report

  Body:
  ## Summary
  Ran `/ultrareview` on a branch (`full-review` → `main`). The verify step completed successfully (15 candidates → 12 confirmed, 3 refuted), but

_来源热度：6_
