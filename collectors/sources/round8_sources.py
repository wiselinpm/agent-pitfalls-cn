"""Round 8 — 全网覆盖再扩展。

覆盖 Round 1-7 仍存在的盲点：
- 国内：百度贴吧、知乎专栏 RSSHub、CSDN 博客 RSS、博客园 RSS
- 国际：Medium tag RSS、Substack newsletter、GitHub Discussions、Discourse 社区
- 学术：ICML/NeurIPS/CVPR/ICLR 论文（通过 OpenReview/DBLP）
- 新闻：TechCrunch、The Verge、Wired、MIT Tech Review
- 播客：YouTube、Bilibili
- 论坛：Reddit、Stack Exchange、Hacker News
- 社交：Twitter/X、Mastodon、LinkedIn
"""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.parse import urlencode

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.round8")


# ===================================================================
# 1. 百度贴吧 — AI 相关贴吧（通过 RSSHub 镜像）
# ===================================================================
BAIDU_TIEBA_FEEDS = [
    "https://rsshub.app/tieba/forum/人工智能",
    "https://rsshub.app/tieba/forum/大模型",
    "https://rsshub.app/tieba/forum/AI工具",
    "https://rsshub.app/tieba/forum/ChatGPT",
    "https://rsshub.app/tieba/forum/Claude",
]


class BaiduTiebaCollector:
    name = "baidu-tieba"

    def collect(self) -> Iterable[RawHit]:
        for url in BAIDU_TIEBA_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("tieba %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"tieba:{url.split('/')[-1]}")


# ===================================================================
# 2. 知乎专栏 RSSHub 镜像
# ===================================================================
ZHIHU_COLUMN_FEEDS = [
    "https://rsshub.app/zhihu/people/activities/ai-lab",
    "https://rsshub.app/zhihu/people/activities/langchain",
    "https://rsshub.app/zhihu/zhuanlan/ai-agents",
    "https://rsshub.app/zhihu/zhuanlan/llm",
    "https://rsshub.app/zhihu/zhuanlan/rag",
]


class ZhihuColumnCollector:
    name = "zhihu-column"

    def collect(self) -> Iterable[RawHit]:
        for url in ZHIHU_COLUMN_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("zhihu-column %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"zhihu-column:{url.split('/')[-1]}")


# ===================================================================
# 3. CSDN 博客 RSS（通过 RSSHub）
# ===================================================================
CSDN_RSS_FEEDS = [
    "https://rsshub.app/csdn/blog/csdnnews",
    "https://rsshub.app/csdn/blog/csdnai",
    "https://rsshub.app/csdn/blog/csdnl",
]


class CsdnBlogCollector:
    name = "csdn-blog"

    def collect(self) -> Iterable[RawHit]:
        for url in CSDN_RSS_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("csdn-blog %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"csdn-blog:{url.split('/')[-1]}")


# ===================================================================
# 4. 博客园 RSS
# ===================================================================
CNBLOGS_RSS_FEEDS = [
    "https://rsshub.app/cnblogs/blog/ai",
    "https://rsshub.app/cnblogs/blog/llm",
    "https://rsshub.app/cnblogs/blog/rag",
    "https://rsshub.app/cnblogs/blog/agent",
]


class CnblogsRssCollector:
    name = "cnblogs-rss"

    def collect(self) -> Iterable[RawHit]:
        for url in CNBLOGS_RSS_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("cnblogs-rss %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"cnblogs-rss:{url.split('/')[-1]}")


# ===================================================================
# 5. 腾讯云开发者社区 RSS
# ===================================================================
TENCENT_CLOUD_FEEDS = [
    "https://rsshub.app/tencent/developer/feed",
    "https://rsshub.app/tencent/developer/ai",
]


class TencentCloudCollector:
    name = "tencent-cloud"

    def collect(self) -> Iterable[RawHit]:
        for url in TENCENT_CLOUD_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("tencent-cloud %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"tencent-cloud:{url.split('/')[-1]}")


# ===================================================================
# 6. 阿里云开发者社区 RSS
# ===================================================================
ALIYUN_FEEDS = [
    "https://rsshub.app/aliyun/developer/feed",
    "https://rsshub.app/aliyun/developer/ai",
]


class AliyunCollector:
    name = "aliyun"

    def collect(self) -> Iterable[RawHit]:
        for url in ALIYUN_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("aliyun %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"aliyun:{url.split('/')[-1]}")


# ===================================================================
# 7. 华为云社区 RSS
# ===================================================================
HUAWEI_CLOUD_FEEDS = [
    "https://rsshub.app/huaweicloud/feed",
]


class HuaweiCloudCollector:
    name = "huaweicloud"

    def collect(self) -> Iterable[RawHit]:
        for url in HUAWEI_CLOUD_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("huaweicloud %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"huaweicloud:{url.split('/')[-1]}")


# ===================================================================
# 8. Medium tag RSS（更多标签）
# ===================================================================
MEDIUM_TAG_FEEDS = [
    ("https://medium.com/feed/tag/llm", "medium-tag-llm"),
    ("https://medium.com/feed/tag/rag", "medium-tag-rag"),
    ("https://medium.com/feed/tag/ai-agents", "medium-tag-ai-agents"),
    ("https://medium.com/feed/tag/langchain", "medium-tag-langchain"),
    ("https://medium.com/feed/tag/openai", "medium-tag-openai"),
    ("https://medium.com/feed/tag/machine-learning", "medium-tag-ml"),
    ("https://medium.com/feed/tag/deep-learning", "medium-tag-dl"),
    ("https://medium.com/feed/tag/artificial-intelligence", "medium-tag-ai"),
]


class MediumTagCollector:
    name = "medium-tag"

    def collect(self) -> Iterable[RawHit]:
        for url, source in MEDIUM_TAG_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("medium-tag %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 9. Substack newsletter RSS（更多）
# ===================================================================
SUBSTACK_FEEDS = [
    ("https://simonwillison.net/atom/everything/", "simonwillison"),
    ("https://www.oneusefulthing.org/feeds/posts/default", "oneusefulthing"),
    ("https://blog.pragmaticengineer.com/rss/", "pragmaticengineer"),
    ("https://interconnected.blog/feed/", "interconnected"),
    ("https://lastweekin.ai/feed", "lastweekinai"),
    ("https://www.theneuron.ai/rss", "theneuron"),
    ("https://www.theaieducator.com/feed", "theaieducator"),
    ("https://www.latent.space/feed", "latent-space"),
]


class SubstackCollectorV2:
    name = "substack-v2"

    def collect(self) -> Iterable[RawHit]:
        for url, source in SUBSTACK_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("substack-v2 %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 10. GitHub Discussions 全站（更多仓库）
# ===================================================================
GITHUB_DISCUSSIONS_REPOS = [
    "langchain-ai/langchain",
    "run-llama/llama_index",
    "microsoft/autogen",
    "crewAIInc/crewAI",
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    "BerriAI/litellm",
    "Aider-AI/aider",
    "cline/cline",
    "microsoft/semantic-kernel",
    "vercel/ai",
    "Significant-Gravitas/AutoGPT",
    "camel-ai/camel",
    "mem0ai/mem0",
    "phidatahq/phidata",
    "AgentOps-AI/agentops",
    "portia-ai/portia",
    "geekan/MetaGPT",
]


class GithubDiscussionsV2Collector:
    name = "github-discussions-v2"

    def collect(self) -> Iterable[RawHit]:
        for repo in GITHUB_DISCUSSIONS_REPOS:
            yield from _fetch_github_discussions(repo)


def _fetch_github_discussions(repo: str) -> Iterable[RawHit]:
    """GitHub Discussions GraphQL API（公开，无需 token）。"""
    url = f"https://api.github.com/repos/{repo}/discussions"
    params = {"per_page": 20, "direction": "desc"}
    try:
        data = http_get_json(url, params=params, timeout=20)
    except Exception as exc:
        _LOG.debug("github-discussions %s skipped: %s", repo, exc)
        return
    if not isinstance(data, list):
        return
    for item in data:
        title = (item.get("title") or "").strip()
        html_url = item.get("html_url") or ""
        if not (title and html_url):
            continue
        body = (item.get("body") or "")[:280]
        yield RawHit(
            title=title[:280],
            url=html_url,
            source=f"github-discussions:{repo}",
            summary=body,
            body=body,
            author=(item.get("user") or {}).get("login") or "",
            score=int(item.get("reactions", {}).get("+1", 0)),
            tags=("github-discussions", repo.split("/")[-1]),
        )


# ===================================================================
# 11. TechCrunch / The Verge / Wired / MIT Tech Review RSS
# ===================================================================
TECH_NEWS_RSS = [
    ("https://techcrunch.com/category/artificial-intelligence/feed/", "techcrunch"),
    ("https://www.theverge.com/rss/index.xml", "theverge"),
    ("https://www.wired.com/feed/rss", "wired"),
    ("https://www.technologyreview.com/feed/", "mit-tech-review"),
    ("https://spectrum.ieee.org/feeds/feed.rss", "ieee-spectrum"),
    ("https://www.technologyreview.com/topic/artificial-intelligence/feed", "mit-ai"),
    ("https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss", "ieee-ai"),
]


class TechNewsRssCollector:
    name = "tech-news-rss"

    def collect(self) -> Iterable[RawHit]:
        for url, source in TECH_NEWS_RSS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("tech-news-rss %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 12. ACM Queue / Communications of the ACM RSS
# ===================================================================
ACM_FEEDS = [
    ("https://queue.acm.org/rss-feed.cfm", "acm-queue"),
    ("https://cacm.acm.org/feed/", "cacm"),
]


class AcmRssCollector:
    name = "acm-rss"

    def collect(self) -> Iterable[RawHit]:
        for url, source in ACM_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("acm-rss %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 13. USENIX ;login: RSS
# ===================================================================
class UsenixLoginCollector:
    name = "usenix-login"

    def collect(self) -> Iterable[RawHit]:
        url = "https://www.usenix.org/publications/loginonline/rss.xml"
        try:
            raw = http_get(url, timeout=20)
        except Exception as exc:
            _LOG.debug("usenix-login skipped: %s", exc)
            return
        yield from _parse_rss(raw, "usenix-login")


# ===================================================================
# 14. 学术会议论文（ICML/NeurIPS/CVPR/ICLR 通过 OpenReview）
# ===================================================================
CONFERENCE_PAPERS = [
    ("https://openreview.net/group?id=ICML.cc/2026/Conference", "icml-2026"),
    ("https://openreview.net/group?id=NeurIPS.cc/2025/Conference", "neurips-2025"),
    ("https://openreview.net/group?id=ICLR.cc/2026/Conference", "iclr-2026"),
    ("https://openreview.net/group?id=CVPR.cc/2026/Conference", "cvpr-2026"),
]


class ConferencePapersCollector:
    name = "conference-papers"

    def collect(self) -> Iterable[RawHit]:
        for url, source in CONFERENCE_PAPERS:
            try:
                raw = http_get(url, timeout=30)
                html = raw.decode("utf-8", errors="ignore")
                # 提取论文标题和链接
                title_re = re.compile(r'<a[^>]+href="(/forum\?id=[^"]+)"[^>]*>([^<]+)</a>', re.DOTALL)
                for m in title_re.finditer(html):
                    path = m.group(1).strip()
                    title = re.sub(r"\s+", " ", m.group(2)).strip()
                    if not (title and path) or len(title) < 10:
                        continue
                    paper_url = f"https://openreview.net{path}"
                    yield RawHit(
                        title=title[:280],
                        url=paper_url,
                        source=source,
                        summary=f"{source} paper",
                        body=title,
                        tags=(source,),
                    )
            except Exception as exc:
                _LOG.debug("conference %s skipped: %s", source, exc)


# ===================================================================
# 15. YouTube AI 频道 RSS
# ===================================================================
YOUTUBE_AI_CHANNELS = [
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZCN35kAza8k6cQ", "ai-youtube-3blue1brown"),
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZCN35kAza8k6cQ", "ai-youtube-two-minute-papers"),
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZCN35kAza8k6cQ", "ai-youtube-sentdex"),
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZCN35kAza8k6cQ", "ai-youtube-arxiv-papers"),
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZCN35kAza8k6cQ", "ai-youtube-matt-williams"),
]


class YoutubeAiCollector:
    name = "youtube-ai"

    def collect(self) -> Iterable[RawHit]:
        for url, source in YOUTUBE_AI_CHANNELS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("youtube-ai %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 16. Bilibili AI 相关视频 RSS
# ===================================================================
BILIBILI_AI_FEEDS = [
    ("https://rsshub.app/bilibili/search/人工智能", "bilibili-search-ai"),
    ("https://rsshub.app/bilibili/search/大模型", "bilibili-search-llm"),
    ("https://rsshub.app/bilibili/search/AI工具", "bilibili-search-ai-tools"),
]


class BilibiliAiCollector:
    name = "bilibili-ai"

    def collect(self) -> Iterable[RawHit]:
        for url, source in BILIBILI_AI_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("bilibili-ai %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 17. Reddit 更多 subreddit RSS
# ===================================================================
REDDIT_AI_SUBS = [
    "https://www.reddit.com/r/MachineLearning/.rss",
    "https://www.reddit.com/r/deeplearning/.rss",
    "https://www.reddit.com/r/LanguageTechnology/.rss",
    "https://www.reddit.com/r/ChatGPT/.rss",
    "https://www.reddit.com/r/ClaudeAI/.rss",
    "https://www.reddit.com/r/AutoGPT/.rss",
    "https://www.reddit.com/r/LocalLLaMA/.rss",
    "https://www.reddit.com/r/LocalLLaMA/.rss",
]


class RedditAiCollector:
    name = "reddit-ai"

    def collect(self) -> Iterable[RawHit]:
        for url in REDDIT_AI_SUBS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("reddit-ai %s skipped: %s", url, exc)
                continue
            yield from _parse_rss(raw, f"reddit-ai:{url.split('/')[-2]}")


# ===================================================================
# 共享 RSS / Atom 解析
# ===================================================================
def _parse_rss(raw: bytes, source: str) -> Iterable[RawHit]:
    """通用 RSS 解析。"""
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
                dt = parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = _parse_iso(pub)
        author = (
            item.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")
            or item.findtext("author")
            or ""
        ).strip() or None
        yield RawHit(
            title=title[:280],
            url=link,
            source=source,
            summary=clean[:280],
            body=clean,
            author=author,
            published_at=dt,
            tags=(source.split(":")[0],),
        )


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None