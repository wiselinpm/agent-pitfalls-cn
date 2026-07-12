---
title: Vercel Functions now support graceful shutdown
summary: '<p>Vercel Functions running on Node.js and Python runtimes now support graceful shutdown, giving you up to 500 milliseconds to run cleanup tasks before termination.</p><p>When a function is terminated, such as during scale-down, the runtime receives a <code>SIGTERM</code> signal.'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Vercel Functions now support graceful shutdown
  url: https://vercel.com/changelog/vercel-functions-now-support-graceful-shutdown
  source: vercel-blog
tags:
- vercel-blog
contributor: Tom Lienard
discovered_at: '2025-09-08'
verified: false
---
- [Vercel Functions now support graceful shutdown](https://vercel.com/changelog/vercel-functions-now-support-graceful-shutdown) — vercel-blog

## 摘要

<p>Vercel Functions running on Node.js and Python runtimes now support graceful shutdown, giving you up to 500 milliseconds to run cleanup tasks before termination.</p><p>When a function is terminated, such as during scale-down, the runtime receives a <code>SIGTERM</code> signal.
