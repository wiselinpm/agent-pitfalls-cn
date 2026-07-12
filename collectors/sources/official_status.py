"""Anthropic + OpenAI status page 采集。

跟踪官方服务状态变更，覆盖 API 限速/中断/降级等「坑」。
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
    ("https://status.anthropic.com/history.rss", "anthropic-status"),
    ("https://status.openai.com/history.rss", "openai-status"),
]

# 关键词过滤 — 只保留跟 LLM/agent 相关的 incident
KEYWORDS = (
    "claude", "anthropic", "openai", "chatgpt", "gpt-", "gpt4", "gpt5",
    "api", "model", "agent", "rate limit", "rate-limit", "degraded",
    "elevated", "outage", "latency", "completion", "inference",
    "embedding", "fine-tun", "vision", "function", "tools",
    "tokens", "context", "stream", "messages",
)


class OfficialStatusCollector:
    name = "official-status"

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
    if not title:
        return None
    haystack = title.lower()
    if not any(k in haystack for k in KEYWORDS):
        return None

    link = (item.findtext("link") or "").strip()
    desc = (item.findtext("description") or "").strip()
    pub = item.findtext("pubDate")

    published = None
    if pub:
        try:
            published = parsedate_to_datetime(pub)
        except (TypeError, ValueError):
            pass

    if not link:
        return None

    return RawHit(
        title=title[:120],
        url=link,
        source=source,
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        published_at=published,
        tags=("status", source),
    )


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()