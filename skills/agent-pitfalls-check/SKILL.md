---
name: agent-pitfalls-check
description: Statically scan a project directory for known AI-agent antipatterns (hardcoded API keys, missing max-iterations, no rate-limit retries, system-prompt drift, unbounded tool output, missing tool-call timeouts, unvalidated MCP inputs, etc.) and link each finding back to a documented real-world failure. Use when reviewing agent code before a PR, running pre-commit checks, setting up CI gates, onboarding a new contributor, or auditing an existing agent codebase. Triggers on phrases like "check this project", "scan for agent issues", "review my agent code", "any antipatterns here", "before I push", "audit my agent", "CI check for agent pitfalls".
license: MIT
metadata:
  author: wiselinpm
  version: "1.0.0"
  argument-hint: "[path] (default: current directory)"
---

# Agent Pitfalls Check

Static-analysis pass over a project tree. Each finding is matched against the `agent-pitfalls` corpus so the user gets **a rule id + a real-world case**, not a generic lint warning.

## When to Apply

Use this skill when the user is:

- Pushing a PR and wants a final sanity check on agent code
- Wiring up **CI** to gate merges on agent antipatterns
- Onboarding a new contributor and wants a baseline pass
- Auditing an existing agent codebase before a redesign
- Doing a code-review pass on agent code and wants concrete case citations to put in the PR comment

Do **not** use this skill for:

- A specific bug ("why does my agent crash on X?") — use `agent-pitfalls-search` instead
- Browsing the corpus without a project to scan — use `agent-pitfalls-list` instead
- Runtime debugging — this skill does **not** execute the agent

## Prerequisites

Install the `agent-pitfalls` CLI once per machine:

```bash
pip install agent-pitfalls
# or
npm i -g agent-pitfalls
```

Verify with `agent-pitfalls --version`.

## Steps

1. Run the scan against the path the user gave (default to current directory):

   ```bash
   agent-pitfalls check <path> --no-color
   ```

   Useful flags:

   - `--json` — emit machine-readable output for CI parsing
   - `--severity <min>` — fail only on `critical`/`high` etc.
   - omit `--no-color` when piping to a file

2. Each finding has the shape:

   ```
   ● <rule_id> — <rule title>
     <file>:<line>
     > <matched source line>

       → <related pitfall title>
         <slug>  [<severity>]
         ref: <url>
   ```

3. Triage by severity:

   - `critical` / `high` — block the PR / merge; ask the user to fix before proceeding
   - `medium` — file as follow-up issues
   - `low` — note but don't block

4. When a finding's **related pitfall** is unfamiliar, drill down:

   ```bash
   agent-pitfalls show <slug>
   ```

   Use the **fix** field from that record verbatim in the PR comment.

5. For CI integration, prefer JSON output and fail on non-zero findings:

   ```bash
   # .github/workflows/agent-pitfalls.yml (sketch)
   - run: pip install agent-pitfalls
   - run: agent-pitfalls check . --json --severity high > report.json
   - uses: actions/upload-artifact@v4
     with: { name: agent-pitfalls-report, path: report.json }
   ```

## Output Format

Human-readable output is grouped by file and severity. Summarize before pasting the raw output:

```
Found 12 issues in 7 files (3 critical, 4 high, 5 medium).

Top priorities:
1. src/agent.py:42  [critical]  hardcoded API key in source
   → "API key leaked in logs" (api-key-leaked-in-logs, critical)
   Fix: move to env var; see https://...

2. src/tools/search.py:88  [high]  unbounded tool output
   → "Tool output buffer overflow" (tool-output-overflow, high)
   Fix: cap output at 8k tokens before returning to LLM
```

For CI, parse JSON and emit a summary table; do not print thousands of lines of source matches to the GitHub Actions log.

## Quality Rules

- **Always link findings to a pitfall slug.** A bare rule id without a real-world case is just lint.
- **Cap the report.** If the scan returns hundreds of findings, group by file and only show top 5 per file by default.
- **Suggest fixes verbatim** from the linked pitfall record, not paraphrased. The user came for the canonical answer.
- **Don't reformat the user's source.** Quote the matched line as-is so the user can grep for it later.

## Related Skills

- `agent-pitfalls-search` — free-text search when a scan surfaces an unfamiliar error
- `agent-pitfalls-list` — browse the rule catalog before writing custom scan policies