---
title: OpenAIConversationsSession strips required id from file_search_call before conversations.items.create, causing 400 missi
summary: '### Please read this first - **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Others may have faced similar issues. I can’t post to GitHub from here, but I’ve got a ready-to-file issue. Iss'
severity: high
platforms:
- openai-agents
- langchain
categories:
- streaming
- observability
- state
symptoms:
- Create an agent with hosted `file_search`
- Use `OpenAIConversationsSession`
- Upload/index a file
- Ask a question that triggers `file_search`
root_causes:
- 'I traced the persistence path in `openai-agents==0.15.2`:'
fixes:
- I worked around this on the app side by wrapping `OpenAIConversationsSession.add_items(...)` and filtering/dropping invalid items so the rest of the turn can still persist, but that is only a mitigation.
references:
- title: OpenAIConversationsSession strips required id from file_search_call before conversations.items.create, causing 400 missing items[0].id
  url: https://github.com/openai/openai-agents-python/issues/3267
  source: github:openai/openai-agents-python
tags:
- bug
- feature:sessions
contributor: Hassan90785
discovered_at: '2026-05-08'
verified: false
---

- [OpenAIConversationsSession strips required id from file_search_call before conversations.items.create, causing 400 missing items[0].id](https://github.com/openai/openai-agents-python/issues/3267) — github:openai/openai-agents-python

## 摘要

### Please read this first

- **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/)
- **Have you searched for related issues?** Others may have faced similar issues.
I can’t post to GitHub from here, but I’ve got a ready-to-file issue.


Iss

_来源热度：1_
