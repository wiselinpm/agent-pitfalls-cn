---
title: Claude Code 在缺乏权限确认时执行破坏性命令
summary: 'Claude Code 默认会征求用户确认，但通过 `--dangerously-skip-permissions` 或错误配置 `--allowedTools`，它能在没有 prompt 的情况下执行 `rm`、`git push --force`、`chmod -R 777` 等命令，CI 流水线里尤其危险。'
severity: critical
platforms: ['claude-code']
categories: [security, sandbox, tool-use]
symptoms:
  - CI 容器里 agent 删除了 build 产物
  - '`git push --force` 覆盖了主分支'
  - '`chmod` / `chown` 改变了不该改的目录权限'
root_causes:
  - '`--dangerously-skip-permissions` 在 CI 中被滥用以追求「零交互」'
  - '`--allowedTools` 配置过宽（包括 `Bash(*)`）'
  - 容器内 agent 以 root 运行
fixes:
  - 'CI 里用受限的 `--allowedTools`，精确到 `Bash(npm:*)` / `Bash(pytest)`'
  - 容器里使用非 root 用户 + 只读根文件系统
  - 关键操作（rm、push --force、chmod）通过 hooks 强制二次确认
  - 开启 Claude Code 的「permission mode」而非「auto-accept edits」
references:
  - title: 'Claude Code 安全最佳实践'
    url: https://docs.anthropic.com/en/docs/claude-code/security
    source: Anthropic Docs
contributor: agent-pitfalls-bot
discovered_at: 2026-01-05
verified: true
---
