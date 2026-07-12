---
title: "[BUG] Oversized-image 400 error triggers a retry loop that invalidates prompt cache and inflates cost ~35×"
summary: '### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn''t been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]'
severity: critical
platforms:
- claude-code
- claude-api
categories:
- streaming
- cost
- observability
symptoms:
- In a long-running session, have the agent read/attach an image larger than 2000px in some dimension (e.g. a generated plot / screenshot).
- The API rejects the request with the 400 above.
- Observe Claude Code remove the image and continue issuing requests.
- Inspect token usage in the session `.jsonl` (or `ccusage`).
root_causes:
- Image exceeds the `2000px` many-image limit → API `400`.
- Claude Code mutates the message history to remove the image.
- The cached prefix no longer matches → cache miss for the whole prefix.
fixes:
- '**Pre-validate & auto-resize images** to the API''s max dimensions (and per-image / many-image rules) before sending.'
- '**Don''t enter an unbounded retry loop** on `invalid_request_error` for images — fail fast and ask the user once.'
- When history is edited mid-session, **warn that the prompt cache will be invalidated**, and/or restructure edits to preserve the cacheable prefix.
- Optionally surface a cost/cache-miss warning when cache-read drops to ~0 across many consecutive turns.
references:
- title: '[BUG] Oversized-image 400 error triggers a retry loop that invalidates prompt cache and inflates cost ~35×'
  url: https://github.com/anthropics/claude-code/issues/65636
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- area:cost
- area:core
- platform:wsl
- stale
contributor: PeterGanZW
discovered_at: '2026-06-05'
verified: false
---

- [[BUG] Oversized-image 400 error triggers a retry loop that invalidates prompt cache and inflates cost ~35×](https://github.com/anthropics/claude-code/issues/65636) — github:anthropics/claude-code

## 摘要

### Preflight Checklist - [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet - [x] This is a single bug report (please file separate reports for different bugs) - [x]
