---
title: Anthropic Claude API 2025-12 tool_use id 偶发重复
summary: 在 2025-12 的若干次小版本发布中，部分客户端报告 tool_use id 在同一轮响应里出现重复，导致下游按 id 去重的状态机失效。官方在 2026-01-08 已修复。
severity: high
affected:
  - claude-api
  - claude-code
published_at: 2026-01-09
references:
  - title: Anthropic Status Page
    url: https://status.anthropic.com/incidents/2026-01-08
  - title: 社区报告
    url: https://github.com/anthropics/claude-code/issues/3142
---