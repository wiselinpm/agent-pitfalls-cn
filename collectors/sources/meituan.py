"""美团技术团队 RSS 采集。

国内一线大厂技术博客，覆盖 LLM/agent 在生产环境的实战经验。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEED = "https://tech.meituan.com/feed"

KEYWORDS = (
    "agent", "llm", "大模型", "gpt", "claude", "openai",
    "langchain", "rag", "prompt", "工具调用", "function call",
    "embedding", "向量", "智能体", "人工智能", "深度学习",
    "知识库", "推理", "训练", "微调", "对齐",
)


class MeituanCollector:
    name = "meituan"

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
        source="meituan-tech",
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        author=author,
        published_at=published,
        tags=("meituan", "tech-blog"),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()