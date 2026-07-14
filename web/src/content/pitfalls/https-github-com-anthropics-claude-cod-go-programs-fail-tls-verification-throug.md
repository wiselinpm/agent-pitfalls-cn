---
title: 'Go programs fail TLS verification through built-in proxy on macOS Tahoe (x509: OSStatus -26276)'
summary: '## Description Go-based CLI tools (`gh`, `flyctl`, and likely all Go programs) fail with TLS certificate verification errors when their traffic is routed through Claude Code''s built-in network proxy on macOS Tahoe (26.x). The proxy itself works correctly — `curl` succeeds throu'
severity: critical
platforms:
- claude-code
categories:
- streaming
- security
- sandbox
symptoms:
- '## Description


  Go-based CLI tools (`gh`, `flyctl`, and likely all Go programs) fail with TLS certificate verification errors when their traffic is routed through Claude Code''s built-in network proxy on macOS Tahoe (26.x).


  The proxy itself works correctly — `curl` succeeds throu'
root_causes: []
fixes:
- Run `gh`/`flyctl` in a separate terminal outside of Claude Code, where the proxy env vars are not set.
references:
- title: 'Go programs fail TLS verification through built-in proxy on macOS Tahoe (x509: OSStatus -26276)'
  url: https://github.com/anthropics/claude-code/issues/77334
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:macos
- area:networking
contributor: dawnho
discovered_at: '2026-07-14'
verified: false
---

- [Go programs fail TLS verification through built-in proxy on macOS Tahoe (x509: OSStatus -26276)](https://github.com/anthropics/claude-code/issues/77334) — github:anthropics/claude-code

## 摘要

## Description

Go-based CLI tools (`gh`, `flyctl`, and likely all Go programs) fail with TLS certificate verification errors when their traffic is routed through Claude Code's built-in network proxy on macOS Tahoe (26.x).

The proxy itself works correctly — `curl` succeeds throu

_来源热度：1_
