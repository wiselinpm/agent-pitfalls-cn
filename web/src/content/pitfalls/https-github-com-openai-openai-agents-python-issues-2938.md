---
title: "Windows: import agents.sandbox.sandboxes fails with ModuleNotFoundError: fcntl"
summary: '**Body** ### Describe the bug On Windows, importing `agents.sandbox.sandboxes` fails with `ModuleNotFoundError: No module named ''fcntl''`. The sandboxes package eagerly imports the Unix-only backend from src/agents/sandbox/sandboxes/unix_local.py, which depends on Unix-only stdli'
severity: high
platforms:
- openai-agents
categories:
- sandbox
symptoms:
- 'On Windows, importing `agents.sandbox.sandboxes` fails with `ModuleNotFoundError: No module named ''fcntl''`.'
root_causes: []
fixes:
- Guard the Unix-only backend import behind a platform check in src/agents/sandbox/sandboxes/__init__.py and add a small regression test to prevent the Windows import regression.
references:
- title: 'Windows: import agents.sandbox.sandboxes fails with ModuleNotFoundError: fcntl'
  url: https://github.com/openai/openai-agents-python/issues/2938
  source: github:openai/openai-agents-python
tags:
- bug
- feature:sandboxes
contributor: DhanushKenkiri
discovered_at: '2026-04-18'
verified: false
---

- [Windows: import agents.sandbox.sandboxes fails with ModuleNotFoundError: fcntl](https://github.com/openai/openai-agents-python/issues/2938) — github:openai/openai-agents-python

## 摘要

**Body** ### Describe the bug On Windows, importing `agents.sandbox.sandboxes` fails with `ModuleNotFoundError: No module named 'fcntl'`. The sandboxes package eagerly imports the Unix-only backend from src/agents/sandbox/sandboxes/unix_local.py, which depends on Unix-only stdli
