---
title: OpenAI Chat Completions 工具调用 arguments 偶发返回空字符串
summary: 在使用 gpt-4o / gpt-4-turbo 系列时，`tool_calls[i].function.arguments` 偶尔返回 `""`，导致客户端 JSON 解析崩溃；新版 Responses API 行为不同但迁移路径上仍有坑。
severity: high
platforms: ['openai-api', 'openai-agents']
categories: [tool-use, reliability]
symptoms:
  - '`json.loads(arguments)` 抛出 `JSONDecodeError: Expecting value`'
  - 同样 prompt 多次调用结果不稳定
  - 流式场景下第一个 chunk 就拿到空 arguments，剩余 chunk 才到达
root_causes:
  - 流式传输时 arguments 是按 delta 增量返回的，开发者常误用非流式字段处理
  - 模型在「思考」过程中可能先发出空 arguments 占位
  - 旧 SDK 在 function calling 与 parallel tool calls 之间处理不一致
fixes:
  - '在解析前先判断 `if not arguments.strip(): continue`'
  - '累计 `tool_calls[i].function.arguments += delta` 直到 finish_reason=tool_calls'
  - 迁移到 Responses API 并启用 strict mode + function tool 严格 schema
  - 给关键参数设置默认值，减少模型生成空对象的可能
references:
  - title: OpenAI Streaming Tool Calls 指南
    url: https://platform.openai.com/docs/guides/function-calling/streaming
    source: OpenAI Docs
  - title: langchain #20564: empty arguments on partial chunks
    url: https://github.com/langchain-ai/langchain/issues/20564
    source: GitHub Issue
contributor: agent-pitfalls-bot
discovered_at: 2025-11-30
verified: true
---

## 最小修复代码

```python
def safe_parse_args(args_str: str) -> dict:
    s = (args_str or "").strip()
    if not s:
        return {}
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # 模型生成截断：尝试补全
        return json.loads(s + "}")
```