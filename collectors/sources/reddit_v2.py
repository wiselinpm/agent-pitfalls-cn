"""Reddit 备用源 — 通过 Brave Search 公开搜索结果命中 reddit.com 内容。

原 reddit.py 完全失败（403）。本 collector 通过 Brave 搜索
`site:reddit.com` 命中 Reddit 帖子。Brave 不需要 API key。
"""

from __future__ import annotations

import logging
from typing import Iterable

from ..base import RawHit
from .brave_search import REDDIT_QUERIES, _brave_results

_LOG = logging.getLogger("collectors.reddit_v2")


class RedditV2Collector:
    name = "reddit-v2"

    def collect(self) -> Iterable[RawHit]:
        for q in REDDIT_QUERIES:
            for hit in _brave_results(q):
                if "reddit.com" not in hit.url:
                    continue
                yield RawHit(
                    title=hit.title,
                    url=hit.url,
                    source="reddit-via-brave",
                    summary=hit.summary,
                    body=hit.body,
                    published_at=hit.published_at,
                    score=2,
                    tags=("reddit", "brave-indexed", f"q:{q}"),
                )