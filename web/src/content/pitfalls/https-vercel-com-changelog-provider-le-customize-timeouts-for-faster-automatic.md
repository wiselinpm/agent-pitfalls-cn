---
title: Customize timeouts for faster automatic failover on Vercel AI Gateway
summary: '<p>AI Gateway now supports per-inference <a href="https://vercel.com/docs/ai-gateway/models-and-providers">provider</a> timeouts for faster failover than the provider default. If a provider doesn''''t start responding within your configured timeout, AI Gateway aborts the request and'
severity: critical
platforms:
- generic
categories:
- streaming
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Customize timeouts for faster automatic failover on Vercel AI Gateway
  url: https://vercel.com/changelog/provider-level-custom-timeouts-for-faster-fail-over-on-ai-gateway
  source: vercel-blog
tags:
- vercel-blog
contributor: Jerilyn Zheng
discovered_at: '2026-03-05'
verified: false
---
- [Customize timeouts for faster automatic failover on Vercel AI Gateway](https://vercel.com/changelog/provider-level-custom-timeouts-for-faster-fail-over-on-ai-gateway) — vercel-blog

## 摘要

<p>AI Gateway now supports per-inference <a href="https://vercel.com/docs/ai-gateway/models-and-providers">provider</a> timeouts for faster failover than the provider default. If a provider doesn't start responding within your configured timeout, AI Gateway aborts the request and
