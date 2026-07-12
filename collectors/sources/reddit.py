"""Reddit 采集 — 使用公开 .rss 端点（更稳定，免鉴权）。

注：search.json 端点经常返回 403；.rss 端点通过率更高且数据足够。
"""

from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable
import xml.etree.ElementTree as ET

from ..base import RawHit
from ._http import http_get


SUBREDDITS = [
    "ClaudeAI",
    "OpenAI",
    "LangChain",
    "LocalLLaMA",
]

_LOG = logging.getLogger("collectors.reddit")


class RedditCollector:
    name = "reddit"

    def collect(self) -> Iterable[RawHit]:
        for sub in SUBREDDITS:
            for hit in _fetch_sub(sub):
                yield hit


def _fetch_sub(sub: str) -> Iterable[RawHit]:
    # 关键词搜索：通过 .rss 端点
    for q in ("agent+OR+claude+code+OR+tool+use+OR+prompt+injection", "bug+OR+error+OR+broken"):
        url = f"https://www.reddit.com/r/{sub}/search.rss?q={q}&restrict_sr=1&sort=new"
        try:
            raw = http_get(url, headers={"User-Agent": "agent-pitfalls/0.1 (+opensource)"})
        except Exception as exc:
            _LOG.debug("reddit rss %s/%s skipped: %s", sub, q, exc)
            continue
        for hit in _parse_rss(raw, sub):
            yield hit


def _parse_rss(raw: bytes, sub: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.debug("reddit rss parse fail: %s", exc)
        return
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not (title and link):
            continue
        pub = item.findtext("pubDate")
        dt: datetime | None = None
        if pub:
            try:
                dt = parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        yield RawHit(
            title=title,
            url=link,
            source=f"reddit:r/{sub}",
            summary=(item.findtext("description") or "")[:280],
            body=item.findtext("description") or "",
            published_at=dt,
            score=0,
            tags=(sub,),
        )