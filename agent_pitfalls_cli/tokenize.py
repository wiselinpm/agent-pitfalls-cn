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
# 只展开「agent 开发」语境下的同义词，避免 "死循环" → "loop" → ImageMagick
SYNONYMS: dict[str, tuple[str, ...]] = {
    "context": ("上下文", "context window", "token limit", "max tokens"),
    "loop": ("死循环", "infinite loop", "recursion limit", "agent loop"),
    "leak": ("泄漏", "leak", "exposed", "secret leak"),
    "injection": ("注入", "prompt injection", "jailbreak", "indirect injection"),
    "crash": ("崩溃", "crash", "oom", "out of memory"),
    "timeout": ("超时", "timeout", "streaming timeout"),
    "rate": ("限流", "rate limit", "429", "retry backoff"),
    "billing": ("账单", "token cost", "billing", "cost runaway"),
    "deprecated": ("弃用", "deprecated", "migration"),
    "secret": ("密钥", "api key", "secret", "credential leak"),
    "verbose": ("冗余", "verbose logging", "debug log"),
    "truncat": ("截断", "truncation", "context truncation"),
    "overflow": ("溢出", "overflow", "context overflow", "token overflow"),
    "tool": ("工具", "tool call", "function calling", "tool use"),
    "memory": ("记忆", "memory leak", "context memory", "rag"),
    "prompt": ("提示词", "prompt", "system prompt", "prompt engineering"),
    "agent": ("智能体", "agent", "multi-agent", "agent loop"),
    "token": ("令牌", "token", "tokenization", "token limit"),
    "embed": ("嵌入", "embedding", "vector", "vector store"),
    "hallucinate": ("幻觉", "hallucination", "rag hallucination"),
}

# —— 中文→英文反向映射 ——
# 当用户输入纯中文时，自动补充对应的英文术语
CN_TO_EN: dict[str, tuple[str, ...]] = {
    "上下文": ("context", "context window", "token limit"),
    "溢出": ("overflow", "truncation"),
    "截断": ("truncation", "cutoff"),
    "泄漏": ("leak", "exposed"),
    "密钥": ("api key", "secret", "credential"),
    "注入": ("injection", "jailbreak"),
    "死循环": ("infinite loop", "recursion limit", "agent loop"),
    "崩溃": ("crash", "oom", "panic"),
    "超时": ("timeout", "deadline"),
    "限流": ("rate limit", "429", "throttle"),
    "账单": ("cost", "billing", "token cost"),
    "弃用": ("deprecated", "migration"),
    "沙箱": ("sandbox", "docker", "permission"),
    "幻觉": ("hallucination", "rag"),
    "嵌入": ("embedding", "vector"),
    "工具": ("tool call", "function calling"),
    "智能体": ("agent", "multi-agent"),
    "令牌": ("token", "tokenization"),
    "记忆": ("memory", "rag", "vector store"),
    "提示词": ("prompt", "system prompt"),
    "冗余": ("verbose", "debug log"),
    "安全": ("security", "vulnerability"),
    "可靠性": ("retry", "flaky", "idempotent"),
    "延迟": ("latency", "slow", "ttft"),
    "状态": ("state", "checkpoint"),
}


_TOKEN_RE = re.compile(
    r"[A-Za-z][A-Za-z0-9_-]{1,}|[一-鿿]+|\d+",
)

# 已知的中文复合词（优先匹配）
_CN_COMPOUND_RE = re.compile(
    "|".join(re.escape(k) for k in sorted(CN_TO_EN.keys(), key=len, reverse=True))
)


def tokenize(text: str) -> list[str]:
    """中英混合分词：小写化 + 中文按已知复合词切分 + 英文/数字按词切分。"""
    if not text:
        return []
    text = text.lower()
    tokens: list[str] = []
    # 先提取英文和数字
    en_parts = _TOKEN_RE.findall(text)
    # 对中文部分做复合词切分
    cn_text = re.sub(r"[A-Za-z0-9_ -]+", " ", text)
    for seg in cn_text.split():
        if not seg:
            continue
        # 尝试匹配已知复合词
        pos = 0
        matched = False
        for m in _CN_COMPOUND_RE.finditer(seg):
            if m.start() > pos:
                # 中间未匹配的中文字符，2字一组切分
                mid = seg[pos:m.start()]
                for i in range(0, len(mid), 2):
                    chunk = mid[i:i+2]
                    if len(chunk) >= 2:
                        tokens.append(chunk)
            tokens.append(m.group())
            pos = m.end()
            matched = True
        if pos < len(seg):
            mid = seg[pos:]
            for i in range(0, len(mid), 2):
                chunk = mid[i:i+2]
                if len(chunk) >= 2:
                    tokens.append(chunk)
        elif not matched:
            # 整段未匹配，2字一组
            for i in range(0, len(seg), 2):
                chunk = seg[i:i+2]
                if len(chunk) >= 2:
                    tokens.append(chunk)
    # 合并英文 token
    for t in en_parts:
        t = t.lower()
        if len(t) >= 2 or t.isdigit():
            tokens.append(t)
    return tokens


def expand_query(tokens: Iterable[str]) -> list[str]:
    """用同义词扩展查询 token，用于召回。"""
    expanded: list[str] = []
    for tok in tokens:
        expanded.append(tok)
        # 中文→英文反向映射（优先，解决纯中文查询问题）
        for cn, en_terms in CN_TO_EN.items():
            if tok == cn:
                expanded.extend(en_terms)
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