"""规范化层：RawHit -> PitfallDraft，统一字段与 slug。

抽取规则（2026-07-14 升级）：
- 结构化 section：markdown `# Symptom/Fix/Root Cause` heading + list items
- Prose 模式：plain text 里捕捉"The fix is...", "Symptom: ...", "Root cause: ..." 引导短语
- Summary 回退：body 空时用 summary 的句法结构硬切
- 长度裁剪 + 噪声过滤（太短不要、太长不要、纯 URL 不要）
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from .base import RawHit
from .dedupe import url_fingerprint


SEVERITY_HINTS = {
    "critical": ("critical", "data loss", "security", "production", "rce", "leak", "vulnerability"),
    "high": ("high", "broken", "fails", "crash", "hang", "oom"),
    "medium": ("medium", "warning", "degrade", "slow", "rate"),
    "low": ("low", "typo", "cosmetic", "minor"),
}


PLATFORM_KEYWORDS = {
    "claude-code": ("claude code", "claude-code", "@anthropic-ai/claude-code"),
    "openai-agents": ("openai agents", "agents sdk", "openai-agents"),
    "langchain": ("langchain", "langsmith"),
    "langgraph": ("langgraph",),
    "autogen": ("autogen",),
    "crewai": ("crewai", "crew ai"),
    "open-interpreter": ("open interpreter", "open-interpreter"),
    "cursor": ("cursor",),
    "aider": ("aider",),
    "devin": ("devin",),
    "claude-api": ("anthropic api", "claude api", "messages api"),
    "openai-api": ("openai api", "chat completions", "responses api"),
    "gemini-api": ("gemini api", "google ai", "vertex ai"),
}


CATEGORY_KEYWORDS = {
    "context-window": ("context window", "context length", "token limit", "max_tokens"),
    "tool-use": ("tool call", "function calling", "tool use", "tool_use"),
    "streaming": ("stream", "sse", "websocket"),
    "cost": ("cost", "billing", "expensive", "token price"),
    "security": ("security", "vulnerability", "cve"),
    "observability": ("trace", "log", "telemetry", "observability", "monitor"),
    "memory": ("memory", "vector store", "rag", "embeddings"),
    "multi-agent": ("multi-agent", "multi agent", "orchestr"),
    "prompt-injection": ("prompt injection", "indirect injection", "tool poisoning", "jailbreak"),
    "sandbox": ("sandbox", "docker", "permission", "shell escape"),
    "reliability": ("retry", "transient", "flaky", "idempot"),
    "latency": ("latency", "slow", "ttft", "time to first"),
    "state": ("state", "checkpoint", "persistence"),
    "tokenization": ("tokeniz", "bpe", "encoding"),
}


# === 头部关键词（中英文）===
SYMPTOM_HEADERS = (
    "symptom", "issue", "problem", "what happened", "bug", "error", "repro",
    "症状", "现象", "问题", "复现",
)
ROOT_CAUSE_HEADERS = (
    "root cause", "cause", "why", "reason", "analysis",
    "根因", "原因", "分析",
)
FIX_HEADERS = (
    "fix", "solution", "workaround", "mitigation", "resolution", "how to fix", "suggested",
    "修复", "解决", "缓解", "建议",
)

# Prose 引导词（句首/句中）
_PROSE_SYMPTOM_RE = re.compile(
    r"(?i)(?:^|[\.\!\?\;\n]\s*)(?:symptom(?:s)?\s*[:：]|what happens?\s*[:：]|"
    r"the (?:bug|issue|problem) (?:is|was)\s*[:：]|"
    r"you(?:'ll| will) (?:see|notice|observe)\s+)([^\.。\?\!\;\n]+)",
)
_PROSE_FIX_RE = re.compile(
    r"(?i)(?:^|[\.\!\?\;\n]\s*)(?:fix(?:es)?\s*[:：]|solution\s*[:：]|workaround\s*[:：]|"
    r"to fix (?:this|the)\s*[:：,，]|"
    r"the fix is\s*[:：,，]|"
    r"resolved by\s+)([^\.。\?\!\;\n]+)",
)
_PROSE_CAUSE_RE = re.compile(
    r"(?i)(?:^|[\.\!\?\;\n]\s*)(?:root cause\s*[:：]|cause\s*[:：]|because\s+of\s+)([^\.。\?\!\;\n]+)",
)


@dataclass(frozen=True)
class PitfallDraft:
    """规范化后的待写入 Markdown 的草稿。"""

    slug: str
    title: str
    summary: str
    severity: str
    platforms: tuple[str, ...]
    categories: tuple[str, ...]
    symptoms: tuple[str, ...]
    root_causes: tuple[str, ...]
    fixes: tuple[str, ...]
    references: tuple[dict, ...]
    tags: tuple[str, ...]
    contributor: str | None
    discovered_at: str | None
    verified: bool
    score: int
    fingerprint: str


def _infer_severity(text: str) -> str:
    haystack = (text or "").lower()
    for level, hints in SEVERITY_HINTS.items():
        for h in hints:
            if h in haystack:
                return level
    return "medium"


def _infer_platforms(text: str) -> tuple[str, ...]:
    haystack = (text or "").lower()
    hits = [name for name, keys in PLATFORM_KEYWORDS.items() if any(k in haystack for k in keys)]
    return tuple(hits) or ("generic",)


def _infer_categories(text: str) -> tuple[str, ...]:
    haystack = (text or "").lower()
    hits = [name for name, keys in CATEGORY_KEYWORDS.items() if any(k in haystack for k in keys)]
    return tuple(hits[:3])


def _slugify(text: str) -> str:
    s = (text or "").lower()
    s = re.sub(r"[^a-z0-9一-鿿]+", "-", s)
    s = s.strip("-")
    return s[:80] or "untitled"


# === 抽取核心 ===

NOISE_PATTERNS = (
    re.compile(r"^https?://\S+$"),       # 纯 URL
    re.compile(r"^\s*[#>*\-]+\s*$"),     # 纯 markdown 符号
    re.compile(r"^(yes|no|maybe|n/a|todo)$", re.I),
)


def _clean(item: str) -> str | None:
    """过滤噪声项，返回清洗后的字符串或 None。"""
    if not item:
        return None
    item = item.strip().strip("-").strip("*").strip("`").strip()
    if not item:
        return None
    if any(p.match(item) for p in NOISE_PATTERNS):
        return None
    if len(item) < 8 or len(item) > 320:
        return None
    return item


def _dedup_keep_order(items: list[str]) -> tuple[str, ...]:
    seen = set()
    out = []
    for it in items:
        key = it.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return tuple(out)


def _extract_markdown_section(text: str, header_patterns: tuple[str, ...], max_items: int = 4) -> list[str]:
    """从 markdown body 抓某个标题下的列表项 / 段落。"""
    if not text:
        return []
    lines = text.splitlines()
    in_section = False
    items: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("#"):
            in_section = any(p.lower() in stripped.lower() for p in header_patterns)
            continue
        if not in_section:
            continue
        if stripped.startswith("```"):
            break  # 代码块结束
        if not stripped:
            continue
        m = re.match(r"^[-*]\s+(.+)$", stripped) or re.match(r"^\d+\.\s+(.+)$", stripped)
        if m:
            item = _clean(m.group(1))
            if item:
                items.append(item)
            if len(items) >= max_items:
                break
        elif not in_section:
            continue
        else:
            # 段落整段作为单条
            item = _clean(stripped)
            if item:
                items.append(item)
                break
    return items


def _extract_prose(text: str, pattern: re.Pattern[str], max_items: int = 2) -> list[str]:
    """从 plain text 用引导词匹配句子。"""
    if not text:
        return []
    items = []
    for m in pattern.finditer(text):
        item = _clean(m.group(1))
        if item:
            items.append(item)
        if len(items) >= max_items:
            break
    return items


def _extract_sentences_from_summary(summary: str, max_items: int = 1) -> list[str]:
    """Summary 是单段时，把它当作一个 symptom 描述。"""
    if not summary:
        return []
    item = _clean(summary.strip())
    return [item] if item and len(items := [item]) <= max_items else (items[:max_items] if item else [])


def _extract_body_structure(
    body: str,
    summary: str = "",
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """抽取 symptoms / root_causes / fixes。

    优先级（每类独立）：
      1. markdown 结构化 section
      2. prose 引导词模式
      3. summary 单句兜底（仅 symptoms/fixes）
    """
    symptoms = _extract_markdown_section(body or "", SYMPTOM_HEADERS, max_items=4)
    root_causes = _extract_markdown_section(body or "", ROOT_CAUSE_HEADERS, max_items=3)
    fixes = _extract_markdown_section(body or "", FIX_HEADERS, max_items=4)

    if not symptoms:
        symptoms = _extract_prose(body or "", _PROSE_SYMPTOM_RE, max_items=2)
    if not fixes:
        fixes = _extract_prose(body or "", _PROSE_FIX_RE, max_items=2)
    if not root_causes:
        root_causes = _extract_prose(body or "", _PROSE_CAUSE_RE, max_items=2)

    if not symptoms and summary:
        symptoms = _extract_sentences_from_summary(summary)
    if not fixes and summary:
        fixes = _extract_sentences_from_summary(summary)  # 兜底时和 symptom 共享标记，dedup 会处理

    return (
        _dedup_keep_order(symptoms)[:4],
        _dedup_keep_order(root_causes)[:3],
        _dedup_keep_order(fixes)[:4],
    )


def normalize(hit: RawHit) -> PitfallDraft:
    """单条 RawHit -> PitfallDraft。"""
    text = " ".join([hit.title, hit.summary, hit.body or ""])
    severity = _infer_severity(text)
    platforms = _infer_platforms(text)
    categories = _infer_categories(text)
    symptoms, root_causes, fixes = _extract_body_structure(hit.body or "", hit.summary or "")
    fp = url_fingerprint(hit.url)
    slug = f"{fp[:40]}-{_slugify(hit.title)[:40]}".strip("-")
    discovered = hit.published_at.date().isoformat() if hit.published_at else None
    return PitfallDraft(
        slug=slug,
        title=hit.title.strip()[:120],
        summary=(hit.summary or hit.title).strip()[:300],
        severity=severity,
        platforms=platforms,
        categories=categories,
        symptoms=symptoms,
        root_causes=root_causes,
        fixes=fixes,
        references=({"title": hit.title or hit.url, "url": hit.url, "source": hit.source},),
        tags=hit.tags,
        contributor=hit.author,
        discovered_at=discovered,
        verified=False,
        score=hit.score,
        fingerprint=fp,
    )