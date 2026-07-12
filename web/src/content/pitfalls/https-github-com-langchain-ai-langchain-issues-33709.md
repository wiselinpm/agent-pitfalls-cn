---
title: "`AnthropicPromptCachingMiddleware` breaks model fallback with `cache_control` param"
summary: '### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn''t find it. - [x] I am sure that this is a bug in LangChain rather tha'
severity: critical
platforms:
- langchain
- langgraph
- claude-api
categories:
- observability
- state
symptoms:
- 'result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})'
root_causes:
- 'When ModelFallbackMiddleware switches to a fallback model:'
fixes: []
references:
- title: '`AnthropicPromptCachingMiddleware` breaks model fallback with `cache_control` param'
  url: https://github.com/langchain-ai/langchain/issues/33709
  source: github:langchain-ai/langchain
tags:
- bug
- anthropic
- external
contributor: bart0401
discovered_at: '2025-10-29'
verified: false
---

- [`AnthropicPromptCachingMiddleware` breaks model fallback with `cache_control` param](https://github.com/langchain-ai/langchain/issues/33709) — github:langchain-ai/langchain

## 摘要

### Checked other resources - [x] This is a bug, not a usage question. - [x] I added a clear and descriptive title that summarizes this issue. - [x] I used the GitHub search to find a similar question and didn't find it. - [x] I am sure that this is a bug in LangChain rather tha
