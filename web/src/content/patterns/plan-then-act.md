---
title: Plan-then-Act — ReAct 的两阶段替代
summary: 让 agent 先输出完整计划（编号步骤），再开始执行；中途可重新回到计划节点调整。比 ReAct 更易调试、更易中断、且对 token 预算友好。
use_when: 复杂多步任务、需要用户审批计划、或希望降低 agent 失控风险时。
pros:
  - 计划可被人类审查、修改
  - 中断/恢复简单：从「当前步骤」继续
  - 减少 ReAct 的无目的探索
cons:
  - 第一次规划消耗额外时间
  - 对短任务过度设计
  - 模型可能「假装规划」但实际执行时偏离
example: |
  def run(goal):
      plan = llm(f"为以下目标生成 1-7 步计划：{goal}")
      approved = human_review(plan)  # 可选
      for step in plan.steps:
          result = execute(step, context)
          context.append(result)
          if needs_replan(result):
              plan = replan(plan, result)
---