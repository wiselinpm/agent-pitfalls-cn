---
title: "Cloud routine environments silently changed AWS_* env handling twice (stripped, then platform-injected), breaking produc"
summary: '## Summary The session environment that Claude Code **scheduled routines** (cloud environments, kind `anthropic_cloud`) provide to tasks has changed its handling of standard AWS credential variables **twice in five days, with no announcement, changelog entry, or documentation**'
severity: critical
platforms:
- claude-code
categories:
- cost
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Cloud routine environments silently changed AWS_* env handling twice (stripped, then platform-injected), breaking production workloads
  url: https://github.com/anthropics/claude-code/issues/76851
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- area:routines
contributor: jamkini
discovered_at: '2026-07-12'
verified: false
---

- [Cloud routine environments silently changed AWS_* env handling twice (stripped, then platform-injected), breaking production workloads](https://github.com/anthropics/claude-code/issues/76851) — github:anthropics/claude-code

## 摘要

## Summary

The session environment that Claude Code **scheduled routines** (cloud environments, kind `anthropic_cloud`) provide to tasks has changed its handling of standard AWS credential variables **twice in five days, with no announcement, changelog entry, or documentation**

_来源热度：1_
