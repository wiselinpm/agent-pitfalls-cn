---
title: "[ToolNode在LangGraph中的运用-01]LangChain和LangGraph两种编程模式的同一性"
summary: 本文深入剖析LangGraph与LangChain两种AI编程模式的内在统一性，指出LangChain Agent底层实际构建的是以State为载体、含LLMNode和ToolNode的双节点状态图；通过工厂函数生成的状态图结构、消息驱动的路由机制（含ToolMessage传递与条件边跳转）、以及ToolNode对工具调用的并发执行与状态更新，揭示二者在抽象模型层面的本质一致性。
severity: medium
platforms:
- langchain
- langgraph
categories:
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: '[ToolNode在LangGraph中的运用-01]LangChain和LangGraph两种编程模式的同一性'
  url: https://blog.csdn.net/JaydenAI/article/details/159814452?ops_request_misc=elastic_search_misc&request_id=022a537598734c78be484f87021ccecf&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-7-159814452-null-null.142^v102^pc_search_result_base6&utm_term=LangGraph
  source: csdn
tags:
- csdn
- LangGraph
contributor: JaydenAI
verified: false
---

- [[ToolNode在LangGraph中的运用-01]LangChain和LangGraph两种编程模式的同一性](https://blog.csdn.net/JaydenAI/article/details/159814452?ops_request_misc=elastic_search_misc&request_id=022a537598734c78be484f87021ccecf&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-7-159814452-null-null.142^v102^pc_search_result_base6&utm_term=LangGraph) — csdn

## 摘要

本文深入剖析LangGraph与LangChain两种AI编程模式的内在统一性，指出LangChain Agent底层实际构建的是以State为载体、含LLMNode和ToolNode的双节点状态图；通过工厂函数生成的状态图结构、消息驱动的路由机制（含ToolMessage传递与条件边跳转）、以及ToolNode对工具调用的并发执行与状态更新，揭示二者在抽象模型层面的本质一致性。
