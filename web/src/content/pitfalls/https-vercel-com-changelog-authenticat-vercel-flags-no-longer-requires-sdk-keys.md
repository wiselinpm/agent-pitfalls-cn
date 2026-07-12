---
title: Vercel Flags no longer requires SDK Keys for Vercel deployments
summary: '<p>New projects using Vercel Flags no longer need to configure SDK Keys or the <code>FLAGS</code> environment variable when evaluating flags inside a Vercel deployment. At runtime, the Vercel adapter automatically receives a short-lived OIDC token, so authentication is handled fo'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Vercel Flags no longer requires SDK Keys for Vercel deployments
  url: https://vercel.com/changelog/authenticate-vercel-flags-with-openid-connect-by-default
  source: vercel-blog
tags:
- vercel-blog
contributor: Luis Meyer
discovered_at: '2026-06-24'
verified: false
---
- [Vercel Flags no longer requires SDK Keys for Vercel deployments](https://vercel.com/changelog/authenticate-vercel-flags-with-openid-connect-by-default) — vercel-blog

## 摘要

<p>New projects using Vercel Flags no longer need to configure SDK Keys or the <code>FLAGS</code> environment variable when evaluating flags inside a Vercel deployment. At runtime, the Vercel adapter automatically receives a short-lived OIDC token, so authentication is handled fo
