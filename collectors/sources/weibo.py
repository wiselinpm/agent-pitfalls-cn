"""微博热搜 + 关键词搜索采集 — 通过公开搜索接口（无需登录）。

微博热搜榜单是公开的，但热搜本身主要是娱乐话题，技术相关少。
更实用的是通过 m.weibo.cn 公开搜索 API 抓技术博主的内容。
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.weibo")


# 已知技术博主 / 大 V — 抓他们最近发过的微博
TECH_BLOGGERS = [
    "1915541391",  # 宝玉
    "1652476120",  # 玉伯
    "1778742963",  # 邱锡鹏
    "1773294044",  # 微软亚研
    "5239570837",  # 差评君
    "5675606178",  # 老王
]

# 关键词搜索 query
SEARCH_QUERIES = [
    "Claude Code",
    "LangChain 报错",
    "AI Agent 部署",
    "Prompt 注入",
    "OpenAI Agents SDK",
    "RAG 踩坑",
    "LLM 工具调用",
    "Cursor 教程",
    "Aider 教程",
    "LangGraph 实战",
]


class WeiboCollector:
    name = "weibo"

    def collect(self) -> Iterable[RawHit]:
        # 1) 关键词搜索（公开 API）
        for q in SEARCH_QUERIES:
            yield from _search(q)
        # 2) 抓技术博主最近微博
        for uid in TECH_BLOGGERS:
            yield from _fetch_user(uid)


def _search(q: str) -> Iterable[RawHit]:
    """通过 m.weibo.cn 公开搜索 API。"""
    url = "https://m.weibo.cn/api/container/getIndex"
    try:
        data = http_get_json(
            url,
            params={
                "containerid": f"100103type=1&q={q}",
                "page_type": "searchall",
            },
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
                ),
                "Referer": "https://m.weibo.cn/",
            },
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("weibo search %r skipped: %s", q, exc)
        return
    cards = (data or {}).get("data", {}).get("cards") or []
    for card in cards:
        if card.get("card_type") != 9:  # 9 = 微博
            continue
        mblog = card.get("mblog") or {}
        text = (mblog.get("text") or "").strip()
        # 去除 HTML 标签
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        bid = mblog.get("bid") or mblog.get("id")
        if not (text and bid):
            continue
        # 提取标题：取前 60 字
        title = text[:80].strip()
        url = f"https://m.weibo.cn/detail/{bid}"
        user = mblog.get("user") or {}
        score = int(mblog.get("reposts_count") or 0) + int(mblog.get("comments_count") or 0) * 2 + int(mblog.get("attitudes_count") or 0)
        yield RawHit(
            title=title,
            url=url,
            source="weibo-search",
            summary=text[:280],
            body=text,
            author=(user.get("screen_name") if isinstance(user, dict) else None),
            published_at=_parse_ts(mblog.get("created_at")),
            score=score,
            tags=("weibo", f"q:{q}"),
        )


def _fetch_user(uid: str) -> Iterable[RawHit]:
    """抓某用户最近微博。"""
    url = "https://m.weibo.cn/api/container/getIndex"
    try:
        data = http_get_json(
            url,
            params={
                "containerid": f"107603{uid}",
                "page_type": "03",
            },
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
                ),
                "Referer": "https://m.weibo.cn/",
            },
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("weibo user %s skipped: %s", uid, exc)
        return
    cards = (data or {}).get("data", {}).get("cards") or []
    for card in cards[:10]:  # 每个用户最多取 10 条
        if card.get("card_type") != 9:
            continue
        mblog = card.get("mblog") or {}
        text = (mblog.get("text") or "").strip()
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        bid = mblog.get("bid") or mblog.get("id")
        if not (text and bid):
            continue
        title = text[:80].strip()
        url = f"https://m.weibo.cn/detail/{bid}"
        user = mblog.get("user") or {}
        score = int(mblog.get("reposts_count") or 0) + int(mblog.get("comments_count") or 0) * 2
        yield RawHit(
            title=title,
            url=url,
            source=f"weibo-user:{user.get('screen_name') if isinstance(user, dict) else uid}",
            summary=text[:280],
            body=text,
            author=(user.get("screen_name") if isinstance(user, dict) else None),
            published_at=_parse_ts(mblog.get("created_at")),
            score=score,
            tags=("weibo", f"uid:{uid}"),
        )


def _parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    # m.weibo.cn 返回 "Sat Jul 12 14:30:00 +0800 2026"
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(s)
    except Exception:
        return None