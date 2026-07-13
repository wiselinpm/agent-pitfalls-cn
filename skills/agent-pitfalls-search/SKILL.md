---
name: agent-pitfalls-search
description: Search a curated knowledge base of 5,500+ real-world AI agent failures (Claude Code, Codex, Cursor, LangChain, OpenAI Agents, MCP, RAG, etc.) for symptoms, root causes, and fixes. Use when debugging agent crashes, context-window overflow, tool-call loops, prompt injection, API key leaks in logs, broken retries, hallucinated function arguments, or any "why is my LLM agent doing X?" question. Triggers on phrases like "agent crashed", "context overflow", "tool use failed", "agent looping", "API key leaked", "prompt injection", "MCP server error", "RAG returns wrong", or when reviewing/refactoring agent code.
license: MIT
metadata:
  author: wiselinpm
  version: "1.0.0"
  argument-hint: "<search-query>"
---

# Agent Pitfalls Search

Search the `agent-pitfalls` corpus for known failures and fixes. The corpus is built from GitHub issues, HackerNews threads, arXiv papers, blog postmortems, and Zhihu case studies, each normalized into a structured `symptom → root_cause → fix` record with severity, platform, and category tags.

## When to Apply

Use this skill when the user is:

- Debugging an LLM agent failure and wants a **known case** to compare against
- Reviewing agent code and asking "is there a documented antipattern for this?"
- Answering "why is my agent doing X?" with real-world cases instead of guessing
- Looking for the canonical fix for a recurring error (rate-limit storms, recursive tool calls, broken streaming, etc.)
- Doing incident postmortems and needs reference architecture for what *not* to do

Do **not** use this skill for:

- Generic "how do I write an agent?" tutorials (use framework docs instead)
- Live debugging of running processes (this skill reads a static corpus)
- Issues unrelated to LLM-based autonomous agents

## Prerequisites

Install the `agent-pitfalls` CLI once per machine:

```bash
pip install agent-pitfalls
# or
npm i -g agent-pitfalls
```

Verify with `agent-pitfalls --version`. If installation is not possible in the current sandbox, fall back to `npx agent-pitfalls search "..."` per call.

## Steps

1. Run the search with the user's query, preserving any platform/category/severity constraints they mentioned:

   ```bash
   agent-pitfalls search "<query>" --no-color
   ```

   Common flags worth passing through when the user names them:

   - `--platform claude-code,langchain` — filter to one or more platforms (comma-separated)
   - `--category context-window` — narrow to a category (see `agent-pitfalls categories`)
   - `--severity critical|high|medium|low` — restrict by severity

2. Read the top 1–3 hits. Each hit includes:

   - **title** + **severity** + **score**
   - detected **platforms** / **categories**
   - which fields matched (title / summary / symptoms)
   - one-line excerpt of the most relevant symptom or fix
   - **slug** (stable reference, e.g. `claude-code-context-overflow-2024-08`)
   - source **reference URL**

3. For full context on a hit (all symptoms / root causes / fixes / verified status), fetch it:

   ```bash
   agent-pitfalls show <slug>
   # or, if the local HTTP server is running:
   curl http://localhost:8765/pitfall/<slug>
   ```

4. Synthesize the answer for the user:

   - Lead with the **root cause** the case points to
   - Quote the **fix** verbatim when the user is about to apply it
   - Cite the **slug** and **reference URL** so the user can verify
   - If multiple hits disagree, surface the conflict explicitly rather than picking one

## Output Format

Present results as a short list, not a wall of text. Recommended layout:

```
1. <title>  [<severity>]  score=...
   Why it matches: <one-line>
   Root cause: <one sentence>
   Fix: <one sentence or short snippet>
   Ref: <reference URL>
   slug: <slug>
```

When `--platform` or `--category` were detected from the query, mention them so the user knows the corpus was filtered, e.g.:

```
🔍 3/5561 matches for "context overflow"
   detected: platforms=[claude-code] categories=[context-window]
```

## Quality Rules

- **Do not invent slugs.** Only cite slugs that appear in the CLI output.
- **Prefer `critical` and `high` severity** hits first when the user is debugging a live issue.
- **Cross-check at least two hits** when the user is making an architectural decision, not just one.
- **Surface conflicting fixes honestly** — if one case recommends timeouts and another recommends retries, say so.

## Related Skills

- `agent-pitfalls-check` — static-scan a project for these patterns before they hit production
- `agent-pitfalls-list` — browse the corpus by platform/category/severity (training material, audit prep)