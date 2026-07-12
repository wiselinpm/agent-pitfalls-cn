"""TLDR AI / Ben's Bites Newsletter 聚合 — 每日 AI 新闻 + 实战经验。

覆盖业界每日精选 + LLM/agent 实际落地中遇到的坑。
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
    ("https://tldr.tech/api/rss/ai", "tldr-ai"),
    ("https://www.bensbites.com/feed", "bens-bites"),
]


KEYWORDS = (
    "agent", "llm", "claude", "openai", "gpt", "anthropic",
    "langchain", "rag", "prompt", "tool", "function call",
    "embedding", "cursor", "copilot", "deepseek", "gemini",
    "mistral", "qwen", "claude code", "bug", "fix", "issue",
    "vulner", "security", "injection", "jailbreak",
)


class TLDRCollector:
    name = "tldr"

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
        published_at=published, tags=("newsletter", source),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()