"""少数派 (sspai.com) 采集 — 国内优质技术/工具评测社区。

大量 AI 工具实战评测，覆盖大众用户视角的坑。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEED = "https://sspai.com/feed"

# 关键词过滤
KEYWORDS = (
    "ai", "gpt", "claude", "openai", "anthropic", "llm",
    "agent", "大模型", "人工智能", "prompt", "rag",
    "cursor", "copilot", "工具", "聊天", "智能体",
    "claude code", "chatgpt", "deepseek", "通义", "文心",
    "gemini", "perplexity", "stable diffusion",
)


class SspaiCollector:
    name = "sspai"

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

    author = (item.findtext("author") or item.findtext("dc:creator") or "").strip() or None

    return RawHit(
        title=title[:120],
        url=link,
        source="sspai",
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        author=author,
        published_at=published,
        tags=("sspai",),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()