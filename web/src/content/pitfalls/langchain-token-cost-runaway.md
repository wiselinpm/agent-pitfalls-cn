---
title: LangChain AgentExecutor 隐性 token 成本爆炸
summary: '默认 `AgentExecutor` 在每一步都把全部中间历史塞进 LLM 调用，且不会主动截断；多步任务中 token 消耗呈 O(n²) 增长，几小时就烧光月度预算。'
severity: high
platforms: ['langchain', 'langgraph']
categories: [cost, memory, observability]
symptoms:
  - 单次任务从预估 $0.05 飙到 $5+ 没有报错
  - 账单明细里 input_tokens 单次调用超过 50k
  - 任务完成时间线性增长，但 prompt 长度呈指数增长
root_causes:
  - '`AgentExecutor` 默认无截断策略，会保留所有 ChatPromptTemplate 模板与历史'
  - 工具返回的大段内容（如整段文件、HTTP 响应体）不会被裁剪
  - '缺少 `max_iterations` 上限保护，agent 会陷入无效循环'
fixes:
  - '用 `ConversationSummaryBufferMemory` 替代默认 memory'
  - '给每个工具结果加 `truncate_to=2000` 包装器'
  - '显式设置 `max_iterations=10` 与 `max_execution_time=120`'
  - '在每个 chain 节点用 `get_openai_callback()` 打点成本'
references:
  - title: 'LangChain Cost Optimization'
    url: https://python.langchain.com/docs/how_to/llm_token_usage_tracking/
    source: LangChain Docs
  - title: '实战分享：AgentExecutor 成本失控案例'
    url: https://news.ycombinator.com/item?id=42552117
    source: Hacker News
contributor: agent-pitfalls-bot
discovered_at: 2025-12-04
verified: true
---
