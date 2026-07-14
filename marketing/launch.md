# agent-pitfalls — 推广文案

发布日期：2026-07-13
真实数据（来自 `web/src/content/pitfalls/*.md`）：
- **7,893 条** pitfall（不是 README 写的 5,561+）
- 严重度：2,838 critical / 776 high / 4,135 medium / 144 low
- 13 个平台：aider, autogen, claude-api, claude-code, crewai, cursor, gemini-api, generic, langchain, langgraph, open-interpreter, openai-agents, openai-api
- 13 个类别：context-window, cost, latency, memory, multi-agent, observability, prompt-injection, reliability, sandbox, security, state, streaming, tool-use
- 来源：GitHub issues、HackerNews、arXiv、博客、知乎

---

## 1. Hacker News — Show HN

**建议发布时间**：周二/周三/周四 美东时间 8–10 点
**Title**（≤80 字符）：

```
Show HN: agent-pitfalls – 7,893 real AI agent failures, indexed
```

**URL**：

```
https://github.com/wiselinpm/agent-pitfalls-cn
```

**正文**：

```
I spent the last few months collecting AI agent postmortems from GitHub
issues, HN, arXiv, blog writeups, and Zhihu threads. Each case is
normalized into a structured record:

  symptom → root_cause → fix
  severity (critical/high/medium/low) × platform × category

The corpus currently holds 7,893 cases across 13 platforms
(claude-code, langchain, openai-agents, autogen, cursor, ...) and 13
failure categories (context-window overflow, tool-use loops, prompt
injection, API-key leaks, ...).

Three ways to use it:

1. CLI — `pip install agent-pitfalls && agent-pitfalls search "context
   overflow"` runs BM25 over title × symptoms × summary with platform
   and severity boosts.

2. Static scanner — `agent-pitfalls check ./src` greps your code for
   patterns that have caused documented failures (hardcoded API keys,
   unbounded tool output, missing max-iterations, system prompt drift,
   unvalidated MCP inputs, etc.) and links every hit back to the
   original case.

3. Skill — just shipped three skills.sh-compatible SKILL.md files so
   Claude Code, Codex, Cursor, OpenCode, and Gemini CLI can call the
   CLI via `npx skills add ...`.

The collectors are 100+ scripts in `collectors/sources/` — each one
tries to pull a specific source (rss feeds, HN threads, arXiv queries,
GitHub repo searches) and yields raw hits that get normalized and
deduped before writing markdown.

Everything is MIT and the corpus is rebuilt weekly. Curious which
failure patterns people hit that aren't in here yet — would love
PRs that add new collectors or new cases.

Install: https://github.com/wiselinpm/agent-pitfalls-cn
Live site (5k+ pages): `git clone && npm install && npm run dev` →
http://localhost:4321
```

**回复准备**（HN 评论常见质疑）：

| 问题 | 回复方向 |
|---|---|
| "数据来源可信吗？" | 每个 pitfall markdown 末尾都附 `references: [url]`，可点击验证；CLI 提供 `show <slug>` 看原始来源 |
| "5k+ 怎么来的？" | 100 个 Python collector 自动跑，每周一轮；人工编辑可 PR 加新案例 |
| "跟 X 比有什么不同？" | 不和通用 LLM 失败案例比，专门 agent（tool-use / multi-agent / MCP）；结构化数据可 grep，可静态扫描 |
| "为什么不用向量检索？" | BM25 对短查询 + 关键词触发效果更好；每个 pitfall 长度 < 500 字，向量检索反而过拟合；后续可加 RAG 混合检索 |

---

## 2. Reddit r/ClaudeAI

**Title**：

```
I indexed 7,893 real AI agent failures into a skill you can call from Claude Code
```

**正文**：

```
Spent the last few months collecting postmortems — agent crashed,
context overflow, tool-call loops, API keys in logs, MCP server errors,
you name it. Each case has a verified symptom → root_cause → fix with
a source link.

Just shipped three Skills.sh SKILL.md files so it plugs straight into
Claude Code:

    npx skills add https://github.com/wiselinpm/agent-pitfalls-cn

Once installed, ask Claude things like:

  > "Why does my Claude Code session keep running out of context after
     the 4th tool call?"
  > "Scan my agent code for known antipatterns"
  > "What are the top critical pitfalls in the langchain category?"

The CLI itself (`agent-pitfalls search/list/check`) also works
standalone from any shell. 7,893 cases, 13 platforms, 13 categories,
MIT-licensed.

Repo: https://github.com/wiselinpm/agent-pitfalls-cn
HF-style search via the static site (5K+ pages, no JS hydration):
clone the repo, run `npm install && npm run dev`, open http://localhost:4321

PRs welcome — especially new collectors (we currently pull from ~100
sources but I'm sure there are subreddits / Discords / blogs I'm
missing).
```

---

## 3. Reddit r/LocalLLaMA

**Title**：

```
Cataloged 7,893 self-hosted / open-weight agent failures with symptom→fix entries
```

**正文**：

```
Quick dataset dump for anyone running local agents (Llama, Qwen,
Mistral, DeepSeek, etc.): I curate a corpus of documented AI agent
failures that hits the failure modes most relevant to open-weight
deployments:

  - Context overflow on long conversations (no infinite context window)
  - Tool-use loops when models don't pick stop_token properly
  - Cost-storm from runaway agents (relevant when you're paying per
    token, not per request)
  - Security: hardcoded API keys in agent prompts that get logged
  - MCP server errors with self-hosted backends

Stats:
- 7,893 cases, 2,838 marked critical
- 13 platforms including langchain, autogen, crewai, open-interpreter
- 13 categories including cost, reliability, security, sandbox

Queryable two ways:

1. CLI: `pip install agent-pitfalls && agent-pitfalls search "..."`
2. Static site with 5K+ pages — clone the repo, run `npm install && npm run dev`,
   open http://localhost:4321 (GitHub Pages deploy is currently being set up)

Repo: https://github.com/wiselinpm/agent-pitfalls-cn
```

---

## 4. Reddit r/MachineLearning

**Title**：

```
[D] A catalog of 7,893 AI agent failure cases with structured symptom→cause→fix entries
```

**正文**：

```
Sharing a dataset I've been building for the past few months:
**agent-pitfalls** — a curated catalog of AI agent failure postmortems
with a fixed schema (symptom / root_cause / fix / severity / platform /
category / source_url).

**Composition:**
- 7,893 records
- 13 platforms: claude-code, langchain, openai-agents, autogen,
  crewai, langgraph, cursor, aider, open-interpreter, claude-api,
  gemini-api, openai-api, generic
- 13 categories: context-window, cost, latency, memory, multi-agent,
  observability, prompt-injection, reliability, sandbox, security,
  state, streaming, tool-use
- 36% critical, 10% high, 52% medium, 2% low
- Sources: GitHub issues, HackerNews threads, arXiv papers, blog
  writeups, Zhihu case studies
- Each record is human-curated from a public source with a verified
  reference URL

**Schema** (per record):
```
title: str  # ≤120 chars
summary: str  # 10-300 chars
severity: enum  # critical|high|medium|low
platforms: list[enum]
categories: list[enum]
symptoms: list[str]
root_causes: list[str]
fixes: list[str]  # ≥1 entry, executable
references: list[{title, url}]  # ≥1 entry, URL must resolve
discovered_at: date
verified: bool
```

**Use cases I'm hoping the community explores:**
- Failure-mode classification / clustering
- Pre-deployment agent risk assessment
- Training data for self-debugging models
- Empirical study of which failure modes correlate with which platforms

**Access:**
- Static site (5K+ pages, no JS): clone the repo, `npm install && npm run dev` → http://localhost:4321
  (GitHub Pages deploy is currently being set up — see repo README for status)
- CLI with BM25 search: `pip install agent-pitfalls`
- Raw markdown corpus: https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/web/src/content/pitfalls
- 100+ collector scripts for re-running the pipeline: https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/collectors

**Limitations I'm aware of:**
- Source bias toward English-speaking communities (mitigated by Zhihu
  collector, still underrepresented)
- Severity is curator-assigned, not crowd-rated
- "Fixes" are verified by the curator that they exist, not by automated
  reproduction

Happy to answer questions about the collection methodology, schema
design choices, or to take PRs that add new collectors / new cases.
```

---

## 5. X / Twitter — Thread (5 tweets)

**Tweet 1/5**（hook）：

```
I collected 7,893 real AI agent failures into a searchable database.

Each one has:
• symptom
• root cause
• fix you can actually run
• source link to verify

Free, MIT, queryable from Claude Code / Codex / Cursor. 🧵
```

**Tweet 2/5**（mechanism）：

```
How the corpus gets built:

100+ Python collectors pull from GitHub issues, HN threads, arXiv,
blog postmortems, Zhihu.

Each hit gets normalized into a fixed schema, deduped by URL
fingerprint + title hash + Jaccard similarity, severity-tagged by
keyword rules.

Output: ~8k structured markdown records.
```

**Tweet 3/5**（usage）：

```
Three ways to query it:

1️⃣ CLI
   pip install agent-pitfalls
   agent-pitfalls search "context overflow"

2️⃣ Static scanner
   agent-pitfalls check ./src

3️⃣ Skills.sh skill
   npx skills add https://github.com/wiselinpm/agent-pitfalls-cn
```

**Tweet 4/5**（failure mode coverage）：

```
The 13 categories that show up most:

• tool-use (loops, bad args, unbounded output)
• context-window (overflow, drift, late-truncation)
• prompt-injection (direct, indirect, MCP-borne)
• cost (runaway agents, no max-tokens)
• security (API keys in logs, prompt leaks)
• reliability (no retries, no timeouts)
```

**Tweet 5/5**（CTA）：

```
If you're shipping agents, this is the postmortem library I wish
I'd had six months ago.

Repo: https://github.com/wiselinpm/agent-pitfalls-cn
(`npm install && npm run dev` for the 5K+ page static site)

PRs welcome — especially new collectors or new failure cases.
```

---

## 6. 一句话变体（用于 bio / 项目描述）

```
7,893 real AI agent failures, symptom → cause → fix, queryable from
Claude Code / Codex / Cursor / OpenCode / Gemini.
```

---

## 发布节奏建议

| 时间 | 平台 | 备注 |
|---|---|---|
| 周二上午美东 | HN | Show HN 流量最大 |
| 周三 | r/ClaudeAI | 用户最对口 |
| 周四 | r/LocalLLaMA | 错开 HN 热度 |
| 下周一 | r/MachineLearning | 学术向讨论质量高 |
| 同步 | X | 跨平台扩散 |

**关键**：每个平台都要用对应平台的语言。HN 是工程语言、Reddit r/ClaudeAI 是用户痛点语言、r/MachineLearning 是数据集语言。不要同一段话复制粘贴到三个平台。

---

## 数据校正提醒

README.md 和 CLAUDE.md 里都写 `5,561+ pitfalls`，实际是 **7,893**。已在本分支统一修订：
- `README.md` / `README.en.md` / `README.ja.md`：搜 `5,561` / `5561` / `5,500+` / `5,569`
- `CLAUDE.md`：`5K+` → `8K+` markdown 页面
- `plugin/.claude-plugin/plugin.json` / `plugin/codex/prompts.toml` / `agent_pitfalls_cli/README-CLI.md`
- `docs/UI-pages.md` / `docs/UI-components.md`：mockup 中的数字
- `skills/agent-pitfalls-search/SKILL.md`：`5,500+` → `7,893`
- `plugin/commands/pitfall.md`：`1/5561` → `1/7893`

放在单独的 commit：`docs: bump pitfall count to 7,893 + severity breakdown`。