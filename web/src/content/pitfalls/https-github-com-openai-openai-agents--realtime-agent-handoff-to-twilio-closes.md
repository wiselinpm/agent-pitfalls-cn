---
title: Realtime agent handoff to twilio closes twilio session and sends noise over phone
summary: '@rm-openai ### Describe the bug I tried modifying the demo in /examples/realtime/twilio to support multiple agent to have more complex behaviour. The first agent works fine, and the handoff gets detected and executed, but as soon as the next agent is in place the session gets'
severity: high
platforms:
- openai-agents
categories:
- sandbox
symptoms:
- 'Agents SDK version: newest version'
- 'Python version: Python 3.10'
- Extend https://github.com/openai/openai-agents-python/blob/main/examples/realtime/twilio/twilio_handler.py
root_causes: []
fixes: []
references:
- title: Realtime agent handoff to twilio closes twilio session and sends noise over phone
  url: https://github.com/openai/openai-agents-python/issues/1632
  source: github:openai/openai-agents-python
tags:
- bug
- feature:realtime
contributor: Eirikalb
discovered_at: '2025-09-01'
verified: false
---

- [Realtime agent handoff to twilio closes twilio session and sends noise over phone](https://github.com/openai/openai-agents-python/issues/1632) — github:openai/openai-agents-python

## 摘要

@rm-openai 


### Describe the bug
I tried modifying the demo in /examples/realtime/twilio to support multiple agent to have more complex behaviour. The first agent works fine, and the handoff gets detected and executed, but as soon as the next agent is in place the session gets

_来源热度：3_
