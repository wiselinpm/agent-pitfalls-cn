"""RSS 采集：覆盖主流 agent 厂商博客与 changelog。"""

from __future__ import annotations

import email.utils
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


FEEDS = [
    ("https://openai.com/blog/rss.xml", "openai-blog"),
    ("https://github.blog/changelog/feed.xml", "github-changelog"),
    ("https://blog.langchain.dev/rss.xml", "langchain-blog"),
    ("https://simonwillison.net/atom/everything/", "simonwillison"),
    ("https://hnrss.org/newest?q=claude+code+OR+openai+agents+OR+langchain&count=50", "hn-newest"),
    ("https://www.reddit.com/r/ClaudeAI/.rss", "reddit-claudeai"),
    ("https://www.reddit.com/r/OpenAI/.rss", "reddit-openai"),
    ("https://www.reddit.com/r/LangChain/.rss", "reddit-langchain"),
]


_LOG = logging.getLogger("collectors")


class RSSCollector:
    name = "rss"

    def collect(self) -> Iterable[RawHit]:
        for feed_url, source in FEEDS:
            try:
                raw = http_get(feed_url)
            except Exception as exc:
                _LOG.warning("RSS feed %s failed: %s", feed_url, exc)
                continue
            for hit in _parse(raw, source):
                yield hit


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.warning("RSS parse error for %s: %s", source, exc)
        return
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall("atom:entry", ns)
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or item.findtext("atom:link", namespaces=ns) or "").strip()
        if not link:
            guid = item.findtext("guid")
            if guid:
                link = guid.strip()
        desc = (item.findtext("description") or item.findtext("summary", namespaces=ns) or "").strip()
        author = (item.findtext("author") or item.findtext("atom:author/atom:name", namespaces=ns) or "").strip()
        pub = item.findtext("pubDate") or item.findtext("published", namespaces=ns)
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        if not (title and link):
            continue
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=_strip_html(desc)[:280],
            body=_strip_html(desc),
            author=author or None,
            published_at=dt,
        )


def _strip_html(s: str) -> str:
    import re

    return re.sub(r"<[^>]+>", "", s or "").strip()