# skills/ — Skills.sh 收录目录

本目录是 `agent-pitfalls` 在 [skills.sh](https://skills.sh) 上的索引布局。每个子目录是一个独立 skill，目录里的 `SKILL.md` 是该 skill 的入口描述文件。

skills.sh 通过 GitHub 自动扫描含 `SKILL.md` 的仓库并索引，**无需注册、无需审核、无需中央注册表**。只要仓库是 public、SKILL.md 的 YAML frontmatter 合规，skill 就会出现在搜索结果里。

## 目录结构

```
skills/
├── README.md                       # 本文件
├── agent-pitfalls-search/          # 智能搜索避坑知识
│   └── SKILL.md
├── agent-pitfalls-list/            # 按平台/类别/严重度浏览
│   └── SKILL.md
└── agent-pitfalls-check/           # 静态扫描项目代码
    └── SKILL.md
```

| Skill | 触发场景 | CLI 子命令 |
|---|---|---|
| `agent-pitfalls-search` | 调试 agent 故障、查询已知症状/根因/修复 | `agent-pitfalls search <query>` |
| `agent-pitfalls-list` | 培训材料、审计清单、批量导出 | `agent-pitfalls list [--platform ...] [--category ...] [--severity ...]` |
| `agent-pitfalls-check` | PR/CI/上线前静态扫描 | `agent-pitfalls check [path]` |

每个 skill 与 `plugin/commands/` 下同名 Claude Code 命令、`plugin/codex/prompts.toml`、`plugin/opencode.json`、`plugin/gemini-extension.json` 的对应命令行为一致。

## 安装

### 单 skill 安装（推荐，按需）

```bash
# 只装搜索能力
npx skills add https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/skills/agent-pitfalls-search

# 只装静态扫描能力
npx skills add https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/skills/agent-pitfalls-check
```

### 整库安装

```bash
npx skills add https://github.com/wiselinpm/agent-pitfalls-cn
```

### 前置依赖

所有 skill 都依赖 `agent-pitfalls` CLI（提供 BM25 索引 + 静态扫描规则）：

```bash
pip install agent-pitfalls
# 或
npm i -g agent-pitfalls
```

`SKILL.md` 里的 Steps 段会显式调用这些 CLI 子命令。

## SKILL.md 格式约定

参考 [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) 的真实示例：

```yaml
---
name: <kebab-case-唯一名>
description: >              # 第三人称、含 "Use when..." / "Triggers on..." 触发词
  做什么 + 何时使用
license: MIT                # 可选但强烈建议
metadata:
  author: <handle>
  version: "<semver>"
  argument-hint: "<arg-shape>"   # 可选，描述参数形状
---
```

正文段落约定：

- `# <Skill Name>` — 一级标题
- `## When to Apply` — 触发场景 + 反例（何时不要用）
- `## Prerequisites` — 依赖与安装
- `## Steps` — 一步步执行命令
- `## Output Format` — 输出排版建议
- `## Quality Rules` — 引用真实性等约束
- `## Related Skills` — 链接到本仓库其他 skill

## 收录验证清单

PR 合并后等待 skills.sh 抓取（一般几天）。可通过以下方式验证：

1. 搜索框输入 `agent-pitfalls`，应出现三个 skill
2. 每个 skill 详情页能正确渲染 frontmatter
3. `npx skills add <repo-url>` 能正常安装

若一周后仍未索引，去 [vercel-labs/skills](https://github.com/vercel-labs/skills) 提 issue 询问。

## 本目录 vs plugin/

| 用途 | 路径 | 目标用户 |
|---|---|---|
| skills.sh 收录 | `skills/<name>/SKILL.md` | 全网 agent 用户（Claude Code / Codex / Cursor / OpenCode / Gemini 等） |
| Claude Code 原生 slash commands | `plugin/commands/*.md` | Claude Code 用户 |
| Codex CLI prompts | `plugin/codex/prompts.toml` | OpenAI Codex CLI 用户 |
| OpenCode / Gemini 适配器 | `plugin/opencode.json`、`plugin/gemini-extension.json` | 对应 CLI 用户 |

两套布局并存，不冲突。修改 SKILL.md 不影响 plugin/commands/，反之亦然。