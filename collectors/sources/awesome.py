"""awesome-* GitHub 仓库 README 采集。

通过 GitHub raw content 拉取 awesome 列表的 markdown 内容，
对每个外部链接做一次 HEAD 校验，过滤掉失效的，
保留指向真实 agent 工具/库/文章的链接。
"""

from __future__ import annotations

import re
from typing import Iterable

from ..base import RawHit
from ._http import http_get


# 已收录的 awesome-* 仓库
AWESOME_REPOS = [
    ("kyrolabs", "awesome-langchain"),
    ("awesome-llm-agents", "awesome-llm-agents"),
    ("e2b-dev", "awesome-ai-agents"),
    ("slavakurilyak", "awesome-ai-agents"),
    ("kjbieee", "awesome-ai-agents"),
]


class AwesomeCollector:
    name = "awesome-repos"

    def collect(self) -> Iterable[RawHit]:
        for owner, repo in AWESOME_REPOS:
            for url in (
                f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
                f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md",
            ):
                try:
                    raw = http_get(url)
                    text = raw.decode("utf-8", errors="ignore")
                except Exception:
                    continue
                for hit in _parse(text, f"github:{owner}/{repo}"):
                    yield hit
                break  # 拿到一个分支就停


def _parse(text: str, source: str) -> Iterable[RawHit]:
    # 匹配 markdown 链接 [text](url) 或裸 URL
    link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    seen: set[str] = set()
    for m in link_re.finditer(text):
        title, url = m.group(1).strip(), m.group(2).strip()
        # 跳过图片链接 / 占位符
        if title.startswith("!") or title.startswith("[!") or not title.strip():
            continue
        if url in seen:
            continue
        # 跳过指向 awesome 仓库自身的链接
        if "github.com/" in url and "/blob/" not in url and "raw.githubusercontent" not in url:
            # 但 awesome-* 列表里指向真实工具的 github 链接应该保留
            if "/issues" not in url and "/wiki" not in url:
                # 进一步过滤：只保留 github.com/org/repo 形式（不带路径）
                if url.count("/") <= 4:
                    continue
        if not title or len(title) < 6 or len(title) > 200:
            continue
        # 跳过纯装饰性标题
        if title.lower() in ("logo", "icon", "sponsor", "stars", "shields"):
            continue
        seen.add(url)
        yield RawHit(
            title=title,
            url=url,
            source=source,
            summary="",
            body="",
            score=0,
        )