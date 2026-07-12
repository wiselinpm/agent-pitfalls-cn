---
title: MCP invalid JSON errors still include raw tool input when DONT_LOG_TOOL_DATA is enabled
summary: '### Please read this first - [x] **Have you read the docs?** [Agents SDK docs](https://openai.github.io/openai-agents-python/) - [x] **Have you searched for related issues?** Others may have faced similar issues. ### Describe the bug `MCPUtil.invoke_mcp_tool()` suppresses debu'
severity: critical
platforms:
- openai-agents
categories:
- streaming
- observability
- memory
symptoms:
- '`MCPUtil.invoke_mcp_tool()` suppresses debug logging when `DONT_LOG_TOOL_DATA` is enabled, but it still includes the raw malformed `input_json` in the raised `ModelBehaviorError`.'
root_causes: []
fixes: []
references:
- title: MCP invalid JSON errors still include raw tool input when DONT_LOG_TOOL_DATA is enabled
  url: https://github.com/openai/openai-agents-python/issues/3087
  source: github:openai/openai-agents-python
tags:
- bug
- feature:mcp
contributor: Aphroq
discovered_at: '2026-05-02'
verified: false
---

- [MCP invalid JSON errors still include raw tool input when DONT_LOG_TOOL_DATA is enabled](https://github.com/openai/openai-agents-python/issues/3087) — github:openai/openai-agents-python

## 摘要

### Please read this first

- [x] **Have you read the docs?** [Agents SDK docs](https://openai.github.io/openai-agents-python/)
- [x] **Have you searched for related issues?** Others may have faced similar issues.

### Describe the bug

`MCPUtil.invoke_mcp_tool()` suppresses debu

_来源热度：1_
