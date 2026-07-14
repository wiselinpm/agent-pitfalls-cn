---
title: "skill-creator plugin: trigger-eval harness false-negatives (shared probe-root contamination, first-tool-only d..."
summary: '## Component The `skill-creator` skill shipped in the `anthropic-skills` plugin (creatorType: anthropic, Claude Desktop local agent mode) — specifically its description-triggering eval harness, `scripts/run_eval.py`. ## Summary Evaluating a previously optimized skill descripti'
severity: medium
platforms:
- generic
categories:
- tool-use
- streaming
symptoms: []
root_causes: []
fixes: []
references:
- title: 'skill-creator plugin: trigger-eval harness false-negatives (shared probe-root contamination, first-tool-only detection, 30s timeout)'
  url: https://github.com/anthropics/claude-code/issues/76818
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:skills
- area:plugins
contributor: vdelacou
discovered_at: '2026-07-12'
verified: false
---

- [skill-creator plugin: trigger-eval harness false-negatives (shared probe-root contamination, first-tool-only detection, 30s timeout)](https://github.com/anthropics/claude-code/issues/76818) — github:anthropics/claude-code

## 摘要

## Component

The `skill-creator` skill shipped in the `anthropic-skills` plugin (creatorType: anthropic, Claude Desktop local agent mode) — specifically its description-triggering eval harness, `scripts/run_eval.py`.

## Summary

Evaluating a previously optimized skill descripti

_来源热度：1_
