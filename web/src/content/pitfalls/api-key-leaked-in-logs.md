---
title: Agent 调试日志意外打印 API Key / 用户隐私
summary: 在把 LangChain / OpenAI Agents SDK 的 verbose 模式打开后，完整的 prompt（含 system message 里的密钥、用户 PII）会被打印到 stdout 或写入日志文件，导致安全事故。
severity: critical
platforms: ['langchain', 'openai-agents', 'generic']
categories: [security, observability]
symptoms:
  - '日志文件里出现 `sk-proj-...` 或用户邮箱/手机号'
  - CI 把 prompt 上传到日志聚合服务（Sentry/Datadog）
  - 团队成员通过截图分享「调试输出」时泄漏
root_causes:
  - '`verbose=True` / `debug=True` 默认打印所有 LLM 输入输出'
  - prompt 模板里硬编码了密钥或从环境变量注入但仍会被序列化
  - 结构化日志框架（structlog/loguru）默认不脱敏
fixes:
  - 永远不在 prompt 模板里硬编码密钥；从外部 secret manager 注入
  - '实现 `RedactingFilter` 拦截 `sk-`、`Bearer `、邮箱等模式'
  - '生产环境关闭 verbose，调试时用 `dry_run` 模式只打摘要'
  - 团队规范：调试输出截图前必须先 grep 密钥
references:
  - title: LangChain Debugging 与日志
    url: https://python.langchain.com/docs/how_to/debugging/
    source: LangChain Docs
  - title: Sentry data scrubbing
    url: https://docs.sentry.io/platforms/python/data-management/sensitive-data/
    source: Sentry
contributor: agent-pitfalls-bot
discovered_at: 2025-10-01
verified: true
---

## 推荐的 Redacting Filter

```python
import re, logging

_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "[REDACTED_KEY]"),
    (re.compile(r"Bearers+[A-Za-z0-9._-]+"), "Bearer [REDACTED]"),
    (re.compile(r"[w.+-]+@[w-]+.[w.-]+"), "[REDACTED_EMAIL]"),
]

class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pat, repl in _PATTERNS:
            msg = pat.sub(repl, msg)
        record.msg = msg
        record.args = ()
        return True
```