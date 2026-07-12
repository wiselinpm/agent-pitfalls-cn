"""B 站技术区视频采集 — 通过 bilibili 官方 API 和 RSSHub 公开镜像。

视频字幕本身需要登录态 + NLP 处理，超出本 collector 能力范围。本 collector
只抓「视频元数据 + 标题 + 简介」，由 normalize 层判断是否含 pitfall 关键词。
"""

from __future__ import annotations

import email.utils
import json
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.bilibili")


# B 站技术区 UP 主 / 关键词
FEEDS = [
    # 官方热门 RSS（公开 RSSHub 镜像，多数会 403；这里作为兜底）
    ("https://rsshub.app/bilibili/ranking/0/3/30", "bilibili-ranking-tech"),
    ("https://rsshub.app/bilibili/channel/knowledge", "bilibili-knowledge"),
    # 直接 RSS（如果可用）
    ("https://www.bilibili.com/rss/whitelist/knowledge.xml", "bilibili-knowledge-direct"),
]

# 通过 B 站 web API 搜索关键词（公开搜索 API）
SEARCH_QUERIES = [
    "Claude Code 踩坑",
    "Agent 内存泄漏",
    "LangChain 报错",
    "OpenAI Agents SDK 问题",
    "Prompt 注入",
    "RAG 实战 报错",
    "AI 工具调用 失败",
    "Cursor 使用 教程",
    "Function Calling 错误",
    "LLM 部署 失败",
]


class BilibiliCollector:
    name = "bilibili"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=15)
                yield from _parse_feed(raw, source)
            except Exception as exc:
                _LOG.debug("bilibili feed %s skipped: %s", url, exc)
                continue
        for q in SEARCH_QUERIES:
            yield from _search(q)


def _parse_feed(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    for item in root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not (title and link):
            continue
        desc = (item.findtext("description") or item.findtext("summary") or "").strip()
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = item.findtext("pubDate") or item.findtext("published")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            published_at=dt,
        )


def _search(q: str) -> Iterable[RawHit]:
    """B 站 web search 公开 API — 不需要登录。"""
    url = "https://api.bilibili.com/x/web-interface/search/type"
    try:
        data = http_get_json(
            url,
            params={"search_type": "video", "keyword": q, "page": 1, "page_size": 20},
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"},
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("bilibili search %r skipped: %s", q, exc)
        return
    if not isinstance(data, dict) or data.get("code") != 0:
        return
    items = (data.get("data") or {}).get("result") or []
    for item in items:
        title = (item.get("title") or "").strip()
        # 去除 <em> 标签
        title = re.sub(r"</?em[^>]*>", "", title)
        bvid = item.get("bvid")
        if not (title and bvid):
            continue
        url = f"https://www.bilibili.com/video/{bvid}"
        desc = (item.get("description") or "").strip()
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        author = (item.get("author") or "").strip()
        pub_ts = item.get("pubdate") or 0
        dt: datetime | None = None
        if pub_ts:
            try:
                dt = datetime.utcfromtimestamp(int(pub_ts))
            except (TypeError, ValueError, OSError):
                dt = None
        score = int(item.get("play") or 0) // 100 + int(item.get("like") or 0)
        yield RawHit(
            title=title,
            url=url,
            source="bilibili-search",
            summary=clean[:280],
            body=clean,
            author=author or None,
            published_at=dt,
            score=score,
            tags=("bilibili", f"q:{q}"),
        )