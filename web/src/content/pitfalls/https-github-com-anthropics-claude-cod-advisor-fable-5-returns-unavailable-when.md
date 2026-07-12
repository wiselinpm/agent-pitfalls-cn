---
title: Advisor (Fable 5) returns "unavailable" whenever the transcript contains any prior tool call — one Bash(ls) suffices; Op
summary: '## Summary The server-side advisor tool with `advisorModel: "fable"` (`claude-fable-5`) returns `advisor_tool_result_error` with `error_code: "unavailable"` **whenever the session transcript contains at least one prior tool call — any tool, e.g. a single `Bash(ls)` or one `Read`'
severity: high
platforms:
- claude-code
- claude-api
categories:
- tool-use
- streaming
- sandbox
symptoms: []
root_causes:
- '**Transcript size** (cf. #67609): failures at 36K tokens, success at 700K+ (single huge user message, no tool calls). Size does not predict outcome; prior tool use does.'
- '**Background/daemon sessions**: a fresh `claude --bg` job calling advisor immediately succeeds; interactive/headless sessions fail after one tool call. Session kind is a proxy for "did work before consulting", not a cause.'
- '**`[1m]` context beta, `--permission-mode bypassPermissions`, `--agent`**: each tested in isolation, no effect.'
fixes: []
references:
- title: Advisor (Fable 5) returns "unavailable" whenever the transcript contains any prior tool call — one Bash(ls) suffices; Opus advisor immune
  url: https://github.com/anthropics/claude-code/issues/76189
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:model
- api:anthropic
contributor: perelin
discovered_at: '2026-07-09'
verified: false
---

- [Advisor (Fable 5) returns "unavailable" whenever the transcript contains any prior tool call — one Bash(ls) suffices; Opus advisor immune](https://github.com/anthropics/claude-code/issues/76189) — github:anthropics/claude-code

## 摘要

## Summary

The server-side advisor tool with `advisorModel: "fable"` (`claude-fable-5`) returns `advisor_tool_result_error` with `error_code: "unavailable"` **whenever the session transcript contains at least one prior tool call — any tool, e.g. a single `Bash(ls)` or one `Read`

_来源热度：8_
