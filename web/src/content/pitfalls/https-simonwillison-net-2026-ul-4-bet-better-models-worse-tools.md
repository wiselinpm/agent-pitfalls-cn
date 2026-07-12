---
title: "Better Models: Worse Tools"
summary: 'Better Models: Worse Tools Armin reports on a weird problem he ran into while hacking on Pi: The short version is that newer Claude models sometimes call Pi’s edit tool with extra, invented fields in the nested edits[] array. And not Haiku or some small model: Opus 4.8. The edit'
severity: critical
platforms:
- claude-code
categories:
- tool-use
- streaming
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Better Models: Worse Tools'
  url: https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything
  source: simon-willison
tags:
- newsletter
- simon-willison
discovered_at: '2026-07-04'
verified: false
---

- [Better Models: Worse Tools](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) — simon-willison

## 摘要

Better Models: Worse Tools
Armin reports on a weird problem he ran into while hacking on Pi:

The short version is that newer Claude models sometimes call Pi’s edit tool with extra, invented fields in the nested edits[] array. And not Haiku or some small model: Opus 4.8. The edit
