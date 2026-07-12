---
title: "permissions.ask does not fire for Bash commands under sandbox.autoAllowBashIfSandboxed: true"
summary: '## Bug description `permissions.ask` rules for `Bash(...)` patterns do not fire for commands executed under `sandbox.autoAllowBashIfSandboxed: true`. The command runs immediately with no confirmation prompt, as if the `ask` rule didn''t exist. This contradicts the documented beh'
severity: critical
platforms:
- claude-code
categories:
- sandbox
- state
symptoms:
- '`permissions.ask` rules for `Bash(...)` patterns do not fire for commands executed under `sandbox.autoAllowBashIfSandboxed: true`. The command runs immediately with no confirmation prompt, as if the `ask` rule didn''t exist.'
root_causes: []
fixes: []
references:
- title: 'permissions.ask does not fire for Bash commands under sandbox.autoAllowBashIfSandboxed: true'
  url: https://github.com/anthropics/claude-code/issues/76850
  source: github:anthropics/claude-code
tags:
- bug
- has repro
- platform:wsl
- area:permissions
- area:sandbox
contributor: goodjobandrew
discovered_at: '2026-07-12'
verified: false
---

- [permissions.ask does not fire for Bash commands under sandbox.autoAllowBashIfSandboxed: true](https://github.com/anthropics/claude-code/issues/76850) — github:anthropics/claude-code

## 摘要

## Bug description

`permissions.ask` rules for `Bash(...)` patterns do not fire for commands executed under `sandbox.autoAllowBashIfSandboxed: true`. The command runs immediately with no confirmation prompt, as if the `ask` rule didn't exist.

This contradicts the documented beh

_来源热度：2_
