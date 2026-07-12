"""RSS 聚合器 — 通过 feedparser 解析任意 RSS/Atom feed，覆盖更多边缘博客。

与现有 rss.py 不同，本 collector 用更宽松的解析器（feedparser），
能容忍格式不规范的真实 feed。
"""

from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

import feedparser  # type: ignore

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.feed_aggregator")


# 边缘博客 / 个人技术博客 / 公司 dev blog
FEEDS = [
    # 个人深度博客
    ("https://martinfowler.com/feed.atom", "martin-fowler"),
    ("https://blog.codinghorror.com/rss/", "coding-horror"),
    ("https://overreacted.io/rss.xml", "overreacted-dan-abramov"),
    ("https://www.swyx.io/rss.xml", "swyx"),
    ("https://www.seangoedde.com/rss.xml", "sean-goedde"),
    ("https://timkellogg.me/rss.xml", "tim-kellogg"),
    # Python + AI
    ("https://realpython.com/atom.xml", "real-python"),
    ("https://www.pyimagesearch.com/feed/", "pyimagesearch"),
    # 数据库 / ML 平台
    ("https://www.timescale.com/blog/rss/", "timescale-blog"),
    ("https://supabase.com/blog/rss.xml", "supabase-blog"),
    ("https://blog.langchain.dev/rss.xml", "langchain-blog-direct"),
    # 国内额外
    ("https://coolshell.cn/feed", "coolshell"),
    ("https://www.ruanyifeng.com/blog/atom.xml", "ruanyifeng"),
    ("https://blog.csdn.net/rss.html", "csdn-top"),
    # 创业/产品
    ("https://ycombinator.com/blog/rss", "yc-blog"),
    ("https://www.lennysnewsletter.com/feed", "lenny-newsletter"),
    ("https://readwise.io/feed", "readwise"),
    # 教育
    ("https://www.deeplearning.ai/feed/", "deeplearning-ai"),
    ("https://www.fast.ai/atom.xml", "fastai"),
    # 设计 + AI
    ("https://www.smashingmagazine.com/feed/", "smashing-magazine"),
    # DevOps + AI
    ("https://www.thinktecture.com/en/feed/", "thinktecture"),
    ("https://blog.gitguardian.com/rss/", "gitguardian"),
    # 安全
    ("https://blog.trailofbits.com/feed/", "trailofbits"),
    ("https://www.schneier.com/feed/atom/", "schneier"),
    ("https://krebsonsecurity.com/feed/", "krebs-security"),
    ("https://www.darkreading.com/rss.xml", "dark-reading"),
    ("https://threatpost.com/feed/", "threatpost"),
    ("https://www.securityweek.com/feed", "securityweek"),
    # Stack Overflow blog
    ("https://stackoverflow.blog/feed/", "stackoverflow-blog"),
    # Netlify / Vercel blog
    ("https://www.netlify.com/blog/index.xml", "netlify-blog"),
    ("https://vercel.com/blog/rss.xml", "vercel-blog"),
    # Replit
    ("https://blog.replit.com/feed", "replit-blog"),
    # Twilio
    ("https://www.twilio.com/blog/feed", "twilio-blog"),
    # Cloudflare
    ("https://blog.cloudflare.com/rss/", "cloudflare-blog"),
    # Stripe
    ("https://stripe.com/blog/feed.rss", "stripe-blog"),
    # GitHub Engineering
    ("https://github.blog/engineering/feed/", "github-engineering"),
    ("https://github.blog/news-insights/feed/", "github-news"),
    # Discord Blog
    ("https://discord.com/blog/rss.xml", "discord-blog"),
    # Slack Engineering
    ("https://slack.engineering/feed/", "slack-engineering"),
]


class FeedAggregatorCollector:
    name = "feed-aggregator"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=25)
            except Exception as exc:
                _LOG.debug("feed-aggregator %s skipped: %s", source, exc)
                continue
            yield from _parse(raw, source)


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    parsed = feedparser.parse(raw)
    if parsed.bozo and not parsed.entries:
        return
    for entry in parsed.entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not (title and link):
            continue
        summary = entry.get("summary") or entry.get("description") or ""
        # 处理 Atom 多 content
        if not summary and "content" in entry and entry["content"]:
            try:
                summary = entry["content"][0].get("value", "")
            except (KeyError, IndexError, TypeError):
                summary = ""
        # 发布时间
        pub = entry.get("published_parsed") or entry.get("updated_parsed")
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime(*pub[:6])
            except (TypeError, ValueError):
                dt = None
        else:
            pub_str = entry.get("published") or entry.get("updated")
            if pub_str:
                try:
                    dt = parsedate_to_datetime(pub_str)
                except (TypeError, ValueError):
                    dt = None
        author = entry.get("author") or ""
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=summary[:280] if summary else "",
            body=summary,
            author=author or None,
            published_at=dt,
            tags=(source.split(":")[0],),
        )