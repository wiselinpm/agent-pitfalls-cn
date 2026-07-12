---
title: Scratchpad File — 多 agent 共享内存的「文件即记忆」模式
summary: 不把所有状态塞进 context，而是写入一个结构化的 .md / .jsonl 文件，每次 agent 启动时只读取它需要的相关段落，避免 context 膨胀且天然持久化。
use_when: 多 agent 编排、长时间任务（>1 小时）、需要在崩溃后恢复的场景。
pros:
  - 不消耗 context 预算
  - 天然持久化、可 git 版本化
  - 支持细粒度权限控制（只读 / 只写某段）
cons:
  - 引入文件 I/O，调试时需额外工具
  - 多 writer 仍需并发控制
  - 不适合「无文件系统」的纯函数 agent
example: |
  state/
  ├── plan.md        # 主 agent 写
  ├── findings.jsonl # worker append-only
  └── decisions.md   # 用户审批后写入
---