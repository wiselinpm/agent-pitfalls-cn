---
title: Why Cursor Keeps Writing Path Traversal Into Your File Downloads
summary: 'TL;DR AI editors love building file-download endpoints that pass req.query.file straight into a filesystem path. That one line lets an attacker request ../../../../etc/passwd and walk right out of your uploads folder. Fix is boring: resolve the path, then confirm it still live'
severity: critical
platforms:
- claude-code
- cursor
categories:
- security
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Why Cursor Keeps Writing Path Traversal Into Your File Downloads
  url: https://dev.to/c_k_fb750e731394/why-cursor-keeps-writing-path-traversal-into-your-file-downloads-7ml
  source: dev-community
tags:
- dev-community
discovered_at: '2026-07-12'
verified: false
---

- [Why Cursor Keeps Writing Path Traversal Into Your File Downloads](https://dev.to/c_k_fb750e731394/why-cursor-keeps-writing-path-traversal-into-your-file-downloads-7ml) — dev-community

## 摘要

TL;DR



AI editors love building file-download endpoints that pass req.query.file straight into a filesystem path.
That one line lets an attacker request ../../../../etc/passwd and walk right out of your uploads folder.
Fix is boring: resolve the path, then confirm it still live
