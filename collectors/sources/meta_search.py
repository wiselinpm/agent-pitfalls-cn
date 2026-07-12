"""通用元搜索补充 — 通过 Brave Search 命中各种不直接收录的网站内容。

覆盖：Cursor Forum, Aider Discussions, LangChain Hub, LangSmith 等无公开 RSS
的社区。优点是不需要登录态/cookie/付费 API。
"""

from __future__ import annotations

import logging
from typing import Iterable

from ..base import RawHit
from .brave_search import GENERIC_QUERIES, _brave_results

_LOG = logging.getLogger("collectors.meta_search")


# 额外针对 Cursor/Aider/Cline/LangSmith/Replicate 社区的 query
EXTRA_QUERIES = [
    "site:forum.cursor.sh bug",
    "site:forum.cursor.sh issue",
    "site:aider.chat error",
    "site:github.com/cline/cline issue",
    "site:community.librechat.ai error",
    "site:smith.langchain.com issue",
    "site:discord.com channels anthropic claude",
    "site:docs.aider.chat pitfall",
    "site:replicate.com bug",
    "site:huggingface.co spaces error",
    "site:platform.openai.com docs prompt-injection",
    "site:docs.anthropic.com claude-code tool-use issue",
]


class MetaSearchCollector:
    name = "meta-search"

    def collect(self) -> Iterable[RawHit]:
        for q in list(GENERIC_QUERIES) + EXTRA_QUERIES:
            for hit in _brave_results(q):
                yield hit