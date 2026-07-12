---
title: "[BUG] Prompt cache invalidated by rewrites of messages in long sessions"
summary: '### What''s Wrong? Claude code sessions sometimes reprocess the entire conversation instead of just a new message that a user sends. This is not due to *any reason visible in the chat itself*. I found two causes by diffing `/v1/messages` requests around a cost spike. 1. Claude'
severity: high
platforms:
- claude-code
- claude-api
categories:
- tool-use
- streaming
- cost
symptoms:
- Run a long VS Code session with PreToolUse hooks that add extra context to tool calls
- Diff consecutive raw request bodies around a big `cache_creation_input_tokens` spike which should hit eventually
- You'll see an old `<system-reminder>` block change shape, either split into its own message or merged into a neighboring one, breaking the cache for everything after it
root_causes: []
fixes: []
references:
- title: '[BUG] Prompt cache invalidated by rewrites of messages in long sessions'
  url: https://github.com/anthropics/claude-code/issues/76606
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:cost
- area:core
- platform:vscode
- area:hooks
contributor: oakif
discovered_at: '2026-07-11'
verified: false
---

- [[BUG] Prompt cache invalidated by rewrites of messages in long sessions](https://github.com/anthropics/claude-code/issues/76606) — github:anthropics/claude-code

## 摘要

### What's Wrong?

Claude code sessions sometimes reprocess the entire conversation instead of just a new message that a user sends. This is not due to *any reason visible in the chat itself*.

I found two causes by diffing `/v1/messages` requests around a cost spike.

1. Claude

_来源热度：2_
