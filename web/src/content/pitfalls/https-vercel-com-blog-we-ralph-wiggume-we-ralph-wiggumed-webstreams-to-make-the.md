---
title: We Ralph Wiggumed WebStreams to make them 10x faster
summary: '<p>When we started profiling Next.js server rendering earlier this year, one thing kept showing up in the flamegraphs: WebStreams. Not the application code running inside them, but the streams themselves. The Promise chains, the per-chunk object allocations, the microtask queue h'
severity: critical
platforms:
- generic
categories:
- streaming
- cost
- security
symptoms: []
root_causes: []
fixes: []
references:
- title: We Ralph Wiggumed WebStreams to make them 10x faster
  url: https://vercel.com/blog/we-ralph-wiggumed-webstreams-to-make-them-10x-faster
  source: vercel-blog
tags:
- vercel-blog
contributor: Malte Ubl
discovered_at: '2026-02-18'
verified: false
---
- [We Ralph Wiggumed WebStreams to make them 10x faster](https://vercel.com/blog/we-ralph-wiggumed-webstreams-to-make-them-10x-faster) — vercel-blog

## 摘要

<p>When we started profiling Next.js server rendering earlier this year, one thing kept showing up in the flamegraphs: WebStreams. Not the application code running inside them, but the streams themselves. The Promise chains, the per-chunk object allocations, the microtask queue h
