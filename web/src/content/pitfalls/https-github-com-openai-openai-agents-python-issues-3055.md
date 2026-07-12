---
title: Model refusals with structured output aren\'t handled
summary: If an API [response is a refusal](https://developers.openai.com/api/docs/guides/structured-outputs#refusals), and structured output has been requested, the agents SDK just tries again and keeps looping until `max_turns` is reached. This is because `ItemHelpers.extract_text()` ig
severity: critical
platforms:
- openai-agents
categories:
- streaming
symptoms:
- 'Agents SDK version: 0.14.8'
- 'Python version: 3.14'
- Here I've mocked out a model response because it's really hard to actually get a refusal from the API that doesn't use the structured response.
root_causes: []
fixes: []
references:
- title: Model refusals with structured output aren't handled
  url: https://github.com/openai/openai-agents-python/issues/3055
  source: github:openai/openai-agents-python
tags:
- bug
- feature:core
contributor: davidgilbertson
discovered_at: '2026-04-30'
verified: false
---

- [Model refusals with structured output aren't handled](https://github.com/openai/openai-agents-python/issues/3055) — github:openai/openai-agents-python

## 摘要

If an API [response is a refusal](https://developers.openai.com/api/docs/guides/structured-outputs#refusals), and structured output has been requested, the agents SDK just tries again and keeps looping until `max_turns` is reached. This is because `ItemHelpers.extract_text()` ig
