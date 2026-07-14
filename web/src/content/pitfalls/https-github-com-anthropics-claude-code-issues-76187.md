---
title: "[BUG] Cowork (Windows): project context folders never mount in new sessions; Add-folder dialog cannot confirm ..."
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: high
platforms:
- claude-code
- claude-api
categories:
- streaming
- observability
- sandbox
symptoms:
- Open an existing Cowork project that has a context folder attached (visible in the Context panel)
- Start a new session in that project (any first message)
- Ask Claude to list the connected folder → it reports no folders are connected to the device
- Click **+ → Add folder**, select the folder → the dialog will not confirm
root_causes: []
fixes: []
references:
- title: '[BUG] Cowork (Windows): project context folders never mount in new sessions; Add-folder dialog cannot confirm — reproduced on two machines after latest update'
  url: https://github.com/anthropics/claude-code/issues/76187
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:windows
- area:cowork
- regression
contributor: jwishon
discovered_at: '2026-07-09'
verified: false
---

- [[BUG] Cowork (Windows): project context folders never mount in new sessions; Add-folder dialog cannot confirm — reproduced on two machines after latest update](https://github.com/anthropics/claude-code/issues/76187) — github:anthropics/claude-code

## 摘要

### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]
