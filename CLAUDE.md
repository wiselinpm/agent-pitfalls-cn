# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目速览

`agent-pitfalls` 是一个 **AI agent 开发避坑知识库**，由 100+ 采集器从 GitHub / HackerNews / arXiv / 知乎 / 博客等全网自动汇总 AI agent 开发的真实失败案例，每条含结构化的 **症状 / 根因 / 修复 / 来源**。

仓库同时承载三件产物：
1. **Astro 静态站点** (`web/`) — 8K+ markdown 页面纯静态导出，零 JS hydration
2. **Python CLI** (`agent_pitfalls_cli/`) — 装到本地后在开发期即时查询
3. **采集器与合并管线** (`collectors/`, `scripts/`) — 持续扩库

## 常用命令

### 安装依赖

```bash
npm install                                  # Astro + Tailwind + Sitemap + MDX
pip install -r requirements-dev.txt          # pytest + collectors 依赖
```

### 本地开发

```bash
npm run dev                                  # 站点预览 → http://localhost:4321
npm run build                                # 静态站点输出到 dist/
npm run preview                              # 预览生产构建
```

### 采集与合并

```bash
# 配置 GITHUB_TOKEN 提高 rate limit（强烈建议）
export GITHUB_TOKEN=ghp_xxx

# 跑全部采集器（默认 100 个，输出到 web/src/content/pitfalls/）
python -m collectors.run_all --out data/raw

# 仅跑部分 round
python -m collectors.run_all --no-filter --min-score 0   # 不过滤关键词
python -m collectors.sources.github_issues              # 单个 source

# 严格去重 + 写入 web/src/content/pitfalls/
python scripts/merge_round4.py --in-dirs data/raw* --apply
```

### 测试

```bash
npm test                                     # 等价 pytest collectors/tests -q
pytest -q agent_pitfalls_cli/tests           # CLI 单元测试
pytest --cov=agent_pitfalls_cli              # 带覆盖率
```

### CLI 子命令

```bash
# 全局安装后
pip install -e .
agent-pitfalls search "claude code context overflow"
agent-pitfalls search "tool call" --platform openai-agents --severity high
agent-pitfalls list --category cost --limit 10
agent-pitfalls show <slug>
agent-pitfalls check .                       # 项目避坑体检（静态扫描代码）
agent-pitfalls check src/ --json             # CI 用 JSON
agent-pitfalls serve                         # 本地 HTTP (MCP 通道) 默认 :8765
agent-pitfalls build                         # 重建索引缓存
```

## 架构

```
Sources (100+ collectors/*.py)
       │ yield RawHit
       ▼
normalize.py (RawHit → PitfallDraft, 加 fingerprint / severity / platform / category)
       │
       ▼
dedupe.py (URL fp + title hash + title Jaccard/SequenceMatcher ≥0.85)
       │
       ▼
emit.py → web/src/content/pitfalls/*.md   (Zod schema 强校验: web/src/content.config.ts)
       │
       ▼
Astro 5 静态生成 → dist/  (纯 HTML/CSS, 零 hydration)
       │
       ▼
agent-pitfalls CLI: BM25 多字段加权检索 (title×4 / symptoms×3 / summary×2 / ...)
```

### 关键模块

| 模块 | 路径 | 职责 |
|---|---|---|
| `BaseCollector` 协议 | `collectors/base.py` | 所有采集器实现 `name` + `collect() -> Iterable[RawHit]` |
| `RawHit` dataclass | `collectors/base.py` | 不可变，URL fingerprint 跨 source 去重 |
| `all_collectors()` | `collectors/sources/__init__.py` | 惰性 import + 注册 100+ collector；`safe_collect` 单源失败不阻断 |
| `run_all.py` | `collectors/run_all.py` | 调度入口；PITFALL_KEYWORDS 粗筛 + score 阈值；标题级二次去重 |
| `normalize.py` | `collectors/normalize.py` | 关键词表 → severity / platform / category 推断 |
| `PitfallRecord` | `agent_pitfalls_cli/index.py` | frontmatter + body 的不可变表示；含 BM25 索引字段 |
| `_BM25Index` | `agent_pitfalls_cli/search.py` | 单字段 BM25；多字段加权求和 + 平台/类别/严重度加成 |
| `scan_project()` | `agent_pitfalls_cli/search.py` | 静态扫描代码 → `ScanIssue`，每条 issue 关联相关 pitfall |
| CLI | `agent_pitfalls_cli/cli.py` | argparse 子命令: build/search/list/show/check/platforms/categories/serve |
| Astro config | `astro.config.mjs` | `srcDir: web/src`，`output: 'static'`，shiki github-dark-dimmed |

### Pitfall frontmatter 契约（Zod 权威定义在 `web/src/content.config.ts`）

```yaml
---
title: 一句话描述（4-120 字）          # 必填
summary: 2-3 句话（10-300 字）          # 必填
severity: critical | high | medium | low   # 必填
platforms: [claude-code, langchain, ...]   # 14 个枚举
categories: [context-window, tool-use, ...]  # 14 个枚举
symptoms: ['现象 1', ...]
root_causes: ['根因 1', ...]
fixes: ['可执行修复 1', ...]            # 至少 1 条
references:                              # 至少 1 条，URL 必须 200
  - title: ...
    url: https://...
contributor: github-handle
discovered_at: 2026-01-15
verified: false                          # critical 进入首页推荐位必须 true
---
```

完整枚举值与校验规则见 `docs/SCHEMA.md`。

## 贡献新内容

### 加一条 pitfall

1. `web/src/content/pitfalls/<kebab-case>.md`
2. 复制上面 frontmatter 模板
3. 正文：复现步骤 / 为什么坑 / 修复代码
4. 提 PR — CI 自动校验 zod + 链接可达性

### 加一个 collector

```python
# collectors/sources/my_source.py
from typing import Iterable
from ..base import RawHit

class MySourceCollector:
    name = "my-source"

    def collect(self) -> Iterable[RawHit]:
        for item in fetch_my_data():
            yield RawHit(
                title=item.title, url=item.url,
                source="my-source", summary=item.summary,
            )
```

在 `collectors/sources/__init__.py` 注册，加 `collectors/tests/test_<name>.py`。网络异常必须被 `safe_collect` 兜住（不要抛）。

### 加 CLI 集成（Claude Code / Codex / OpenCode / Gemini）

修改 `plugin/commands/*.md`、`plugin/codex/prompts.toml`、`plugin/opencode.json`、`plugin/gemini-extension.json`。这些插件都依赖 `agent-pitfalls serve` 起的本地 HTTP（默认 :8765）。

## 重要约定

- **不可变优先**：`PitfallRecord` / `RawHit` / `SearchHit` 全是 `@dataclass(frozen=True)`；扩展请返回新对象
- **零后端**：站点纯静态，可直推 gh-pages；CLI 本地 HTTP 仅给 plugin 用
- **采集幂等**：`run_all.py` 默认跳过已存在 markdown（除非 `--overwrite`），不会覆盖人工编辑
- **三维度去重**：URL fingerprint（去 utm_/fbclid） + 标题 SHA1 + 标题相似度 (Jaccard/SequenceMatcher ≥0.85)；合并脚本用 token 反向索引加速
- **关键词过滤**：默认 `_looks_like_pitfall` 强关键词（bug/crash/leak/jailbreak/上下文/死循环/坑…）+ score ≥ 3；可用 `--no-filter --min-score 0` 关闭
- **缓存**：`~/.cache/agent-pitfalls/index-v1-<version>.json`；CLI 启动时优先 load_cache，失败回落到 live 解析
- **路径别名**：`@` → `web/src`（在 `astro.config.mjs` vite alias）
- **CLI 入口**：`agent-pitfalls` 与 `apf` 都是 `agent_pitfalls_cli.cli:main`

## 常见任务

- **新增平台 / 类别枚举** → 同时改三处：`docs/SCHEMA.md`、`web/src/content.config.ts`（zod）、`agent_pitfalls_cli/tokenize.py`（PLATFORM_ALIASES / CATEGORY_ALIASES）
- **改 BM25 权重** → `agent_pitfalls_cli/search.py:FIELD_WEIGHTS` 与 `*_BOOST` 常量
- **加 SCAN_RULES**（静态扫描规则）→ `agent_pitfalls_cli/search.py` 末尾的 `SCAN_RULES` 列表，支持 `match` / `anti_match`（全文） / `anti_match_window`（±1500 字符）
- **调整采集轮次** → 改 `collectors/run_all.py` 默认参数；新 source 注册到 `collectors/sources/__init__.py`