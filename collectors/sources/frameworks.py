"""框架 release & 官方博客 — LlamaIndex / CrewAI / AutoGen 等。

跟踪 agent 框架的版本发布说明，从 changelog 抓 breaking change。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


# (url, source-name, content-kind)
# kind: rss=RSS 2.0, atom=Atom, github-release=GitHub releases atom
FEEDS = [
    ("https://blog.crewai.com/rss", "crewai-blog", "rss"),
    ("https://github.com/run-llama/llama_index/releases.atom", "llamaindex-release", "atom"),
    ("https://github.com/microsoft/autogen/releases.atom", "autogen-release", "atom"),
    ("https://github.com/langchain-ai/langchain/releases.atom", "langchain-release", "atom"),
    ("https://github.com/langchain-ai/langgraph/releases.atom", "langgraph-release", "atom"),
    ("https://github.com/openai/openai-agents-python/releases.atom", "openai-agents-release", "atom"),
    ("https://github.com/anthropics/anthropic-cookbook/releases.atom", "anthropic-cookbook", "atom"),
    ("https://github.com/anthropics/claude-code/releases.atom", "claude-code-release", "atom"),
]


# 关键词 — 关注 breaking change / bug fix / deprecation
KEYWORDS = (
    "break", "breaking", "deprecat", "removed", "fix", "bug",
    "fail", "fail", "issue", "crash", "leak", "vulner",
    "security", "cve", "injection", "jailbreak", "advisory",
    "patch", "patched", "hotfix", "regression", "leak",
    "patch release", "release notes",
)


class FrameworksCollector:
    name = "frameworks"

    def collect(self) -> Iterable[RawHit]:
        for url, source, kind in FEEDS:
            try:
                raw = http_get(url)
            except Exception:
                continue
            try:
                root = ET.fromstring(raw)
            except ET.ParseError:
                continue

            if kind == "rss":
                for item in root.findall(".//item"):
                    hit = _rss_to_hit(item, source)
                    if hit:
                        yield hit
            else:  # atom
                for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
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
        title=title[:120], url=link, source=source,
        summary=_strip_html(desc)[:280], body=_strip_html(desc),
        published_at=published, tags=("framework", source),
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
        # GitHub Atom: link rel=self
        for link_el in entry.findall(f"{ATOM}link"):
            if link_el.get("rel") == "self":
                link = (link_el.get("href") or "").strip()
                break
    summary = (entry.findtext(f"{ATOM}content") or entry.findtext(f"{ATOM}summary") or "").strip()
    if not _is_relevant(title, summary):
        return None
    pub_str = entry.findtext(f"{ATOM}updated") or entry.findtext(f"{ATOM}published") or ""
    published = None
    if pub_str:
        try:
            published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass
    if not link:
        return None
    return RawHit(
        title=title[:120], url=link, source=source,
        summary=_strip_html(summary)[:280], body=_strip_html(summary),
        published_at=published, tags=("framework", source),
    )


def _is_relevant(title: str, desc: str) -> bool:
    haystack = (title + " " + desc).lower()
    return any(k in haystack for k in KEYWORDS)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()