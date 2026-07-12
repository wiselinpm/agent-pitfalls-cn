---
title: Faster deploys with improved function caching
summary: '<p>Function uploads are now skipped when code hasn''''t changed, reducing build times by 400-600ms on average and up to 5 seconds for larger builds.</p><p>Previously, deployment-specific environment variables like <code>VERCEL_DEPLOYMENT_ID</code> were included in the function paylo'
severity: critical
platforms:
- generic
categories:
- observability
- memory
symptoms: []
root_causes: []
fixes: []
references:
- title: Faster deploys with improved function caching
  url: https://vercel.com/changelog/faster-deploys-with-improved-function-caching
  source: vercel-blog
tags:
- vercel-blog
contributor: Felix Haus
discovered_at: '2026-01-23'
verified: false
---
- [Faster deploys with improved function caching](https://vercel.com/changelog/faster-deploys-with-improved-function-caching) — vercel-blog

## 摘要

<p>Function uploads are now skipped when code hasn't changed, reducing build times by 400-600ms on average and up to 5 seconds for larger builds.</p><p>Previously, deployment-specific environment variables like <code>VERCEL_DEPLOYMENT_ID</code> were included in the function paylo
