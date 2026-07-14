---
title: 'TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization'
summary: The Key-Value (KV) cache in generative large language models (LLMs) introduces substantial memory overhead. Existing works mitigate this burden by offloading or compressing the KV cache. However, loading the entire cache incurs significant latency due to PCIe bandwidth bottleneck
severity: medium
platforms:
- generic
categories:
- memory
- latency
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization'
  url: https://www.semanticscholar.org/paper/4f537682b00fe2be5ca480d6f43a2513f6657a69
  source: semantic-scholar:long context degradation
tags:
- semantic-scholar
- q:long context degradation
contributor: Dingyu Yao, Bowen Shen, Zheng Lin (2025)
discovered_at: '2025-05-26'
verified: false
---

- [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](https://www.semanticscholar.org/paper/4f537682b00fe2be5ca480d6f43a2513f6657a69) — semantic-scholar:long context degradation

## 摘要

The Key-Value (KV) cache in generative large language models (LLMs) introduces substantial memory overhead. Existing works mitigate this burden by offloading or compressing the KV cache. However, loading the entire cache incurs significant latency due to PCIe bandwidth bottleneck

_来源热度：10_
