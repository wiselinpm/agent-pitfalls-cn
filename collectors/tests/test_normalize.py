"""测试 normalize 层。"""

from __future__ import annotations

from datetime import datetime

import pytest

from collectors.base import RawHit
from collectors.normalize import (
    PitfallDraft,
    _infer_categories,
    _infer_platforms,
    _infer_severity,
    _slugify,
    normalize,
)


def _hit(title: str = "t", body: str = "", summary: str = "s") -> RawHit:
    return RawHit(
        title=title,
        url="https://example.com/x",
        source="test",
        summary=summary,
        body=body,
        published_at=datetime(2026, 1, 1),
    )


def test_infer_severity_critical() -> None:
    assert _infer_severity("data loss in production") == "critical"
    assert _infer_severity("RCE vulnerability") == "critical"


def test_infer_severity_default() -> None:
    assert _infer_severity("random unrelated topic") == "medium"


def test_infer_platforms() -> None:
    assert "claude-code" in _infer_platforms("using claude code")
    assert "langchain" in _infer_platforms("LangChain memory leak")
    assert _infer_platforms("nothing here") == ("generic",)


def test_infer_categories() -> None:
    cats = _infer_categories("context window overflow + tool use bug")
    assert "context-window" in cats
    assert "tool-use" in cats


def test_slugify_chinese() -> None:
    slug = _slugify("OpenAI Chat Completions 工具调用")
    assert slug
    assert " " not in slug


def test_normalize_emits_frozen_draft() -> None:
    d = normalize(_hit(title="Claude code crash", body="production data loss"))
    assert isinstance(d, PitfallDraft)
    assert d.severity == "critical"
    assert "claude-code" in d.platforms
    assert d.fingerprint  # 非空
    assert d.discovered_at == "2026-01-01"
    assert d.references and d.references[0]["url"] == "https://example.com/x"


def test_normalize_frozen() -> None:
    d = normalize(_hit())
    with pytest.raises(Exception):
        d.title = "mutate"  # type: ignore[misc]