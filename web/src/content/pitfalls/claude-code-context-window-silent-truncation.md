---
title: Claude Code 长会话中上下文被静默截断，模型「忘记」早期指令
summary: 在长会话或多步 agent 循环中，当历史累积超过上下文窗口时，旧消息不会报错而是直接被截断，导致早期 system prompt、工具契约或用户偏好被遗忘，行为发生难以察觉的漂移。
severity: critical
platforms: ['claude-code', 'claude-api', 'generic']
categories: [context-window, reliability]
symptoms:
  - agent 在第 N 轮突然忽略最初设定的输出格式约束
  - 工具返回结构突然变化，但 prompt 里要求的是另一种结构
  - 用户在前几轮指定的语言/风格偏好失效
  - 单轮内模型反复询问同一个已经被回答过的字段
root_causes:
  - Anthropic / OpenAI / Gemini 等模型的 context window 是硬上限
  - 客户端 SDK（如 Claude Code 的 SDK / Vercel AI SDK）默认在到达上限时丢弃最早的消息而非报错
  - 多 agent 编排中若没有外层状态压缩，每个子 agent 都会独立遇到这个问题
fixes:
  - '在每一轮结束时显式计算并打印 `usage.input_tokens`，设置 80% 警戒线'
  - 使用滚动摘要（rolling summary）压缩最早 N 轮：让模型生成结构化摘要后替换原文
  - 关键 system prompt（输出格式、工具契约、安全约束）必须每次都重发，而不是只放在首条 message
  - 多 agent 场景下用「scratchpad 文件」+ 每轮重新加载，避免全部历史都塞进 context
references:
  - title: Anthropic Prompt Caching 最佳实践
    url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
    source: Anthropic Docs
  - title: Claude Code 长会话策略讨论
    url: https://github.com/anthropics/claude-code/issues/1280
    source: GitHub Issue
contributor: agent-pitfalls-bot
discovered_at: 2026-01-12
verified: true
---

## 复现路径

1. 启动一个 Claude Code 会话
2. 在 system prompt 里要求「所有输出必须以 JSON 形式返回」
3. 连续进行 50+ 轮对话，工具调用累计超过 50k tokens
4. 观察：模型开始用自然语言回复，丢失 JSON 格式

## 为什么不容易发现

大多数客户端 **不会抛出错误**，只会把旧消息从请求中剔除。从 API 返回的 `usage` 字段看，input_tokens 增长平缓，掩盖了历史被丢弃的事实。

## 检测手段

```python
def check_context_health(messages: list[dict], model_limit: int) -> dict:
    est = sum(len(json.dumps(m)) // 4 for m in messages)
    return {
        "estimated_tokens": est,
        "utilization": est / model_limit,
        "warning": est > model_limit * 0.8,
    }
```