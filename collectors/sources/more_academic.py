"""学术论文补充源 — OpenReview / PapersWithCode / arXiv 分类。

OpenReview：NeurIPS / ICML / ICLR 等顶会论文，含 reviewer 评审意见（本身就是 bug 报告）
PapersWithCode：论文 + benchmark 趋势，含论文 + 评测坑
"""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get, http_get_json


_LOG = logging.getLogger("collectors.more_academic")


# OpenReview API — 公开
OPENREVIEWS = [
    # NeurIPS 2024+5 顶会
    "NeurIPS.cc/2024/Conference",
    "NeurIPS.cc/2025/Conference",
    "ICML.cc/2024/Conference",
    "ICML.cc/2025/Conference",
    "ICLR.cc/2025/Conference",
    # 单独 Workshop：agent / safety
    "NeurIPS.cc/2024/Workshop/Agents",
    "NeurIPS.cc/2024/Workshop/AI_Safety",
    "NeurIPS.cc/2024/Workshop/Large_Language_Model_Agents",
]


class OpenReviewCollector:
    name = "openreview"

    def collect(self) -> Iterable[RawHit]:
        for venue in OPENREVIEWS:
            yield from _fetch_openreview(venue)


def _fetch_openreview(venue: str) -> Iterable[RawHit]:
    """OpenReview Notes API：返回指定 venue 的论文/评论。"""
    url = "https://api2.openreview.net/notes/search"
    try:
        data = http_get_json(
            url,
            params={
                "query": "LLM agent OR prompt injection OR jailbreak OR safety",
                "group": venue,
                "limit": 25,
            },
            timeout=30,
        )
    except Exception as exc:
        _LOG.debug("openreview %s skipped: %s", venue, exc)
        return
    if not isinstance(data, dict):
        return
    notes = data.get("notes") or []
    for n in notes:
        content = n.get("content") or {}
        title = content.get("title", {}).get("value") if isinstance(content.get("title"), dict) else content.get("title")
        if not title:
            continue
        abstract = content.get("abstract", {}).get("value") if isinstance(content.get("abstract"), dict) else content.get("abstract", "")
        nid = n.get("id", "")
        url_out = f"https://openreview.net/forum?id={nid}"
        # published date
        cdate = n.get("cdate") or 0
        dt: datetime | None = None
        if cdate:
            try:
                dt = datetime.utcfromtimestamp(int(cdate) / 1000)
            except (TypeError, ValueError, OSError):
                dt = None
        clean_abs = re.sub(r"\s+", " ", abstract or "")
        yield RawHit(
            title=title,
            url=url_out,
            source=f"openreview:{venue}",
            summary=clean_abs[:280],
            body=clean_abs,
            published_at=dt,
            score=2,
            tags=("openreview", venue),
        )


class PapersWithCodeCollector:
    name = "papers-with-code"

    def collect(self) -> Iterable[RawHit]:
        # PapersWithCode 任务 API — 公开
        for task in ["language-modelling", "question-answering", "text-generation", "code-generation"]:
            yield from _fetch_pwc(task)


def _fetch_pwc(task: str) -> Iterable[RawHit]:
    url = "https://paperswithcode.com/api/v1/papers/"
    try:
        data = http_get_json(
            url,
            params={
                "task": task,
                "ordering": "-published",
                "items_per_page": 25,
            },
            timeout=30,
        )
    except Exception as exc:
        _LOG.debug("papers-with-code %s skipped: %s", task, exc)
        return
    if not isinstance(data, dict):
        return
    results = data.get("results") or []
    for p in results:
        title = p.get("title") or ""
        pid = p.get("id", "")
        if not (title and pid):
            continue
        url_out = f"https://paperswithcode.com/paper/{pid}"
        abstract = p.get("abstract") or ""
        clean_abs = re.sub(r"\s+", " ", abstract).strip()
        pub = p.get("published") or ""
        dt: datetime | None = None
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        yield RawHit(
            title=title,
            url=url_out,
            source=f"papers-with-code:{task}",
            summary=clean_abs[:280],
            body=clean_abs,
            published_at=dt,
            score=1,
            tags=("papers-with-code", f"task:{task}"),
        )