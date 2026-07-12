"""搜狗微信搜索 — 公开搜索页（无需 API key）。

搜狗的 https://weixin.sogou.com/weixin 会把公众号文章索引到搜索结果里，
返回 HTML。我们从中抽取标题/链接/摘要/sourcename。

注意：搜狗有 IP 频控，单次请求建议带较长 User-Agent 和随机 Referer。
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from html import unescape
from typing import Iterable
from urllib.parse import unquote

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.sogou_wechat")


# 中文 agent 坑相关关键词（与 zhihu/juejin 互补）
QUERIES = [
    "Claude Code 报错",
    "LangChain 报错",
    "OpenAI Agents SDK 问题",
    "Agent 内存泄漏",
    "Prompt 注入",
    "RAG 踩坑",
    "LLM 工具调用",
    "AI Agent 部署",
]


_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class SogouWeChatCollector:
    name = "sogou-wechat"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES:
            try:
                html = http_get(
                    "https://weixin.sogou.com/weixin",
                    params={"type": "2", "query": q, "ie": "utf8"},
                    headers={
                        "User-Agent": _UA,
                        "Referer": "https://weixin.sogou.com/",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                    },
                    timeout=20,
                ).decode("utf-8", errors="ignore")
            except Exception as exc:
                _LOG.debug("sogou-wechat %r skipped: %s", q, exc)
                continue
            yield from _parse(html, q)


def _parse(html: str, query: str) -> Iterable[RawHit]:
    # 搜狗返回结构：<div class="vr-title">...</div> 包含标题 + 公众号名 + 时间
    # 链接格式：/link?url=base64(实际 url) — 我们保留原始 weixin.sogou.com 链接
    # 但 RawHit.url 用实际文章 url（解码后），方便点击。
    item_re = re.compile(
        r'<div[^>]+class="vr-title"[^>]*>(.*?)</div>\s*</a>',
        re.S | re.I,
    )
    href_re = re.compile(r'<a[^>]+href="([^"]+)"', re.I)
    txt_re = re.compile(r"<[^>]+>")
    time_re = re.compile(
        r'<div class="vr-time"[^>]*>(.*?)</div>', re.S | re.I
    )

    # 退化方案：抓取每个 <li class="news-list">/ <div class="vrwrap">
    blocks = re.split(r'<div class="vr-wrap[^"]*"', html)
    if len(blocks) <= 1:
        # 兜底：直接每条 result 用 mini-block
        blocks = re.split(r'<div class="vr-title">', html)

    for blk in blocks[1:]:
        title_m = re.search(
            r'<a[^>]+>(.*?)</a>', blk[:600], re.S | re.I
        )
        if not title_m:
            continue
        title_raw = title_m.group(1)
        title = txt_re.sub("", title_raw).strip()
        if not title:
            continue
        href_m = href_re.search(blk[:600])
        if not href_m:
            continue
        href = href_m.group(1)
        # sogou 把真 url 编码在 /link?url=... 里
        real = ""
        if "url=" in href:
            try:
                real = unquote(href.split("url=", 1)[1].split("&", 1)[0])
            except Exception:
                real = ""
        real_url = real or ("https://weixin.sogou.com" + href if href.startswith("/") else href)
        time_m = time_re.search(blk[:1200])
        pub_text = txt_re.sub("", time_m.group(1)).strip() if time_m else ""
        score = 0
        summary_text = unescape(title)
        yield RawHit(
            title=unescape(title),
            url=real_url,
            source="sogou-wechat",
            summary=summary_text[:280],
            body=summary_text,
            published_at=None,
            score=score,
            tags=("wechat", f"q:{query}"),
            raw_metadata={"sogou_href": href, "pub_text": pub_text},
        )