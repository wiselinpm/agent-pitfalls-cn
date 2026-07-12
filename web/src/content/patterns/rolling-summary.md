---
title: Rolling Summary — 长会话的滚动摘要模式
summary: 当会话超过上下文窗口阈值时，让模型先生成当前历史的结构化摘要，再把摘要塞回 system prompt 顶部的「稳定前缀」里，从而保留关键事实且释放 token。
use_when: 单次会话预计超过 50 轮工具调用，或 input_tokens 接近 80% 警戒线。
pros:
  - 显著降低后续调用的成本
  - 关键事实（用户偏好、约束、已完成步骤）不丢失
  - 与 prompt caching 兼容
cons:
  - 摘要本身消耗一次额外调用
  - 摘要质量不稳，需要校验步骤
  - 不适合高频细节查询
example: |
  def maybe_summarize(messages):
      if count_tokens(messages) > THRESHOLD:
          summary = llm(f"请把以下对话压缩为 200 字事实清单：{messages}")
          return [{"role": "system", "content": f"历史摘要：{summary}"}] + messages[-20:]
      return messages
---