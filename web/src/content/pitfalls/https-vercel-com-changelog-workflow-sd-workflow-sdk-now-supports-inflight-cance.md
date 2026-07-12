---
title: Workflow SDK now supports inflight cancellation
summary: '<p>The Workflow SDK 5 beta now supports the standard <code>AbortController</code> and <code>AbortSignal</code> APIs across workflow and step boundaries.</p><p>Create a controller inside a workflow, pass its signal into one or more steps, and cancel in-flight operations using the'
severity: critical
platforms:
- generic
categories:
- observability
- latency
symptoms: []
root_causes: []
fixes: []
references:
- title: Workflow SDK now supports inflight cancellation
  url: https://vercel.com/changelog/workflow-sdk-now-supports-inflight-cancellation
  source: vercel-blog
tags:
- vercel-blog
contributor: Pranay Prakash
discovered_at: '2026-06-16'
verified: false
---
- [Workflow SDK now supports inflight cancellation](https://vercel.com/changelog/workflow-sdk-now-supports-inflight-cancellation) — vercel-blog

## 摘要

<p>The Workflow SDK 5 beta now supports the standard <code>AbortController</code> and <code>AbortSignal</code> APIs across workflow and step boundaries.</p><p>Create a controller inside a workflow, pass its signal into one or more steps, and cancel in-flight operations using the
