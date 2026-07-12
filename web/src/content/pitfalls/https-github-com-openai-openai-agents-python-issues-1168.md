---
title: Realtime API with Multiple Tool Calls Results in No Voice Output
summary: '### Describe the bug When the SDK uses multiple took calls which return JSON (in this instance asking for film times which calls to search for the film and then for times of that film_id near a location), there is no voice output. When I say something back to it to say "What were'
severity: medium
platforms:
- openai-agents
categories:
- tool-use
- observability
symptoms:
- 'See this trace: [Imgur](https://imgur.com/a/BCjukuj)'
root_causes: []
fixes: []
references:
- title: Realtime API with Multiple Tool Calls Results in No Voice Output
  url: https://github.com/openai/openai-agents-python/issues/1168
  source: github:openai/openai-agents-python
tags:
- bug
- feature:realtime
contributor: sibblegp
discovered_at: '2025-07-17'
verified: false
---

- [Realtime API with Multiple Tool Calls Results in No Voice Output](https://github.com/openai/openai-agents-python/issues/1168) — github:openai/openai-agents-python

## 摘要

### Describe the bug When the SDK uses multiple took calls which return JSON (in this instance asking for film times which calls to search for the film and then for times of that film_id near a location), there is no voice output. When I say something back to it to say "What were
