---
title: Duplicate tool names across MCP servers cause errors
summary: '### Describe the bug When using multiple MCP servers with identically named tools (but potentially different behaviors or arguments) in OpenAI''s Agents SDK, the SDK raises a **`Duplicate tool names found across MCP servers`** error, preventing simultaneous usage. This is partic'
severity: low
platforms:
- openai-agents
- cursor
categories:
- tool-use
symptoms:
- '**Agents SDK version:** v0.0.8'
- '**Python version:** Python 3.13.2'
- 'Run the following minimal Python script:'
root_causes: []
fixes: []
references:
- title: Duplicate tool names across MCP servers cause errors
  url: https://github.com/openai/openai-agents-python/issues/464
  source: github:openai/openai-agents-python
tags:
- bug
- feature:mcp
contributor: nikhil-pandey
discovered_at: '2025-04-09'
verified: false
---

- [Duplicate tool names across MCP servers cause errors](https://github.com/openai/openai-agents-python/issues/464) — github:openai/openai-agents-python

## 摘要

### Describe the bug

When using multiple MCP servers with identically named tools (but potentially different behaviors or arguments) in OpenAI's Agents SDK, the SDK raises a **`Duplicate tool names found across MCP servers`** error, preventing simultaneous usage.

This is partic

_来源热度：9_
