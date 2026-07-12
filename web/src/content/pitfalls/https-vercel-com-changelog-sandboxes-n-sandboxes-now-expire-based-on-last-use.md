---
title: Sandboxes now expire based on last use
summary: '<p>Vercel Sandbox snapshots now expire based on when they were last used, not when they were created. Active snapshots stay alive as long as workflows depend on them, while unused snapshots expire on their retention policy.</p><div></div><p>Every time a snapshot is used, its expi'
severity: critical
platforms:
- generic
categories:
- observability
- sandbox
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: Sandboxes now expire based on last use
  url: https://vercel.com/changelog/sandboxes-now-expire-based-on-last-use
  source: vercel-blog
tags:
- vercel-blog
contributor: Marc Codina Segura
discovered_at: '2026-06-29'
verified: false
---
- [Sandboxes now expire based on last use](https://vercel.com/changelog/sandboxes-now-expire-based-on-last-use) — vercel-blog

## 摘要

<p>Vercel Sandbox snapshots now expire based on when they were last used, not when they were created. Active snapshots stay alive as long as workflows depend on them, while unused snapshots expire on their retention policy.</p><div></div><p>Every time a snapshot is used, its expi
