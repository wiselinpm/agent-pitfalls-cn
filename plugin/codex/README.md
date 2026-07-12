# Codex CLI 集成 — agent-pitfalls

把整个 `codex/` 目录拷贝到 `~/.codex/prompts/agent-pitfalls/` 即可启用：

```bash
mkdir -p ~/.codex/prompts/agent-pitfalls
cp -r plugin/codex/* ~/.codex/prompts/agent-pitfalls/
```

## 提供的命令

| 命令 | 作用 |
|------|------|
| `/pitfall <query>` | 智能搜索 pitfall |
| `/pitfall-check [path]` | 扫描项目避坑 |
| `/pitfall-platforms` | 列出平台 |
| `/pitfall-categories` | 列出类别 |

## 依赖

需要先安装 agent-pitfalls CLI：

```bash
pip install agent-pitfalls
# 或
npm i -g agent-pitfalls
```