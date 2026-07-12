---
title: "[vercel/ai] @ai-sdk/groq@4.0.8"
summary: '### Patch Changes - 23ca4c9: fix (provider/groq): surface prompt cache reads in usage `convertGroqUsage` accepted `prompt_tokens_details.cached_tokens` but never read it, so cache hits were reported as `cacheRead: undefined` and the entire prompt was counted as `noCache`.'
severity: critical
platforms:
- generic
categories: []
symptoms: []
root_causes: []
fixes: []
references:
- title: '[vercel/ai] @ai-sdk/groq@4.0.8'
  url: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%404.0.8
  source: github-releases:vercel/ai
tags:
- release
- repo:vercel/ai
contributor: github-actions[bot]
discovered_at: '2026-07-11'
verified: false
---

- [[vercel/ai] @ai-sdk/groq@4.0.8](https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%404.0.8) — github-releases:vercel/ai

## 摘要

### Patch Changes

-   23ca4c9: fix (provider/groq): surface prompt cache reads in usage

    `convertGroqUsage` accepted `prompt_tokens_details.cached_tokens` but never read it, so cache hits were reported as `cacheRead: undefined` and the entire prompt was counted as `noCache`.
