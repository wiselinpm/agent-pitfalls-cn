"""Brave Search 公共页采集 — 不需要 API key。

Brave Search 在公开 HTML 里返回真实的搜索结果，没有 Bing 那样的 CAPTCHA 拦截。
我们对每个 query 抓一次 HTML，从 `<div data-type="web">` 里抽取 title/url/snippet。

限制：Brave 在频繁请求时会返回 429，需要 sleep。匿名 IP 大约 30 req/min 限额。
"""

from __future__ import annotations

import logging
import re
import time
from html import unescape
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.brave_search")


_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _brave_results(query: str, count: int = 20) -> Iterable[RawHit]:
    try:
        html = http_get(
            "https://search.brave.com/search",
            params={"q": query, "source": "web"},
            headers={
                "User-Agent": _UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            },
            timeout=25,
        ).decode("utf-8", errors="ignore")
    except Exception as exc:
        _LOG.debug("brave %r skipped: %s", query, exc)
        return

    # Brave 把每条结果放在 <div data-type="web" data-keynav="true">…</div>
    # 标题：<a class="result-header" href="…"><span class="snippet-title" title="…">…</span></a>
    # 摘要：<p class="snippet-description">…</p>
    blocks = re.findall(
        r'<div[^>]+data-type="web"[^>]*>(.*?)(?=<div[^>]+data-type="web"|</main)',
        html,
        re.S | re.I,
    )
    n = 0
    for blk in blocks:
        if n >= count:
            break
        href_m = re.search(
            r'<a[^>]+class="result-header"[^>]+href="([^"]+)"',
            blk,
            re.I,
        )
        if not href_m:
            # 兜底：任何指向外部链接的 a 标签
            href_m = re.search(
                r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*result',
                blk,
                re.I,
            )
        if not href_m:
            continue
        url = unescape(href_m.group(1))
        if "brave.com" in url:
            continue
        # 标题
        title_m = re.search(
            r'<span[^>]+class="[^"]*snippet-title[^"]*"[^>]*title="([^"]+)"',
            blk,
            re.I,
        )
        if not title_m:
            title_m = re.search(
                r'<span[^>]+class="[^"]*snippet-title[^"]*"[^>]*>(.*?)</span>',
                blk,
                re.S | re.I,
            )
            if title_m:
                title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
            else:
                title = url
        else:
            title = title_m.group(1)
        # 摘要
        snip_m = re.search(
            r'<p[^>]+class="[^"]*snippet-description[^"]*"[^>]*>(.*?)</p>',
            blk,
            re.S | re.I,
        )
        snippet = ""
        if snip_m:
            snippet = re.sub(r"<[^>]+>", " ", snip_m.group(1))
            snippet = re.sub(r"\s+", " ", snippet).strip()
        if not title:
            continue
        yield RawHit(
            title=unescape(title),
            url=url,
            source="brave-search",
            summary=snippet[:280],
            body=snippet,
            published_at=None,
            score=1,
            tags=("brave", f"q:{query}"),
        )
        n += 1


# ====== 不同领域的 query 集 ======

ZHIHU_QUERIES = [
    "site:zhihu.com agent 避坑",
    "site:zhihu.com Claude Code 报错",
    "site:zhihu.com LangChain 内存",
    "site:zhihu.com Prompt 注入",
    "site:zhihu.com OpenAI Agents SDK",
    "site:zhihu.com LLM 工具调用",
    "site:zhihu.com RAG 踩坑",
    "site:zhihu.com Function Calling 问题",
    "site:zhihu.com Cursor 踩坑",
    "site:zhihu.com Aider 坑",
]

JUEJIN_QUERIES = [
    "site:juejin.cn LangChain 踩坑",
    "site:juejin.cn Claude API 报错",
    "site:juejin.cn AI Agent 部署",
    "site:juejin.cn Prompt 注入",
    "site:juejin.cn RAG 优化",
    "site:juejin.cn OpenAI Agents SDK",
    "site:juejin.cn Function Calling 报错",
    "site:juejin.cn Cursor 使用 坑",
    "site:juejin.cn Aider 教程 问题",
    "site:juejin.cn LangGraph 实战",
]

REDDIT_QUERIES = [
    "site:reddit.com Claude Code bug",
    "site:reddit.com LangChain error",
    "site:reddit.com OpenAI agents SDK issue",
    "site:reddit.com Anthropic prompt injection",
    "site:reddit.com RAG hallucination",
    "site:reddit.com agent memory leak",
]

GENERIC_QUERIES = [
    "LLM agent prompt injection 2026",
    "Claude Code rate limit 429",
    "OpenAI Agents SDK breaking change",
    "LangGraph state persistence bug",
    "Cursor IDE indexing slow",
    "Aider repo map not working",
    "agent tool call hallucination",
    "RAG retrieval quality pitfall",
]