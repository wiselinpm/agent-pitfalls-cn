---
title: "Responses API + Structured Outputs (gpt-5.6-luna): garbage tokens (foreign scripts / leaked reasoning) inside string..."
summary: 'Summary Since migrating structured-output calls from Chat Completions to the Responses API, gpt-5.6-luna intermittently emits degenerate tokens inside string values, immediately before the closing quote. The JSON is always schema-valid (strict: true), so the garbage flows straigh'
severity: critical
platforms:
- openai-api
categories:
- streaming
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Responses API + Structured Outputs (gpt-5.6-luna): garbage tokens (foreign scripts / leaked reasoning) inside string val'
  url: https://community.openai.com/t/responses-api-structured-outputs-gpt-5-6-luna-garbage-tokens-foreign-scripts-leaked-reasoning-inside-string-values-right-before-the-closing-quote-identical-request-via-chat-completions-is-clean/1386422
  source: openai-forum
tags:
- forum
- openai-forum
discovered_at: '2026-07-11'
verified: false
---

- [Responses API + Structured Outputs (gpt-5.6-luna): garbage tokens (foreign scripts / leaked reasoning) inside string val](https://community.openai.com/t/responses-api-structured-outputs-gpt-5-6-luna-garbage-tokens-foreign-scripts-leaked-reasoning-inside-string-values-right-before-the-closing-quote-identical-request-via-chat-completions-is-clean/1386422) — openai-forum

## 摘要

Summary
Since migrating structured-output calls from Chat Completions to the Responses API, gpt-5.6-luna intermittently emits degenerate tokens inside
string values, immediately before the closing quote. The JSON is always schema-valid (strict: true), so the garbage flows straigh
