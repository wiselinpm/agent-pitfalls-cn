---
title: OpenAI这次重写Agents SDK，把LangChain们的饭碗端了
summary: OpenAI全面重写Agents SDK，将harness与沙盒彻底解耦，引入Manifest实现多沙盒厂商（如Modal、E2B等）无缝切换，并内置快照恢复、多沙盒并行等长周期Agent必需能力。新SDK封装了配置化记忆、MCP工具调用、安全沙盒执行等基础设施，显著降低Agent工程复杂度，对LangChain等第三方框架构成底层替代压力。
severity: medium
platforms:
- openai-agents
- langchain
categories: []
symptoms: []
root_causes: []
fixes: []
references:
- title: OpenAI这次重写Agents SDK，把LangChain们的饭碗端了
  url: https://blog.csdn.net/fzuim/article/details/160233980?ops_request_misc=elastic_search_misc&request_id=0a12da06826542cab4d5be5d51274eb1&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-20-160233980-null-null.142^v102^pc_search_result_base8&utm_term=OpenAI%20Agents%20SDK
  source: csdn
tags:
- csdn
- OpenAI Agents SDK
contributor: fzuim
verified: false
---

- [OpenAI这次重写Agents SDK，把LangChain们的饭碗端了](https://blog.csdn.net/fzuim/article/details/160233980?ops_request_misc=elastic_search_misc&request_id=0a12da06826542cab4d5be5d51274eb1&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-20-160233980-null-null.142^v102^pc_search_result_base8&utm_term=OpenAI%20Agents%20SDK) — csdn

## 摘要

OpenAI全面重写Agents SDK，将harness与沙盒彻底解耦，引入Manifest实现多沙盒厂商（如Modal、E2B等）无缝切换，并内置快照恢复、多沙盒并行等长周期Agent必需能力。新SDK封装了配置化记忆、MCP工具调用、安全沙盒执行等基础设施，显著降低Agent工程复杂度，对LangChain等第三方框架构成底层替代压力。
