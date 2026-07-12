"""ProductHunt 采集 — 公开 Atom feed。

跟踪 agent 相关新发布的产品，从 description 抓摘要。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEED = "https://www.producthunt.com/feed"
ATOM = "{http://www.w3.org/2005/Atom}"

# 关键词 — 过滤 AI/agent 相关产品
KEYWORDS = (
    "agent", "ai ", "ai-", "llm", "gpt", "claude", "openai",
    "anthropic", "langchain", "langgraph", "rag", "prompt",
    "chatbot", "copilot", "automation", "no-code", "workflow",
    "chatgpt", "deepseek", "gemini", "mistral", "perplexity",
    "vector", "embedding", "stable diffusion",
)


class ProductHuntCollector:
    name = "producthunt"

    def collect(self) -> Iterable[RawHit]:
        try:
            raw = http_get(FEED)
        except Exception:
            return
        try:
            root = ET.fromstring(raw)
        except ET.ParseError:
            return

        for entry in root.findall(f"{ATOM}entry"):
            hit = _atom_to_hit(entry)
            if hit:
                yield hit


def _atom_to_hit(entry) -> RawHit | None:
    title = (entry.findtext(f"{ATOM}title") or "").strip()
    if not title:
        return None
    haystack = title.lower()
    if not any(k in haystack for k in KEYWORDS):
        return None

    link = ""
    for link_el in entry.findall(f"{ATOM}link"):
        href = link_el.get("href") or ""
        if link_el.get("rel") in (None, "alternate") and href:
            link = href.strip()
            break

    summary = (entry.findtext(f"{ATOM}summary") or entry.findtext(f"{ATOM}content") or "").strip()

    pub_str = (
        entry.findtext(f"{ATOM}published")
        or entry.findtext(f"{ATOM}updated")
        or ""
    )
    published = None
    if pub_str:
        try:
            published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass

    author_el = entry.find(f"{ATOM}author/{ATOM}name")
    author = (author_el.text or "").strip() if author_el is not None and author_el.text else None

    if not link:
        return None

    return RawHit(
        title=title[:120],
        url=link,
        source="producthunt",
        summary=_strip_html(summary)[:280],
        body=_strip_html(summary),
        author=author,
        published_at=published,
        tags=("producthunt",),
    )


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()