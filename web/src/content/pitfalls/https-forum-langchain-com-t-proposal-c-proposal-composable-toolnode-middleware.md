---
title: "Proposal: composable ToolNode middleware (tool-call dedup + wrap_tool_call chaining)"
summary: 'I opened PR #8291 to add a few small, dependency-free utilities to langgraph.prebuilt for two patterns that teams frequently re-implement when working with ToolNode: build_tool_call_key, deduplicate_tool_calls, and deduplicate_tool_calls_in_state Remove duplicate parallel tool'
severity: critical
platforms:
- langchain
- langgraph
categories:
- tool-use
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Proposal: composable ToolNode middleware (tool-call dedup + wrap_tool_call chaining)'
  url: https://forum.langchain.com/t/proposal-composable-toolnode-middleware-tool-call-dedup-wrap-tool-call-chaining/4098
  source: langchain-forum
tags:
- forum
- langchain-forum
discovered_at: '2026-07-06'
verified: false
---

- [Proposal: composable ToolNode middleware (tool-call dedup + wrap_tool_call chaining)](https://forum.langchain.com/t/proposal-composable-toolnode-middleware-tool-call-dedup-wrap-tool-call-chaining/4098) — langchain-forum

## 摘要

I opened PR #8291 to add a few small, dependency-free utilities to langgraph.prebuilt for two patterns that teams frequently re-implement when working with ToolNode:


build_tool_call_key, deduplicate_tool_calls, and deduplicate_tool_calls_in_state

Remove duplicate parallel tool
