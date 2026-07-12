"""更多英文高质量 source — Hashnode / dev.to tag / Substack / IndieHackers。

这些 source 不需要 API key，纯 RSS / 公开页面。
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


_LOG = logging.getLogger("collectors.extra_en")


FEEDS = [
    # Hashnode — AI / LLM / agents 主题
    ("https://hashnode.com/api/feed/llms-and-ai", "hashnode-llm"),
    ("https://hashnode.com/api/feed/ai-agents", "hashnode-agents"),
    # dev.to — tag RSS（公开）
    ("https://dev.to/feed/tag/aiagents", "devto-aiagents"),
    ("https://dev.to/feed/tag/llm", "devto-llm"),
    ("https://dev.to/feed/tag/langchain", "devto-langchain"),
    ("https://dev.to/feed/tag/claude", "devto-claude"),
    ("https://dev.to/feed/tag/openai", "devto-openai"),
    ("https://dev.to/feed/tag/chatgpt", "devto-chatgpt"),
    ("https://dev.to/feed/tag/rag", "devto-rag"),
    # IndieHackers — AI 类
    ("https://www.indiehackers.com/tag/ai.rss", "indiehackers-ai"),
    # Substack — 公开 newsletter（无 API key）
    ("https://newsletter.pragmaticengineer.com/feed", "pragmatic-engineer"),
    ("https://www.latent.space/feed", "latent-space-substack"),
    ("https://interconnects.substack.com/feed", "interconnects"),
    ("https://simonwillison.substack.com/feed", "simon-willison-substack"),
    ("https://bensbites.substack.com/feed", "bens-bites"),
    # InfoQ 英文
    ("https://www.infoq.com/ai-ml-data-eng/news/rss", "infoq-en-ai"),
    ("https://www.infoq.com/llms/news/rss", "infoq-en-llm"),
    # The New Stack — AI
    ("https://thenewstack.io/category/ai/feed/", "thenewstack-ai"),
    # DZone AI zone
    ("https://feeds.dzone.com/ai", "dzone-ai"),
    # KDnuggets
    ("https://www.kdnuggets.com/feed", "kdnuggets"),
    # Hacker Noon — AI tag
    ("https://hackernoon.com/tagged/ai/feed", "hackernoon-ai"),
    ("https://hackernoon.com/tagged/llm/feed", "hackernoon-llm"),
]


class ExtraENCollector:
    name = "extra-en"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("extra-en %s skipped: %s", source, exc)
                continue
            yield from _parse(raw, source)


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.debug("parse fail %s: %s", source, exc)
        return
    items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not link:
            guid = item.findtext("guid")
            if guid:
                link = guid.strip()
        if not (title and link):
            continue
        desc = item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary") or ""
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}published")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        author = item.findtext("author") or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name") or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}email") or ""
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=desc,
            author=author.strip() or None,
            published_at=dt,
        )