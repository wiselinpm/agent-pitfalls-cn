---
title: AutoGen 多 Agent 陷入无限对话循环
summary: 当 GroupChat 里的 agent 没有清晰的 termination condition 时，它们会互相「回话」直到达到 max_round 或 token 预算耗尽，账单一夜清零。
severity: high
platforms: ['autogen']
categories: [multi-agent, cost, reliability]
symptoms:
  - 日志里看到两个 agent 重复相同内容超过 10 轮
  - 同一函数被反复调用
  - terminate 消息永远不被发出
root_causes:
  - '`is_termination_msg` 没有正确定义，或检测对象不是最后一条消息'
  - Agent prompt 里没说明「如果任务完成请显式说 TERMINATE」
  - '`max_consecutive_auto_reply` 没设置或设置过大'
fixes:
  - '始终显式设置 `max_consecutive_auto_reply=3`'
  - 在 system message 里写死「完成时必须输出字面量 TERMINATE」
  - '用 `GroupChatManager` 的 `speaker_selection_method` 改成 `round_robin` 而不是默认 `auto`'
  - 加成本监控，超阈值自动 abort
references:
  - title: 'AutoGen GroupChat 终止策略'
    url: https://microsoft.github.io/autogen/docs/tutorial/termination-conditions
    source: AutoGen Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-09-18
verified: true
---
