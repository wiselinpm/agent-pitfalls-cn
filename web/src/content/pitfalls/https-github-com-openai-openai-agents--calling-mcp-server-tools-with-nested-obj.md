---
title: Calling MCP server tools with nested object params from Realtime API agents
summary: '## Description The OpenAI Realtime API flattens tool arguments incorrectly, ignoring the provided JSON schema for nested objects. This causes tool calls to fail because the arguments don''t match the expected structure. When using MCP tools with nested object parameters through'
severity: high
platforms:
- openai-agents
categories:
- tool-use
- observability
symptoms:
- 'Added debug logging to `agents/mcp/util.py` in the `to_function_tool()` and `invoke_mcp_tool()` methods:'
root_causes: []
fixes: []
references:
- title: Calling MCP server tools with nested object params from Realtime API agents
  url: https://github.com/openai/openai-agents-python/issues/1681
  source: github:openai/openai-agents-python
tags:
- bug
- enhancement
- feature:realtime
contributor: thomasmansencal
discovered_at: '2025-09-08'
verified: false
---

- [Calling MCP server tools with nested object params from Realtime API agents](https://github.com/openai/openai-agents-python/issues/1681) — github:openai/openai-agents-python

## 摘要

## Description

The OpenAI Realtime API flattens tool arguments incorrectly, ignoring the provided JSON schema for nested objects. This causes tool calls to fail because the arguments don't match the expected structure.

When using MCP tools with nested object parameters through

_来源热度：3_
