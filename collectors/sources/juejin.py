"""掘金 (Juejin) 采集 — 公开 API，无需鉴权。

覆盖国内 LLM/agent 开发者的实战文章与踩坑笔记。
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors")

# 掘金搜索 API — 不需要登录，公开
_SEARCH_URL = "https://api.juejin.cn/search/api/v1/search"

# 关键词覆盖 agent 开发常见坑
QUERIES = [
    "LangChain 踩坑",
    "Claude API 报错",
    "OpenAI Agents SDK 问题",
    "Prompt 注入",
    "LLM agent 内存泄漏",
    "Function calling 失败",
    "RAG 召回率低",
    "LangGraph 死循环",
    "Agent 工具调用超时",
    "MCP 协议",
]

# 类别 ID：后端、AI、工具
CATEGORY_IDS = ["6809637767543259144", "6809637769959178254"]  # 后端、AI


class JuejinCollector:
    name = "juejin"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            for cat in CATEGORY_IDS:
                payload = {
                    "keyword": q,
                    "search_type": "article",
                    "cursor": "0",
                    "limit": 20,
                    "sort_type": 2,  # 按热度
                    "version": 1,
                    "category_id": cat,
                }
                try:
                    raw = http_get(
                        _SEARCH_URL,
                        params=payload,
                        headers={
                            "User-Agent": (
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
                            ),
                            "Content-Type": "application/json",
                            "Referer": "https://juejin.cn/",
                        },
                    )
                    data = json.loads(raw.decode("utf-8"))
                except Exception as exc:
                    _LOG.debug("juejin %r/%s skipped: %s", q, cat, exc)
                    continue

                # 新版 API 返回结构略有差异，做兼容
                entries = (
                    (data or {}).get("data", {}).get("result", [])
                    if isinstance((data or {}).get("data"), dict)
                    else (data or {}).get("data", [])
                )
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    hit = _to_hit(entry, q)
                    if hit:
                        yield hit


def _to_hit(entry: dict, query: str) -> RawHit | None:
    title = (entry.get("title") or entry.get("article_info", {}).get("title") or "").strip()
    if not title:
        return None
    article_id = entry.get("article_id") or entry.get("id") or ""
    url = f"https://juejin.cn/post/{article_id}" if article_id else (entry.get("url") or "")
    if not url:
        return None

    info = entry.get("article_info") or {}
    summary = (
        info.get("brief_content")
        or info.get("content")
        or entry.get("description")
        or ""
    ).strip()[:280]

    # 时间戳（毫秒）
    ts_ms = info.get("ctime") or entry.get("ctime") or 0
    published = None
    try:
        if ts_ms:
            published = datetime.utcfromtimestamp(int(ts_ms) / 1000)
    except (ValueError, TypeError, OSError):
        published = None

    user = info.get("author") or entry.get("user") or {}
    author = user.get("user_name") or user.get("name")

    return RawHit(
        title=title[:120],
        url=url,
        source="juejin",
        summary=summary,
        body=summary,
        author=author,
        published_at=published,
        score=int(entry.get("view_count") or entry.get("hot_rank") or 0),
        tags=("juejin", query),
    )