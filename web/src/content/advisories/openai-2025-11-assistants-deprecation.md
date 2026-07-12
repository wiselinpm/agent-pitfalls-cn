---
title: OpenAI Assistants API 将在 2026 年中全面下线
summary: OpenAI 已宣布 Assistants API 将于 2026 年中正式下线，建议所有依赖 thread / run / file_search 的项目迁移到新的 Responses API。迁移过程中存在 tool 兼容性、文件索引重建等已知断点。
severity: high
affected:
  - openai-agents
  - openai-api
published_at: 2025-11-20
references:
  - title: OpenAI Deprecation 公告
    url: https://platform.openai.com/docs/deprecations
  - title: 迁移指南
    url: https://platform.openai.com/docs/guides/migrate-to-responses
---