"""DEV.to (dev.to) 通用 RSS — 用 AI 关键词过滤。

Dev.to tag RSS 已经被 devto.py 覆盖，但通用 RSS 可以抓到未被 tag 的文章。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEED = "https://dev.to/feed"

KEYWORDS = (
    "agent", "llm", "claude", "openai", "gpt", "anthropic",
    "langchain", "rag", "prompt", "tool", "function call",
    "embedding", "cursor", "copilot", "chatgpt", "deepseek",
    "gemini", "mistral", "qwen", "claude code", "openai agents",
    "mcp", "autogen", "crewai", "langgraph",
)


class DevCommunityCollector:
    name = "dev-community"

    def collect(self) -> Iterable[RawHit]:
        try:
            raw = http_get(FEED)
        except Exception:
            return
        try:
            root = ET.fromstring(raw)
        except ET.ParseError:
            return
        for item in root.findall(".//item"):
            hit = _to_hit(item)
            if hit:
                yield hit


def _to_hit(item) -> RawHit | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    desc = (item.findtext("description") or "").strip()
    # DEV Community 用 categories 字段
    cats = " ".join(c.text or "" for c in item.findall("category"))
    if not (title and link):
        return None
    if not _is_relevant(title, desc + " " + cats):
        return None
    pub = item.findtext("pubDate")
    published = None
    if pub:
        try:
            published = parsedate_to_datetime(pub)
        except (TypeError, ValueError):
            pass
    author = (item.findtext("author") or "").strip() or None
    return RawHit(
        title=title[:120], url=link, source="dev-community",
        summary=_strip_html(desc)[:280], body=_strip_html(desc),
        author=author, published_at=published,
        tags=("dev-community",),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()