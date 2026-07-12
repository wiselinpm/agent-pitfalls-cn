"""更多国际平台兜底：HN show / shownewest / 关键词订阅、Reddit json RSS 镜像。

覆盖：
- HackerNews Algolia show + comments
- Reddit 公开 json RSS（使用 RSSHub 镜像 / Teddit 镜像）
- Lobsters comments
- dev.to latest
"""

from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable
import xml.etree.ElementTree as ET

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.hn_reddit")


# === HN Algolia show + comments ===
HN_QUERIES = [
    "Claude Code",
    "OpenAI agents SDK",
    "LangChain",
    "LangGraph",
    "Aider",
    "Cursor",
    "MCP",
    "agent prompt injection",
    "agent jailbreak",
    "agent failure",
    "RAG hallucination",
]


def _hn_search(q: str, *, tags: str = "story") -> Iterable[RawHit]:
    try:
        data = http_get_json(
            "https://hn.algolia.com/api/v1/search",
            params={"query": q, "tags": tags, "hitsPerPage": 25},
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("hn search %r skipped: %s", q, exc)
        return
    for hit in data.get("hits") or []:
        url = hit.get("url") or hit.get("story_url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        title = hit.get("title") or hit.get("story_title") or ""
        if not title:
            continue
        score = int(hit.get("points") or 0)
        yield RawHit(
            title=title,
            url=url,
            source=f"hn-search:{q[:30]}",
            summary=(hit.get("story_text") or "")[:280],
            body=hit.get("story_text") or "",
            score=score,
            published_at=_parse_ts(hit.get("created_at")),
            tags=("hackernews", f"q:{q}"),
        )


class HackerNewsSearchCollector:
    name = "hn-search"

    def collect(self) -> Iterable[RawHit]:
        for q in HN_QUERIES:
            yield from _hn_search(q)


# === Reddit 公开 json RSS — 用 reddit.com/r/X/comments.rss 之类 ===
# 注：reddit 主域公开 RSS 持续 403；这里用更稳的 RSSHub 镜像
REDDIT_FEEDS = [
    "https://rsshub.app/reddit/subreddit/ClaudeAI",
    "https://rsshub.app/reddit/subreddit/LocalLLaMA",
    "https://rsshub.app/reddit/subreddit/MachineLearning",
    "https://rsshub.app/reddit/subreddit/ChatGPT",
    "https://rsshub.app/reddit/subreddit/Anthropic",
    "https://rsshub.app/reddit/subreddit/OpenAI",
    "https://rsshub.app/reddit/subreddit/Bard",
    "https://rsshub.app/reddit/subreddit/singularity",
]


class RedditFeedCollector:
    name = "reddit-feed"

    def collect(self) -> Iterable[RawHit]:
        for url in REDDIT_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("reddit-feed %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, url.split("/")[-1])


def _parse_rss(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not (title and link):
            continue
        desc = item.findtext("description") or item.findtext("content:encoded") or ""
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
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
            source=f"reddit:{source}",
            summary=clean[:280],
            body=clean,
            published_at=dt,
            tags=("reddit",),
        )


# === Lobsters 标签 / 主题 ===
LOBSTERS_TAGS = [
    "ai",
    "llm",
    "ml",
    "databases",
    "programming",
    "distributed",
    "performance",
    "security",
    "cryptography",
    "linux",
    "python",
    "javascript",
]


class LobstersTagsCollector:
    name = "lobsters-tags"

    def collect(self) -> Iterable[RawHit]:
        for tag in LOBSTERS_TAGS:
            url = f"https://lobste.rs/tag/{tag}/rss"
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("lobsters tag %s skipped: %s", tag, exc)
                continue
            yield from _parse_rss(raw, f"lobsters:{tag}")


# === dev.to latest（已有 devto 但最新文章不是 tag 命中）===
class DevToLatestCollector:
    name = "devto-latest"

    def collect(self) -> Iterable[RawHit]:
        try:
            data = http_get_json(
                "https://dev.to/api/articles",
                params={"per_page": 30, "top": 1},
                timeout=20,
            )
        except Exception as exc:
            _LOG.debug("devto-latest skipped: %s", exc)
            return
        if not isinstance(data, list):
            return
        for item in data:
            title = item.get("title") or ""
            url_out = item.get("url") or item.get("canonical_url") or ""
            if not (title and url_out):
                continue
            body = (item.get("description") or "")[:280]
            tags = tuple(item.get("tag_list") or [])
            author = (item.get("user") or {}).get("username") if isinstance(item.get("user"), dict) else None
            pub = item.get("published_at")
            dt: datetime | None = None
            if pub:
                try:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                except ValueError:
                    dt = None
            yield RawHit(
                title=title,
                url=url_out,
                source="devto-latest",
                summary=body,
                body=item.get("description") or "",
                author=author,
                published_at=dt,
                score=int(item.get("positive_reactions_count") or 0)
                + int(item.get("comments_count") or 0) * 2,
                tags=tags,
            )


def _parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None