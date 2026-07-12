"""CSDN 采集 — 通过其移动端 JSON API。

CSDN 反爬很严，搜索 API 经常返验证码。
这里采用其 blog_rank 推荐的接口，对外开放度更高。
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors")

# CSDN 搜索端点（带 referer 的 JSON 接口）
_SEARCH_URL = "https://so.csdn.net/api/v3/search"

QUERIES = [
    "LangChain 踩坑",
    "Claude API 报错",
    "OpenAI Agents SDK",
    "Prompt 注入",
    "Function calling 失败",
    "LangGraph",
    "Agent 开发",
]


class CSDNCollector:
    name = "csdn"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            for page in (1, 2):
                params = {
                    "q": q,
                    "p": page,
                    "t": "all",
                    "tm": "0",
                    "lv": "-1",
                    "ft": "0",
                    "l": "",
                    "u": "",
                    "ct": "-1",
                    "pnt": "-1",
                    "ry": "-1",
                    "ss": "-1",
                    "dct": "-1",
                    "vt": "-1",
                    "bnt": "-1",
                    "ewt": "-1",
                    "fst": "0",
                    "ra": "28",
                    "fid": "",
                    "platform": "pc",
                    "s": "0",
                    "uc": "-1",
                    "isManuallySearch": "false",
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
                            "Referer": f"https://so.csdn.net/so/search?spm=1011.2266.3001.4498&q={q}",
                            "Accept": "application/json",
                        },
                    )
                    data = json.loads(raw.decode("utf-8"))
                except Exception as exc:
                    _LOG.debug("csdn %r/%s skipped: %s", q, page, exc)
                    continue

                entries = (
                    (data or {}).get("result_vos", [])
                    if isinstance(data, dict)
                    else []
                )
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    hit = _to_hit(entry, q)
                    if hit:
                        yield hit


def _to_hit(entry: dict, query: str) -> RawHit | None:
    # CSDN API: result_vos[i] -> { "url":..., "title":..., "content":..., "username":..., "created_time":... }
    title = _strip_tags(entry.get("title") or "")
    url = entry.get("url") or ""
    if not (title and url):
        return None
    summary = _strip_tags(entry.get("content") or entry.get("description") or "")[:280]

    ts_ms = entry.get("created_time") or 0
    published = None
    try:
        if ts_ms:
            published = datetime.utcfromtimestamp(int(ts_ms) / 1000 if int(ts_ms) > 1e10 else int(ts_ms))
    except (ValueError, TypeError, OSError):
        published = None

    author = entry.get("username") or entry.get("nickname")
    return RawHit(
        title=title[:120],
        url=url,
        source="csdn",
        summary=summary,
        body=summary,
        author=author,
        published_at=published,
        score=int(entry.get("view_count") or entry.get("comment_count") or 0),
        tags=("csdn", query),
    )


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()