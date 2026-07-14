---
title: "Cloud Agents API: auto-created PRs switched from ready-for-review to draft around July 11 (no client-side chan..."
summary: 'Where does the bug appear (feature/product)? Cloud Agent (GitHub, Slack, Web, Linear) Describe the Bug We dispatch Cloud Agents from CI via POST https://api.cursor.com/v1/agents to auto-fix nightly Docker build failures in a private repository, with autoCreatePR: true and skipRev'
severity: critical
platforms:
- cursor
categories:
- observability
- sandbox
- state
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Cloud Agents API: auto-created PRs switched from ready-for-review to draft around July 11 (no client-side change)'
  url: https://forum.cursor.com/t/cloud-agents-api-auto-created-prs-switched-from-ready-for-review-to-draft-around-july-11-no-client-side-change/165483
  source: cursor-forum
tags:
- cursor-forum
discovered_at: '2026-07-11'
verified: false
---

- [Cloud Agents API: auto-created PRs switched from ready-for-review to draft around July 11 (no client-side change)](https://forum.cursor.com/t/cloud-agents-api-auto-created-prs-switched-from-ready-for-review-to-draft-around-july-11-no-client-side-change/165483) — cursor-forum

## 摘要

Where does the bug appear (feature/product)? Cloud Agent (GitHub, Slack, Web, Linear) Describe the Bug We dispatch Cloud Agents from CI via POST https://api.cursor.com/v1/agents to auto-fix nightly Docker build failures in a private repository, with autoCreatePR: true and skipRev
