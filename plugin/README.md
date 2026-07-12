# agent-pitfalls plugin — 多 CLI 适配器

这一目录是 **agent-pitfalls** 在主流 AI CLI 里的插件清单打包版。结构：

```
plugin/
├── .claude-plugin/
│   └── plugin.json         # Claude Code 插件清单
├── commands/
│   ├── pitfall.md          # /pitfall
│   ├── pitfall-check.md    # /pitfall-check
│   └── pitfall-list.md     # /pitfall-list
├── codex/
│   ├── prompts.toml        # Codex (OpenAI Codex CLI) prompts
│   └── README.md
├── opencode.json           # OpenCode 插件清单
├── gemini-extension.json   # Gemini CLI extension 清单
└── README.md
```

## 安装方法

### Claude Code

把整个 `plugin/` 目录软链或拷贝到 `~/.claude/plugins/agent-pitfalls/`：

```bash
mkdir -p ~/.claude/plugins
ln -s "$(pwd)/plugin" ~/.claude/plugins/agent-pitfalls
# 或
cp -r plugin ~/.claude/plugins/agent-pitfalls
```

之后在 Claude Code 里就能用：

```
/pitfall claude code context overflow
/pitfall-check .
```

### Codex (OpenAI Codex CLI)

```bash
mkdir -p ~/.codex/prompts/agent-pitfalls
cp -r plugin/codex/* ~/.codex/prompts/agent-pitfalls/
```

### OpenCode

把 `plugin/opencode.json` 软链到 `~/.opencode/plugins/agent-pitfalls.json`：

```bash
mkdir -p ~/.opencode/plugins
ln -s "$(pwd)/plugin/opencode.json" ~/.opencode/plugins/agent-pitfalls.json
```

### Gemini CLI

```bash
mkdir -p ~/.gemini/extensions/agent-pitfalls
cp plugin/gemini-extension.json ~/.gemini/extensions/agent-pitfalls/
```

## 前提

无论哪种 CLI 集成，都需要先安装 `agent-pitfalls` CLI 本身：

```bash
pip install agent-pitfalls          # 推荐
npm i -g agent-pitfalls             # 或
npx agent-pitfalls search "..."     # 不安装也能用，但每次要 npx
```

## 工作原理

- `agent-pitfalls search` / `list` / `check` 子命令：直接读 `web/src/content/pitfalls/*.md`，做 BM25 + 平台/类别加权的智能匹配
- `agent-pitfalls serve` 启动本地 HTTP 服务（默认 :8765），给 Claude Code / OpenCode / Gemini 的 MCP 通道调用
  - `GET /search?q=...&platform=...&category=...`
  - `GET /pitfall/<slug>`
  - `GET /platforms` / `GET /categories`
- Claude Code / OpenCode / Gemini 通过 MCP 直接调本地服务，子命令通过 shell 调用 CLI