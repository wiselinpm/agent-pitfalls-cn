"""采集器基类与数据结构。"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Iterable, Protocol


@dataclass(frozen=True)
class RawHit:
    """单条来自数据源的原始命中。

    所有 source 必须产出这个形态的数据，由 normalize 层再转换成
    PitfallDraft。
    """

    title: str
    url: str
    source: str
    summary: str
    body: str = ""
    author: str | None = None
    published_at: datetime | None = None
    score: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        """基于 URL 的稳定指纹，用于跨 source 去重。"""
        from .dedupe import url_fingerprint

        return url_fingerprint(self.url)


class BaseCollector(Protocol):
    """所有采集器必须实现的协议。"""

    name: str

    def collect(self) -> Iterable[RawHit]: ...


def safe_asdict(hit: RawHit) -> dict[str, Any]:
    """不可变 dataclass -> dict，便于序列化。"""
    d = asdict(hit)
    if isinstance(d.get("published_at"), datetime):
        d["published_at"] = d["published_at"].isoformat()
    return d