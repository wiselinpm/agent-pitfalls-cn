"""知乎采集（搜索 API，匿名即可）。

注：知乎的反爬较强，本实现只做 best-effort，遇到 403/HTML 响应时静默跳过，
不会抛异常影响其它 source。
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_SEARCH_URL = "https://www.zhihu.com/api/v4/search_v3"
_LOG = logging.getLogger("collectors")

QUERIES = [
    "agent 避坑",
    "Claude Code 报错",
    "LangChain 内存泄漏",
    "OpenAI Agents SDK 问题",
    "Prompt 注入",
]


class ZhihuCollector:
    name = "zhihu"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            params = {
                "t": "general",
                "q": q,
                "correction": "1",
                "offset": "0",
                "limit": "20",
                "show_all_topics": "0",
                "time_interval": "month",
            }
            try:
                raw = http_get(
                    _SEARCH_URL,
                    params=params,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
                        ),
                        "Referer": "https://www.zhihu.com/search",
                    },
                )
                data = json.loads(raw.decode("utf-8"))
            except Exception as exc:
                _LOG.debug("zhihu search %r skipped: %s", q, exc)
                continue
            for hit in _iter(data):
                yield hit


def _iter(data: dict) -> Iterable[RawHit]:
    items = (((data or {}).get("data") or []))
    for entry in items:
        obj = entry.get("object") or {}
        kind = obj.get("type")
        if kind not in {"answer", "article", "question"}:
            continue
        title = obj.get("title") or obj.get("question", {}).get("title") or ""
        url = obj.get("url") or f"https://www.zhihu.com/{kind}/{obj.get('id')}"
        excerpt = obj.get("excerpt") or obj.get("content") or ""
        ts = obj.get("created_time") or 0
        published = (
            datetime.utcfromtimestamp(int(ts)) if isinstance(ts, (int, float)) and ts else None
        )
        yield RawHit(
            title=title.strip(),
            url=url,
            source="zhihu",
            summary=excerpt.strip()[:280],
            body=excerpt,
            author=(obj.get("author") or {}).get("name"),
            published_at=published,
            score=int(obj.get("voteup_count") or 0),
            tags=("zhihu",),
        )