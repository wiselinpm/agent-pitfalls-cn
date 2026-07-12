"""Round 4 续 — 更多国内外源。"""
from __future__ import annotations
import email.utils, logging, re, xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable
from ..base import RawHit
from ._http import http_get, http_get_json

_LOG = logging.getLogger("collectors.round4_more")

CN_TECH_MEDIA = [
    ("https://www.36kr.com/feed", "36kr"),
    ("https://www.huxiu.com/rss/0.xml", "huxiu"),
    ("https://www.geekpark.net/rss", "geekpark"),
    ("https://www.ithome.com/rss/", "ithome"),
    ("https://www.tmtpost.com/rss", "tmtpost"),
    ("https://www.jiqizhixin.com/rss", "jiqizhixin"),
    ("https://rsshub.app/36kr/information/AI", "36kr-ai"),
    ("https://rsshub.app/huxiu/ai", "huxiu-ai"),
    ("https://rsshub.app/ithome/tag/AI", "ithome-ai"),
    ("https://rsshub.app/ithome/tag/agent", "ithome-agent"),
    ("https://rsshub.app/jiqizhixin/articles", "jiqizhixin-articles"),
]


class CnTechMediaCollector:
    name = "cn-tech-media"
    def collect(self) -> Iterable[RawHit]:
        for url, source in CN_TECH_MEDIA:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("cn-tech-media %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


def _parse_rss(raw: bytes, source: str) -> Iterable[RawHit]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    items = root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not link:
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
        pub = (
            item.findtext("pubDate")
            or item.findtext("{http://www.w3.org/2005/Atom}published")
            or item.findtext("{http://www.w3.org/2005/Atom}updated")
        )
        dt = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                try:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                except ValueError:
                    dt = None
        yield RawHit(
            title=title,
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            published_at=dt,
            tags=(source.split("-")[0],),
        )


# === Reddit proxy — 用 HN 搜索 reddit.com 引用 ===
REDDIT_PROXY_QUERIES = [
    "site:reddit.com Claude Code",
    "site:reddit.com LangChain",
    "site:reddit.com LLM agent",
    "site:reddit.com prompt injection",
    "site:reddit.com OpenAI agents",
    "site:reddit.com jailbreak",
]


class RedditProxyCollector:
    name = "reddit-proxy"
    def collect(self) -> Iterable[RawHit]:
        for q in REDDIT_PROXY_QUERIES:
            try:
                data = http_get_json(
                    "https://hn.algolia.com/api/v1/search",
                    params={"query": q, "tags": "story", "hitsPerPage": 25},
                    timeout=20,
                )
            except Exception as exc:
                _LOG.debug("reddit-proxy %s skipped: %s", q, exc)
                continue
            for hit in data.get("hits") or []:
                url_out = hit.get("url") or hit.get("story_url") or ""
                if "reddit.com" not in url_out:
                    continue
                title = hit.get("title") or hit.get("story_title") or ""
                if not title:
                    continue
                yield RawHit(
                    title=title,
                    url=url_out,
                    source=f"reddit-proxy:{q[:30]}",
                    summary=(hit.get("story_text") or "")[:280],
                    body=hit.get("story_text") or "",
                    score=int(hit.get("points") or 0),
                    tags=("reddit", "via-hn"),
                )


# === Discourse 公共论坛（langchain/gradio/aider）===
DISCOURSE_FEEDS = [
    ("https://discuss.langchain.dev/posts.rss", "langchain-discourse"),
    ("https://github.com/langchain-ai/langchain/discussions.atom", "langchain-discussions"),
    ("https://github.com/run-llama/llama_index/discussions.atom", "llamaindex-discussions"),
    ("https://github.com/microsoft/autogen/discussions.atom", "autogen-discussions"),
    ("https://github.com/crewAIInc/crewAI/discussions.atom", "crewai-discussions"),
    ("https://github.com/openai/openai-python/discussions.atom", "openai-python-discussions"),
    ("https://github.com/anthropics/anthropic-sdk-python/discussions.atom", "anthropic-sdk-discussions"),
    ("https://github.com/BerriAI/litellm/discussions.atom", "litellm-discussions"),
    ("https://github.com/Aider-AI/aider/discussions.atom", "aider-discussions"),
    ("https://github.com/cline/cline/discussions.atom", "cline-discussions"),
    ("https://github.com/openai/openai-agents-python/discussions.atom", "openai-agents-discussions"),
    ("https://github.com/microsoft/semantic-kernel/discussions.atom", "semantic-kernel-discussions"),
    ("https://github.com/vercel/ai/discussions.atom", "vercel-ai-discussions"),
    ("https://github.com/mastra-ai/mastra/discussions.atom", "mastra-discussions"),
    ("https://github.com/letta-ai/letta/discussions.atom", "letta-discussions"),
]


class DiscourseCollector:
    name = "discourse-forums"
    def collect(self) -> Iterable[RawHit]:
        for url, source in DISCOURSE_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("discourse %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)