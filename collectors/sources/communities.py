"""技术社区 RSS / Atom 采集 — 覆盖 Reddit/HN/Lobsters 替代品 + Cursor Forum + Replicate。

为 Reddit/Juejin/Zhihu 这些反爬严重平台提供替代源（直接 RSS）。
"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.communities")


# 通过第三方 RSS 镜像 / 公开论坛 RSS 抓 Reddit 内容
FEEDS = [
    # Reddit 直接 RSS（可能 403，作为兜底）
    ("https://www.reddit.com/r/LocalLLaMA/.rss", "reddit-rss:LocalLLaMA"),
    # 直接论坛 RSS
    ("https://forum.cursor.com/latest.rss", "cursor-forum"),
    ("https://community.replicate.com/latest.rss", "replicate-community"),
    ("https://forum.cloudflare.com/c/ai-workers/44.rss", "cloudflare-ai-forum"),
    # GitHub Discussions via RSS（部分 repo）
    ("https://github.com/anthropics/claude-code/discussions.atom", "gh-discuss:claude-code"),
    ("https://github.com/langchain-ai/langchain/discussions.atom", "gh-discuss:langchain"),
    ("https://github.com/langchain-ai/langgraph/discussions.atom", "gh-discuss:langgraph"),
    ("https://github.com/microsoft/autogen/discussions.atom", "gh-discuss:autogen"),
    ("https://github.com/crewAIInc/crewAI/discussions.atom", "gh-discuss:crewai"),
    ("https://github.com/Aider-AI/aider/discussions.atom", "gh-discuss:aider"),
    ("https://github.com/cline/cline/discussions.atom", "gh-discuss:cline"),
    ("https://github.com/openai/openai-agents-python/discussions.atom", "gh-discuss:openai-agents"),
    # Discourse 公共论坛
    ("https://meta.discourse.org/c/dev/8.rss", "discourse-meta-dev"),
]


class CommunitiesCollector:
    name = "communities"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("community feed %s skipped: %s", url, exc)
                continue
            yield from _parse(raw, source)


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    items = root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not link:
            guid = item.findtext("guid")
            if guid:
                link = guid.strip()
        if not (title and link):
            continue
        desc = (
            item.findtext("description")
            or item.findtext("{http://www.w3.org/2005/Atom}summary")
            or item.findtext("{http://www.w3.org/2005/Atom}content")
            or ""
        ).strip()
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}published")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        author = (
            item.findtext("author")
            or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")
            or ""
        ).strip()
        score = 0
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            author=author or None,
            published_at=dt,
            score=score,
            tags=(source.split(":")[0],),
        )