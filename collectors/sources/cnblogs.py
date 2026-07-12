"""博客园 (cnblogs) RSS/Atom 采集。

cnblogs 的搜索 API 反爬严（返 HTML），改为抓首页 + 推荐榜的 Atom feed。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


ATOM = "{http://www.w3.org/2005/Atom}"

# 博客园 RSS 源
FEEDS = [
    ("https://www.cnblogs.com/rss", "cnblogs-home"),
    ("https://www.cnblogs.com/pick/rss", "cnblogs-pick"),
]


# 关键词 — 用于过滤
KEYWORDS = (
    "langchain", "claude", "openai", "gpt", "llm", "agent",
    "prompt", "function call", "工具调用", "大模型", "人工智能",
    "rag", "embedding", "向量", "深度学习", "transformer",
    "ai", "智能", "模型",
)


class CnblogsCollector:
    name = "cnblogs"

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

            # Atom format — <entry>
            for entry in root.findall(f"{ATOM}entry"):
                hit = _atom_to_hit(entry, source)
                if hit:
                    yield hit


def _atom_to_hit(entry, source: str) -> RawHit | None:
    title = (entry.findtext(f"{ATOM}title") or "").strip()
    # link 在 href 属性
    link = ""
    for link_el in entry.findall(f"{ATOM}link"):
        href = link_el.get("href") or ""
        if href and (link_el.get("rel") in (None, "alternate")):
            link = href.strip()
            break
    if not link and entry.findtext(f"{ATOM}id"):
        link = entry.findtext(f"{ATOM}id").strip()
    summary = (entry.findtext(f"{ATOM}summary") or entry.findtext(f"{ATOM}content") or "").strip()

    if not (title and link):
        return None
    if not _is_relevant(title, summary):
        return None

    # 时间
    pub_str = (
        entry.findtext(f"{ATOM}published")
        or entry.findtext(f"{ATOM}updated")
        or ""
    )
    published = None
    if pub_str:
        try:
            published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass

    author_el = entry.find(f"{ATOM}author/{ATOM}name")
    author = (author_el.text or "").strip() if author_el is not None and author_el.text else None

    return RawHit(
        title=title[:120],
        url=link,
        source=source,
        summary=_strip_html(summary)[:280],
        body=_strip_html(summary),
        author=author,
        published_at=published,
        tags=("cnblogs",),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()