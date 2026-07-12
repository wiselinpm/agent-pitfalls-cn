---
title: 'Workflow 4.1 Beta: Event-sourced architecture'
summary: '<p><a href="https://github.com/vercel/workflow/releases/tag/workflow%404.1.0-beta.51">Workflow 4.1 Beta</a> changes how workflows track state internally. Instead of updating records in place, every state change is now stored as an event, and current state is reconstructed by repl'
severity: critical
platforms:
- generic
categories:
- streaming
- observability
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Workflow 4.1 Beta: Event-sourced architecture'
  url: https://vercel.com/changelog/workflow-event-sourcing
  source: vercel-blog
tags:
- vercel-blog
contributor: John Lindquist
discovered_at: '2026-02-03'
verified: false
---
- [Workflow 4.1 Beta: Event-sourced architecture](https://vercel.com/changelog/workflow-event-sourcing) — vercel-blog

## 摘要

<p><a href="https://github.com/vercel/workflow/releases/tag/workflow%404.1.0-beta.51">Workflow 4.1 Beta</a> changes how workflows track state internally. Instead of updating records in place, every state change is now stored as an event, and current state is reconstructed by repl
