"""测试 normalize 层。"""

from __future__ import annotations

from datetime import datetime

import pytest

from collectors.base import RawHit
from collectors.normalize import (
    PitfallDraft,
    _extract_body_structure,
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


# === body extraction tests ===

_MD_BODY = """# Symptom
- Agent silently drops recent tool_result when context > 80% full
- Logs show no truncation warning anywhere

# Root Cause
The model truncates from the middle of the conversation history, not the tail.

# Fix
- Echo critical tool results back into the system prompt
- Compress context proactively when usage > 70%
"""


def test_extract_markdown_sections() -> None:
    sym, cause, fix = _extract_body_structure(_MD_BODY)
    assert len(sym) == 2
    assert "silently drops recent tool_result" in sym[0]
    assert len(cause) >= 1
    assert "truncates from the middle" in cause[0]
    assert len(fix) == 2
    assert "Echo critical tool results" in fix[0]


def test_extract_prose_pattern() -> None:
    text = (
        "We hit a critical issue. Symptom: agents leak the API key into logs. "
        "Root cause: the prompt template inlines secrets. "
        "The fix is: pull secrets from a manager and add a redacting filter."
    )
    sym, cause, fix = _extract_body_structure(text)
    assert any("leak the API key" in s for s in sym)
    assert any("prompt template" in c for c in cause)
    assert any("pull secrets" in f for f in fix)


def test_extract_summary_fallback() -> None:
    """body 全空、summary 有内容时，symptoms/fixes 用 summary 兜底。"""
    sym, _cause, fix = _extract_body_structure("", summary="Critical: production crash with data loss")
    assert sym and "production crash" in sym[0]
    assert fix and "production crash" in fix[0]


def test_extract_filters_noise() -> None:
    text = """# Fix
- yes
- https://example.com
- Implement proper input validation in the form handler
"""
    _sym, _cause, fix = _extract_body_structure(text)
    assert len(fix) == 1
    assert "input validation" in fix[0]


def test_extract_chinese_sections() -> None:
    text = """# 症状
- agent 在上下文超 80% 时静默截断
- 日志里看不到任何警告

# 根因
模型从对话历史中间截断

# 修复
- 显式 echo 关键工具结果
"""
    sym, cause, fix = _extract_body_structure(text)
    assert any("静默截断" in s for s in sym)
    assert any("中间截断" in c for c in cause)
    assert any("echo" in f for f in fix)


def test_extract_dedups_and_caps() -> None:
    text = """# Fix
- same fix as above
- same fix as above
- another fix here
- one more
- too many
- six
"""
    _sym, _cause, fix = _extract_body_structure(text)
    assert all(f != "yes" for f in fix)
    # dedup → 4 unique
    assert len(fix) <= 4


def test_normalize_fills_via_summary() -> None:
    d = normalize(_hit(title="crash bug", body="", summary="production data loss on heavy load"))
    # 即使 body 空，summary 兜底应让 symptoms/fixes 非空
    assert d.symptoms or d.fixes