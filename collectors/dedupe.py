"""去重工具：URL 指纹 + 标题相似度。"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from urllib.parse import urlsplit, urlunsplit


_TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "source",
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
}


def url_fingerprint(url: str) -> str:
    """规范化 URL 并去除 tracking 参数，输出稳定指纹。"""
    parts = urlsplit(url.strip())
    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = re.sub(r"/+", "/", parts.path or "/")
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]
    query_pairs = []
    for kv in (parts.query or "").split("&"):
        if not kv or "=" not in kv:
            continue
        k, _, v = kv.partition("=")
        if k.lower() in _TRACKING_PARAMS:
            continue
        query_pairs.append((k, v))
    query_pairs.sort()
    query = "&".join(f"{k}={v}" for k, v in query_pairs)
    return urlunsplit((scheme, netloc, path, query, ""))


def title_similarity(a: str, a2: str) -> float:
    """标题相似度（0-1），忽略大小写与多余空白。"""
    na = re.sub(r"\s+", " ", a or "").strip().lower()
    nb = re.sub(r"\s+", " ", a2 or "").strip().lower()
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def is_likely_duplicate(
    url_a: str,
    url_b: str,
    title_a: str,
    title_b: str,
    *,
    title_threshold: float = 0.82,
) -> bool:
    """判定两个 hit 是否为同一坑。"""
    if url_fingerprint(url_a) == url_fingerprint(url_b):
        return True
    return title_similarity(title_a, title_b) >= title_threshold