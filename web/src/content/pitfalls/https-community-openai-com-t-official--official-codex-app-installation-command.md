---
title: Official Codex app installation command resolves to an unrelated third-party app
summary: 'The Windows Codex app documentation at docs/windows/windows-app recommends the following command: winget install Codex -s msstore This command does not resolve to an official OpenAI application. Instead, WinGet selects an unrelated Microsoft Store app called “Codex - QR Reader &'
severity: critical
platforms:
- generic
categories:
- security
symptoms: []
root_causes: []
fixes: []
references:
- title: Official Codex app installation command resolves to an unrelated third-party app
  url: https://community.openai.com/t/official-codex-app-installation-command-resolves-to-an-unrelated-third-party-app/1386469
  source: openai-forum
tags:
- forum
- openai-forum
discovered_at: '2026-07-11'
verified: false
---

- [Official Codex app installation command resolves to an unrelated third-party app](https://community.openai.com/t/official-codex-app-installation-command-resolves-to-an-unrelated-third-party-app/1386469) — openai-forum

## 摘要

The Windows Codex app documentation at docs/windows/windows-app recommends the following command:
winget install Codex -s msstore

This command does not resolve to an official OpenAI application. Instead, WinGet selects an unrelated Microsoft Store app called “Codex - QR Reader &
