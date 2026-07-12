---
title: Workflow SDK now compresses run and step payloads
summary: '<p>The <a href="https://workflow-sdk.dev/">Workflow SDK</a> 5 beta now compresses all run, hook, and step inputs and outputs with <code>zstd</code>.</p><p>Compression kicks in automatically, but only when it helps. Small payloads stay as-is, larger ones get compressed before they'
severity: critical
platforms:
- generic
categories:
- streaming
- cost
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Workflow SDK now compresses run and step payloads
  url: https://vercel.com/changelog/workflow-sdk-now-compresses-run-and-step-payloads
  source: vercel-blog
tags:
- vercel-blog
contributor: Pranay Prakash
discovered_at: '2026-06-22'
verified: false
---
- [Workflow SDK now compresses run and step payloads](https://vercel.com/changelog/workflow-sdk-now-compresses-run-and-step-payloads) — vercel-blog

## 摘要

<p>The <a href="https://workflow-sdk.dev/">Workflow SDK</a> 5 beta now compresses all run, hook, and step inputs and outputs with <code>zstd</code>.</p><p>Compression kicks in automatically, but only when it helps. Small payloads stay as-is, larger ones get compressed before they
