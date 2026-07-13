---
name: agent-pitfalls-list
description: Browse and export the curated AI-agent pitfalls knowledge base by platform, category, and severity. Use when preparing training material, building a checklist for an audit, populating a Notion/Confluence page, generating a CSV of known risks, surveying "what goes wrong with LangChain / Claude Code / MCP / RAG", or asking "show me all critical issues in category X". Triggers on phrases like "list pitfalls", "show all failures for", "audit checklist", "training material", "export to CSV", "what platforms are covered", "what categories exist".
license: MIT
metadata:
  author: wiselinpm
  version: "1.0.0"
  argument-hint: "[--platform X] [--category Y] [--severity Z] [--limit N]"
---

# Agent Pitfalls List

Bulk-browse the `agent-pitfalls` corpus by structured filters. Unlike `search`, this skill returns matching records by metadata (platform, category, severity) rather than by free-text relevance.

## When to Apply

Use this skill when the user wants to:

- Survey what the corpus covers (`platforms`, `categories`, counts)
- Build a **checklist** for a security review, architecture review, or PR template
- Prepare **training material** or onboarding docs for a team building agents
- Export subsets as **JSON / CSV** for downstream tooling
- Get a full inventory of `critical`-severity issues in a specific category (e.g. all prompt-injection CVEs)
- Compare failure modes across platforms ("what breaks in LangChain vs OpenAI Agents")

Do **not** use this skill for:

- A specific debugging question — use `agent-pitfalls-search` instead
- Live code review — use `agent-pitfalls-check` instead
- Reading the full text of one record — pipe the slug into `agent-pitfalls show`

## Prerequisites

Install the `agent-pitfalls` CLI once per machine:

```bash
pip install agent-pitfalls
# or
npm i -g agent-pitfalls
```

Verify with `agent-pitfalls --version`.

## Steps

1. If the user has not specified filters, start by listing the available axes:

   ```bash
   agent-pitfalls platforms --no-color
   agent-pitfalls categories --no-color
   ```

   These return counts so the user can pick the right scope.

2. Run the filtered list:

   ```bash
   agent-pitfalls list \
     --platform <p1,p2,...> \
     --category <c1,c2,...> \
     --severity <critical|high|medium|low> \
     --limit <N> \
     --no-color
   ```

   Filter behavior:

   - Filters **AND** together across types, **OR** within a single type (comma-separated)
   - `--limit` defaults to a sensible value; override when scanning many records
   - Without `--json`, output is human-readable; with `--json`, output is one record per line for piping into `jq`

3. For machine-readable export:

   ```bash
   agent-pitfalls list --platform langchain --severity critical --json | jq -r '.[] | "\(.slug)\t\(.severity)\t\(.title)"'
   ```

4. To read the full text of any record returned by `list`, follow up with:

   ```bash
   agent-pitfalls show <slug>
   ```

## Output Format

Human-readable output looks like:

```
● <slug>  [<severity>]  <title>
  platforms: [...]
  categories: [...]
  discovered_at: <YYYY-MM-DD>
```

For audit prep, recommend grouping by `severity` (critical first) and within severity by `category`. For training material, recommend grouping by `category` so each section teaches one failure mode.

When exporting, default to TSV (tab-separated) so it pastes cleanly into spreadsheets:

```bash
agent-pitfalls list --json | jq -r '.[] | [.slug, .severity, .title, (.platforms | join("|")), (.categories | join("|"))] | @tsv'
```

## Quality Rules

- **Always show counts before listing.** The user needs to know "there are 247 LangChain pitfalls" before deciding whether to filter further.
- **Never dump the full corpus unfiltered.** Even a `head` view of thousands of records is unhelpful — push the user toward a filter.
- **For audits, default to `critical` only.** A 50-item critical list is actionable; a 5,500-item full list is noise.

## Related Skills

- `agent-pitfalls-search` — fuzzy-search by symptom / free text
- `agent-pitfalls-check` — static-scan a project to find which of these pitfalls apply