"""arXiv API 采集 — 抓 LLM agent 相关论文的标题/摘要。

注：arXiv 大部分是研究/方法论文，不是「坑」。这里只采集 title + abstract，
供 normalize 层判断是否包含 pitfall 关键词。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


QUERIES = [
    "LLM agent failure",
    "prompt injection attack",
    "tool use LLM failure",
    "LLM agent safety",
    "agent planning error",
    "RAG hallucination",
    "tool calling LLM vulnerability",
    "code generation LLM bug",
    "agent jailbreak",
    "indirect prompt injection",
    "agent benchmark failure",
    "agent security risk",
    "LLM reasoning failure",
    "chain of thought error",
    "agent hallucination",
    "factuality LLM",
    "agent evaluation challenge",
    "LLM alignment failure",
    "agent red team",
    "adversarial attack LLM",
    "tool use error",
    "function calling benchmark",
    "retrieval augmented generation failure",
    "RAG evaluation",
    "vector database pitfall",
    "embedding failure",
    "tokenizer bug",
    "context window overflow",
    "long context degradation",
    "LLM cost estimation",
    "inference latency",
    "agent cost optimization",
    "agent observability",
    "LLM monitoring",
    "agent reliability",
    "agent flaky behavior",
    "agent memory failure",
    "conversation memory limitation",
    "agent state persistence",
    "MCP protocol security",
]


class ArxivCollector:
    name = "arxiv"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            yield from _search(q)


def _search(q: str) -> Iterable[RawHit]:
    url = "http://export.arxiv.org/api/query"
    # 按时间倒序拉最新 15 篇，由 normalize 层过滤关键词
    try:
        raw = http_get(
            url,
            params={
                "search_query": f"all:{q}",
                "start": "0",
                "max_results": "15",
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
        author_el = entry.find("a:author/a:name", ns)
        author = author_el.text.strip() if author_el is not None and author_el.text else None
        pub = entry.findtext("a:published", namespaces=ns)
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        if not (title and link):
            continue
        # 缩略摘要
        clean = re.sub(r"\s+", " ", summary)
        yield RawHit(
            title=title,
            url=link,
            source=f"arxiv:q:{q}",
            summary=clean[:280],
            body=clean,
            author=author,
            published_at=dt,
            tags=(q,),
        )