"""Lobsters 采集 — 主站 RSS（Hottest）。

技术质量高、讨论深度的技术社区。海外 RSS 比 Reddit 可靠。
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEEDS = [
    ("https://lobste.rs/rss", "lobsters-hottest"),
    ("https://lobste.rs/newest.rss", "lobsters-newest"),
]


# 关键词过滤 — 减少噪声
KEYWORDS = (
    "ai", "llm", "agent", "claude", "openai", "langchain",
    "rag", "prompt", "tool", "function call", "model",
    "anthropic", "machine learning", "neural", "transformer",
    "embedding", "vector", "gpt", "deep learning", "inference",
)


class LobstersCollector:
    name = "lobsters"

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

    author = (item.findtext("author") or "").strip() or None
    comments_url = (item.findtext("comments") or "").strip()

    # 提取 score — Lobsters 在描述里附带
    score = 0
    m = re.search(r"score\s*[:：]\s*(\d+)", desc)
    if m:
        score = int(m.group(1))

    return RawHit(
        title=title[:120],
        url=link,
        source=source,
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        author=author,
        published_at=published,
        score=score,
        tags=("lobsters",),
        raw_metadata={"comments_url": comments_url} if comments_url else {},
    )


import re  # 放在末尾，规避局部 import 副作用


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()