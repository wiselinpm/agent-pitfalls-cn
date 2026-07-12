"""SegmentFault (思否) 采集 — 公开 API。

国内老牌技术问答社区，文章质量较高。
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors")

# SegmentFault 公开搜索
_SEARCH_URL = "https://api.segmentfault.com/search"

QUERIES = [
    "LangChain",
    "Claude API",
    "OpenAI Function calling",
    "Prompt 注入",
    "LangGraph",
    "AutoGen",
    "CrewAI",
    "agent 工具调用",
]


class SegmentFaultCollector:
    name = "segmentfault"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            for page in (1, 2):
                params = {
                    "q": q,
                    "page": page,
                    "pagesize": 20,
                    "order": "newest",
                    "type": "article",
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
                            "Referer": "https://segmentfault.com/search",
                        },
                    )
                    data = json.loads(raw.decode("utf-8"))
                except Exception as exc:
                    _LOG.debug("segmentfault %r/%s skipped: %s", q, page, exc)
                    continue

                # 响应：{ "status":0, "data": { "rows": [...], "total":N } }
                rows = (
                    (data or {}).get("data", {}).get("rows", [])
                    if isinstance((data or {}).get("data"), dict)
                    else []
                )
                if not isinstance(rows, list):
                    continue
                for entry in rows:
                    hit = _to_hit(entry, q)
                    if hit:
                        yield hit


def _to_hit(entry: dict, query: str) -> RawHit | None:
    title = (entry.get("title") or "").strip()
    if not title:
        return None

    # 优先用 url 字段；否则按 id 拼
    url = entry.get("url") or ""
    if not url and entry.get("id"):
        url = f"https://segmentfault.com/a/{entry['id']}"

    # 补全相对 URL
    if url.startswith("/"):
        url = f"https://segmentfault.com{url}"

    if not url:
        return None

    excerpt = (entry.get("excerpt") or entry.get("content") or entry.get("description") or "").strip()[:280]
    author = (entry.get("user") or {}).get("name") or entry.get("author")

    ts = entry.get("created") or entry.get("create_time") or 0
    published = None
    try:
        if ts:
            published = datetime.utcfromtimestamp(int(ts))
    except (ValueError, TypeError, OSError):
        published = None

    return RawHit(
        title=title[:120],
        url=url,
        source="segmentfault",
        summary=excerpt,
        body=excerpt,
        author=author,
        published_at=published,
        score=int(entry.get("votes") or entry.get("recommend") or entry.get("hot") or 0),
        tags=("segmentfault", query),
    )