---
title: Automatic recursion protection for Vercel Functions
summary: '<p>Vercel now has automatic recursion protection for Vercel Functions.</p><p>This provides safety against your code inadvertently triggering itself repeatedly, incurring unintentional usage. Recursion protection supports using the <code>http</code> module or <code>fetch</code> in'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Automatic recursion protection for Vercel Functions
  url: https://vercel.com/changelog/automatic-recursion-protection-for-vercel-serverless-functions
  source: vercel-blog
tags:
- vercel-blog
contributor: Seiya Nuta
discovered_at: '2023-05-11'
verified: false
---
- [Automatic recursion protection for Vercel Functions](https://vercel.com/changelog/automatic-recursion-protection-for-vercel-serverless-functions) — vercel-blog

## 摘要

<p>Vercel now has automatic recursion protection for Vercel Functions.</p><p>This provides safety against your code inadvertently triggering itself repeatedly, incurring unintentional usage. Recursion protection supports using the <code>http</code> module or <code>fetch</code> in
