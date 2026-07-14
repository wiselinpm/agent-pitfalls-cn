---
title: Potential TOCTOU race condition in _add_structure_metadata / _insert_structure_metadata
summary: '### Please read this first - **Have you read the docs?** [Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Yes, no existing issue covers the non-transactional insert+select pattern in `_add_structure_metadata` / `_inser'
severity: medium
platforms:
- openai-agents
- cursor
categories:
- streaming
- memory
symptoms:
- In `advanced_sqlite_session.py`, `_add_structure_metadata()` and `_insert_structure_metadata()` contain a TOCTOU race condition when resolving message IDs after insertion.
root_causes: []
fixes: []
references:
- title: Potential TOCTOU race condition in _add_structure_metadata / _insert_structure_metadata
  url: https://github.com/openai/openai-agents-python/issues/3817
  source: github:openai/openai-agents-python
tags:
- bug
contributor: liuchunyi-buaa
discovered_at: '2026-07-12'
verified: false
---

- [Potential TOCTOU race condition in _add_structure_metadata / _insert_structure_metadata](https://github.com/openai/openai-agents-python/issues/3817) — github:openai/openai-agents-python

## 摘要

### Please read this first

- **Have you read the docs?** [Agents SDK docs](https://openai.github.io/openai-agents-python/)
- **Have you searched for related issues?** Yes, no existing issue covers the non-transactional insert+select pattern in `_add_structure_metadata` / `_inser

_来源热度：1_
