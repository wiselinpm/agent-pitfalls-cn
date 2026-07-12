---
title: "Model behavior: /goal Stop-hook directive cited as authorization for unrequested actions; absence-from-search treate..."
summary: '## Summary Single-session observations of three repeating Claude Code model behaviors that user-side rules in `~/.claude/CLAUDE.md` did not catch. Reporting because the patterns appear to be model-side and likely generalize beyond one user''s setup. Filed at the user''s explicit d'
severity: critical
platforms:
- claude-code
categories:
- streaming
- memory
- state
symptoms:
- Activate `/goal <condition>` Stop hook.
- Ask the model for analysis (e.g., "give me a plan to do X").
- Model produces plan and asks "want me to execute?"
- Do not answer.
root_causes:
- 'Existing user-side mitigations (CLAUDE.md, rules files, memory entries, custom skills) are textual. Under task pressure, the model reasons around them. In this session:'
fixes: []
references:
- title: 'Model behavior: /goal Stop-hook directive cited as authorization for unrequested actions; absence-from-search treated as evidence of absence; structure-as-substance under pushback'
  url: https://github.com/anthropics/claude-code/issues/60705
  source: github:anthropics/claude-code
tags:
- bug
- platform:macos
- area:model
contributor: RTinkslinger
discovered_at: '2026-05-19'
verified: false
---

- [Model behavior: /goal Stop-hook directive cited as authorization for unrequested actions; absence-from-search treated as evidence of absence; structure-as-substance under pushback](https://github.com/anthropics/claude-code/issues/60705) — github:anthropics/claude-code

## 摘要

## Summary

Single-session observations of three repeating Claude Code model behaviors that user-side rules in `~/.claude/CLAUDE.md` did not catch. Reporting because the patterns appear to be model-side and likely generalize beyond one user's setup. Filed at the user's explicit d

_来源热度：50_
