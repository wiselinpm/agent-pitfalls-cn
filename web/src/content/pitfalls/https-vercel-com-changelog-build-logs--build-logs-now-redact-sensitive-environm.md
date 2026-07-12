---
title: Build logs now redact Sensitive Environment Variable values
summary: '<p>When an Environment Variable is marked Sensitive and has a value 32 characters or longer, Vercel now replaces it with <code>[REDACTED]</code> in the deployment''''s build logs.</p><p>The Build Logs view also indicates when redaction happened, giving teams visibility into why outp'
severity: critical
platforms:
- generic
categories:
- security
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Build logs now redact Sensitive Environment Variable values
  url: https://vercel.com/changelog/build-logs-now-redact-sensitive-environment-variable-values
  source: vercel-blog
tags:
- vercel-blog
contributor: Andrew Healey
discovered_at: '2026-07-09'
verified: false
---
- [Build logs now redact Sensitive Environment Variable values](https://vercel.com/changelog/build-logs-now-redact-sensitive-environment-variable-values) — vercel-blog

## 摘要

<p>When an Environment Variable is marked Sensitive and has a value 32 characters or longer, Vercel now replaces it with <code>[REDACTED]</code> in the deployment's build logs.</p><p>The Build Logs view also indicates when redaction happened, giving teams visibility into why outp
