---
title: Faster CDN proxying to external origins
summary: '<p>We’ve optimized connection pooling in our CDN to reduce latency when connecting to external backends, regardless of traffic volume.</p><ul><li><p><b>Lower latency</b>: Improved connection reuse and TLS session resumption reduce response times by up to 60% in some regions, with'
severity: critical
platforms:
- generic
categories:
- cost
- observability
- memory
symptoms: []
root_causes: []
fixes: []
references:
- title: Faster CDN proxying to external origins
  url: https://vercel.com/changelog/faster-cdn-proxying-to-external-origins
  source: vercel-blog
tags:
- vercel-blog
contributor: Joe Haddad
discovered_at: '2025-05-23'
verified: false
---
- [Faster CDN proxying to external origins](https://vercel.com/changelog/faster-cdn-proxying-to-external-origins) — vercel-blog

## 摘要

<p>We’ve optimized connection pooling in our CDN to reduce latency when connecting to external backends, regardless of traffic volume.</p><ul><li><p><b>Lower latency</b>: Improved connection reuse and TLS session resumption reduce response times by up to 60% in some regions, with
