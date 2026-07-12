"""Round 4 新源 — 填补全网覆盖的更多边缘 / 高质量源。

- arxiv 分类（cs.AI/cs.CL/cs.CR/cs.MA/cs.SE）— 拉最新一周的论文摘要
- 国内 engineering blog（字节/腾讯/阿里/小红书/京东等）
- GitHub platform changelog
- Anthropic research / OpenAI research
- 学术 newsletter（The Batch / AI Tidbits / Import AI）
"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.round4")


# === arXiv 分类 — 按主题聚合，最新一周 ===
ARXIV_CATEGORIES = [
    "cs.AI",  # 人工智能
    "cs.CL",  # 计算语言学
    "cs.CR",  # 安全
    "cs.MA",  # 多智能体
    "cs.SE",  # 软件工程
    "cs.LG",  # 机器学习
    "cs.IR",  # 信息检索
    "cs.HC",  # 人机交互
]


class ArxivCategoriesCollector:
    name = "arxiv-categories"

    def collect(self) -> Iterable[RawHit]:
        for cat in ARXIV_CATEGORIES:
            yield from _fetch_arxiv_cat(cat)


def _fetch_arxiv_cat(cat: str) -> Iterable[RawHit]:
    """按 arXiv 分类拉最新 20 篇（按 submittedDate 倒序）。"""
    url = "http://export.arxiv.org/api/query"
    try:
        raw = http_get(
            url,
            params={
                "search_query": f"cat:{cat}",
                "start": "0",
                "max_results": "20",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            },
            timeout=30,
        )
    except Exception as exc:
        _LOG.debug("arxiv cat %s skipped: %s", cat, exc)
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", namespaces=ns) or "").strip()
        link_el = entry.find("a:id", ns)
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        summary = (entry.findtext("a:summary", namespaces=ns) or "").strip()
        pub = entry.findtext("a:published", namespaces=ns)
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        if not (title and link):
            continue
        clean = re.sub(r"\s+", " ", summary)
        yield RawHit(
            title=title,
            url=link,
            source=f"arxiv-cat:{cat}",
            summary=clean[:280],
            body=clean,
            published_at=dt,
            score=1,
            tags=("arxiv", cat),
        )


# === 国内 engineering blog ===
CN_ENG_BLOGS = [
    # 字节跳动技术
    ("https://tech.bytedance.net/api/v1/articles/rss", "bytedance-tech"),
    # 美团技术（已有 meituan）
    # 腾讯云 / 腾讯技术
    ("https://cloud.tencent.com/developer/column/News/rss", "tencent-cloud"),
    # 阿里云开发者社区
    ("https://developer.aliyun.com/feed", "aliyun-developer"),
    # 京东技术 — 通过 RSSHub
    ("https://rsshub.app/jd/home", "jd-tech"),
    # 小红书技术 — 通过 RSSHub
    ("https://rsshub.app/xiaohongshu/explore", "xiaohongshu"),
    # 知乎日报 — 已有 zhihu-daily
    # 掘金 — 已失败
    # 微信小程序社区
    ("https://developers.weixin.qq.com/community/mp/rss", "weixin-mp"),
    # 飞书开放平台
    ("https://open.feishu.cn/community/forum/atom", "feishu-forum"),
    # 头条号 / Toutiao
    # 安全客 / FreeBuf — 已有
    # InfoQ 中文 — 已有
    # 阿里云栖社区
    ("https://yq.aliyun.com/feed", "aliyun-yq"),
    # 数据库内核月报（阿里云 RDS 团队）
    ("http://mysql.taobao.org/index/feed/", "taobao-mysql"),
    # 阿里中间件
    ("https://mp.weixin.qq.com/rss", "weixin-mp-rss"),
    # 网易云音乐技术
    ("https://music.163.com/feed", "netease-music-tech"),
    # Bilibili 技术 — 通过 RSSHub
    ("https://rsshub.app/bilibili/user/article/1566088477", "bilibili-tech-rsshub"),
    # 哔哩哔哩技术 — 同上
    # 奇安信技术研究院
    ("https://ti.qianxin.com/blog/feed", "qianxin-ti"),
    # 360 安全
    ("https://blogs.360.cn/feed", "qihoo-360"),
    # OPPO / Vivo 技术博客
    # 商汤技术
    ("https://www.sensetime.com/cn/feed", "sensetime"),
    # 旷视科技
    ("https://www.megvii.com/feed", "megvii"),
]


class CnEngBlogCollector:
    name = "cn-eng-blog"

    def collect(self) -> Iterable[RawHit]:
        for url, source in CN_ENG_BLOGS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("cn-eng-blog %s skipped: %s", source, exc)
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
        dt: datetime | None = None
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


# === GitHub Changelog ===
GITHUB_FEEDS = [
    ("https://github.blog/changelog/feed/", "github-changelog"),
    ("https://github.blog/news-insights/feed/", "github-news"),
    ("https://github.blog/engineering/feed/", "github-engineering"),
]


class GithubChangelogCollector:
    name = "github-changelog"

    def collect(self) -> Iterable[RawHit]:
        for url, source in GITHUB_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("github-changelog %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# === Anthropic / OpenAI research ===
RESEARCH_FEEDS = [
    ("https://www.anthropic.com/research/rss.xml", "anthropic-research"),
    ("https://openai.com/research/index.xml", "openai-research"),
    ("https://blog.google/technology/ai/rss/", "google-ai-blog"),
    ("https://deepmind.google/blog/rss.xml", "deepmind-blog"),
    ("https://huggingface.co/blog/feed.xml", "huggingface-blog-feed"),
    ("https://www.ai21.com/blog/rss.xml", "ai21-blog"),
    ("https://blog.together.ai/rss/", "together-blog"),
    ("https://www.deepset.ai/blog/rss.xml", "deepset-blog"),
    ("https://weaviate.io/blog/rss.xml", "weaviate-blog"),
    ("https://www.pinecone.io/blog/feed.xml", "pinecone-blog"),
    ("https://qdrant.tech/blog/rss.xml", "qdrant-blog"),
    ("https://www.elastic.co/blog/feed", "elastic-blog"),
    ("https://blog.langchain.dev/rss.xml", "langchain-blog-direct"),
    ("https://blog.llamaindex.ai/rss.xml", "llamaindex-blog-direct"),
    ("https://www.anyscale.com/blog/rss.xml", "anyscale-blog"),
    ("https://blog.crewai.com/rss/", "crewai-blog"),
]


class AiResearchBlogCollector:
    name = "ai-research-blog"

    def collect(self) -> Iterable[RawHit]:
        for url, source in RESEARCH_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("ai-research %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# === AI Newsletter 补充 ===
AI_NEWSLETTERS = [
    # The Batch (Andrew Ng)
    ("https://www.deeplearning.ai/the-batch/feed/", "the-batch"),
    # Import AI (Jack Clark)
    ("https://importai.substack.com/feed", "import-ai"),
    # AI Tidbits
    ("https://mnai.substack.com/feed", "ai-tidbits"),
    # Ben's Bites (已有)
    # Latent Space (已有)
    # Interconnects (已有)
    # Last Week in AI
    ("https://lastweekin.ai/feed", "last-week-in-ai"),
    # The Gradient
    ("https://thegradient.pub/rss/", "the-gradient"),
    # AI Snake Oil (已有)
    # One Useful Thing (已有)
    # The Rundown AI
    ("https://www.therundown.ai/feed", "the-rundown-ai"),
    # TLDR AI (已有)
    # Alpha Signal
    ("https://alphasignal.ai/feed", "alpha-signal"),
    # The Information AI
    # The Neuron
    ("https://www.theneurondaily.com/feed", "the-neuron"),
    # Mindstream
    ("https://www.mindstream.ai/feed", "mindstream"),
    # MLOps Substack
    ("https://mlops.substack.com/feed", "mlops-substack"),
    # Gradient Flow
    ("https://gradientflow.substack.com/feed", "gradient-flow"),
    # DataTalks.Club
    ("https://datatalks.club/feed", "data-talks-club"),
    # ML Conference Deadlines
    ("https://aideadlin.es/api/v1/feed.rss", "ai-deadlines"),
]


class AiNewsletterCollector:
    name = "ai-newsletter"

    def collect(self) -> Iterable[RawHit]:
        for url, source in AI_NEWSLETTERS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("ai-newsletter %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# === HackerNews comments via Algolia（高质量讨论）===
HN_STORIES = [
    # 显示层：score > 50 的 LLM agent 相关 story
    "https://hn.algolia.com/api/v1/search?tags=story&query=LLM%20agent%20failure&hitsPerPage=25",
    "https://hn.algolia.com/api/v1/search?tags=story&query=Claude%20Code%20bug&hitsPerPage=25",
    "https://hn.algolia.com/api/v1/search?tags=story&query=prompt%20injection&hitsPerPage=25",
    "https://hn.algolia.com/api/v1/search?tags=story&query=OpenAI%20hallucination&hitsPerPage=25",
    "https://hn.algolia.com/api/v1/search?tags=story&query=RAG%20production&hitsPerPage=25",
    "https://hn.algolia.com/api/v1/search?tags=story&query=vector%20database&hitsPerPage=25",
]


class HnAlgoliaExtendedCollector:
    name = "hn-algolia-extended"

    def collect(self) -> Iterable[RawHit]:
        for url in HN_STORIES:
            try:
                data = http_get_json(url, timeout=20)
            except Exception as exc:
                _LOG.debug("hn-algolia-ext %s skipped: %s", url[:60], exc)
                continue
            for hit in data.get("hits") or []:
                url_out = hit.get("url") or hit.get("story_url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                title = hit.get("title") or hit.get("story_title") or ""
                if not title:
                    continue
                yield RawHit(
                    title=title,
                    url=url_out,
                    source=f"hn-algolia-ext:{url.split('=')[1].split('&')[0] if '=' in url else 'unknown'}",
                    summary=(hit.get("story_text") or "")[:280],
                    body=hit.get("story_text") or "",
                    score=int(hit.get("points") or 0),
                    tags=("hackernews",),
                )