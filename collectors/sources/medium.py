"""Medium tag RSS — 通过公开 RSS 端点采集（无需 API key）。"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.medium")

# Medium tag RSS 是公开的，无需登录
TAGS = [
    "artificial-intelligence",
    "machine-learning",
    "llm",
    "chatgpt",
    "claude",
    "openai",
    "langchain",
    "ai-agent",
    "generative-ai",
]

USER_HANDLES = [
    "simonw",
    "latent.space",
    "alphasignal",
]


class MediumCollector:
    name = "medium"

    def collect(self) -> Iterable[RawHit]:
        for tag in TAGS:
            yield from _fetch_tag(tag)
        for handle in USER_HANDLES:
            yield from _fetch_user(handle)


def _fetch_tag(tag: str) -> Iterable[RawHit]:
    url = f"https://medium.com/feed/tag/{tag}"
    try:
        raw = http_get(url, headers={"User-Agent": "agent-pitfalls/0.1 (+opensource)"})
    except Exception as exc:
        _LOG.debug("medium tag %s skipped: %s", tag, exc)
        return
    yield from _parse(raw, f"medium:tag:{tag}")


def _fetch_user(handle: str) -> Iterable[RawHit]:
    url = f"https://medium.com/feed/@{handle}"
    try:
        raw = http_get(url, headers={"User-Agent": "agent-pitfalls/0.1 (+opensource)"})
    except Exception as exc:
        _LOG.debug("medium user %s skipped: %s", handle, exc)
        return
    yield from _parse(raw, f"medium:user:{handle}")


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.debug("medium parse fail: %s", exc)
        return
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or item.findtext("guid") or "").strip()
        if not (title and link):
            continue
        desc = item.findtext("description") or item.findtext("content:encoded") or ""
        pub = item.findtext("pubDate")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        author = item.findtext("dc:creator") or ""
        # Medium 描述里经常有 <img> / <p>，剥掉
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=desc,
            author=author or None,
            published_at=dt,
        )