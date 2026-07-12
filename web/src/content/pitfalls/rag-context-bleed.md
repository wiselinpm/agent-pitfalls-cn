---
title: RAG 检索结果让 Agent「记错」私有文档内容
summary: 向量检索返回的 top-k 文档片段包含过时或无关上下文，agent 会把片段里的错误信息当成「事实」回答用户，且不会主动声明「这是我检索到的旧版本」。
severity: high
platforms: ['langchain', 'langgraph', 'generic']
categories: [memory, reliability, observability]
symptoms:
  - 用户问「最新的 API 文档说 X 是什么」，agent 引用了已经被废弃的旧版本
  - 多个 chunk 互相矛盾时，agent 随机挑一个
  - 检索召回率很高但精确率低
root_causes:
  - 向量库没有时间衰减权重，旧文档与新文档等权
  - 没有 chunk-level 元数据（版本、更新时间）传给 LLM
  - top_k 过大，模型被淹没在不相关信息里
fixes:
  - '写入向量库时附带 `updated_at`、`version`、`source_url` 元数据'
  - 检索 prompt 里强制要求「引用时请注明来源 URL 与版本」
  - top_k 设为 3-5，配合 reranker（如 Cohere Rerank）
  - 使用 LangGraph 的「reflection」节点让 agent 自检引用是否一致
references:
  - title: LangChain RAG Best Practices
    url: https://python.langchain.com/docs/how_to/rag/
    source: LangChain Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-11-08
verified: true
---
