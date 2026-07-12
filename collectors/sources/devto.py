"""Dev.to API 采集（公开免费，无需 key）。"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get_json


TAGS = ["ai", "llm", "openai", "claude", "chatgpt", "agents"]


class DevToCollector:
    name = "devto"

    def collect(self) -> Iterable[RawHit]:
        for tag in TAGS:
            try:
                data = http_get_json(
                    "https://dev.to/api/articles",
                    params={"tag": tag, "per_page": 30, "top": 7},
                )
            except Exception:
                continue
            if not isinstance(data, list):
                continue
            for art in data:
                if not isinstance(art, dict):
                    continue
                yield RawHit(
                    title=art.get("title") or "",
                    url=art.get("url") or art.get("canonical_url") or "",
                    source=f"devto:{tag}",
                    summary=(art.get("description") or "")[:280],
                    body=art.get("body_html") or art.get("body_markdown") or "",
                    author=art.get("user", {}).get("username") if isinstance(art.get("user"), dict) else None,
                    published_at=_parse_dt(art.get("published_at")),
                    score=int(art.get("public_reactions_count") or 0)
                    + int(art.get("comments_count") or 0) * 2,
                    tags=(tag,),
                )


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None