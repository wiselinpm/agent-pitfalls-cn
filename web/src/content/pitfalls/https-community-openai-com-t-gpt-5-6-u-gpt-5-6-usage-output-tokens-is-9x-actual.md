---
title: "Gpt-5.6: usage.output_tokens is ~9x actual generation (re-summed once per reasoning item), exceeds max_output_tokens..."
summary: On GPT-5.6 (sol and terra, Responses API), usage.output_tokens appears to be a cumulative re-sum of the running reasoning total — re-added once per reasoning item in output[] — rather than the number of tokens actually generated. The inflated value is what appears on the bill. No
severity: high
platforms:
- openai-api
categories:
- cost
- observability
- multi-agent
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Gpt-5.6: usage.output_tokens is ~9x actual generation (re-summed once per reasoning item), exceeds max_output_tokens, an'
  url: https://community.openai.com/t/gpt-5-6-usage-output-tokens-is-9x-actual-generation-re-summed-once-per-reasoning-item-exceeds-max-output-tokens-and-is-what-gets-billed/1386467
  source: openai-forum
tags:
- forum
- openai-forum
discovered_at: '2026-07-11'
verified: false
---

- [Gpt-5.6: usage.output_tokens is ~9x actual generation (re-summed once per reasoning item), exceeds max_output_tokens, an](https://community.openai.com/t/gpt-5-6-usage-output-tokens-is-9x-actual-generation-re-summed-once-per-reasoning-item-exceeds-max-output-tokens-and-is-what-gets-billed/1386467) — openai-forum

## 摘要

On GPT-5.6 (sol and terra, Responses API), usage.output_tokens appears to be a cumulative re-sum of the running reasoning total — re-added once per reasoning item in output[] — rather than the number of tokens actually generated. The inflated value is what appears on the bill.
No
