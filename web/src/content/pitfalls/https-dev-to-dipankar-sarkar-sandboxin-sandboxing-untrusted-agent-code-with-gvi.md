---
title: Sandboxing untrusted agent code with gVisor costs ~200ms per cold start. Blocking syscalls instead of emulating them cos
summary: You are running code you did not write. It might be an AI agent executing an LLM's output, a CI job...
severity: medium
platforms:
- generic
categories:
- cost
- sandbox
symptoms: []
root_causes: []
fixes: []
references:
- title: Sandboxing untrusted agent code with gVisor costs ~200ms per cold start. Blocking syscalls instead of emulating them costs ~8ms
  url: https://dev.to/dipankar_sarkar/sandboxing-untrusted-agent-code-with-gvisor-costs-200ms-per-cold-start-blocking-syscalls-instead-2500
  source: devto:agents
tags:
- agents
contributor: dipankar_sarkar
discovered_at: '2026-07-05'
verified: false
---

- [Sandboxing untrusted agent code with gVisor costs ~200ms per cold start. Blocking syscalls instead of emulating them costs ~8ms](https://dev.to/dipankar_sarkar/sandboxing-untrusted-agent-code-with-gvisor-costs-200ms-per-cold-start-blocking-syscalls-instead-2500) — devto:agents

## 摘要

You are running code you did not write. It might be an AI agent executing an LLM's output, a CI job...

_来源热度：5_
