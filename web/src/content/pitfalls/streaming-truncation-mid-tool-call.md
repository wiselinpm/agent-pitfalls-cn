---
title: 流式响应在 tool_call 中途断流，模型无法续写
summary: 使用 SSE 流式调用时，如果客户端在 tool_call JSON 未完全发出时断开连接，模型的状态留在「已消耗 input tokens 但未完成 output」，用户重试时模型从 0 开始，浪费了一半开销。
severity: medium
platforms: ['claude-api', 'openai-api', 'generic']
categories: [streaming, cost, reliability]
symptoms:
  - 同样的 prompt 两次调用结果完全不同
  - '第一次返回的 `stop_reason=tool_use`，但 tool_calls 字段是空对象'
  - 账单里出现大量「半成品」调用
root_causes:
  - 客户端断连时没有发送 cancellation 信号给上游
  - 服务端默认保留 token 但不续写
  - 缺少 idempotency key
fixes:
  - '实现「resume from last event id」机制（Anthropic 支持 `anthropic-beta: prompt-caching-2024-07-31` + 续传）'
  - 给每次调用生成 idempotency key，5xx 时自动重试相同 key
  - 客户端实现「心跳超时」而不是被动断连
references:
  - title: Anthropic Streaming 续传
    url: https://docs.anthropic.com/en/api/messages-streaming
    source: Anthropic Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-09-12
verified: true
---
