---
title: Rate Limit 重试风暴让上游雪崩
summary: 多个 agent 实例同时触发 429，没有 jittered backoff 与 circuit breaker，全部在同一秒重试，导致上游 API 被彻底击穿，恢复时间比简单 backoff 长 10 倍。
severity: high
platforms: ['generic', 'claude-api', 'openai-api']
categories: [reliability, cost]
symptoms:
  - 上游返回 429 后 2-3 分钟内持续 5xx
  - 客户端 CPU/网络指标出现「周期性尖峰」
  - 账单出现异常 burst
root_causes:
  - 所有实例使用相同 backoff（指数退避但无 jitter）
  - 没有 circuit breaker，被熔断后仍然持续重试
  - retry-after 头被忽略
fixes:
  - '实现「full jitter」: `sleep = random(0, min(cap, base * 2 ** attempt))`'
  - '用 `pybreaker` 或 `tenacity` 的 `stop_after_attempt` + 异常分类'
  - '优先尊重 `Retry-After` header，把它作为最小等待时间'
  - 跨进程共享熔断器状态（Redis 计数器）
references:
  - title: 'AWS Architecture Blog: Exponential Backoff And Jitter'
    url: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    source: AWS
contributor: agent-pitfalls-bot
discovered_at: 2025-07-20
verified: true
---
