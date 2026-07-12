---
title: Preserve local environment variables when linking with the Vercel CLI
summary: '<p>The Vercel CLI now preserves your <code>.env.local</code> file when running <code>vercel link</code>. Previously, linking could overwrite variables already in the file. The CLI now updates <code>VERCEL_OIDC_TOKEN</code> if it exists, or appends it if missing, without touching'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Preserve local environment variables when linking with the Vercel CLI
  url: https://vercel.com/changelog/preserve-local-environment-variables-when-linking-with-the-vercel-cli
  source: vercel-blog
tags:
- vercel-blog
contributor: Melkey Moksyakov
discovered_at: '2026-06-23'
verified: false
---
- [Preserve local environment variables when linking with the Vercel CLI](https://vercel.com/changelog/preserve-local-environment-variables-when-linking-with-the-vercel-cli) — vercel-blog

## 摘要

<p>The Vercel CLI now preserves your <code>.env.local</code> file when running <code>vercel link</code>. Previously, linking could overwrite variables already in the file. The CLI now updates <code>VERCEL_OIDC_TOKEN</code> if it exists, or appends it if missing, without touching
