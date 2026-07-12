"""HuggingFace Daily Papers 采集。

跟踪当日最受关注的 AI 论文，从发布元数据中筛出和「agent 失败 / prompt injection / tool use」相关的。
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


# HF Daily Papers 公开 API
DAILY_URL = "https://huggingface.co/api/daily_papers"

# 关键词 — 用于过滤出真正讨论「坑」的论文
KEYWORDS = (
    "agent", "tool", "prompt", "injection", "jailbreak",
    "alignment", "hallucination", "failure", "robustness",
    "function call", "rag", "retrieval", "context",
    "attack", "safety", "adversar", "guardrail",
    "leak", "exploit", "vulnerab",
)


class HuggingFacePapersCollector:
    name = "huggingface-papers"

    def collect(self) -> Iterable[RawHit]:
        try:
            raw = http_get(DAILY_URL)
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            return

        # 响应是 flat list of { paper: {...}, dayPublishedOnHuggingFace: "...", ... }
        # 兼容两种形态：list[paper] 或 list[day{papers:[...]}, ...]
        for entry in data or []:
            if isinstance(entry, dict) and "papers" in entry:
                # day wrapper 形态
                day = entry.get("day")
                for paper in entry.get("papers") or []:
                    hit = _to_hit(paper, day)
                    if hit:
                        yield hit
            else:
                # flat paper 形态
                hit = _to_hit(entry, None)
                if hit:
                    yield hit


def _to_hit(paper: dict, day: str | None) -> RawHit | None:
    if not isinstance(paper, dict):
        return None
    # flat 形态 paper 直接是 paper 对象；wrapped 形态 paper 在 "paper" key 下
    inner = paper.get("paper", paper) if "paper" in paper else paper

    title = (inner.get("title") or "").strip()
    if not title:
        return None
    paper_id = inner.get("id") or ""
    if not paper_id:
        return None
    url = f"https://huggingface.co/papers/{paper_id}"

    summary = (inner.get("summary") or "").strip()
    if not _is_relevant(title, summary):
        return None

    author_block = inner.get("authors") or []
    author_names = []
    for a in author_block[:3]:
        if isinstance(a, dict):
            author_names.append(a.get("name") or a.get("user", {}).get("name", ""))
        else:
            author_names.append(str(a))
    author = ", ".join([n for n in author_names if n]) or None

    published_at = None
    pub_str = inner.get("publishedAt") or inner.get("submittedOnDailyAt") or day
    if pub_str:
        try:
            published_at = datetime.fromisoformat(str(pub_str).replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass

    upvotes = inner.get("upvotes") or paper.get("upvotes") or 0

    return RawHit(
        title=title[:120],
        url=url,
        source="huggingface-papers",
        summary=summary[:280],
        body=summary,
        author=author,
        published_at=published_at,
        score=int(upvotes) if isinstance(upvotes, (int, float)) else 0,
        tags=("huggingface", "paper"),
    )


def _is_relevant(title: str, summary: str) -> bool:
    haystack = (title + " " + summary).lower()
    return any(k in haystack for k in KEYWORDS)