"""社区论坛 — LangChain forum + OpenAI dev community。

讨论区里大量实战问答，是「坑」的高密度来源。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEEDS = [
    ("https://forum.langchain.com/latest.rss", "langchain-forum"),
    ("https://community.openai.com/latest.rss", "openai-forum"),
]


# 关键词 — 只保留 agent / LLM 实战类
KEYWORDS = (
    "agent", "llm", "claude", "openai", "gpt", "anthropic",
    "langchain", "rag", "prompt", "tool", "function call",
    "embedding", "cursor", "copilot", "deepseek", "gemini",
    "chatgpt", "mcp", "autogen", "crewai", "langgraph",
    "context", "token", "rate limit", "stream", "error", "fail",
)


class ForumsCollector:
    name = "forums"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url)
            except Exception:
                continue
            try:
                root = ET.fromstring(raw)
            except ET.ParseError:
                continue
            for item in root.findall(".//item"):
                hit = _to_hit(item, source)
                if hit:
                    yield hit


def _to_hit(item, source: str) -> RawHit | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    desc = (item.findtext("description") or "").strip()
    if not (title and link):
        return None
    if not _is_relevant(title, desc):
        return None
    pub = item.findtext("pubDate")
    published = None
    if pub:
        try:
            published = parsedate_to_datetime(pub)
        except (TypeError, ValueError):
            pass
    return RawHit(
        title=title[:120], url=link, source=source,
        summary=_strip_html(desc)[:280], body=_strip_html(desc),
        published_at=published, tags=("forum", source),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()