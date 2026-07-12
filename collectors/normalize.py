"""规范化层：RawHit -> PitfallDraft，统一字段与 slug。"""

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


# === 结构化抽取：从 markdown body 里抓 sections ===

SYMPTOM_HEADERS = ("symptom", "issue", "problem", "what happened", "bug", "error", "repro")
ROOT_CAUSE_HEADERS = ("root cause", "cause", "why", "reason", "analysis")
FIX_HEADERS = ("fix", "solution", "workaround", "mitigation", "resolution", "how to fix", "suggested")


def _extract_section_items(text: str, header_patterns: tuple[str, ...], max_items: int = 4) -> tuple[str, ...]:
    """从 markdown body 抓某个标题下的列表项。"""
    if not text:
        return ()
    lines = text.splitlines()
    in_section = False
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            in_section = any(p.lower() in stripped.lower() for p in header_patterns)
            continue
        if in_section:
            if stripped.startswith("```"):
                break
            m = re.match(r"^[-*]\s+(.+)$", stripped) or re.match(r"^\d+\.\s+(.+)$", stripped)
            if m:
                item = m.group(1).strip()
                if 6 <= len(item) <= 240:
                    items.append(item)
                    if len(items) >= max_items:
                        break
            elif not stripped:
                continue
            else:
                # 非列表行：作为段落整段收集一次
                if 20 <= len(stripped) <= 240 and len(items) < max_items:
                    items.append(stripped)
                    break
    return tuple(items)


def _extract_body_structure(body: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    symptoms = _extract_section_items(body, SYMPTOM_HEADERS, max_items=4)
    root_causes = _extract_section_items(body, ROOT_CAUSE_HEADERS, max_items=3)
    fixes = _extract_section_items(body, FIX_HEADERS, max_items=4)
    return symptoms, root_causes, fixes


def normalize(hit: RawHit) -> PitfallDraft:
    """单条 RawHit -> PitfallDraft。"""
    text = " ".join([hit.title, hit.summary, hit.body])
    severity = _infer_severity(text)
    platforms = _infer_platforms(text)
    categories = _infer_categories(text)
    symptoms, root_causes, fixes = _extract_body_structure(hit.body or "")
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