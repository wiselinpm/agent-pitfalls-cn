---
title: 'Remote Control fails: `bridge_state: failed - /login` (bridge reachable, valid personal-account token rejected)'
summary: '**Summary:** `/remote-control` fails immediately with `bridge_state: failed - /login`. The Remote Control bridge host is fully reachable and the account is eligible, but the auth handshake is rejected. Appears to be a server-side account-provisioning / rollout gap rather than a c'
severity: critical
platforms:
- claude-code
categories:
- observability
- memory
- sandbox
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Remote Control fails: `bridge_state: failed - /login` (bridge reachable, valid personal-account token rejected)'
  url: https://github.com/anthropics/claude-code/issues/65801
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:windows
- area:auth
- area:desktop
- stale
contributor: kahless2k
discovered_at: '2026-06-06'
verified: false
---

- [Remote Control fails: `bridge_state: failed - /login` (bridge reachable, valid personal-account token rejected)](https://github.com/anthropics/claude-code/issues/65801) — github:anthropics/claude-code

## 摘要

**Summary:** `/remote-control` fails immediately with `bridge_state: failed - /login`. The Remote Control bridge host is fully reachable and the account is eligible, but the auth handshake is rejected. Appears to be a server-side account-provisioning / rollout gap rather than a c

_来源热度：4_
