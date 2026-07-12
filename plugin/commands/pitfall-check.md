---
description: 对当前项目做「避坑体检」— 静态扫描已知坑模式（硬编码密钥 / 无 max_iterations / 无 429 重试 / system prompt 漂移 等）
argument-hint: [path]  默认当前目录
allowed-tools: Bash(agent-pitfalls:*), Bash(python:*), Read
---

# /pitfall-check — 项目避坑扫描

对 `$ARGUMENTS`（默认 `.`）做静态扫描，每个潜在问题自动关联知识库里的相关 pitfall。

## 执行

```bash
agent-pitfalls check ${ARGUMENTS:-.}
```

## 输出解读

每个 issue 形如：

```
● <规则标题>
  <文件>:<行号>
  > <匹配行>

    → <关联 pitfall 标题>
      <slug>  [<severity>]
```

修复建议：

- 高严重度（critical / high）：立即处理
- medium / low：纳入下一个 sprint

## 常用场景

- 上线前 / 提 PR 前做最后一遍检查
- 新成员入职后跑一遍 `check .` 找 baseline
- 在 CI 里加 `agent-pitfalls check . --json` 出报告