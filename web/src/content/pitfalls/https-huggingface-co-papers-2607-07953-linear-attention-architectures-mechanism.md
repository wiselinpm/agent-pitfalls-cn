---
title: "Linear Attention Architectures: Mechanisms, Trade-offs, and Cross-Layer Routing"
summary: Self-attention lets each token retrieve information from the full context, but its quadratic cost in sequence length limits training and inference at long context. This paper presents a comparative study of softmax attention and four recent recurrent linear-attention architecture
severity: high
platforms:
- generic
categories:
- streaming
- cost
- memory
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Linear Attention Architectures: Mechanisms, Trade-offs, and Cross-Layer Routing'
  url: https://huggingface.co/papers/2607.07953
  source: huggingface-papers
tags:
- huggingface
- paper
contributor: Tommaso Cerruti, Tim Rieder, George Rowlands
discovered_at: '2026-07-08'
verified: false
---

- [Linear Attention Architectures: Mechanisms, Trade-offs, and Cross-Layer Routing](https://huggingface.co/papers/2607.07953) — huggingface-papers

## 摘要

Self-attention lets each token retrieve information from the full context, but its quadratic cost in sequence length limits training and inference at long context. This paper presents a comparative study of softmax attention and four recent recurrent linear-attention architecture

_来源热度：10_
