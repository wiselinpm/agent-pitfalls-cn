"""国内云厂商技术博客 RSS — 阿里云 / 腾讯云 / 华为云 / 字节跳动 / 美团 等。

这些 RSS 端点长期稳定，且 AI/agent 团队会分享实战踩坑经验。
"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.cloud_cn")


# 已验证可用的 RSS 端点
FEEDS = [
    # 阿里云 — 云栖 / 开发者社区
    ("https://developer.aliyun.com/feed", "aliyun-developer"),
    ("https://yq.aliyun.com/rss", "aliyun-yq"),
    # 腾讯云 — 开发者社区
    ("https://cloud.tencent.com/developer/feed", "tencent-cloud"),
    # 华为云 — 博客
    ("https://bbs.huaweicloud.com/blog/feed", "huaweicloud-blog"),
    # 美团技术团队（已有 meituan collector，这里加补充）
    ("https://tech.meituan.com/feed/", "meituan-tech"),
    # 字节跳动技术博客（公开 RSSHub 镜像）
    ("https://rsshub.app/bytedance/blog", "bytedance-blog"),
    # 哔哩哔哩技术
    ("https://rsshub.app/bilibili/tech/article", "bilibili-tech"),
    # 京东技术
    ("https://rsshub.app/jd-tech", "jd-tech"),
    # 滴滴技术
    ("https://rsshub.app/didichuxing/techblog", "didi-tech"),
    # 知乎专栏（通过 RSSHub，部分受限）
    ("https://rsshub.app/zhihu/people/activities/ai-agent", "zhihu-rsshub"),
    # 微信公众号 — 通过 RSSHub 公开镜像
    ("https://rsshub.app/wechat/mp/homepage?__url=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FaIEXeaGtQ", "wechat-mp"),
    # 即刻（公开 RSSHub）
    ("https://rsshub.app/jike/topic/55e1b8d2e16a44f414c0a3c9", "jike-ai"),
    # 少数派 sspai 已在独立 collector
    # 51CTO / 极客邦 — RSSHub
    ("https://rsshub.app/51cto/blog", "51cto"),
    ("https://rsshub.app/geekbang/column", "geekbang"),
]


class CloudCNCollector:
    name = "cloud-cn"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("cloud-cn %s skipped: %s", source, exc)
                continue
            yield from _parse(raw, source)


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.debug("parse fail %s: %s", source, exc)
        return
    items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not link:
            guid = item.findtext("guid")
            if guid:
                link = guid.strip()
        if not (title and link):
            continue
        desc = item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary") or ""
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}published")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        author = item.findtext("author") or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name") or ""
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=desc,
            author=author.strip() or None,
            published_at=dt,
        )