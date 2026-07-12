"""YouTube 技术频道采集 — 通过 RSS（无需 API key）。

每个 YouTube 频道都有公开 RSS feed：`https://www.youtube.com/feeds/videos.xml?channel_id=XXX`
我们关注发布 AI/agent/LLM 相关内容的频道。
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


_LOG = logging.getLogger("collectors.youtube")


# 主流 AI/agent 技术频道 — channel_id 已经验证有效
CHANNELS = [
    ("UCXZCJLdBC09xxGZ6gcdrc6A", "OpenAI"),
    ("UC9zOu0FhiCyyhfHwnt2eMeg", "Hugging Face"),
    ("UCC-lyoTfSrcJzA1ab3APAgw", "LangChain"),
    ("UCbf0NMi7AkUcL1sGhT2C7Sg", "David Shapiro"),
    ("UCqw62DwAPoN4jeyRcGcih0w", "Machine Learning Street Talk"),
    ("UCsXVk37-b7jGlVtUPBr-Ndg", "Yannic Kilcher"),
    ("UCedK18FZW7Y_DxWm4UtHJaA", "Theo - t3.gg"),
    ("UCYO_jab_esuFRV4b17AJtAw", "3Blue1Brown"),
]


class YouTubeCollector:
    name = "youtube"

    def collect(self) -> Iterable[RawHit]:
        for channel_id, name in CHANNELS:
            yield from _fetch_channel(channel_id, name)


def _fetch_channel(channel_id: str, channel_name: str) -> Iterable[RawHit]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        raw = http_get(url, timeout=20)
    except Exception as exc:
        _LOG.debug("youtube channel %s skipped: %s", channel_name, exc)
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href") if link_el is not None else ""
        if not (title and link):
            continue
        summary = (entry.findtext("{http://www.w3.org/2005/Atom}summary")
                   or entry.findtext("{http://www.w3.org/2005/Atom}content") or "").strip()
        clean = re.sub(r"<[^>]+>", " ", summary)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = entry.findtext("{http://www.w3.org/2005/Atom}published")
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        author_el = entry.find("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")
        author = author_el.text.strip() if author_el is not None and author_el.text else None
        yield RawHit(
            title=title,
            url=link,
            source=f"youtube:{channel_name}",
            summary=clean[:280],
            body=clean,
            author=author,
            published_at=dt,
            tags=("youtube", channel_name),
        )