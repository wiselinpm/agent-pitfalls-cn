"""Stack Overflow 官方 API 采集（无需 key，有匿名 quota）。"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get_json


QUERIES = [
    "claude-code",
    "openai-agents",
    "langchain",
    "langgraph",
    "agent prompt injection",
    "function calling arguments",
    "context window overflow",
    "tool use agent",
]

TAGS = ["openai-api", "langchain", "anthropic", "llm", "agent"]


class StackOverflowCollector:
    name = "stackoverflow"

    def collect(self) -> Iterable[RawHit]:
        # 1) 关键词搜索（高信号）
        for q in QUERIES:
            try:
                data = http_get_json(
                    "https://api.stackexchange.com/2.3/search/advanced",
                    params={
                        "order": "desc",
                        "sort": "votes",
                        "q": q,
                        "site": "stackoverflow",
                        "pagesize": 20,
                        "filter": "default",
                    },
                )
            except Exception:
                continue
            for item in (data or {}).get("items", []):
                yield _to_hit(item, f"so:q:{q}")

        # 2) 按 tag 拉高赞问题
        for tag in TAGS:
            try:
                data = http_get_json(
                    "https://api.stackexchange.com/2.3/questions",
                    params={
                        "order": "desc",
                        "sort": "votes",
                        "tagged": tag,
                        "site": "stackoverflow",
                        "pagesize": 15,
                        "filter": "default",
                    },
                )
            except Exception:
                continue
            for item in (data or {}).get("items", []):
                yield _to_hit(item, f"so:tag:{tag}")


def _to_hit(item: dict, source: str) -> RawHit:
    title = item.get("title") or ""
    link = item.get("link") or ""
    tags = tuple(item.get("tags") or ())
    return RawHit(
        title=title,
        url=link,
        source=source,
        summary=_html_strip(item.get("excerpt") or "")[:280],
        body=item.get("body") or "",
        author=item.get("owner", {}).get("display_name") if isinstance(item.get("owner"), dict) else None,
        published_at=_parse_unix(item.get("creation_date")),
        score=int(item.get("score") or 0) + int(item.get("view_count") or 0) // 100,
        tags=tags,
    )


def _parse_unix(ts: int | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.utcfromtimestamp(int(ts))
    except (TypeError, ValueError, OSError):
        return None


def _html_strip(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s or "").strip()