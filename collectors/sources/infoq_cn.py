"""InfoQ 中文站 RSS 采集。

InfoQ 中文站对 AI/LLM 趋势报道及时，质量高。
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


# InfoQ 中文 RSS 列表
FEEDS = [
    ("https://www.infoq.cn/feed.xml", "infoq.cn-all"),
    ("https://www.infoq.cn/topic/AI.feed", "infoq.cn-ai"),
    # 备用源：极客邦 / AI 前线
    ("https://feed.infoq.cn/topic/llm", "infoq.cn-llm"),
]


class InfoQCNCollector:
    name = "infoq-cn"

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

            # RSS 2.0
            for item in root.findall(".//item"):
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                desc = (item.findtext("description") or "").strip()
                pub = item.findtext("pubDate")
                author = (item.findtext("author") or item.findtext("dc:creator", namespaces={"dc": "http://purl.org/dc/elements/1.1/"}) or "").strip()
                if not (title and link):
                    continue
                published = _parse_rfc2822(pub) if pub else None
                yield RawHit(
                    title=title[:120],
                    url=link,
                    source=source,
                    summary=_strip_html(desc)[:280],
                    body=_strip_html(desc),
                    author=author or None,
                    published_at=published,
                    tags=("infoq-cn",),
                )

            # Atom fallback
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for entry in root.findall(".//a:entry", ns):
                title = (entry.findtext("a:title", namespaces=ns) or "").strip()
                link_el = entry.find("a:link", ns)
                link = (link_el.get("href") if link_el is not None else "") or ""
                summary = (entry.findtext("a:summary", namespaces=ns) or "").strip()
                published_str = entry.findtext("a:published", namespaces=ns)
                published = _parse_iso(published_str) if published_str else None
                if not (title and link):
                    continue
                yield RawHit(
                    title=title[:120],
                    url=link,
                    source=source,
                    summary=_strip_html(summary)[:280],
                    body=_strip_html(summary),
                    published_at=published,
                    tags=("infoq-cn",),
                )


def _strip_html(s: str) -> str:
    import re

    return re.sub(r"<[^>]+>", "", s or "").strip()


def _parse_rfc2822(s: str) -> datetime | None:
    from email.utils import parsedate_to_datetime

    try:
        return parsedate_to_datetime(s)
    except (TypeError, ValueError):
        return None


def _parse_iso(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None