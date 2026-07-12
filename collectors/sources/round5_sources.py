"""Round 5 — 更多学术 / 趋势 / Reddit 备选 / Kaggle / Tech news 源。"""
from __future__ import annotations
import logging, re, xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable
from ..base import RawHit
from ._http import http_get, http_get_json

_LOG = logging.getLogger("collectors.round5")


# === Semantic Scholar — 学术论文数据库 ===
S2_QUERIES = [
    "LLM agent failure",
    "prompt injection attack",
    "tool use LLM",
    "RAG hallucination",
    "agent jailbreak",
    "indirect prompt injection",
    "chain of thought error",
    "code generation bug",
    "agent evaluation benchmark",
    "vector database pitfall",
    "embedding failure",
    "long context degradation",
    "LLM reasoning failure",
    "adversarial prompt",
    "alignment failure",
]


class SemanticScholarCollector:
    name = "semantic-scholar"

    def collect(self) -> Iterable[RawHit]:
        for q in S2_QUERIES:
            yield from _fetch_s2(q)


def _fetch_s2(q: str) -> Iterable[RawHit]:
    """Semantic Scholar Graph API — 公开 endpoint，无 key 限制（但有 RPS）。"""
    try:
        data = http_get_json(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params={
                "query": q,
                "limit": 20,
                "fields": "title,abstract,url,year,authors,venue,publicationDate,citationCount",
            },
            timeout=30,
        )
    except Exception as exc:
        _LOG.debug("semantic-scholar %r skipped: %s", q, exc)
        return
    if not isinstance(data, dict):
        return
    for p in data.get("data") or []:
        title = (p.get("title") or "").strip()
        url_out = p.get("url") or ""
        if not (title and url_out):
            continue
        abstract = p.get("abstract") or ""
        clean = re.sub(r"\s+", " ", abstract).strip()
        pub = p.get("publicationDate") or ""
        dt = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        authors = p.get("authors") or []
        author = ", ".join(a.get("name", "") for a in authors[:3] if a.get("name"))
        year = p.get("year")
        if year:
            author = f"{author} ({year})" if author else f"({year})"
        yield RawHit(
            title=title,
            url=url_out,
            source=f"semantic-scholar:{q[:30]}",
            summary=clean[:280] if clean else title[:280],
            body=clean,
            author=author or None,
            published_at=dt,
            score=int(p.get("citationCount") or 0),
            tags=("semantic-scholar", f"q:{q}"),
        )


# === GitHub Trending — 每日热门 repos ===
class GithubTrendingCollector:
    name = "github-trending"

    def collect(self) -> Iterable[RawHit]:
        # GitHub Trending 全语言 daily
        for lang, period in [
            ("", "daily"),
            ("python", "daily"),
            ("typescript", "daily"),
            ("go", "daily"),
            ("", "weekly"),
            ("python", "weekly"),
        ]:
            yield from _fetch_gh_trending(lang, period)


def _fetch_gh_trending(lang: str, period: str) -> Iterable[RawHit]:
    url = "https://github.com/trending"
    if lang:
        url += f"/{lang}"
    url += f"?since={period}"
    try:
        raw = http_get(url, timeout=30, headers={"Accept": "text/html"})
    except Exception as exc:
        _LOG.debug("github-trending %s/%s skipped: %s", lang, period, exc)
        return
    text = raw.decode("utf-8", errors="ignore")
    # 解析 article.h-entry li
    # 简化：正则提取 repo URL + description
    repo_re = re.compile(r'<h2[^>]*>\s*<a[^>]+href="(/[^"]+)"', re.DOTALL)
    desc_re = re.compile(r'<p class="col-9[^"]*">\s*(.+?)\s*</p>', re.DOTALL)
    repos = repo_re.findall(text)
    descs = desc_re.findall(text)
    for i, repo_path in enumerate(repos[:25]):
        repo_path = repo_path.strip()
        if not repo_path.startswith("/"):
            continue
        repo_path = repo_path.lstrip("/")
        url_out = f"https://github.com/{repo_path}"
        # 仓库名 = 最后一段
        title = f"GitHub Trending: {repo_path}"
        # 描述
        desc = ""
        if i < len(descs):
            desc = re.sub(r"<[^>]+>", " ", descs[i])
            desc = re.sub(r"\s+", " ", desc).strip()
        yield RawHit(
            title=title,
            url=url_out,
            source=f"github-trending:{lang or 'all'}/{period}",
            summary=desc[:280] if desc else f"Trending repository on GitHub ({period})",
            body=desc,
            tags=("github-trending", f"lang:{lang or 'all'}", f"period:{period}"),
        )


# === Kaggle Discussions / Competitions ===
class KaggleCollector:
    name = "kaggle-discussions"

    def collect(self) -> Iterable[RawHit]:
        # Kaggle 公开搜索：competitions + discussions
        for q in [
            "LLM agent",
            "LangChain",
            "prompt injection",
            "RAG hallucination",
            "AI safety",
        ]:
            yield from _fetch_kaggle(q)


def _fetch_kaggle(q: str) -> Iterable[RawHit]:
    # Kaggle discussion API
    try:
        data = http_get_json(
            "https://www.kaggle.com/api/v1/discussions/list",
            params={"search": q, "pageSize": 20},
            timeout=30,
        )
    except Exception as exc:
        _LOG.debug("kaggle %r skipped: %s", q, exc)
        return
    if not isinstance(data, dict):
        return
    threads = data.get("threads") or []
    for t in threads:
        title = (t.get("title") or "").strip()
        url_out = "https://www.kaggle.com" + (t.get("url") or "")
        if not (title and url_out):
            continue
        body = t.get("message") or t.get("snippet") or ""
        if isinstance(body, dict):
            body = body.get("text", "") or ""
        clean = re.sub(r"\s+", " ", str(body)).strip()
        yield RawHit(
            title=title,
            url=url_out,
            source=f"kaggle:{q[:30]}",
            summary=clean[:280] if clean else title[:280],
            body=clean,
            tags=("kaggle", f"q:{q}"),
        )


# === HackerNews Comments — 抓取高质量 comment thread ===
class HnCommentsCollector:
    name = "hn-comments"

    def collect(self) -> Iterable[RawHit]:
        # 拉取几个高 vote story 的所有 comments
        story_ids = [39881234, 39876543, 39895432]  # placeholder
        try:
            data = http_get_json(
                "https://hn.algolia.com/api/v1/search",
                params={"tags": "story", "numericFilters": "points>200", "hitsPerPage": 10},
                timeout=30,
            )
        except Exception:
            return
        for hit in data.get("hits") or []:
            oid = hit.get("objectID", "")
            if not oid:
                continue
            # 拉取该 story 的所有 comments
            try:
                comments_data = http_get_json(
                    f"https://hn.algolia.com/api/v1/items/{oid}",
                    timeout=30,
                )
            except Exception:
                continue
            yield from _walk_hn_comments(comments_data, hit)


def _walk_hn_comments(item: dict, parent_hit: dict) -> Iterable[RawHit]:
    """递归遍历 HN comment tree。"""
    if not isinstance(item, dict):
        return
    text = item.get("text") or ""
    if text and len(text) > 50:
        # Strip HTML
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        # 父 story URL
        url_out = item.get("url") or f"https://news.ycombinator.com/item?id={item.get('id')}"
        title = parent_hit.get("title", "HN discussion")
        author = item.get("author") or None
        yield RawHit(
            title=f"[HN comment on: {title}] {clean[:60]}...",
            url=url_out,
            source=f"hn-comments:{item.get('id')}",
            summary=clean[:280],
            body=clean,
            author=author,
            score=int(item.get("points") or 0),
            tags=("hackernews", "comment"),
        )
    for child in item.get("children") or []:
        yield from _walk_hn_comments(child, parent_hit)


# === Tech News RSS aggregator（techmeme / phoronix / theverge / arstechnica）===
TECH_NEWS_FEEDS = [
    ("https://www.techmeme.com/feed.xml", "techmeme"),
    ("https://www.theverge.com/rss/index.xml", "theverge"),
    ("https://feeds.arstechnica.com/arstechnica/index", "arstechnica"),
    ("https://www.wired.com/feed/rss", "wired"),
    ("https://www.technologyreview.com/feed/", "mit-tech-review"),
    ("https://www.zdnet.com/news/rss.xml", "zdnet"),
    ("https://www.infoworld.com/index.rss", "infoworld"),
    ("https://thenewstack.io/feed/", "thenewstack"),
    ("https://www.theregister.com/headlines.atom", "theregister"),
    ("https://www.bleepingcomputer.com/feed/", "bleepingcomputer"),
    ("https://krebsonsecurity.com/feed/", "krebsonsecurity"),
    ("https://www.darkreading.com/rss/all.xml", "darkreading"),
    ("https://threatpost.com/feed/", "threatpost"),
    ("https://www.securityweek.com/feed/", "securityweek"),
    ("https://feeds.feedburner.com/TheHackersNews", "the-hackers-news"),
    ("https://www.cyberscoop.com/feed/", "cyberscoop"),
]


class TechNewsCollector:
    name = "tech-news"

    def collect(self) -> Iterable[RawHit]:
        for url, source in TECH_NEWS_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("tech-news %s skipped: %s", source, exc)
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
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(pub)
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