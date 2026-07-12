"""中英文混合分词与同义词扩展。"""

from __future__ import annotations

import re
from typing import Iterable


# —— 平台别名 ——
PLATFORM_ALIASES: dict[str, tuple[str, ...]] = {
    "claude-code": ("claude code", "claudecode", "anthropic-cli", "@anthropic-ai/claude-code"),
    "openai-agents": ("openai agents", "openai-agents", "agents sdk", "oai-agents"),
    "langchain": ("langchain", "lang-chain", "langsmith"),
    "langgraph": ("langgraph", "lang-graph"),
    "autogen": ("autogen", "auto-gen", "auto gen"),
    "crewai": ("crewai", "crew ai", "crew-ai"),
    "open-interpreter": ("open interpreter", "open-interpreter", "openinterpreter"),
    "cursor": ("cursor", "cursor ide", "cursoride"),
    "aider": ("aider",),
    "devin": ("devin", "devin ai"),
    "claude-api": ("anthropic api", "claude api", "messages api", "anthropic sdk"),
    "openai-api": ("openai api", "openai-sdk", "chatgpt api", "responses api"),
    "gemini-api": ("gemini api", "google ai", "vertex ai", "gemini-sdk"),
    "generic": ("generic", "通用"),
}

# —— 类别同义词 ——
CATEGORY_ALIASES: dict[str, tuple[str, ...]] = {
    "context-window": ("上下文", "context", "token", "context window", "context length", "max_tokens"),
    "tool-use": ("工具调用", "tool call", "function calling", "tool use", "tool_use"),
    "streaming": ("流式", "stream", "sse", "websocket", "streaming"),
    "cost": ("成本", "cost", "billing", "expensive", "token price", "账单"),
    "security": ("安全", "security", "vulnerability", "cve", "漏洞"),
    "observability": ("可观测", "observability", "trace", "log", "telemetry", "monitor", "日志"),
    "memory": ("记忆", "memory", "vector store", "rag", "embeddings", "向量"),
    "multi-agent": ("多智能体", "multi-agent", "multi agent", "orchestr"),
    "prompt-injection": ("prompt注入", "prompt injection", "indirect injection", "tool poisoning", "jailbreak"),
    "sandbox": ("沙箱", "sandbox", "docker", "permission", "shell escape"),
    "reliability": ("可靠性", "retry", "transient", "flaky", "idempot"),
    "latency": ("延迟", "latency", "slow", "ttft"),
    "state": ("状态", "state", "checkpoint", "persistence"),
    "tokenization": ("分词", "tokeniz", "bpe", "encoding"),
}

# —— 症状/根因常见关键词同义词 ——
SYNONYMS: dict[str, tuple[str, ...]] = {
    "context": ("上下文", "context window", "token limit", "max tokens"),
    "loop": ("死循环", "infinite loop", "stuck", "recursion"),
    "leak": ("泄漏", "leak", "exposed", "verbose"),
    "injection": ("注入", "injection", "jailbreak", "bypass"),
    "crash": ("崩溃", "crash", "panic", "oom", "hang"),
    "timeout": ("超时", "timeout", "deadline"),
    "rate": ("限流", "rate limit", "429", "throttle"),
    "billing": ("账单", "cost", "billing", "expensive", "token price"),
    "deprecated": ("弃用", "deprecated", "deprecation", "migration"),
    "secret": ("密钥", "secret", "api key", "token", "credential"),
    "verbose": ("冗余", "verbose", "debug log", "日志"),
    "truncat": ("截断", "truncat", "cutoff", "cut off"),
}


_TOKEN_RE = re.compile(
    r"[A-Za-z][A-Za-z0-9_-]{1,}|[一-鿿]{2,}|\d+",
)


def tokenize(text: str) -> list[str]:
    """中英混合分词：小写化 + 中文字符按 2-字切分 + 英文/数字按词切分。"""
    if not text:
        return []
    text = text.lower()
    return [t for t in _TOKEN_RE.findall(text) if len(t) >= 2 or t.isdigit()]


def expand_query(tokens: Iterable[str]) -> list[str]:
    """用同义词扩展查询 token，用于召回。"""
    expanded: list[str] = []
    for tok in tokens:
        expanded.append(tok)
        # 平台别名
        for canon, aliases in PLATFORM_ALIASES.items():
            if tok in aliases or tok == canon:
                expanded.extend(aliases)
        # 类别别名
        for canon, aliases in CATEGORY_ALIASES.items():
            if tok in aliases or tok == canon:
                expanded.extend(aliases)
        # 通用同义词
        for canon, aliases in SYNONYMS.items():
            if tok == canon or tok in aliases:
                expanded.append(canon)
                expanded.extend(aliases)
    # 去重保序
    seen: set[str] = set()
    out: list[str] = []
    for t in expanded:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def detect_platforms(text: str) -> set[str]:
    """从查询文本中识别平台（返回 canonical 名）。"""
    t = (text or "").lower()
    hits: set[str] = set()
    for canon, aliases in PLATFORM_ALIASES.items():
        if any(a in t for a in aliases) or canon in t:
            hits.add(canon)
    return hits


def detect_categories(text: str) -> set[str]:
    """从查询文本中识别类别。"""
    t = (text or "").lower()
    hits: set[str] = set()
    for canon, aliases in CATEGORY_ALIASES.items():
        if any(a in t for a in aliases) or canon in t:
            hits.add(canon)
    return hits


def detect_severity(text: str) -> str | None:
    """从查询文本中识别严重度过滤。"""
    t = (text or "").lower()
    if any(k in t for k in ("critical", "严重", "高危", "致命", "崩溃")):
        return "critical"
    if any(k in t for k in ("high", "高", "重要", "broken", "故障")):
        return "high"
    if any(k in t for k in ("medium", "中", "warning", "警告")):
        return "medium"
    if any(k in t for k in ("low", "低", "minor", "typo", "小问题")):
        return "low"
    return None