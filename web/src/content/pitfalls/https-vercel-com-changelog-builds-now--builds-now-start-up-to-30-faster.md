---
title: 'Builds now start up to 30% faster'
summary: '<p>The build cache stores files from previous builds to speed up future ones. We''''ve improved its performance by downloading parts of the cache in parallel using a worker pool.</p><p>This decreased the build initialization time by <b>30% on average</b>, reducing build times by up'
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
- title: Builds now start up to 30% faster
  url: https://vercel.com/changelog/builds-now-start-up-to-30-faster
  source: vercel-blog
tags:
- vercel-blog
contributor: Luke Phillips-Sheard
discovered_at: '2025-09-16'
verified: false
---
- [Builds now start up to 30% faster](https://vercel.com/changelog/builds-now-start-up-to-30-faster) — vercel-blog

## 摘要

<p>The build cache stores files from previous builds to speed up future ones. We've improved its performance by downloading parts of the cache in parallel using a worker pool.</p><p>This decreased the build initialization time by <b>30% on average</b>, reducing build times by up
