"""厂商 AI 博客 RSS 聚合 — DeepMind / AWS ML / Anthropic News 等。

覆盖最权威的模型/agent 厂商一手内容。
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
    ("https://deepmind.google/blog/rss.xml", "deepmind-blog"),
    ("https://aws.amazon.com/about-aws/whats-new/recent/feed/", "aws-ml"),
    ("https://www.anthropic.com/news/rss.xml", "anthropic-news"),
    ("https://openai.com/blog/rss.xml", "openai-blog"),
    ("https://blog.langchain.dev/rss/", "langchain-blog"),
    ("https://huggingface.co/blog/feed.xml", "huggingface-blog"),
]


# 关键词 — 过滤真正讨论 LLM/agent 的文章
KEYWORDS = (
    "agent", "llm", "claude", "openai", "gpt", "anthropic",
    "langchain", "rag", "prompt", "tool", "function call",
    "model", "deepmind", "gemini", "embedding", "inference",
    "transformer", "fine-tun", "alignment", "safety", "jailbreak",
    "injection", "hallucination", "evaluation", "benchmark",
)


class VendorBlogsCollector:
    name = "vendor-blogs"

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
                hit = _rss_to_hit(item, source)
                if hit:
                    yield hit

            # Atom fallback
            ATOM = "{http://www.w3.org/2005/Atom}"
            for entry in root.findall(f"{ATOM}entry"):
                hit = _atom_to_hit(entry, source)
                if hit:
                    yield hit


def _rss_to_hit(item, source: str) -> RawHit | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    desc = (item.findtext("description") or "").strip()
    if not (title and link):
        return None
    if not _is_relevant(title, desc):
        return None

    pub = item.findtext("pubDate")
    published = None
    if pub:
        try:
            published = parsedate_to_datetime(pub)
        except (TypeError, ValueError):
            pass

    return RawHit(
        title=title[:120],
        url=link,
        source=source,
        summary=_strip_html(desc)[:280],
        body=_strip_html(desc),
        published_at=published,
        tags=("vendor", source),
    )


def _atom_to_hit(entry, source: str) -> RawHit | None:
    ATOM = "{http://www.w3.org/2005/Atom}"
    title = (entry.findtext(f"{ATOM}title") or "").strip()
    if not title:
        return None
    link = ""
    for link_el in entry.findall(f"{ATOM}link"):
        href = link_el.get("href") or ""
        if link_el.get("rel") in (None, "alternate") and href:
            link = href.strip()
            break
    if not link:
        return None
    summary = (entry.findtext(f"{ATOM}summary") or entry.findtext(f"{ATOM}content") or "").strip()
    if not _is_relevant(title, summary):
        return None

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
        tags=("vendor", source),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()