---
title: "Incorrect model was used?"
summary: '### Please read this first - **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Others may have faced similar issues. ### Describe the bug 1. I copied the code of https://github.com/openai/ope'
severity: high
platforms:
- openai-agents
categories:
- streaming
- memory
- sandbox
symptoms:
- I copied the code of https://github.com/openai/openai-agents-python/blob/main/examples/sandbox/memory.py
- Run with one change `DEFAULT_MODEL = "gpt-5.4-mini"`
- The first phase was indeed gpt-5.4-mini but all turns of second phase is gpt-5.5
- <img width="1444" height="364" alt="Image" src="https://github.com/user-attachments/assets/49308112-9877-4f07-ac56-72e6a3a5c96f" />
root_causes: []
fixes: []
references:
- title: Incorrect model was used?
  url: https://github.com/openai/openai-agents-python/issues/3703
  source: github:openai/openai-agents-python
tags:
- bug
contributor: johnsyin-nextbe
discovered_at: '2026-06-29'
verified: false
---

- [Incorrect model was used?](https://github.com/openai/openai-agents-python/issues/3703) — github:openai/openai-agents-python

## 摘要

### Please read this first - **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Others may have faced similar issues. ### Describe the bug 1. I copied the code of https://github.com/openai/ope
