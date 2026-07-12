"""厂商 changelog / status / 官方 RSS 补充源 — 覆盖更多国内外厂商。"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.vendor_official")


FEEDS = [
    # Replicate changelog
    ("https://replicate.com/changelog/rss", "replicate-changelog"),
    # OpenAI Cookbook
    ("https://github.com/openai/openai-cookbook/commits/main.atom", "openai-cookbook-commits"),
    # Anthropic cookbook
    ("https://github.com/anthropics/claude-cookbook/commits/main.atom", "anthropic-cookbook-commits"),
    # HuggingFace blog & changelog
    ("https://huggingface.co/blog/feed.xml", "huggingface-blog"),
    ("https://github.com/huggingface/transformers/releases.atom", "transformers-releases"),
    # Microsoft AutoGen
    ("https://github.com/microsoft/autogen/releases.atom", "autogen-releases"),
    # Microsoft Semantic Kernel
    ("https://github.com/microsoft/semantic-kernel/releases.atom", "semantic-kernel-releases"),
    # Haystack (deepset)
    ("https://github.com/deepset-ai/haystack/releases.atom", "haystack-releases"),
    # Hugging Face smolagents
    ("https://github.com/huggingface/smolagents/releases.atom", "smolagents-releases"),
    # LlamaIndex
    ("https://github.com/run-llama/llama_index/releases.atom", "llamaindex-releases"),
    # Mistral AI
    ("https://github.com/mistralai/client-python/releases.atom", "mistral-releases"),
    # Cohere
    ("https://github.com/cohere-ai/cohere-python/releases.atom", "cohere-releases"),
    # Together AI
    ("https://github.com/togethercomputer/together-python/releases.atom", "together-releases"),
    # Anyscale
    ("https://github.com/ray-project/ray/releases.atom", "ray-releases"),
    # GitLab.com explore trending
    ("https://gitlab.com/explore/projects/trending.atom", "gitlab-trending"),
    # Papers with Code RSS
    ("https://paperswithcode.com/feed.rss", "papers-with-code-feed"),
    # 国内
    # 字节技术博客
    ("https://blog.cloudcachetx.com/feed", "cloudcachetx"),
    # 美团技术（已有 meituan）
    # 京东技术（已有 cloud-cn 但 RSSHub 失效）
    ("https://www.infoq.cn/rss/topic/ai.rss", "infoq-ai"),
    ("https://www.infoq.cn/rss/topic/cloud.rss", "infoq-cloud"),
    ("https://www.infoq.cn/rss/topic/architecture.rss", "infoq-arch"),
    # Bilibili 公开排行榜 — 仅 RSS 端点
    ("https://rsshub.app/bilibili/hot-search", "bilibili-hot"),
    # 知乎日报
    ("https://rsshub.app/zhihu/daily", "zhihu-daily"),
    # 安全资讯 — 安全客
    ("https://api.anquanke.com/data/v1/rss", "anquanke"),
    # FreeBuf
    ("https://www.freebuf.com/feed", "freebuf"),
]


class VendorOfficialCollector:
    name = "vendor-official"

    def collect(self) -> Iterable[RawHit]:
        for url, source in FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("vendor %s skipped: %s", source, exc)
                continue
            yield from _parse(raw, source)


def _parse(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    items = root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not link:
            guid = item.findtext("guid")
            if guid:
                link = guid.strip()
            # Atom link
            atom_link = item.find("{http://www.w3.org/2005/Atom}link")
            if atom_link is not None:
                href = atom_link.get("href")
                if href:
                    link = href
        if not (title and link):
            continue
        desc = (
            item.findtext("description")
            or item.findtext("{http://www.w3.org/2005/Atom}summary")
            or item.findtext("{http://www.w3.org/2005/Atom}content")
            or ""
        ).strip()
        clean = re.sub(r"<[^>]+>", " ", desc)
        clean = re.sub(r"\s+", " ", clean).strip()
        pub = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}published") or item.findtext("{http://www.w3.org/2005/Atom}updated")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                try:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                except ValueError:
                    dt = None
        author = (
            item.findtext("author")
            or item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")
            or ""
        ).strip()
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            author=author or None,
            published_at=dt,
            tags=(source.split(":")[0],),
        )