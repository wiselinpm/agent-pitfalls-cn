---
title: Proxied responses now cacheable via CDN-Cache-Control headers
summary: '<p>Vercel’s CDN, which can proxy requests to external backends, now caches proxied responses using the <code>CDN-Cache-Control</code> and <code>Vercel-CDN-Cache-Control</code> headers. This aligns caching behavior for external backends with how Vercel Functions are already cached'
severity: critical
platforms:
- generic
categories:
- cost
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Proxied responses now cacheable via CDN-Cache-Control headers
  url: https://vercel.com/changelog/proxied-responses-now-cacheable-via-cdn-cache-control-headers
  source: vercel-blog
tags:
- vercel-blog
contributor: Joe Haddad
discovered_at: '2025-05-13'
verified: false
---
- [Proxied responses now cacheable via CDN-Cache-Control headers](https://vercel.com/changelog/proxied-responses-now-cacheable-via-cdn-cache-control-headers) — vercel-blog

## 摘要

<p>Vercel’s CDN, which can proxy requests to external backends, now caches proxied responses using the <code>CDN-Cache-Control</code> and <code>Vercel-CDN-Cache-Control</code> headers. This aligns caching behavior for external backends with how Vercel Functions are already cached
