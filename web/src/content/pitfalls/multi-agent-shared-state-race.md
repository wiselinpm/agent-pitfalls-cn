---
title: 多 Agent 共享 Blackboard 时竞态导致状态丢失
summary: 多个 worker agent 并发写入同一个 blackboard（如 Redis hash / Postgres row），后写覆盖前写，部分 agent 的中间结果被静默吞掉，最终汇总节点只看到「部分完成」的状态。
severity: high
platforms: ['autogen', 'crewai', 'langgraph', 'generic']
categories: [multi-agent, state, reliability]
symptoms:
  - 任务报告显示 N 个 agent 都「完成」但 blackboard 里只有 M < N 条记录
  - 同一字段被不同 agent 写为不同值，最终随机保留
  - '日志里出现 `WATCHDOG` 超时但没异常栈'
root_causes:
  - 共享状态没有版本号或 CAS
  - agent 之间没有互斥锁
  - 缺少「我刚写的值是否还是当前值」的检查
fixes:
  - '共享状态写入必须用乐观锁（`if version==expected then update version+=1`）'
  - 改用事件溯源（event sourcing），每个 agent 只能 append event
  - '用 LangGraph 的 reducer：`Annotated[list, operator.add]` 代替覆盖'
  - 加幂等 key：同一任务多次执行结果一致
references:
  - title: LangGraph State Reducers
    url: https://langchain-ai.github.io/langgraph/concepts/low_level/
    source: LangGraph Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-10-15
verified: true
---
