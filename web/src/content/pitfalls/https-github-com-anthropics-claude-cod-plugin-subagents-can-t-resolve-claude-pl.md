---
title: Plugin subagents can't resolve ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} — no way to read plugin-bundled files from a
summary: '### What happened A subagent dispatched from a plugin **cannot resolve `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_PROJECT_DIR}`** — the tokens reach the subagent''s tool calls as literal strings. Since a subagent runs with the *project* as its cwd and has no handle on the plugin''s inst'
severity: high
platforms:
- claude-code
categories:
- tool-use
- streaming
- cost
symptoms:
- 'The surprising part is the asymmetry — the same variables resolve everywhere *except* subagents (all verified on **Claude Code 2.1.166** via headless `--output-format stream-json` runs):'
root_causes:
- 'There''s no clean way to give a plugin''s agents a shared contract / base definition / "inheritance." Every workaround has a real cost:'
fixes: []
references:
- title: Plugin subagents can't resolve ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} — no way to read plugin-bundled files from a subagent
  url: https://github.com/anthropics/claude-code/issues/65768
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- area:agents
- area:plugins
- stale
contributor: bekalpaslan
discovered_at: '2026-06-06'
verified: false
---

- [Plugin subagents can't resolve ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} — no way to read plugin-bundled files from a subagent](https://github.com/anthropics/claude-code/issues/65768) — github:anthropics/claude-code

## 摘要

### What happened

A subagent dispatched from a plugin **cannot resolve `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_PROJECT_DIR}`** — the tokens reach the subagent's tool calls as literal strings. Since a subagent runs with the *project* as its cwd and has no handle on the plugin's inst

_来源热度：3_
