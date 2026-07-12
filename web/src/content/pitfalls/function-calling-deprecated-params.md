---
title: "OpenAI function_calling 参数 `functions` 已被弃用，迁移到 tools 时 schema 不兼容"
summary: '2024 年中 OpenAI 弃用 `functions`/`function_call`，推荐 `tools`/`tool_choice`，但两者的 JSON schema 存在差异：strict mode 下 `additionalProperties: false` 与 `required` 数组必须严格对齐，否则 400。'
severity: medium
platforms: ['openai-api']
categories: [tool-use, reliability]
symptoms:
  - '切换到 tools 后 `400 Invalid schema: all properties must be listed in required`'
  - '旧 SDK 仍然能用 `functions` 字段但响应里给出 `deprecation warning`'
  - 并行 tool_calls 数量从 1 变成模型自由选择
root_causes:
  - strict mode 要求所有 properties 必须显式列出
  - '旧代码里 `optional` 字段用 `default: null` 但没列在 `required` 里'
fixes:
  - 写一个迁移脚本：把所有 function schema 转成严格模式（自动补全 required）
  - '使用 Pydantic v2 的 `model_json_schema()` 配合 `mode="validation"` 自动生成'
  - '在 CI 里跑 schema linter，禁止 `additionalProperties` 与 `required` 不一致'
references:
  - title: 'OpenAI Structured Outputs 迁移指南'
    url: https://platform.openai.com/docs/guides/structured-outputs/migration
    source: OpenAI Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-08-12
verified: true
---
