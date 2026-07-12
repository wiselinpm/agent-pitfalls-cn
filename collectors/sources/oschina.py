"""OSChina (开源中国) RSS 采集。

替代 Juejin — 提供 AI/agent 相关的新闻和讨论。
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
    "https://www.oschina.net/news/rss",
    "https://www.oschina.net/question/rss",
]


# 关键词 — 过滤 AI/agent 相关
KEYWORDS = (
    "agent", "llm", "claude", "langchain", "openai", "gpt",
    "anthropic", "deepseek", "qwen", "glm", "通义", "文心",
    "人工智能", "大模型", "rag", "prompt", "工具调用",
    "function call", "agent", "mcp", "claude code",
)


class OSChinaCollector:
    name = "oschina"

    def collect(self) -> Iterable[RawHit]:
        for url in FEEDS:
            try:
                raw = http_get(url)
            except Exception:
                continue
            try:
                root = ET.fromstring(raw)
            except ET.ParseError:
                continue
            source = f"oschina:{url.rsplit('/', 1)[-1].replace('.rss','')}"
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

    author = (item.findtext("author") or item.findtext("dc:creator") or "").strip() or None

    return RawHit(
        title=title[:120],
        url=link,
        source=source,
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        author=author,
        published_at=published,
        tags=("oschina",),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()