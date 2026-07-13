# agent-pitfalls CLI

> **在开发期即时查询 AI agent 避坑知识** — 7,893+ pitfalls · 13+ 平台 · 4 种主流 CLI 集成

把全网散落的 agent 避坑经验收进一个 5 MB 不到的本地索引，让 Claude Code / Codex / OpenCode / Gemini CLI 在写代码的当下就能看到「这里有坑」。

---

## 安装

### 方式 1 — `pip install`（推荐）

```bash
pip install agent-pitfalls
# 或开发模式
pip install -e .
```

装好后：

```bash
agent-pitfalls --version
agent-pitfalls build                          # 首次构建索引（秒级）
agent-pitfalls search "claude code context overflow"
agent-pitfalls check .                        # 对当前项目做避坑体检
```

### 方式 2 — `npx`（无需 Python 环境）

```bash
npx agent-pitfalls search "tool call empty arguments"
npx agent-pitfalls check .
```

`npx agent-pitfalls` 内部会调用 `pipx run agent-pitfalls` / `python -m agent_pitfalls_cli`，透明分发。

### 方式 3 — 一键脚本

```bash
curl -fsSL https://raw.githubusercontent.com/wiselinpm/agent-pitfalls-cn/main/install.sh | bash
```

---

## 子命令

| 命令 | 说明 |
|------|------|
| `agent-pitfalls build` | 构建/刷新索引缓存（`~/.cache/agent-pitfalls/`） |
| `agent-pitfalls search <query>` | 自然语言智能搜索 |
| `agent-pitfalls list` | 列出 pitfalls，支持 `--platform/--category/--severity` 过滤 |
| `agent-pitfalls show <slug>` | 查看单条 pitfall 详情 |
| `agent-pitfalls platforms` | 列出所有平台及数量 |
| `agent-pitfalls categories` | 列出所有类别及数量 |
| `agent-pitfalls check [path]` | 静态扫描项目目录，找已知坑模式 |
| `agent-pitfalls serve` | 启动本地 HTTP 服务，给 Claude Code / OpenCode / Gemini 的 MCP 调用 |
| `agent-pitfalls --version` | 版本 |

### 搜索示例

```bash
# 智能查询
agent-pitfalls search "claude code context overflow"

# 显式过滤
agent-pitfalls search "tool call empty arguments" \
  --platform openai-agents --severity high

# JSON 输出（给 LLM 调）
agent-pitfalls search "prompt injection" --json | jq '.[0].fixes'
```

### 项目体检

```bash
agent-pitfalls check .                              # 人类阅读
agent-pitfalls check . --json                       # CI 用
agent-pitfalls check src/ --limit 100 --severity critical
```

每条 issue 自动关联知识库里的相关 pitfall，附 slug / severity / URL。

---

## 智能查询逻辑

不是关键词匹配，而是**多字段加权 BM25**：

- `title` 权重 4.0（标题是用户最常匹配的目标）
- `symptoms` 权重 3.0（用户报现象时常描述症状）
- `summary` 权重 2.0
- `root_causes` / `fixes` 权重 1.5
- 全文兜底权重 1.0

加上：

- **平台匹配加成**：query 提到 `claude-code` / `langchain` 时，相关 pitfall ×1.5
- **类别匹配加成**：query 提到 `上下文` / `cost` / `memory` 时 ×1.3
- **严重度匹配**：query 显式 `critical` 时优先级最高
- **中英文同义词扩展**：`token limit` ⇄ `上下文` ⇄ `context window` ⇄ `max_tokens`
- **verified 加成**：人工/自动核验过的 ×1.05

---

## 在主流 AI CLI 里使用

详细清单见 [`plugin/README.md`](./plugin/README.md)。最常用的三种：

### Claude Code

```bash
mkdir -p ~/.claude/plugins
ln -s "$(pwd)/plugin" ~/.claude/plugins/agent-pitfalls
```

之后在 Claude Code 里：

```
/pitfall claude code context overflow
/pitfall-check .
/pitfall-list --platform langchain --severity critical
```

### Codex / OpenCode / Gemini CLI

```bash
# Codex
mkdir -p ~/.codex/prompts/agent-pitfalls
cp -r plugin/codex/* ~/.codex/prompts/agent-pitfalls/

# OpenCode
mkdir -p ~/.opencode/plugins
ln -s "$(pwd)/plugin/opencode.json" ~/.opencode/plugins/agent-pitfalls.json

# Gemini CLI
mkdir -p ~/.gemini/extensions/agent-pitfalls
cp plugin/gemini-extension.json ~/.gemini/extensions/agent-pitfalls/
```

---

## 数据来源

直接读仓库内的 `web/src/content/pitfalls/*.md`，无需联网（除首次构建/手动更新）。

数据更新：

```bash
git pull                      # 拉最新 pitfalls
agent-pitfalls build          # 重建索引
```

---

## Python API

```python
from agent_pitfalls_cli import search, load_records, ScanIssue

records = load_records()       # 或 load_records("./my-pitfalls/")
result = search(records, "claude code context overflow", top_k=5)
for hit in result.hits:
    print(hit.score, hit.record.title, hit.record.severity)
```

---

## License

MIT — 同主仓库 [wiselinpm/agent-pitfalls-cn](https://github.com/wiselinpm/agent-pitfalls-cn)