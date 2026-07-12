---
title: "[crewAIInc/crewAI] 1.15.2"
summary: '## What''s Changed ### Features - Pull latest LLM models dynamically in the crew wizard. - Support inline skill definitions. - Add generated Flow Definition authoring skill. - Support templated Flow action inputs. - Add text helper for flow CEL prompts. - Add text helper to flow'
severity: high
platforms:
- crewai
categories:
- streaming
- cost
- observability
symptoms:
- Key model-catalog cache by exact API key, shorten TTL, and skip Ollama.
- Unify `crewai run` flow input resolution and prompt from the state schema.
- Resolve pip-audit failures for onnx 1.22.0 and nltk PYSEC-2026-597.
- Ensure we are writing version for flows.
root_causes: []
fixes:
- Key model-catalog cache by exact API key, shorten TTL, and skip Ollama.
- Unify `crewai run` flow input resolution and prompt from the state schema.
- Resolve pip-audit failures for onnx 1.22.0 and nltk PYSEC-2026-597.
- Ensure we are writing version for flows.
references:
- title: '[crewAIInc/crewAI] 1.15.2'
  url: https://github.com/crewAIInc/crewAI/releases/tag/1.15.2
  source: github-releases:crewAIInc/crewAI
tags:
- release
- repo:crewAIInc/crewAI
contributor: lorenzejay
discovered_at: '2026-07-08'
verified: false
---

- [[crewAIInc/crewAI] 1.15.2](https://github.com/crewAIInc/crewAI/releases/tag/1.15.2) — github-releases:crewAIInc/crewAI

## 摘要

## What's Changed

### Features
- Pull latest LLM models dynamically in the crew wizard.
- Support inline skill definitions.
- Add generated Flow Definition authoring skill.
- Support templated Flow action inputs.
- Add text helper for flow CEL prompts.
- Add text helper to flow
