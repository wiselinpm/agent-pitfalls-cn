---
title: Generic dict output types are wrapped under response
summary: '### Please read this first - **Have you read the docs?** Yes. This concerns structured output schema generation. - **Have you searched for related issues?** Yes. No related issue or PR was found. ### Describe the bug `AgentOutputSchema(dict[str, int], strict_json_schema=False)'
severity: high
platforms:
- openai-agents
categories:
- streaming
symptoms:
- '`output_type=dict[str, int]` has a different top-level JSON shape from `output_type=dict`.'
- 'A model returning the natural dict shape, such as `{"a": 1}`, fails validation.'
- 'The wrapper shape `{"response": {"a": 1}}` is accepted instead, even though the user requested a dict output type.'
- 'Relevant edge cases considered:'
root_causes: []
fixes: []
references:
- title: Generic dict output types are wrapped under response
  url: https://github.com/openai/openai-agents-python/issues/3315
  source: github:openai/openai-agents-python
tags:
- bug
- feature:core
contributor: Aphroq
discovered_at: '2026-05-09'
verified: false
---

- [Generic dict output types are wrapped under response](https://github.com/openai/openai-agents-python/issues/3315) — github:openai/openai-agents-python

## 摘要

### Please read this first

- **Have you read the docs?** Yes. This concerns structured output schema generation.
- **Have you searched for related issues?** Yes. No related issue or PR was found.

### Describe the bug

`AgentOutputSchema(dict[str, int], strict_json_schema=False)

_来源热度：1_
