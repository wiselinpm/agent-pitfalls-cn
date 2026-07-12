"""掘金备用源 — 通过 Brave Search 公开搜索结果命中掘金文章。

原 juejin.py 在生产网络下全部 404。本 collector 通过 Brave 搜索
`site:juejin.cn` 命中掘金文章，不直连掘金 API。
"""

from __future__ import annotations

import logging
from typing import Iterable

from ..base import RawHit
from .brave_search import JUEJIN_QUERIES, _brave_results

_LOG = logging.getLogger("collectors.juejin_v2")


class JuejinV2Collector:
    name = "juejin-v2"

    def collect(self) -> Iterable[RawHit]:
        for q in JUEJIN_QUERIES:
            for hit in _brave_results(q):
                if "juejin.cn" not in hit.url and "juejin.im" not in hit.url:
                    continue
                yield RawHit(
                    title=hit.title,
                    url=hit.url,
                    source="juejin-via-brave",
                    summary=hit.summary,
                    body=hit.body,
                    published_at=hit.published_at,
                    score=2,
                    tags=("juejin", "brave-indexed", f"q:{q}"),
                )