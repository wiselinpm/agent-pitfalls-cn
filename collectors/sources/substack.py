"""Substack / Ghost newsletter 公开 RSS 采集 — 补充 extra-en。

许多独立技术作者用 Substack/Ghost 写作，比 Medium 更深。RSS 公开。
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


_LOG = logging.getLogger("collectors.substack")


# 主流技术 newsletter
FEEDS = [
    # Simon Willison's Weblog（已在 extra-en / vendor-blogs）
    # Latent Space（已在 extra-en / newsletters）
    # 补充更多独立技术 newsletter
    ("https://stratechery.com/feed/", "stratechery"),
    ("https://www.ben-evans.com/feed", "benedictevans"),
    ("https://www.constellationr.com/api/v2/articles.rss", "constellation-research"),
    ("https://battlemobile.substack.com/feed", "battlemobile"),
    ("https://newsletter.machinelearning.org/feed", "ml-newsletter"),
    ("https://gradientflow.substack.com/feed", "gradient-flow"),
    ("https://jack-clark.net/feed/", "import-ai"),
    ("https://www.deeplearning.ai/the-batch/feed/", "the-batch"),
    ("https://feeds.feedburner.com/oreilly/radar", "oreilly-radar"),
    ("https://www.understandingai.org/feed", "understanding-ai"),
    ("https://bair.berkeley.edu/blog/feed.xml", "bair-blog"),
    ("https://aiguide.substack.com/feed", "ai-guide"),
    ("https://thezvi.substack.com/feed", "zvi-mowshowitz"),
    ("https://garymarcus.substack.com/feed", "gary-marcus"),
    ("https://www.oneusefulthing.substack.com/feed", "one-useful-thing"),
    ("https://aisupremacy.substack.com/feed", "ai-supremacy"),
    ("https://www.aisnakeoil.com/feed", "ai-snake-oil"),
    ("https://www.normaltech.ai/feed", "normal-tech"),
    ("https://magazine.sebastianraschka.com/feed", "raschka-magazine"),
    ("https://magazine.atlanta.ai/feed", "atlanta-ai"),
    ("https://www.willthomason.name/feed/", "will-thomason"),
    ("https://ihavenovim.com/index.xml", "ihavenovim"),
    ("https://news.ycombinator.com/rss", "hn-frontpage"),
]


class SubstackCollector:
    name = "substack"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("substack feed %s skipped: %s", url, exc)
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
        pub = (
            item.findtext("pubDate")
            or item.findtext("{http://www.w3.org/2005/Atom}published")
        )
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        author = (
            item.findtext("author")
            or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")
            or item.findtext("dc:creator")
            or ""
        ).strip()
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            author=author or None,
            published_at=dt,
        )