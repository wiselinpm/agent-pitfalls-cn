"""知乎备用源 — 通过 Brave Search 公开搜索结果命中知乎内容。

原 zhihu.py 在生产网络下基本不可用（反爬升级）。本 collector 通过 Brave
Search `site:zhihu.com` 命中知乎文章，不直连知乎。Brave 不需要 API key，且
不像 Bing 那样强制 CAPTCHA。
"""

from __future__ import annotations

import logging
from typing import Iterable

from ..base import RawHit
from .brave_search import ZHIHU_QUERIES, _brave_results

_LOG = logging.getLogger("collectors.zhihu_v2")


class ZhihuV2Collector:
    name = "zhihu-v2"

    def collect(self) -> Iterable[RawHit]:
        for q in ZHIHU_QUERIES:
            for hit in _brave_results(q):
                if "zhihu.com" not in hit.url:
                    continue
                # 替换 source 为更精确的标签
                yield RawHit(
                    title=hit.title,
                    url=hit.url,
                    source="zhihu-via-brave",
                    summary=hit.summary,
                    body=hit.body,
                    published_at=hit.published_at,
                    score=2,  # 知乎命中优先保留
                    tags=("zhihu", "brave-indexed", f"q:{q}"),
                )