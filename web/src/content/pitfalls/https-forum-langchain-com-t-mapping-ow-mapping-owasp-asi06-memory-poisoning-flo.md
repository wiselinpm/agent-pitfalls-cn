---
title: Mapping OWASP ASI06 (memory poisoning) flows in a LangGraph email agent — what I found
summary: I’ve been building a static, repo-level scanner for OWASP ASI06 (memory &amp; context poisoning) in agent code, and I wanted to test it against a real LangGraph agent rather than my own. I ran it on a small public LangGraph email assistant and it flagged a textbook poisoning flow
severity: critical
platforms:
- claude-code
- langgraph
categories:
- streaming
- security
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: Mapping OWASP ASI06 (memory poisoning) flows in a LangGraph email agent — what I found
  url: https://forum.langchain.com/t/mapping-owasp-asi06-memory-poisoning-flows-in-a-langgraph-email-agent-what-i-found/4079
  source: langchain-forum
tags:
- forum
- langchain-forum
discovered_at: '2026-07-02'
verified: false
---

- [Mapping OWASP ASI06 (memory poisoning) flows in a LangGraph email agent — what I found](https://forum.langchain.com/t/mapping-owasp-asi06-memory-poisoning-flows-in-a-langgraph-email-agent-what-i-found/4079) — langchain-forum

## 摘要

I’ve been building a static, repo-level scanner for OWASP ASI06 (memory &amp; context poisoning) in agent code, and I wanted to test it against a real LangGraph agent rather than my own. I ran it on a small public LangGraph email assistant and it flagged a textbook poisoning flow
