---
title: OpenAIConversationsSession persists empty reasoning item {"type":"reasoning","summary":[]} and Conversations API rejects
summary: '### Please read this first - **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/) - **Have you searched for related issues?** Others may have faced similar issues. Body: ```md ## Summary When using `OpenAIConversationsSession` with: -'
severity: low
platforms:
- openai-agents
categories:
- streaming
- observability
- reliability
symptoms:
- This reproduces even without attachments or file search. A simple conversational prompt is enough.
root_causes:
- This happens inside the `OpenAIConversationsSession` persistence path when saving run results back into the conversation store.
fixes: []
references:
- title: OpenAIConversationsSession persists empty reasoning item {"type":"reasoning","summary":[]} and Conversations API rejects it as invalid
  url: https://github.com/openai/openai-agents-python/issues/3268
  source: github:openai/openai-agents-python
tags:
- bug
- feature:sessions
contributor: Hassan90785
discovered_at: '2026-05-08'
verified: false
---

- [OpenAIConversationsSession persists empty reasoning item {"type":"reasoning","summary":[]} and Conversations API rejects it as invalid](https://github.com/openai/openai-agents-python/issues/3268) — github:openai/openai-agents-python

## 摘要

### Please read this first

- **Have you read the docs?**[Agents SDK docs](https://openai.github.io/openai-agents-python/)
- **Have you searched for related issues?** Others may have faced similar issues.


Body:

```md
## Summary

When using `OpenAIConversationsSession` with:

-

_来源热度：1_
