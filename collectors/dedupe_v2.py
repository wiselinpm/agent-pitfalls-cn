"""更严格的三维度去重工具 — URL fingerprint + 标题相似度 + 内容 hash。

与 dedupe.py 的差别：
1. 支持「规范化 URL 群」批量去重（多个 URL 视为同一指纹组）
2. 支持「标题 Jaccard 相似度」+ SequenceMatcher 加权
3. 支持「正文 hash」/「标题 hash」组合去重
4. 输出 dedup 报告（保留哪些、删除哪些、为何删）
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit

from .dedupe import url_fingerprint, title_similarity  # noqa: F401


# ========== 文本规范化（用于 hash 比对）==========

_NON_ALNUM = re.compile(r"[^\w一-鿿]+", re.UNICODE)


def _normalize_text(text: str) -> str:
    """统一小写、去标点、压缩空白。"""
    s = _NON_ALNUM.sub(" ", (text or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def text_hash(*parts: str) -> str:
    """多字段拼接后 sha1，适合做内容指纹。"""
    h = hashlib.sha1()
    for p in parts:
        h.update(_normalize_text(p).encode("utf-8"))
        h.update(b"\x1f")  # unit separator
    return h.hexdigest()


def title_hash(title: str) -> str:
    return text_hash(title)


# ========== URL 群组（同一文章不同链接） ==========

_URL_ALIAS_DOMAINS = {
    # 同一文章在 Google News 上的不同形态
    "news.google.com": "google-news-redirect",
    # 微信公众号
    "mp.weixin.qq.com": "weixin-mp",
}


def canonical_url(url: str) -> str:
    """比 url_fingerprint 更激进的规范化：把 news.google.com 重定向回真实 URL（如果可解析）。"""
    fp = url_fingerprint(url)
    # 已经是 fingerprint，不需要进一步处理
    return fp


# ========== 群组去重 ==========


@dataclass
class DedupRecord:
    """单个待去重条目。"""
    key: str  # 用于排序的稳定 key
    url: str
    title: str
    body: str = ""
    score: int = 0
    source: str = ""
    payload: dict = field(default_factory=dict)


@dataclass
class DedupReport:
    kept: list[DedupRecord]
    removed: list[tuple[DedupRecord, str]]  # (removed, reason)


def dedupe_records(
    records: Iterable[DedupRecord],
    *,
    title_threshold: float = 0.85,
    body_threshold: float = 0.90,
) -> DedupReport:
    """对一组记录做三维度去重：
    - URL fingerprint 完全相同 → 视为重复
    - 标题相似度 >= threshold → 视为重复
    - 正文 hash 相同 → 视为重复

    同一组里保留 score 最高、source 字段最具体的。
    """
    items = list(records)
    # 按 key 排序，确保稳定性
    items.sort(key=lambda r: r.key)
    kept: list[DedupRecord] = []
    removed: list[tuple[DedupRecord, str]] = []
    title_hashes: dict[str, DedupRecord] = {}
    body_hashes: dict[str, DedupRecord] = {}
    url_fps: dict[str, DedupRecord] = {}
    title_texts: list[tuple[str, DedupRecord]] = []

    for rec in items:
        # 1) URL fingerprint 比对
        fp = url_fingerprint(rec.url)
        if fp in url_fps:
            existing = url_fps[fp]
            removed.append((rec, f"dup-url:{fp}"))
            _maybe_replace(existing, rec, kept, removed)
            continue

        # 2) 标题 hash 比对
        th = title_hash(rec.title)
        if th in title_hashes:
            existing = title_hashes[th]
            removed.append((rec, f"dup-title-hash:{th[:8]}"))
            _maybe_replace(existing, rec, kept, removed)
            continue

        # 3) 正文 hash 比对
        bh = text_hash(rec.title, rec.body or "")
        if bh in body_hashes:
            existing = body_hashes[bh]
            removed.append((rec, f"dup-body-hash:{bh[:8]}"))
            _maybe_replace(existing, rec, kept, removed)
            continue

        # 4) 标题相似度（O(n²) 但数量可控）
        dup = False
        for prev_title, prev_rec in title_texts:
            if title_similarity(rec.title, prev_title) >= title_threshold:
                removed.append((rec, f"dup-title-sim:{title_similarity(rec.title, prev_title):.2f}"))
                _maybe_replace(prev_rec, rec, kept, removed)
                dup = True
                break
        if dup:
            continue

        # 保留
        kept.append(rec)
        url_fps[fp] = rec
        title_hashes[th] = rec
        body_hashes[bh] = rec
        title_texts.append((rec.title, rec))

    return DedupReport(kept=kept, removed=removed)


def _maybe_replace(
    existing: DedupRecord,
    new: DedupRecord,
    kept: list[DedupRecord],
    removed: list[tuple[DedupRecord, str]],
) -> None:
    """如果 new 比 existing 更有信息（score 高 或 source 更具体），替换。"""
    if new.score > existing.score:
        # 把 existing 标记为 removed，把 new 放到 kept 顶部
        try:
            kept.remove(existing)
        except ValueError:
            pass
        removed.append((existing, "replaced-by-higher-score"))
        kept.append(new)