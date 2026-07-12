"""Hacker News 关键词采集。"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get_json


SEARCH_TERMS = [
    "claude code",
    "claude agent",
    "openai agents sdk",
    "langchain bug",
    "langgraph memory",
    "agent prompt injection",
    "tool use agent",
]


def _search(term: str) -> Iterable[dict]:
    try:
        data = http_get_json(
            "https://hn.algolia.com/api/v1/search",
            params={"query": term, "tags": "story", "hitsPerPage": 20},
        )
    except Exception:
        return
    return data.get("hits") or []


class HackerNewsCollector:
    name = "hackernews"

    def collect(self) -> Iterable[RawHit]:
        for term in SEARCH_TERMS:
            for hit in _search(term):
                url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                yield RawHit(
                    title=hit.get("title") or hit.get("story_title") or "",
                    url=url,
                    source="hackernews",
                    summary=(hit.get("story_text") or "")[:280],
                    score=int(hit.get("points") or 0),
                    published_at=_parse_ts(hit.get("created_at")),
                    tags=(term,),
                )


def _parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None