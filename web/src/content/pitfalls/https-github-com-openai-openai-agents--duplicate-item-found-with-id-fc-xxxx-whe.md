---
title: Duplicate item found with id fc_xxxx when using conversation_id with function calling
summary: '### Describe the bug When using conversation_id in Runner.run_streamed method for an agent with function calling (custom function), I get the the following error: {''error'': {''message'': ''Duplicate item found with id fc_68d25eda79d481959bd7e424738091a006b9ae17d036a0e7. Remove dupli'
severity: low
platforms:
- openai-agents
categories:
- tool-use
- streaming
symptoms:
- 'When using conversation_id in Runner.run_streamed method for an agent with function calling (custom function), I get the the following error:'
root_causes: []
fixes: []
references:
- title: Duplicate item found with id fc_xxxx when using conversation_id with function calling
  url: https://github.com/openai/openai-agents-python/issues/1789
  source: github:openai/openai-agents-python
tags:
- bug
- feature:core
contributor: kinnari-patwa
discovered_at: '2025-09-23'
verified: false
---

- [Duplicate item found with id fc_xxxx when using conversation_id with function calling](https://github.com/openai/openai-agents-python/issues/1789) — github:openai/openai-agents-python

## 摘要

### Describe the bug
When using conversation_id in Runner.run_streamed method for an agent with function calling (custom function), I get the the following error:
{'error': {'message': 'Duplicate item found with id fc_68d25eda79d481959bd7e424738091a006b9ae17d036a0e7. Remove dupli

_来源热度：14_
