---
title: "[agno-agi/agno] v2.7.2"
summary: '# Changelog ## **New Features** - **OAuth on the AgentOS MCP Endpoint**: Added OAuth support for the AgentOS MCP endpoint via `AgentOS(mcp_auth=...)`. See [cookbook](https://github.com/agno-agi/agno/blob/main/cookbook/05_agent_os/mcp_demo/oauth_builtin_example.py). - **AG-'
severity: critical
platforms:
- generic
categories:
- security
- observability
symptoms:
- '**Remote Runs (Media)**: Serialize media for remote agent and team runs.'
- '**FileSystemKnowledge (Security)**: Prevent path traversal in `FileSystemKnowledge.get_file`.'
- '**`@tool` Methods**: Toolkit methods decorated with `@tool` now receive injected `run_context`, `agent`, and `team` parameters.'
- '**Google Calendar Tools**: Timezone-aware `start_date`/`end_date` are now honored across `list_events`, `create_event`, and `update_event`.'
root_causes: []
fixes:
- '**Remote Runs (Media)**: Serialize media for remote agent and team runs.'
- '**FileSystemKnowledge (Security)**: Prevent path traversal in `FileSystemKnowledge.get_file`.'
- '**`@tool` Methods**: Toolkit methods decorated with `@tool` now receive injected `run_context`, `agent`, and `team` parameters.'
- '**Google Calendar Tools**: Timezone-aware `start_date`/`end_date` are now honored across `list_events`, `create_event`, and `update_event`.'
references:
- title: '[agno-agi/agno] v2.7.2'
  url: https://github.com/agno-agi/agno/releases/tag/v2.7.2
  source: github-releases:agno-agi/agno
tags:
- release
- repo:agno-agi/agno
contributor: kausmeows
discovered_at: '2026-07-09'
verified: false
---

- [[agno-agi/agno] v2.7.2](https://github.com/agno-agi/agno/releases/tag/v2.7.2) — github-releases:agno-agi/agno

## 摘要

# Changelog 
 
## **New Features** 
 
- **OAuth on the AgentOS MCP Endpoint**: Added OAuth support for the AgentOS MCP endpoint via `AgentOS(mcp_auth=...)`. See [cookbook](https://github.com/agno-agi/agno/blob/main/cookbook/05_agent_os/mcp_demo/oauth_builtin_example.py). 
- **AG-

_来源热度：3_
