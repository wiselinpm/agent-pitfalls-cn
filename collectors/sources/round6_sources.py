"""Round 6 — 学术 / 个人 KOL / 政府安全 / Podcast / Twitter 镜像。"""
from __future__ import annotations
import logging, re, xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable
from ..base import RawHit
from ._http import http_get, http_get_json

_LOG = logging.getLogger("collectors.round6")


# === DBLP 学术数据库 ===
DBLP_QUERIES = [
    "LLM agent",
    "prompt injection",
    "RAG hallucination",
    "tool use language model",
    "code generation neural",
    "jailbreak LLM",
    "vector database",
    "embedding",
    "long context",
    "chain of thought",
    "agent benchmark",
]


class DblpCollector:
    name = "dblp"

    def collect(self) -> Iterable[RawHit]:
        for q in DBLP_QUERIES:
            yield from _fetch_dblp(q)


def _fetch_dblp(q: str) -> Iterable[RawHit]:
    """DBLP search API（公开）。"""
    try:
        data = http_get_json(
            "https://dblp.org/search/publ/api",
            params={"q": q, "format": "json", "h": 20},
            timeout=20,
        )
    except Exception as exc:
        _LOG.debug("dblp %r skipped: %s", q, exc)
        return
    if not isinstance(data, dict):
        return
    hits = (data.get("result") or {}).get("hits") or {}
    for h in hits.get("hit") or []:
        info = h.get("info") or {}
        title = (info.get("title") or "").strip()
        # 移除 XML 标记
        title = re.sub(r"<[^>]+>", "", title)
        url_out = info.get("ee") or info.get("url") or ""
        if not (title and url_out):
            continue
        year = info.get("year") or ""
        venue = info.get("venue") or ""
        authors_data = info.get("authors") or {}
        author_list = authors_data.get("author") or []
        if isinstance(author_list, list):
            author_str = ", ".join(a.get("text", "") for a in author_list[:3] if a.get("text"))
        else:
            author_str = ""
        if year:
            author_str = f"{author_str} ({year})" if author_str else f"({year})"
        yield RawHit(
            title=title,
            url=url_out,
            source=f"dblp:{q[:20]}",
            summary=f"{venue} ({year})" if venue else (f"DBLP paper ({year})" if year else "DBLP paper"),
            body=f"Venue: {venue}\nYear: {year}",
            author=author_str or None,
            tags=("dblp", f"q:{q}"),
        )


# === ACL Anthology ===
ACL_VENUES = [
    "acl", "emnlp", "naacl", "eacl", "aacl", "cl",
    "conll", "lrec", "coling", "tacl", "cl", "lattice",
]


class AclAnthologyCollector:
    name = "acl-anthology"

    def collect(self) -> Iterable[RawHit]:
        for year in [2023, 2024, 2025, 2026]:
            url = f"https://aclanthology.org/events/acl-{year}/"
            try:
                raw = http_get(url, timeout=30)
            except Exception as exc:
                _LOG.debug("acl %s skipped: %s", year, exc)
                continue
            yield from _parse_acl_html(raw.decode("utf-8", errors="ignore"), year)


def _parse_acl_html(html: str, year: int) -> Iterable[RawHit]:
    """简单解析 ACL Anthology HTML，提取 paper links。"""
    # 找 /papers/<id> 链接和标题
    paper_re = re.compile(r'<a[^>]+href="(/papers/[^"]+)"[^>]*>([^<]+)</a>', re.DOTALL)
    seen = set()
    for m in paper_re.finditer(html):
        url_path = m.group(1).strip()
        title = m.group(2).strip()
        title = re.sub(r"\s+", " ", title)
        if not (title and url_path) or url_path in seen or len(title) < 10:
            continue
        seen.add(url_path)
        url_out = f"https://aclanthology.org{url_path}"
        yield RawHit(
            title=title[:280],
            url=url_out,
            source=f"acl-anthology:{year}",
            summary=f"ACL Anthology paper ({year})",
            body=title,
            tags=("acl", f"year:{year}"),
        )


# === AAAI / NeurIPS / ICML proceedings（通过 OpenReview 公开）===
# Already covered by openreview collector


# === 个人 KOL 博客（Simon Willison / Ethan Mollick / Andrej Karpathy / Ben Thompson）===
KOL_BLOGS = [
    ("https://simonwillison.net/atom/everything/", "simon-willison"),
    ("https://www.oneusefulthing.org/feeds/posts/default", "ethan-mollick"),
    ("https://karpathy.github.io/feed.xml", "andrej-karpathy"),
    ("https://stratechery.com/feed/", "ben-thompson"),
    ("https://www.ben-evans.com/feed", "ben-evans"),
    ("https://a16z.com/feed/", "a16z"),
    ("https://bhorowitz.com/feed.rss", "ben-horowitz"),
    ("https://www.sequoiacap.com/feed/", "sequoia"),
    ("https://ycombinator.com/libsyn/rss", "yc-podcast"),
    ("https://lexfridman.com/feed/podcast/", "lex-fridman-podcast"),
    ("https://feeds.megaphone.fm/darknetdiaries", "darknet-diaries"),
    ("https://changelog.com/podcast/feed", "changelog-podcast"),
    ("https://feeds.simplecast.com/54nAGcIl", "twig-podcast"),
    ("https://feeds.transistor.fm/software-engineering-daily", "sedaily"),
    ("https://feeds.megaphone.fm/ridehome", "ride-home"),
    ("https://feeds.megaphone.fm/syntax", "syntax-fm"),
]


class KolBlogCollector:
    name = "kol-blog"

    def collect(self) -> Iterable[RawHit]:
        for url, source in KOL_BLOGS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("kol-blog %s skipped: %s", source, exc)
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


# === 政府 / 安全公告：CISA / NVD / US-CERT ===
GOV_SEC_FEEDS = [
    ("https://www.cisa.gov/news.xml", "cisa-news"),
    ("https://www.cisa.gov/cybersecurity-advisories.xml", "cisa-advisory"),
    ("https://nvd.nist.gov/download/nvd-rss.xml", "nvd-cve"),
    ("https://www.us-cert.gov/ncas/alerts.xml", "us-cert-alerts"),
    ("https://www.exploit-db.com/rss.xml", "exploit-db"),
    ("https://www.cvedetails.com/rss.php", "cvedetails"),
    ("https://www.virustotal.com/api/v3/feeds/popular_threat_categories", "vt-popular"),
]


class GovSecCollector:
    name = "gov-sec"

    def collect(self) -> Iterable[RawHit]:
        for url, source in GOV_SEC_FEEDS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("gov-sec %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# === Twitter / X 镜像（Nitter / Mastodon）===
# Nitter 镜像多数失效，但有些仍可用
NITTER_MIRRORS = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.1d4.us",
]

TWITTER_HANDLES = [
    "sama", "demishassabis", "JeffDean", "AndrewYNg", "karpathy",
    "simonw", "drjimfan", "rasbt", "jxmnop", "lmsysorg",
    "AnthropicAI", "OpenAI", "GoogleAI", "DeepMindAI", "huggingface",
    "staboratory", "hwchase17", "jerryjliu0", "LangChainAI",
    "omarsar0", "arankomatsuzaki", "rasbt", "denny_zhou",
    "percyliang", "yannlecun", "pmarca", "paulg", "ylecun",
]

MASTODON_INSTANCES = [
    "https://hachyderm.io",
    "https://mastodon.social",
    "https://infosec.exchange",
]


class TwitterMirrorCollector:
    name = "twitter-mirror"

    def collect(self) -> Iterable[RawHit]:
        # 试 Nitter
        for mirror in NITTER_MIRRORS:
            for handle in TWITTER_HANDLES[:5]:  # 仅试前 5 个，避免 429
                url = f"{mirror}/{handle}/rss"
                try:
                    raw = http_get(url, timeout=15)
                except Exception:
                    continue
                yield from _parse_rss(raw, f"nitter:{handle}")


# === Podcast RSS（专注 AI 相关）===
AI_PODCASTS = [
    ("https://lexfridman.com/feed/podcast/", "lex-fridman"),
    ("https://changelog.com/podcast/feed", "changelog"),
    ("https://softwareengineeringdaily.com/feed/", "sedaily"),
    ("https://feeds.megaphone.fm/darknetdiaries", "darknet-diaries"),
    ("https://feeds.megaphone.fm/syntax", "syntax-fm"),
    ("https://feeds.simplecast.com/JoR28o1x", "latent-space-podcast"),
    ("https://feeds.megaphone.fm/podsaveamerica", "podsaveamerica"),
    ("https://feeds.transistor.fm/codepen-radio", "codepen-radio"),
    ("https://feeds.megaphone.fm/smartless", "smartless"),
]


class PodcastCollector:
    name = "podcast"

    def collect(self) -> Iterable[RawHit]:
        for url, source in AI_PODCASTS:
            try:
                raw = http_get(url, timeout=20)
            except Exception as exc:
                _LOG.debug("podcast %s skipped: %s", source, exc)
                continue
            yield from _parse_rss(raw, source)


# === arxiv-sanity / alphaXiv / HF trending（替代源）===
class HfTrendingCollector:
    name = "hf-trending"

    def collect(self) -> Iterable[RawHit]:
        # HuggingFace trending models / datasets / spaces
        for kind in ["models", "datasets", "spaces"]:
            try:
                data = http_get_json(
                    f"https://huggingface.co/api/{kind}?full=true&limit=20",
                    timeout=20,
                )
            except Exception:
                continue
            if not isinstance(data, list):
                continue
            for item in data:
                item_id = item.get("id") or item.get("name", "")
                if not item_id:
                    continue
                url_out = f"https://huggingface.co/{kind}/{item_id}"
                tags = item.get("tags") or []
                # 只保留含 agent/llm/prompt 标签的
                if not any(t in ["agent", "llm", "rag", "prompt", "chatbot", "text-generation", "transformers"] for t in tags):
                    continue
                yield RawHit(
                    title=f"HF {kind}: {item_id}",
                    url=url_out,
                    source=f"hf-trending:{kind}",
                    summary=f"Tags: {', '.join(tags[:5])}",
                    body=f"HuggingFace trending {kind}: {item_id}\nTags: {', '.join(tags[:10])}",
                    score=int(item.get("downloads") or 0),
                    tags=(f"hf-{kind}", *tags[:3]),
                )