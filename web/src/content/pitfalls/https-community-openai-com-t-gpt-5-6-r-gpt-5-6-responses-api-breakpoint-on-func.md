---
title: "GPT-5.6 Responses API: breakpoint on function_call_output is accepted but never writes cache"
summary: I am seeing a reproducible discrepancy between the Responses API schema and explicit prompt-cache behavior on gpt-5.6-sol. The API schema allows prompt_cache_breakpoint on ResponseInputTextContent inside function_call_output.output. The request is accepted without a 400, but this
severity: low
platforms:
- openai-api
categories: []
symptoms: []
root_causes: []
fixes: []
references:
- title: 'GPT-5.6 Responses API: breakpoint on function_call_output is accepted but never writes cache'
  url: https://community.openai.com/t/gpt-5-6-responses-api-breakpoint-on-function-call-output-is-accepted-but-never-writes-cache/1386415
  source: openai-forum
tags:
- forum
- openai-forum
discovered_at: '2026-07-11'
verified: false
---

- [GPT-5.6 Responses API: breakpoint on function_call_output is accepted but never writes cache](https://community.openai.com/t/gpt-5-6-responses-api-breakpoint-on-function-call-output-is-accepted-but-never-writes-cache/1386415) — openai-forum

## 摘要

I am seeing a reproducible discrepancy between the Responses API schema and explicit prompt-cache behavior on gpt-5.6-sol.
The API schema allows prompt_cache_breakpoint on ResponseInputTextContent inside function_call_output.output. The request is accepted without a 400, but this
