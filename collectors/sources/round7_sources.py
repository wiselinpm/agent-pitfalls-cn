"""Round 7 — 全网覆盖再扩展。

覆盖 Round 1-6 仍存在的盲点：
- Stack Exchange 全站（ai/datascience/security/devops/superuser/serverfault/cs/cs.software）
- V2EX / NodeSeek 国内高质量开发者社区
- Towards Data Science / Better Programming / freeCodeCamp（Medium 顶级出版物）
- ACM Queue / Communications of the ACM / USENIX ;login:
- NeurIPS / ICLR / ICML proceedings（OpenReview 已覆盖，再加 dblp venue 索引）
- IEEE Xplore / ACM Digital Library RSS
- AWS re:Post / Google Cloud Community / Microsoft Q&A — 真实生产经验
- Quora — 问答
- Mastodon AI 时间线（hachyderm / fosstodon / social.linux.pizza）
- JetBrains / InfoQ EN / The New Stack / Smashing Magazine — 工程实践 blog
- 微信公众号 RSSHub 多账号（升级 sogou_wechat）
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


_LOG = logging.getLogger("collectors.round7")


# ===================================================================
# 1. Stack Exchange 全站 — 用 SE API 拉多个站点的 AI 相关问题
# ===================================================================
SE_SITES = [
    "ai",          # Artificial Intelligence
    "datascience",
    "security",
    "devops",
    "cs",
    "softwareengineering",
    "serverfault",
    "superuser",
    "softwarequality",
    "cs.software",
    "cs.ml",
    "cs.nlp",
    "cs.agents",
]

SE_QUERIES = [
    "LLM agent",
    "prompt injection",
    "jailbreak",
    "RAG hallucination",
    "tool calling failure",
    "context window overflow",
    "token limit exceeded",
    "embedding dimension mismatch",
    "vector database",
    "agent timeout",
    "agent loop",
    "rate limit 429",
    "OpenAI API error",
    "Anthropic Claude API",
    "LangChain memory",
    "agent evaluation",
    "AI security",
    "agent jailbreak",
    "fine-tuning failure",
    "inference cost",
    "GPU OOM",
    "model deployment",
    "function calling schema",
    "agent observability",
]


class StackExchangeMultiCollector:
    name = "stackexchange-multi"

    def collect(self) -> Iterable[RawHit]:
        # 策略：每个 site 用 2 个代表性 query（短 query 命中率高）
        # sites × queries 太多会触发 SE 配额（300/天），选代表性组合
        queries_per_site = [
            "LLM agent", "prompt injection", "RAG hallucination",
            "tool calling", "embedding", "rate limit 429",
            "OpenAI API", "LangChain", "vector database",
            "fine-tuning failure", "jailbreak", "agent timeout",
        ]
        for site in SE_SITES:
            # 每个 site 只跑 3 个 query 减少配额消耗
            for q in queries_per_site[:3]:
                yield from _fetch_se_site(site, q)


def _fetch_se_site(site: str, query: str) -> Iterable[RawHit]:
    """使用 Stack Exchange 公开 API（无 key 限制 quota 但有 rate-limit）。"""
    url = f"https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query[:200],
        "site": site,
        "pagesize": 30,
        "filter": "default",
    }
    try:
        data = http_get_json(url, params=params, timeout=20)
    except Exception as exc:
        _LOG.debug("se %s skipped: %s", site, exc)
        return
    if not isinstance(data, dict):
        return
    for item in data.get("items") or []:
        title = (item.get("title") or "").strip()
        link = item.get("link") or ""
        if not (title and link):
            continue
        tags = item.get("tags") or []
        score = int(item.get("score") or 0)
        is_answered = item.get("is_answered")
        view_count = int(item.get("view_count") or 0)
        answer_count = int(item.get("answer_count") or 0)
        creation_date = item.get("creation_date")
        dt = None
        if creation_date:
            try:
                dt = datetime.utcfromtimestamp(int(creation_date))
            except (TypeError, ValueError):
                dt = None
        owner = (item.get("owner") or {}).get("display_name") or ""
        summary_parts = [f"SE {site}", f"score={score}"]
        if is_answered:
            summary_parts.append(f"answered({answer_count})")
        if view_count:
            summary_parts.append(f"views={view_count}")
        yield RawHit(
            title=title[:280],
            url=link,
            source=f"stackexchange:{site}",
            summary=" · ".join(summary_parts),
            body=item.get("excerpt") or title,
            author=owner or None,
            score=score + (50 if is_answered else 0) + view_count // 100,
            published_at=dt,
            tags=("stackexchange", site, *tags[:5]),
        )


# ===================================================================
# 2. V2EX — 国内最活跃的开发者社区（公开 RSS）
# ===================================================================
V2EX_TABS = [
    "programmer",  # 程序员
    "ai",          # AI（新版块）
    "python",      # Python
    "javascript",  # JS
    "llm",         # LLM 相关
]

V2EX_RSS_BASE = "https://www.v2ex.com/feed"


class V2EXCollector:
    name = "v2ex"

    def collect(self) -> Iterable[RawHit]:
        for tab in V2EX_TABS:
            url = f"{V2EX_RSS_BASE}/{tab}.xml"
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("v2ex %s skipped: %s", tab, exc)
                continue
            yield from _parse_atom(raw, f"v2ex:{tab}")


# ===================================================================
# 3. NodeSeek — 国内新兴技术社区
# ===================================================================
NODESEEK_RSS = [
    ("https://rss.nodeseek.com/node/16", "nodeseek-tech"),
    ("https://rss.nodeseek.com/node/56", "nodeseek-ai"),
    ("https://rss.nodeseek.com/node/18", "nodeseek-dev"),
]


class NodeSeekCollector:
    name = "nodeseek"

    def collect(self) -> Iterable[RawHit]:
        for url, source in NODESEEK_RSS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("nodeseek %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 4. Towards Data Science / Better Programming / freeCodeCamp（Medium 子站）
# ===================================================================
TDS_FEEDS = [
    ("https://towardsdatascience.com/feed", "towards-data-science"),
    ("https://betterprogramming.pub/feed", "better-programming"),
    ("https://www.freecodecamp.org/news/rss/", "freecodecamp"),
    ("https://blog.bytebytego.com/feed", "bytebytego"),
    ("https://medium.com/feed/airbnb-engineering", "airbnb-eng"),
    ("https://medium.com/feed/pinterest-engineering", "pinterest-eng"),
    ("https://netflixtechblog.com/feed", "netflix-tech"),
    ("https://eng.uber.com/feed/", "uber-eng"),
    ("https://discord.com/blog/feed", "discord-blog"),
    ("https://slack.engineering/feed", "slack-eng"),
]


class TdsCollector:
    name = "tds-medium"

    def collect(self) -> Iterable[RawHit]:
        for url, source in TDS_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("tds %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 5. ACM Queue / Communications of the ACM / USENIX ;login:
# ===================================================================
ENG_BLOGS_PRACTICE = [
    ("https://queue.acm.org/rss-feed.cfm", "acm-queue"),
    ("https://cacm.acm.org/feed/", "cacm"),
    ("https://www.usenix.org/publications/loginonline/rss.xml", "usenix-login"),
    ("https://www.joelonsoftware.com/feed/", "joel-on-software"),
    ("https://feeds.feedburner.com/oreilly/radar", "oreilly-radar"),
    ("https://martinfowler.com/feed.atom", "martinfowler"),
    ("https://blog.codinghorror.com/rss/", "coding-horror"),
    ("https://www.smashingmagazine.com/feed/", "smashing-magazine"),
    ("https://css-tricks.com/feed/", "css-tricks"),
    ("https://overreacted.io/rss.xml", "overreacted-dan"),
    ("https://news.ycombinator.com/rss", "hn-frontpage"),
]


class AcmEngCollector:
    name = "acm-eng"

    def collect(self) -> Iterable[RawHit]:
        for url, source in ENG_BLOGS_PRACTICE:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("eng-blog %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 6. NeurIPS / ICLR / ICML proceedings — DBLP venue 索引
# ===================================================================
TOP_VENUES = [
    ("NeurIPS", "neurips-cc"),
    ("ICLR", "iclr-cc"),
    ("ICML", "icml-cc"),
    ("ACL", "acl-cc"),
    ("EMNLP", "emnlp-cc"),
    ("CCS", "ccs-cc"),
    ("IEEE S&P", "sp-cc"),
    ("NDSS", "ndss-cc"),
    ("USENIX Security", "usenix-sec-cc"),
    ("AAAI", "aaai-cc"),
    ("IJCAI", "ijcai-cc"),
]


class TopVenuesCollector:
    name = "top-venues"

    def collect(self) -> Iterable[RawHit]:
        for venue, tag in TOP_VENUES:
            yield from _fetch_dblp_venue(venue, tag)


def _fetch_dblp_venue(venue: str, tag: str) -> Iterable[RawHit]:
    """DBLP venue 搜索 — 拉最新一年 papers。"""
    try:
        data = http_get_json(
            "https://dblp.org/search/publ/api",
            params={"q": venue, "format": "json", "h": 30, "f": 0},
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("dblp venue %s skipped: %s", venue, exc)
        return
    if not isinstance(data, dict):
        return
    hits = (data.get("result") or {}).get("hits") or {}
    for h in hits.get("hit") or []:
        info = h.get("info") or {}
        title = re.sub(r"<[^>]+>", "", (info.get("title") or "").strip())
        url_out = info.get("ee") or info.get("url") or ""
        if not (title and url_out):
            continue
        year = info.get("year") or ""
        vvenue_raw = info.get("venue") or venue
        # venue 字段有时是 list（DBLP 多 venue）
        if isinstance(vvenue_raw, list):
            vvenue = ", ".join(str(v) for v in vvenue_raw)
        else:
            vvenue = str(vvenue_raw)
        # 仅保留匹配 venue 的
        if venue.lower() not in vvenue.lower():
            continue
        authors_data = info.get("authors") or {}
        author_list = authors_data.get("author") or []
        if isinstance(author_list, list):
            author_str = ", ".join(
                a.get("text", "") for a in author_list[:3] if a.get("text")
            )
        else:
            author_str = ""
        if year:
            author_str = f"{author_str} ({year})" if author_str else f"({year})"
        yield RawHit(
            title=title[:280],
            url=url_out,
            source=f"dblp-venue:{tag}",
            summary=f"{vvenue} ({year})",
            body=f"Venue: {vvenue}\nYear: {year}",
            author=author_str or None,
            score=int(year) if year and year.isdigit() else 0,
            tags=("dblp-venue", tag, vvenue.lower().replace(" ", "-")),
        )


# ===================================================================
# 7. IEEE Xplore / ACM DL RSS — 顶刊论文（公开 RSS 受限，多数失败但有 partial）
# ===================================================================
IEEE_FEEDS = [
    ("https://ieeexplore.ieee.org/rss/TOC34.xml", "ieee-tpami"),  # TPAMI
    ("https://cacm.acm.org/feed/", "cacm-rss"),
    ("https://feeds.acm.org/cmsfeed/feed.cfm?token=123", "acm-feed"),
]


class IeeeAcmCollector:
    name = "ieee-acm"

    def collect(self) -> Iterable[RawHit]:
        for url, source in IEEE_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("ieee-acm %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 8. AWS re:Post / Google Cloud Community / Microsoft Q&A — 真实生产经验
# ===================================================================
VENDOR_COMMUNITIES = [
    # AWS re:Post（基于 StackOverflow engine，RSS 较丰富）
    ("https://repost.aws/questions?RSS", "aws-repost"),
    ("https://repost.aws/tags/TAxl0kdmmzlqnoM9VVTcB8g/feed.rss", "aws-repost-ml"),
    # Google Cloud Community
    ("https://www.googlecloudcommunity.com/rss/board?board.id=ai-ml", "gcp-community-aiml"),
    ("https://www.googlecloudcommunity.com/rss/board?board.id=cloud-architecture", "gcp-community-arch"),
    # Microsoft Q&A
    ("https://learn.microsoft.com/en-us/answers/topics/azure-machine-learning.rss", "ms-qa-ml"),
    ("https://learn.microsoft.com/en-us/answers/topics/azure-openai-service.rss", "ms-qa-openai"),
    # CNCF / K8s 社区
    ("https://kubernetes.io/feed.xml", "kubernetes-blog"),
    ("https://www.cncf.io/feed/", "cncf-blog"),
    # JetBrains Blog
    ("https://blog.jetbrains.com/feed/", "jetbrains-blog"),
    # InfoQ EN
    ("https://www.infoq.com/ai-ml-dataengineering/machines.fp/", "infoq-en-ml"),
    ("https://www.infoq.com/architecture.fp/", "infoq-en-arch"),
    # The New Stack
    ("https://thenewstack.io/feed/", "the-new-stack"),
]


class VendorCommunityCollector:
    name = "vendor-community"

    def collect(self) -> Iterable[RawHit]:
        for url, source in VENDOR_COMMUNITIES:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("vendor-community %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# ===================================================================
# 9. Quora — 热门 AI 话题（公开 RSS 有限，用 google site: 兜底）
# ===================================================================
QUORA_QUERIES = [
    "LLM agent failure",
    "prompt injection",
    "OpenAI API issue",
    "LangChain bug",
    "Claude API",
    "RAG hallucination",
]


class QuoraCollector:
    name = "quora"

    def collect(self) -> Iterable[RawHit]:
        # Quora 反爬严，用 Brave Search 公开端点
        for q in QUORA_QUERIES:
            url = "https://search.brave.com/search"
            params = {"q": f"site:quora.com {q}"}
            try:
                raw = http_get(url, params=params, timeout=20)
            except Exception as exc:
                _LOG.debug("quora %s skipped: %s", q, exc)
                continue
            yield from _parse_brave_results(raw, f"quora:{q[:30]}")


def _parse_brave_results(html: bytes, source: str) -> Iterable[RawHit]:
    """简单解析 Brave Search HTML 提取链接。"""
    text = html.decode("utf-8", errors="ignore")
    # 抓 <a href="https://www.quora.com/..."> 标题
    link_re = re.compile(
        r'<a[^>]+href="(https?://(?:www\.)?quora\.com/[^"]+)"[^>]*>([^<]+)</a>',
        re.DOTALL,
    )
    seen: set[str] = set()
    for m in link_re.finditer(text):
        url = m.group(1)
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        if not title or url in seen or len(title) < 8:
            continue
        seen.add(url)
        yield RawHit(
            title=title[:280],
            url=url,
            source=source,
            summary=f"Quora result for {source}",
            body=title,
            tags=("quora",),
        )


# ===================================================================
# 10. Mastodon AI 时间线
# ===================================================================
MASTODON_INSTANCES = [
    "https://hachyderm.io",
    "https://fosstodon.org",
    "https://social.linux.pizza",
    "https://infosec.exchange",
]


class MastodonTimelineCollector:
    name = "mastodon-timeline"

    def collect(self) -> Iterable[RawHit]:
        # Mastodon 联邦时间线需要 OAuth，但 /api/v1/timelines/public 可匿名
        for inst in MASTODON_INSTANCES:
            url = f"{inst}/api/v1/timelines/public"
            params = {"limit": 20, "local": "true"}
            try:
                data = http_get_json(url, params=params, timeout=20)
            except Exception as exc:
                _LOG.debug("mastodon %s skipped: %s", inst, exc)
                continue
            if not isinstance(data, list):
                continue
            for status in data:
                content = re.sub(r"<[^>]+>", " ", status.get("content") or "").strip()
                if not content or len(content) < 20:
                    continue
                # 关键词过滤
                if not any(
                    kw in content.lower()
                    for kw in (
                        "agent", "llm", "ai ", "gpt", "claude", "openai", "prompt",
                        "rag", "tool", "embedding", "vector", "model",
                    )
                ):
                    continue
                status_id = status.get("id")
                if not status_id:
                    continue
                acct = (status.get("account") or {}).get("acct") or "anon"
                url_out = f"{inst}/@{acct}/{status_id}"
                yield RawHit(
                    title=content[:120].replace("\n", " "),
                    url=url_out,
                    source=f"mastodon:{inst.split('//')[1]}",
                    summary=content[:280],
                    body=content,
                    author=acct,
                    published_at=_parse_iso(status.get("created_at")),
                    score=int(status.get("reblogs_count") or 0) * 10
                    + int(status.get("favourites_count") or 0),
                    tags=("mastodon",),
                )


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


# ===================================================================
# 11. 微信公众号 RSSHub 多账号（升级 sogou_wechat）
# ===================================================================
WECHAT_RSSHUB_FEEDS = [
    # 知名 AI 公众号
    "https://rsshub.app/wechat/csjzxxh/gssh",  # 故事书
    "https://rsshub.app/wechat/coolshell/feed",
    "https://rsshub.app/wechat/qcloudcommunity/feed",
    "https://rsshub.app/wechat/alibabacloud/feed",
    "https://rsshub.app/wechat/tencent-cloud/feed",
    "https://rsshub.app/wechat/huaweicloud/feed",
    "https://rsshub.app/wechat/bytedancefe/feed",
    "https://rsshub.app/wechat/xiaomi-jfsc/feed",
    "https://rsshub.app/wechat/dop-ud-art/feed",
    "https://rsshub.app/wechat/juejin/feed",
    # AI 公众号
    "https://rsshub.app/wechat/qbitai/feed",      # 量子位
    "https://rsshub.app/wechat/jqr_zh/feed",      # 机器之心
    "https://rsshub.app/wechat/MetaPost/feed",    # 新智元
    "https://rsshub.app/wechat/AI_Thinker/feed",  # AI 科技评论
    "https://rsshub.app/wechat/aicfe/feed",       # 凸优化
    "https://rsshub.app/wechat/infoqchina/feed",  # InfoQ 中文
    "https://rsshub.app/wechat/codeceo/feed",     # 码农翻身
    "https://rsshub.app/wechat/zaodianshuo/feed", # 早安读书
    "https://rsshub.app/wechat/sspaime/feed",     # 少数派
]


class WechatRsshubCollector:
    name = "wechat-rsshub"

    def collect(self) -> Iterable[RawHit]:
        for url in WECHAT_RSSHUB_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("wechat-rsshub %s skipped: %s", url, exc)
                continue
            # 提取公众号 ID 作 source 名
            m = re.search(r"/wechat/([^/]+)/", url)
            tag = m.group(1) if m else "wechat"
            yield from _parse_rss(raw, f"wechat-rsshub:{tag}")


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


def _parse_atom(raw: bytes, source: str) -> Iterable[RawHit]:
    """Atom feed 解析（V2EX 等）。"""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", namespaces=ns) or "").strip()
        link_el = entry.find("a:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        if not (title and link):
            continue
        content_el = entry.find("a:content", ns) or entry.find("a:summary", ns)
        content = content_el.text if content_el is not None and content_el.text else ""
        content = re.sub(r"<[^>]+>", " ", content)
        content = re.sub(r"\s+", " ", content).strip()
        pub = entry.findtext("a:published", namespaces=ns) or entry.findtext(
            "a:updated", namespaces=ns
        )
        author_el = entry.find("a:author/a:name", ns)
        author = author_el.text.strip() if author_el is not None and author_el.text else None
        dt = _parse_iso(pub)
        yield RawHit(
            title=title[:280],
            url=link,
            source=source,
            summary=content[:280],
            body=content,
            author=author,
            published_at=dt,
            tags=(source.split(":")[0],),
        )