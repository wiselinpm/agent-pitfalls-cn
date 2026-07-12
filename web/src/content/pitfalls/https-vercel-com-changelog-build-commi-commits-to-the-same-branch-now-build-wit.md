---
title: Commits to the same branch now build with no queues
summary: '<p>Vercel now builds multiple commits to the same branch at the same time when On-Demand Concurrent Builds is enabled. Previously, a new commit would wait for the previous build on that branch to finish before starting. This update eliminates that queue, allowing commits to star'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Commits to the same branch now build with no queues
  url: https://vercel.com/changelog/build-commits-to-the-same-branch-without-waiting
  source: vercel-blog
tags:
- vercel-blog
contributor: Janos Szathmary
discovered_at: '2025-10-14'
verified: false
---
- [Commits to the same branch now build with no queues](https://vercel.com/changelog/build-commits-to-the-same-branch-without-waiting) — vercel-blog

## 摘要

<p>Vercel now builds multiple commits to the same branch at the same time when On-Demand Concurrent Builds is enabled.

Previously, a new commit would wait for the previous build on that branch to finish before starting. This update eliminates that queue, allowing commits to star
