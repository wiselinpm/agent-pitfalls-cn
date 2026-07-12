---
title: Cursor / Aider 等 IDE agent 索引陈旧导致修改错位置
summary: 当 agent 用 IDE 的 code index 搜索代码时，如果工作区刚经历大量重命名或分支切换，索引没有刷新，agent 会编辑已经被删除的旧文件或旧函数签名，提交后 CI 才报错。
severity: medium
platforms: ['cursor', 'aider']
categories: [observability, reliability, state]
symptoms:
  - agent 修改的文件路径在工作区里不存在
  - 提交后 git diff 显示大量 no-op 修改
  - CI 报「undefined symbol」
root_causes:
  - LSP / tree-sitter 索引后台刷新不及时
  - 'agent 没有先 `git status` 验证文件存在'
fixes:
  - 在 agent prompt 里加约束「修改前必须先 read_file 验证存在」
  - '使用 Cursor 的「Composer」模式开启前先 `Ctrl+Shift+P → Reindex Workspace」'
  - CI 流水线加一道「agent 改动路径校验」步骤
references:
  - title: Cursor Codebase Indexing 文档
    url: https://docs.cursor.com/walkthroughs/codebase-indexing
    source: Cursor Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-12-19
verified: true
---
