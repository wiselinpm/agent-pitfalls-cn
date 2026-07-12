"""arXiv 改进版 — 更精准的关键词密度过滤。

原 arxiv.py 用几个宽泛 query 命中很多噪声论文。本 collector 加上「失败/漏洞/
安全」关键词的密度评分，只保留确实在讨论失败/缺陷/安全/可解释性的论文。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


# 关键词分组
FAILURE_KEYWORDS = (
    "failure", "fails", "fail", "bug", "broken", "crash", "vulnerability",
    "exploit", "attack", "injection", "jailbreak", "leak", "leakage",
    "robustness", "adversarial", "hallucin", "incorrect", "misleading",
    "deprecat", "deprecated", "breaking", "regression", "issue",
)
METHOD_KEYWORDS = (
    "agent", "llm", "language model", "tool use", "function calling",
    "rag", "retrieval", "prompt", "reasoning", "planning",
)

QUERIES = [
    "LLM agent safety",
    "prompt injection attack",
    "tool use LLM failure",
    "jailbreak large language model",
    "RAG hallucination",
    "agent planning error",
    "LLM tool calling vulnerability",
    "code generation LLM bug",
    "agent jailbreak",
    "indirect prompt injection",
    "agent red team",
    "LLM alignment failure",
    "tool poisoning",
    "agent memory leak",
    "vector embedding pitfall",
    "agent context overflow",
    "LLM rate limit",
    "inference cost optimization",
    "MCP protocol vulnerability",
    "agent data leakage",
    "model inversion attack",
    "membership inference",
    "adversarial example LLM",
    "backdoor LLM",
    "agent reward hacking",
    "LLM safety alignment",
    "agent benchmark contamination",
    "LLM benchmark bias",
    "agent hallucination rate",
    "LLM factuality error",
]


class ArxivV2Collector:
    name = "arxiv-v2"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            yield from _search(q)


def _search(q: str) -> Iterable[RawHit]:
    url = "http://export.arxiv.org/api/query"
    # 更宽松：max_results=25，按时间倒序，让 normalize 层过滤
    try:
        raw = http_get(
            url,
            params={
                "search_query": f"all:{q}",
                "start": "0",
                "max_results": "25",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            },
            timeout=30,
        )
    except Exception:
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", namespaces=ns) or "").strip()
        link_el = entry.find("a:id", ns)
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        summary = (entry.findtext("a:summary", namespaces=ns) or "").strip()
        if not (title and link):
            continue
        text = (title + " " + summary).lower()
        # 至少 1 个 failure keyword + 1 个 method keyword
        has_fail = any(k in text for k in FAILURE_KEYWORDS)
        has_method = any(k in text for k in METHOD_KEYWORDS)
        if not (has_fail and has_method):
            continue
        clean = re.sub(r"\s+", " ", summary)
        score = sum(1 for k in FAILURE_KEYWORDS if k in text)
        author_el = entry.find("a:author/a:name", ns)
        author = author_el.text.strip() if author_el is not None and author_el.text else None
        pub = entry.findtext("a:published", namespaces=ns)
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        yield RawHit(
            title=title,
            url=link,
            source=f"arxiv-v2:q:{q}",
            summary=clean[:280],
            body=clean,
            author=author,
            published_at=dt,
            score=score,
            tags=(q,),
        )