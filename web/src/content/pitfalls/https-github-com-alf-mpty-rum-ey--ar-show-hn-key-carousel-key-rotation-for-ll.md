---
title: 'Show HN: key-carousel - Key rotation for LLM agents'
summary: 'I think in-process key management is the right abstraction for multi-key LLM setups. Not LiteLLM, not a Redis queue, not a custom load balancer.<p>The failure modes are well-understood: a key gets rate-limited, you wait, you try the next one. Billing errors need a longer cooldown'
severity: medium
platforms:
- generic
categories:
- cost
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Show HN: key-carousel - Key rotation for LLM agents'
  url: https://github.com/HalfEmptyDrum/Key-Carousel
  source: hn-algolia-ext:story
tags:
- hackernews
verified: false
---
- [Show HN: key-carousel - Key rotation for LLM agents](https://github.com/HalfEmptyDrum/Key-Carousel) — hn-algolia-ext:story

## 摘要

I think in-process key management is the right abstraction for multi-key LLM setups. Not LiteLLM, not a Redis queue, not a custom load balancer.<p>The failure modes are well-understood: a key gets rate-limited, you wait, you try the next one. Billing errors need a longer cooldown

_来源热度：5_
